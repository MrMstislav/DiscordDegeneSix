# Work with Python 3.6
import numpy as np
import os
import discord
import sqlite3
import datetime
import math
from discord.ext.commands import Bot, when_mentioned_or

BOT_PREFIX = ("?", "!")
TOKEN = os.environ.get('ACCESS_TOKEN') # Get at discordapp.com/developers/applications/me

bot = Bot(command_prefix=when_mentioned_or(*BOT_PREFIX))

# Setup database
try:
	connection = sqlite3.connect('degenesis.db')
	cursor = connection.cursor()
	with open('degenesis-schema.sql') as file:
		cursor.executescript(file.read())
except Exception as e:
	print(e)
	print("Database error")
	exit()


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
        result = ('*Success!* <:degenesis:684046972134490130>\n' if successes >= difficulty else "Failure!\n") if ones <= successes else '*It\'s a botch!* :skull:\n'
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

    if difficulty:
        result = ('*Just as planned* <:rg:684046905180684288>\n' if successes >= difficulty else "Failure!\n") if ones <= successes else '*Marauders fucking with my shit again* <:Getrellno:550654128238624768>\n'
        msg = "GG needs %d successes and rolls:" % (difficulty) if autos == 0 else "GG needs %d successes, already had %d cryofreezed and rolls:" % (difficulty,autos)
    else:
        result = '' if ones <= successes else '*Marauders fucking with my shit again* <:Getrellno:550654128238624768>\n'
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

########################## Roll utilities ##########################
def roll(numDice, numEgo):
	totalDice = ((numDice + numEgo) if numEgo else numDice)
	autos = max(totalDice-12, 0)
	results = np.random.randint(1, 7, totalDice-autos)
	ones = countOnes(results).item()
	successes = countSuccesses(results).item() + autos
	triggers = countTriggers(results).item()
	return {
		"results": results,
		"ones": ones,
		"successes": successes,
		"triggers": triggers
	}

def countOnes(rolls):
	return (rolls == 1).sum()

def countSuccesses(rolls):
	return (rolls >= 4).sum()

def countTriggers(rolls):
	return (rolls == 6).sum()

################################ Verbosity ################################
@bot.command(
	name='verbose',
	brief='Change the verbosity of the initiative functions',
	pass_context=True)
async def verbose(context, option:str):
	global cursor, connection
	try:
		await context.trigger_typing()
		if (option.lower() == "on"):
			choice = False
		elif(option.lower() == "off"):
			choice = True
		else:
			await context.send("Please use `on` or `off`")
			return
		cursor.execute("SELECT round_number, cur_initiative, label, start_time FROM initiatives WHERE channel_id=?", (context.channel.id,))
		initiative = cursor.fetchone()
		insertionTuple = (context.channel.id, int(choice), initiative[0], initiative[1], initiative[2], initiative[3])
		cursor.execute("REPLACE INTO initiatives(channel_id, verbose, round_number, cur_initiative, label, start_time) VALUES(?,?,?,?,?,?)", insertionTuple)
		connection.commit()
		msg = "Verbose level set to: `" + option + "`"
		await context.send(msg)
	except Exception as e:
		await context.send("Error while changing verbosity")
		await context.send(e)

########################## Start Initiative ##########################
@bot.command(
	name='start-initiative',
	brief='Allow calls for initiative in this channel',
	pass_context=True)
async def initiativeStart(context, label:str=None):
	global cursor, connection
	msg = ""
	try:
		async with context.typing():
			cursor.execute("SELECT label FROM initiatives WHERE channel_id=?", (context.channel.id,))
			previousInitiative = cursor.fetchone()
			if (previousInitiative and len(previousInitiative) > 0):
				msg += "Deleting previous " + (("initiative \"" + str(previousInitiative[0]) +"\"") if previousInitiative[0] else "initiative") + "...\n"
			cursor.execute("REPLACE INTO initiatives(channel_id, label, start_time) VALUES(?,?,?)", (context.channel.id, label, datetime.date.today()))
			cursor.execute("DELETE FROM characters WHERE channel_id=?", (context.channel.id,))
			cursor.execute("DELETE FROM initiative_values WHERE channel_id=?", (context.channel.id,))
			connection.commit()
			msg += "Initiative " + ("\"" + label + "\" " if label else "") + "started!\nUse `!initiative [name] [dice] [ego]` (name and ego are optional) to join\nType `!next` to start!\n*This is a beta feature. If you find any bugs, please DM <@154353119352848386>*"
		await context.send(msg)
		await cleanupDB()
	except Exception as e:
		await context.send("Failed to start initiative. Try a different channel, or ping <@154353119352848386> for immediate help")

