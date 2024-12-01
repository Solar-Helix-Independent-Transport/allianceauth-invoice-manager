import datetime
import logging

from aadiscordbot.app_settings import get_site_url, get_all_servers
from aadiscordbot.cogs.utils.decorators import has_any_perm, sender_has_perm
from discord import AutocompleteContext, InputTextStyle, Interaction, option
from discord.embeds import Embed
from discord.ext import commands
from discord.ui import InputText, Modal

from django.conf import settings
from django.utils import timezone

from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.modules.discord.models import DiscordUser

from invoices.models import Invoice

logger = logging.getLogger(__name__)


def input_to_number(string_input):
    replacements = {
        "K": "000",
        "M": "000000",
        "B": "000000000"
    }
    for key in replacements.keys():
        string_input = string_input.upper().replace(key, replacements[key])
    return int(string_input)


class Invoices(commands.Cog):
    """
    All about fats!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='invoices', guild_ids=get_all_servers())
    async def invoices(self, ctx):
        """
        Show your current invoices
        """
        try:
            has_any_perm(ctx.author.id, guild=ctx.guild, perms=['invoices.access_invoices'])
            await ctx.defer(ephemeral=True)
            user = DiscordUser.objects.get(uid=ctx.author.id).user
            character_list = user.character_ownerships.all()
            invoices = Invoice.objects.filter(
                character__in=character_list.values_list('character'), paid=False)
            total = 0
            total_overdue = 0

            for i in invoices:
                if i.is_past_due:
                    total_overdue += i.amount
                else:
                    total += i.amount

            embed = Embed()
            embed.title = "Invoices!"
            if total + total_overdue > 0:
                embed.description = "Please check auth for more info!"
                embed.add_field(name="Total Overdue Invoices",
                                value=f"Ƶ{total_overdue:,}",
                                inline=False)
                embed.add_field(name="Total Remaining Invoices",
                                value=f"Ƶ{total:,}",
                                inline=False)

            else:
                embed.description = "No Outstanding Invoices!"

            embed.url = get_site_url()

            await ctx.respond(embed=embed, ephemeral=True)
        except commands.MissingPermissions as e:
            return await ctx.respond(e.missing_permissions[0], ephemeral=True)

    async def search_characters(ctx: AutocompleteContext):
        return list(EveCharacter.objects.filter(character_name__icontains=ctx.value).values_list('character_name', flat=True)[:10])

    class InvoiceReference(Modal):
        def __init__(self, send_from, sent_to, msg=None):
            super().__init__(title="Fine Member")
            self.send_from = send_from
            self.send_to = sent_to
            self.msg = msg

            prefill = None
            if msg:
                prefill = f"`{self.msg.clean_content}` "

            self.add_item(
                InputText(
                    label="Amount",
                    placeholder="How much to Invoice eg. 5B, 5000m, 5kkk",
                )
            )

            self.add_item(
                InputText(
                    label="Reason",
                    placeholder="The Invoice Reason",
                    value=prefill,
                    style=InputTextStyle.long,
                )
            )

        async def callback(self, interaction: Interaction):
            try:
                _t = timezone.now() + datetime.timedelta(days=7)
                _i = Invoice.objects.create(
                    character=self.send_to,
                    amount=input_to_number(self.children[0].value),
                    note=self.children[1].value,
                    invoice_ref=f"{str(self.send_to).replace(' ','')}-{str(hash(_t))[-10:]}".lower(
                    ),
                    due_date=_t
                )
                _i.notify(
                    f"{self.send_from} Sent you a fine!\nPlease check auth for details.")
                msg = f"{self.send_from} has fined {self.send_to}, Ƶ{input_to_number(self.children[0].value):,}"
                if self.msg:
                    await self.msg.reply(msg)
                await interaction.response.send_message(msg, ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(e, ephemeral=True)
            self.stop()

    @commands.message_command(name="Fine User for Message", guild_ids=get_all_servers())
    @sender_has_perm("invoices.add_invoice")
    async def new_invoice_message(self, ctx, message):
        user_to_fine = DiscordUser.objects.get(
            uid=message.author.id).user.profile.main_character
        user_who_fine = DiscordUser.objects.get(
            uid=ctx.author.id).user.profile.main_character
        ask_for_reason_text = Invoices.InvoiceReference(
            user_who_fine, user_to_fine, message)
        await ctx.send_modal(ask_for_reason_text)

    @commands.user_command(name="Fine User", guild_ids=get_all_servers())
    @sender_has_perm("invoices.add_invoice")
    async def new_invoice_user(self, ctx, user):
        user_to_fine = DiscordUser.objects.get(
            uid=user.id).user.profile.main_character
        user_who_fine = DiscordUser.objects.get(
            uid=ctx.author.id).user.profile.main_character
        ask_for_reason_text = Invoices.InvoiceReference(
            user_who_fine, user_to_fine)
        await ctx.send_modal(ask_for_reason_text)

    @commands.slash_command(name='new_invoice', guild_ids=get_all_servers())
    @option("character", description="Character to invoice!", autocomplete=search_characters)
    @option("amount", description="Amount to invoice", type=str)
    @option("reason", description="Reason to put on invoice!", type=str)
    async def send_invoice(self, ctx, character, amount, reason):
        try:
            has_any_perm(ctx.author.id, ['invoices.add_invoice'])
            await ctx.defer(ephemeral=False)
            user = DiscordUser.objects.get(uid=ctx.author.id).user
            try:
                char = EveCharacter.objects.get(character_name=character)
                _t = timezone.now() + datetime.timedelta(days=7)
                _i = Invoice.objects.create(character=char,
                                            amount=input_to_number(amount),
                                            note=reason,
                                            due_date=_t,
                                            invoice_ref=f"{str(char).replace(' ','')}-{str(hash(_t))[-10:]}".lower())
                _i.notify(
                    f"{user.profile.main_character} Sent you an invoice! Please check auth for details!")
                return await ctx.respond(f"Sent {char} and Invoice for Ƶ{input_to_number(amount):,}")

            except EveCharacter.DoesNotExist:
                return await ctx.respond("Character Not Found!")

        except commands.MissingPermissions as e:
            return await ctx.respond(e.missing_permissions[0], ephemeral=True)


def setup(bot):
    bot.add_cog(Invoices(bot))
