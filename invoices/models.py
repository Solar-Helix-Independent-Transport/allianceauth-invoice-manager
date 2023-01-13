from collections import defaultdict
from allianceauth.authentication.models import CharacterOwnership
from django.db import models
from allianceauth.eveonline.models import EveCharacter
from allianceauth.notifications import notify as auth_notify
from corptools.models import CorporationWalletJournalEntry
from django.urls import reverse
from django.contrib.auth.models import User

from . import app_settings
from .managers import InvoiceManager
from django.utils import timezone


if app_settings.discord_bot_active():
    from aadiscordbot import tasks as bot_tasks
    from discord import Embed, Color

import logging
logger = logging.getLogger(__name__)


class Invoice(models.Model):

    objects = InvoiceManager()

    character = models.ForeignKey(
        EveCharacter, null=True, default=None, on_delete=models.SET_NULL, related_name='invoices')
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, default=None)
    invoice_ref = models.CharField(max_length=72)
    due_date = models.DateTimeField()
    notified = models.DateTimeField(null=True, default=None, blank=True)

    paid = models.BooleanField(default=False, blank=True)
    payment = models.OneToOneField(CorporationWalletJournalEntry, blank=True,
                                   null=True, default=None, on_delete=models.SET_NULL, related_name='invoice')

    note = models.TextField(blank=True, null=True, default=None,)

    def __str__(self):
        return "{} - {} - {}".format(self.character, self.invoice_ref, self.amount)

    @property
    def is_past_due(self):
        return timezone.now() > self.due_date

    def notify(self, message, title="Contributions Bot Message"):
        url = f"{app_settings.get_site_url()}{reverse('invoices:r_list')}"
        try:
            u = self.character.character_ownership.user
            if app_settings.discord_bot_active():
                try:
                    if self.paid:
                        color = Color.green()
                    elif self.is_past_due:
                        color = Color.red()
                    else:
                        color = Color.blue()

                    e = Embed(title=title,
                              description=message,
                              url=url,
                              color=color)
                    e.add_field(name="Amount",
                                value=f"${self.amount:,}", inline=False)
                    e.add_field(name="Reference",
                                value=self.invoice_ref, inline=False)
                    e.add_field(name="Due Date", value=self.due_date.strftime(
                        "%Y/%m/%d"), inline=False)

                    bot_tasks.send_message(user_id=u.discord.uid,
                                           embed=e)
                except Exception as e:
                    logger.error(e, exc_info=True)
                    pass

            message = "Invoice:{} Ƶ{:.2f}\n{}\n{}".format(
                self.invoice_ref,
                self.amount,
                message,
                url
            )
            auth_notify(
                u,
                title,
                message,
                'info'
            )
        except Exception as e:
            logger.error(e)
            pass  # todo something nicer...

    class Meta:
        permissions = (('view_corp', 'Can View Own Corps Invoices'),
                       ('view_alliance', 'Can View Own Alliances Invoices'),
                       ('view_all', 'Can View All Invoices'),
                       ('access_invoices', 'Can Access the Invoice App')
                       )


# sec group classes


class FilterBase(models.Model):

    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}: {self.description}"

    def process_filter(self, user: User):
        raise NotImplementedError("Please Create a filter!")


class NoOverdueFilter(FilterBase):

    swap_logic = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Smart Filter: No Overdue Invoice"
        verbose_name_plural = f"{verbose_name}s"

    def process_filter(self, user: User):
        try:
            return self.audit_filter([user])[user.id]['check']
        except Exception as e:
            logger.error(e, exc_info=1)
            return False

    def audit_filter(self, users):
        co = CharacterOwnership.objects.filter(
            user__in=users).select_related('user', 'character')
        chars = {}
        now = timezone.now()
        outstanding_invoices = Invoice.objects.filter(
            character__in=co.values_list('character'), due_date__lte=now, paid=False)

        failure = self.swap_logic
        for i in outstanding_invoices:
            uid = i.character.character_ownership.user.id
            if uid not in chars:
                chars[uid] = 0
            chars[uid] += 1

        output = defaultdict(lambda: {"message": "Failed", "check": False})
        for u in users:
            c = chars.get(u.id, False)
            if c > 0:
                output[u.id] = {"message": f"{c} Overdue", "check": failure}
                continue
            else:
                output[u.id] = {"message": "No Overdue", "check": not failure}
                continue
        return output