async def cleanupDB():
	global cursor, connection
	try:
		cursor.execute("SELECT channel_id, start_time FROM initiatives")
		initiativesToCheck = cursor.fetchall()
		oldestDate = datetime.date.today() - datetime.timedelta(days=45)
		for initiative in initiativesToCheck:
			date = datetime.datetime.strptime(initiative[1], '%Y-%m-%d')
			date = datetime.date(date.year, date.month, date.day)
			if (date < oldestDate):
				id = initiative[0]
				cursor.execute("DELETE FROM initiatives WHERE channel_id=?", (id,))
				cursor.execute("DELETE FROM characters WHERE channel_id=?", (id,))
				cursor.execute("DELETE FROM initiative_values WHERE channel_id=?", (id,))
			connection.commit()
	except Exception as e:
	    print("Error while cleaning database")

########################## Add to Initiative ##########################
@bot.command(
	name='initiative',
	brief='Add yourself to the initiative',
	description='Use `!initiative [name] [dice] [ego]` to add yourself to this channel\'s initiative (name and ego are optional)',
	pass_context=True)
async def initiativeAdd(context, *args):
	global cursor, connection
	msg = ""
	try:
		await context.trigger_typing()
		# Parse and validate
		parsedArgs = parseInitiativeAdd(args)
		if (not parsedArgs):
			await context.send("Invalid input. Use `!help initiative` for more info.")
			return
		name = parsedArgs[0] if parsedArgs[0] else ""
		dice = parsedArgs[1]
		ego = parsedArgs[2]
		if (dice < 0 or (ego and ego < 0)):
			await context.send("Invalid input. Use `!help initiative` for more info.")
			return
		# Check that the initiative exists and is open
		cursor.execute("SELECT label, cur_initiative, verbose FROM initiatives WHERE channel_id=?", (context.channel.id,))
		initiative = cursor.fetchone()
		if (not initiative):
			await context.send("There is no active initiative in this channel")
			return
		if (initiative[1] >= 0):
			msg += "The initiative in this channel has already started. You will join at the beginning of the next round\n"
		# Check if the player is already in that initiative
		cursor.execute("SELECT name FROM characters WHERE channel_id=? AND mention=? AND name=?", (context.channel.id, context.author.mention, name))
		characters = cursor.fetchall()
		if (len(characters) > 0):
			if (not bool(initiative[2])):
				msg += (name if name else context.author.display_name) + " was already in the initiative. Overwriting...\n"
		# Add them and send message
		cursor.execute("REPLACE INTO characters(channel_id, mention, name, num_dice, num_ego) VALUES(?,?,?,?,?)", (context.channel.id, context.author.mention, name, dice, ego))
		connection.commit()
		msg += "Player " + (name if name else context.author.mention) + " was added to the initiative with " + str(dice) + " dice" + ((" and " + str(ego) + " ego") if ego else "")
		await context.send(msg)
	except Exception as e:
		await context.send("An error occurred while adding you to the initiative. Ping <@154353119352848386> for immediate help")

def parseInitiativeAdd(args):
	try:
		if (len(args) == 1 and type(int(args[0])) is int):
			return [None, int(args[0]), None]
		if (len(args) == 2):
			try:
				dice = int(args[0])
				ego = int(args[1])
				return [None, dice, ego]
			except:
				dice = int(args[1])
				return [args[0], dice, None]
		if (len(args) >= 3):
			dice = int(args[1])
			ego = int(args[2])
			return [args[0], dice, ego]
		return None
	except:
		return None

########################## Moving between turns ##########################
@bot.command(
	name='next',
	brief='Move to the next round of initiative',
	aliases=['next-initiative'],
	pass_context=True)
