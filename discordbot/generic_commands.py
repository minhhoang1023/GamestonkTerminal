import discord
import discordbot.config_discordbot as cfg


class GenericCommands(discord.ext.commands.Cog):
    """Generic discord.ext.commands."""

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @discord.ext.commands.command(name="about")
    async def about(self, ctx: discord.ext.commands.Context):
        """About Gamestonk Terminal"""
        links = (
            "Join our community on discord: https://discord.gg/Up2QGbMKHY\n"
            "Follow our twitter for updates: https://twitter.com/gamestonkt\n"
            "Access our landing page: https://gamestonkterminal.vercel.app\n\n"
            "**Main maintainers:** DidierRLopes, jmaslek, aia\n"
        )
        partnerships = (
            "FinBrain: https://finbrain.tech\n"
            "Quiver Quantitative: https://www.quiverquant.com\n"
            "SentimentInvestor: https://sentimentinvestor.com\n"
        )
        disclaimer = (
            "Trading in financial instruments involves high risks including "
            "the risk of losing some, or all, of your investment amount, and "
            "may not be suitable for all investors. Before deciding to trade "
            "in financial instrument you should be fully informed of the risks "
            "and costs associated with trading the financial markets, carefully "
            "consider your investment objectives, level of experience, and risk "
            "appetite, and seek professional advice where needed. The data "
            "contained in Gamestonk Terminal (GST) is not necessarily accurate. "
            "GST and any provider of the data contained in this website will not "
            "accept liability for any loss or damage as a result of your trading, "
            "or your reliance on the information displayed."
        )
        embed = discord.Embed(
            title="Investment Research for Everyone",
            description=links,
            colour=cfg.COLOR,
        )
        embed.set_author(
            name=cfg.AUTHOR_NAME,
            icon_url=cfg.AUTHOR_ICON_URL,
        )
        embed.add_field(name="Partnerships:", value=partnerships, inline=False)
        embed.add_field(name="Disclaimer:", value=disclaimer, inline=False)

        await ctx.send(embed=embed)

    @discord.ext.commands.command(name="help")
    async def help(self, ctx: discord.ext.commands.Context):
        help_message = """
```
Commands:

Economy Menu:
  !economy    - Economy Info

Stocks Menu:
  !stocks.dps - Dark Pool Shorts
  !stocks.gov - Government
  !stocks.opt - Options
  !stocks.scr - Screeners
  !stocks.dd  - Due Diligence
  !stocks.ta  - Technical Analysis

Generic:
  !about      - About us
  !usage      - Usage instructions
  !help       - Print this message
```
        """
        await ctx.send(help_message)

    @discord.ext.commands.command(name="usage")
    async def usage(self, ctx: discord.ext.commands.Context):
        usage_instructions_message = """
```
- Every command starts with an exclamation point "!".

- Any command can be triggered from the chat. For example:

  !about
  or
  !stocks.dps.spos tsla
  or
  !stocks.ta.recom tsla

- Every menu has it's own help command that can be called
  by adding .help to the menu name. For example:

  !stocks.help

- Call the help command to see the list of available menus:

  !help
```
        """
        await ctx.send(usage_instructions_message)


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(GenericCommands(bot))
