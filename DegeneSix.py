# Work with Python 3.6
import numpy as np
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
TOKEN = ""  # Get at discordapp.com/developers/applications/me

bot = Bot(command_prefix=BOT_PREFIX)

# bot = discord.bot()

@bot.command(
    name='Degene6',
    description="Rolls a Degenesis dice pool.",
    brief="Sacrifice everything",
    aliases=['D6', '6pool','roll'],
    pass_context=True)
async def degenesix(context,actionNumber:int,difficulty=0):
    autos = 0 if actionNumber < 13 else actionNumber-12
    actionNumber = 12 if actionNumber > 13 else actionNumber
    roll = np.random.choice([1,2,3,4,5,6],actionNumber)
    successes = (roll > 3).sum()
    successes += autos
    triggers = (roll == 6).sum()
    ones = (roll == 1).sum()

    if difficulty:
        result = ('Success!\n' if successes >= difficulty else "Failure!\n") if ones < successes else 'It\'s a botch!\n'
        msg = "%s needs %d successes and rolls:" % (context.author.mention,difficulty)
    else:
        result = '' if ones < successes else 'It\'s a botch!\n'
        msg = "%s rolls:" % (context.author.mention)
    msg+= " \n %s \n %d successes, %d triggers \n %s" % (', '.join(map(str,roll)),
    successes,
    triggers,
    result)
    await context.send(msg)

@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)

bot.run(TOKEN)
