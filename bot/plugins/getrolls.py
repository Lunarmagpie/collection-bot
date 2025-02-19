import time

import crescent

from bot.model import Plugin
from bot.upgrades import Upgrades

plugin = Plugin()


class GetRollsCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        assert ctx.guild_id is not None
        dbsearch = plugin.model.dbsearch

        user = await dbsearch.create_user(ctx.guild_id, ctx.user)

        regeneration_rate = int(await user.get_upgrade_value(Upgrades.ROLL_REGEN))
        roll_max = int(await user.get_upgrade_value(Upgrades.ROLL_MAX))

        last_claim_time = await user.rolls_claimed_time
        current_time = int(time.time())
        message = ""

        stockpile = int((current_time - last_claim_time) / regeneration_rate)

        if (last_claim_time) == 0:
            stockpile = 10
            await user.set_rolls_claimed_time(current_time)
            await user.set_rolls((await user.rolls) + stockpile)
            regenerate_time = 900
            rolls_to_be_claimed = 10
        else:
            rolls_to_be_claimed = min(stockpile, roll_max)
            last_regeneration = last_claim_time + stockpile * regeneration_rate
            regenerate_time = regeneration_rate - \
                (current_time - last_regeneration)
            await user.set_rolls_claimed_time(last_regeneration)
            await user.set_rolls((await user.rolls) + rolls_to_be_claimed)
        message = f"{rolls_to_be_claimed} roll{'s' if rolls_to_be_claimed != 1 else ''} have been claimed.\nNext roll regenerates in: **{int(regenerate_time/60)}** minutes and **{regenerate_time % 60}** seconds"

        await ctx.respond(message)


@plugin.include
@crescent.command(
    name="getrolls",
    description="Get your rolls. Without upgrades, One roll regenerates every 15 minutes, until 20 is reached.",
)
class LongCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        command = GetRollsCommand()
        await command.callback(ctx)


@plugin.include
@crescent.command(name="gr", description="Alias of /getrolls.")
class ShortenedCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        command = GetRollsCommand()
        await command.callback(ctx)
