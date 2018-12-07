# Work with Python 3.6
import numpy as np
import os
import discord
from discord.ext.commands import Bot, when_mentioned_or, Context

BOT_PREFIX = ("?", "!")
TOKEN = os.environ.get('ACCESS_TOKEN') # Get at discordapp.com/developers/applications/me

bot = Bot(command_prefix=when_mentioned_or(*BOT_PREFIX))
# bot = discord.bot()

@bot.command(
    name='Degene6',
    description="Rolls a Degenesis dice pool.",
    brief="Sacrifice everything",
    aliases=['D6', '6pool','roll','dee6'],
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
        result = ('*Success!* <:degenesis:>\n' if successes >= difficulty else "Failure!\n") if ones <= successes else '*It\'s a botch!* :skull:\n'
        msg = "%s needs %d successes and rolls:" % (context.author.mention,difficulty)
    else:
        result = '' if ones <= successes else '*It\'s a botch!* :skull:\n'
        msg = "%s rolls:" % (context.author.mention)
    msg+= " \n %s \n %d successes, %d triggers \n %s" % (', '.join(map(str,roll)),
    successes,
    triggers,
    result)
    await context.send(msg)
    
@bot.event
async def on_message(msg):
    # we do not want the bot to reply to itself
    if msg.author.bot:
        return 0
    if len(msg.mentions) == 1 and msg.mentions[0] == client.user:
        ctx = await bot.get_context()
        args = msg.split(' ')[1:]
        return degenesix(ctx,*args)

@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)

bot.run(TOKEN)
