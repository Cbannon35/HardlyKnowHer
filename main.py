
###########
# IMPORTS #
###########
import discord
import os
import re
from os.path import exists
from keep_alive import keep_alive

#from geeksforgeeks @citation
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

##############
# CORE LOGIC #
##############
@client.event
async def on_message(message):
  """
  1. Differentiates state file based on server id
  2. Creates a state file if the bot is new and sends init message
  3. Reads user messages and determines if it warrants a response
  """
  # Grab state file
  state_file_path = 'states/' + str(message.guild.id) + '.txt'
  # Create the state file if it does not exist
  if not exists(state_file_path):
    f = open(state_file_path,"w+").write(str(1))
    await message.channel.send('Use \"~help\" to view commands!')

  with open(state_file_path) as f:
    state = f.readlines()
  # Read state file: either 1 or 0 --> on or off
  on = int(state[0])
  # The bot itself cannot trigger a response from itself
  if message.author == client.user:
      return
  # Check for commands
  if message.content.startswith('~'):
    await handle_commands(message, message.content[1:])
    return
  
  # Parses messages for keywords if bot is on.
  if(on):
    if message.content.startswith('hello'):
        await message.channel.send('Hello!')
    split_msg = message.content.split(" ");
    for word in split_msg:
      # Remove puncuation
      word = re.sub('[!@#$\"?\']', '', word)
      # Would be lame to get a response to the bot's name
      if word[-6:] != "knower":
        if count_syllables(word) > 1:
          if word[-2:] == "er":
              await message.channel.send(word +"? " + "But I hardly know her")   

async def handle_commands(message, command):
  """
  Handles command messages
  """
  # Help command
  if command == "help":
    await message.channel.send(open('help.txt', 'r').read())
  state_file_path = 'states/' + str(message.guild.id) + '.txt'
  # On command
  if command == "on":
    open(state_file_path, "w").write("1")
    await message.channel.send("I'm on!")
  # Off command
  if command == "off":
    open(state_file_path,"w").write("0")
    await message.channel.send("I'm off :'(")
    
  return

#
# Taken from code review
# https://codereview.stackexchange.com/questions/224177/python-function-to-count-syllables-in-a-word
#
def count_syllables(word):
    return len(
        re.findall('(?!e$)[aeiouy]+', word, re.I) +
        re.findall('^[^aeiouy]*e$', word, re.I)
    )

# Starts webserver 
keep_alive()

# Gets token of bot from environment variable 
client.run(os.getenv('TOKEN'))
