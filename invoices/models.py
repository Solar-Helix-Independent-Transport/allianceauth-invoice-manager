from collections import defaultdict
from datetime import timedelta

from corptools.models import CorporationWalletJournalEntry

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import EveCharacter
from allianceauth.notifications import notify as auth_notify

from . import app_settings
from .managers import InvoiceManager

if app_settings.discord_bot_active():
    from aadiscordbot import tasks as bot_tasks
    from discord import Embed, Color

import logging

logger = logging.getLogger(__name__)

# CHARACTER_PREPAY_HEADER = f"PREPAY-" # make configurable?


# def get_character_key_string(character_id):
#     return f"{CHARACTER_PREPAY_HEADER}{character_id}"


# class InvoiceBalance(models.Model):
#     user = models.OneToOneField(User)
#     balance = models.DecimalField(
#         max_digits=20, decimal_places=2, null=True, default=None)
#     auto_pay = models.BooleanField(default=False)
#     last_updated = models.DateTimeField(auto_now=True)

#     @property
#     def character_balance_key(self):
#         get_character_key_string(self.character.character_id)


class Invoice(models.Model):

    objects = InvoiceManager()

    character = models.ForeignKey(
        EveCharacter, null=True, default=None, on_delete=models.SET_NULL, related_name='invoices')
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, default=None)
    invoice_ref = models.CharField(max_length=72)
    due_date = models.DateTimeField()
    notified = models.DateTimeField(null=True, default=None, blank=True)
    # corporate_invoice = models.BooleanField(default=False)

    paid = models.BooleanField(default=False, blank=True)
    payment = models.OneToOneField(CorporationWalletJournalEntry, blank=True,
                                   null=True, default=None, on_delete=models.SET_NULL, related_name='invoice')
    marked_paid_by = models.ForeignKey(
        EveCharacter, blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name='paychar')

    note = models.TextField(blank=True, null=True, default=None,)

    def __str__(self):
        return f"{self.character} - {self.invoice_ref} - {self.amount}"

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
                                value=f"Ƶ{self.amount:,.2f}", inline=False)
                    e.add_field(name="Reference",
                                value=self.invoice_ref, inline=False)
                    e.add_field(name="Due Date", value=self.due_date.strftime(
                        "%Y/%m/%d"), inline=False)
                    if app_settings.INVOICES_SEND_DISCORD_BOT_NOTIFICATIONS:
                        bot_tasks.send_message(user=u, embed=e)
                except Exception as e:
                    logger.error(e, exc_info=True)
                    pass

            message = "Invoice:{} Ƶ{:,.2f}\n{}\n{}".format(
                self.invoice_ref,
                self.amount,
                message,
                url
            )
            if app_settings.INVOICES_SEND_AUTH_NOTIFICATIONS:
                auth_notify(
                    u,
                    title,
                    message,
                    'info'
                )
        except Exception as e:
            logger.exception(e)
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


class TotalInvoicesFilter(FilterBase):
    # ignore_groups = models.ManyToManyField(Group, blank=True)
    min_amount = models.BigIntegerField(default=5000000000)
    swap_logic = models.BooleanField(default=False)
    only_paid = models.BooleanField(default=True)
    months = models.IntegerField(default=3)

    class Meta:
        verbose_name = "Smart Filter: Total Invoice Isk"
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
        look_back = timezone.now() - timedelta(days=30 * self.months)
        all_invoices = Invoice.objects.filter(
            character__in=co.values_list('character'), due_date__gte=look_back, paid=self.only_paid)

        failure = self.swap_logic
        for i in all_invoices:
            uid = i.character.character_ownership.user.id
            if uid not in chars:
                chars[uid] = 0
            chars[uid] += i.amount

        output = defaultdict(lambda: {"message": 0, "check": False})
        for u in users:
            c = int(chars.get(u.id, 0))
            if c < self.min_amount:
                output[u.id] = {"message": c, "check": failure}
                continue
            else:
                output[u.id] = {"message": c, "check": not failure}
                continue
        return output
