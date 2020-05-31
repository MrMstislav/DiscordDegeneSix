# Work with Python 3.6
import numpy as np
import os
import discord
from discord.ext.commands import Bot, when_mentioned_or
from discord.utils import get

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
    degEmoji = get(context.message.guild.emojis, name="degenesis") 

    if difficulty:
        result = (f'*Success!* {degEmoji}\n' if successes >= difficulty else "Failure!\n") if ones <= successes else '*It\'s a botch!* :skull:\n'        
        msg = "%s needs %d successes and rolls:" % (context.author.mention,difficulty) if autos == 0 else "%s needs %d successes, already has %d automatic and rolls:" % (context.author.mention,difficulty,autos)
    else:
        result = '' if ones <= successes else '*It\'s a botch!* :skull:\n'
        msg = "%s rolls:" % (context.author.mention) if autos == 0 else "%s has %d automatic successes and rolls:" % (context.author.mention, autos)
    msg+= " \n %s \n %d successes, %d triggers \n %s" % (', '.join(map(str,roll)),
    successes,
    triggers,
    result)
    await context.send(msg)

@bot.command(
    name='GegromeGetroll',
    description="Rolls a hacked Degenesis dice pool.",
    brief="I am the creator.",
    aliases=['GeeGee6','GeromeGetroll'],
    pass_context=True)
async def degenesix(context,actionNumber:int,difficulty=0):
    autos = 0 if actionNumber < 13 else actionNumber-12
    actionNumber = 12 if actionNumber > 13 else actionNumber
    roll = np.random.choice([1,5,6],actionNumber,p=[0.25,0.25,0.5])
    successes = (roll > 3).sum()
    successes += autos
    triggers = (roll == 6).sum()
    ones = (roll == 1).sum()
    rgEmoji = get(context.message.guild.emojis, name="rg") 
    ggnoEmoji = get(context.message.guild.emojis, name="Getrellno") 

    if difficulty:
        result = (f'*Just as planned* {rgEmoji}\n' if successes >= difficulty else "Failure!\n") if ones <= successes else '*Marauders fucking with my shit again* <:Getrellno:716782931045122051>\n'        
        msg = "GG needs %d successes and rolls:" % (difficulty) if autos == 0 else "GG needs %d successes, already had %d cryofreezed and rolls:" % (difficulty,autos)
    else:
        result = '' if ones <= successes else f'*Marauders fucking with my shit again* {ggnoEmoji}\n'
        msg = "GG had always planned to roll:" if autos == 0 else "GG acquired %d automatic successes back in 2079 and rolls:" % (autos)
    msg+= " \n %s \n %d successes, %d triggers \n %s" % (', '.join(map(str,roll)),
    successes,
    triggers,
    result)
    await context.send(msg)

@bot.command(
    name='DevInfo',
    description="Developer Information",
    brief="Code availability",
    aliases=['DI'],
    pass_context=False)
async def degenesix(context):
    msg = "Code available at: https://github.com/MrMstislav/DiscordDegeneSix/\n"
    await context.send(msg)
    
# @bot.event
# async def on_message(msg):
#     # we do not want the bot to reply to itself
#     if msg.author.bot:
#         return 0
#     if len(msg.mentions) == 1 and msg.mentions[0] == bot.user:
#         ctx = await bot.get_context(message=msg)
#         args = msg.content.split(' ')[1:]
#         return degenesix(ctx,*args)

@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)

bot.run(TOKEN)