async def initiativeNext(context, *args):
	global cursor, connection
	msg = ""
	try:
		await context.trigger_typing()
		# Grab the initiative
		cursor.execute("SELECT label, round_number, cur_initiative, verbose FROM initiatives WHERE channel_id=?", (context.channel.id,))
		initiative = cursor.fetchone()
		if (not initiative):
			await context.send("There is no active initiative in this channel")
			return
		cur_initiative = initiative[2]
		round_number = initiative[1]
		# Grab the characters
		cursor.execute("SELECT mention, name, num_dice, num_ego from characters WHERE channel_id=?", (context.channel.id,))
		characters = cursor.fetchall()
		if (not characters):
			await context.send("There is no one in this channel's initiative")
			return
		# Check if we need to restart initiative
		if (cur_initiative < 0):
			round_number += 1
			msg += "Starting round " + str(round_number) + " of initiative" + ((" \"" + initiative[0] + "\"") if initiative [0] else "") + "...\n"
			cursor.execute("DELETE FROM initiative_values WHERE channel_id=?", (context.channel.id,))
			# Roll for everyone
			rolledCharacters = []
			for character in characters:
				result = roll(character[2], (character[3] if character[3] else 0)) #Dice, ego
				rolledCharacters.append(character + (result["successes"], result["triggers"], result["ones"]))
			# Sort them and add to DB
			successDict = sortCharactersBySuccesses(rolledCharacters)
			for val in successDict:
				if val > cur_initiative:
					cur_initiative = val
				cursor.execute("REPLACE INTO initiative_values(channel_id, value) VALUES(?,?)", (context.channel.id, val))
				for character in successDict[val]:
					insertionTuple = (context.channel.id, character[0], character[1], character[2], character[3], character[4], character[5], character[6])
					cursor.execute("REPLACE INTO characters(channel_id, mention, name, num_dice, num_ego, num_successes, num_triggers, num_ones) VALUES(?,?,?,?,?,?,?,?)", insertionTuple)
			connection.commit()
			# Print the overview
			msg += "Initiative order:\n"
			for val in reversed(range(cur_initiative+1)):
				if (val in successDict):
					names = []
					for character in successDict[val]:
						names.append(character[1] if character[1] else character[0])
					msg += "\t" + str(val) + ":\t" + ", ".join(names) + "\n"
			await context.send(msg)
			msg = ""
			await context.trigger_typing()

		# Do the turn
		cursor.execute("SELECT mention, name, num_ego, num_successes, num_triggers FROM characters WHERE channel_id=? AND num_successes=?", (context.channel.id, cur_initiative))
		characters = cursor.fetchall()
		msg += str(cur_initiative) + " successes\n"
		for character in characters:
			msg += character[0] + ", it is " + (character[1] + "\'s turn. " if character[1] else "your turn.")
			extraActions = math.floor(character[4]/2)
			if (extraActions > 0 or (initiative[1] == 1 and character[2])):
				msg += " You have "
			if (extraActions > 0):
				msg += str(extraActions) + " extra action(s) from triggers"
			if (extraActions > 0 and round_number == 1 and character[2]):
				msg += " and "
			if (round_number == 1 and character[2]):
				msg += str(character[2]) + " extra dice for your first action (from ego)"
			msg += "\n"
		await context.send(msg)

		# update the round number
		cursor.execute("SELECT MAX(value) FROM initiative_values WHERE value < ?", (cur_initiative,))
		nextInitiative = cursor.fetchone()
		cur_initiative = -1 if (nextInitiative[0] is None) else nextInitiative[0]
		insertionTuple = (context.channel.id, initiative[0], round_number, cur_initiative, initiative[3], datetime.date.today())
		cursor.execute("REPLACE INTO initiatives(channel_id, label, round_number, cur_initiative, verbose, start_time) VALUES(?,?,?,?,?,?)", insertionTuple)
		connection.commit()

	except Exception as e:
		await context.send("An error occurred while moving to next initiative. Ping <@154353119352848386> for immediate help")


def sortCharactersBySuccesses(characters):
	dict = {}
	for character in characters:
		if (character[4] in dict):
			dict[character[4]].append(character)
		else:
			dict[character[4]] = [character]
	return dict

########################## Debugging Functions ##########################
@bot.command(
	name='debugDB',
	brief='Debug the DB',
    enabled=True,
	pass_context=True)
async def debugDB(context, field:str):
	global cursor, connection
	try:
		cursor.execute("SELECT * FROM " + field)
		result = cursor.fetchall()
		await context.send(str(result))
	except Exception as e:
		await context.send(e)

@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)

bot.run(TOKEN)
