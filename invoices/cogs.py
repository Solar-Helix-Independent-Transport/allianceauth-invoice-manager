# Cog Stuff
from discord import option
from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Color

# AA Contexts
from django.conf import settings
from django.utils import timezone

# AA-Discordbot
from aadiscordbot.cogs.utils.decorators import has_any_perm
from allianceauth.services.modules.discord.models import DiscordUser
from aadiscordbot.app_settings import get_site_url

import logging

from invoices.models import Invoice

logger = logging.getLogger(__name__)


class Invoices(commands.Cog):
    """
    All about fats!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='invoices', guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def invoices(self, ctx):
        """
        Show your current invoices
        """
        try:
            has_any_perm(ctx.author.id, ['invoices.access_invoices'])
            await ctx.defer(ephemeral=True)
            start_time = timezone.now()
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
            embed.title = "Invocies!"
            if total+total_overdue > 0:
                embed.description = f"Please check auth for more info!"
                embed.add_field(name=f"Total Overdue Invoices",
                                value=f"${total_overdue:,}",
                                inline=False)
                embed.add_field(name=f"Total Remaining Invoices",
                                value=f"${total:,}",
                                inline=False)

            else:
                embed.description = f"No Outstanding Invoices!"

            embed.url = get_site_url()

            await ctx.respond(embed=embed, ephemeral=True)
        except commands.MissingPermissions as e:
            return await ctx.respond(e.missing_permissions[0], ephemeral=True)


def setup(bot):
    bot.add_cog(Invoices(bot))
