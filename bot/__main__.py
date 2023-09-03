import os

import crescent
import dotenv
import hikari
import miru

from bot.model import Model

dotenv.load_dotenv()

bot = hikari.GatewayBot(os.environ["TOKEN"])
miru.install(bot)

model = Model()

client = crescent.Client(bot, model)
client.plugins.load_folder("bot.plugins")

bot.subscribe(hikari.StartingEvent, model.on_start)
bot.subscribe(hikari.StoppedEvent, model.on_stop)

bot.run()
