import discord
import os
import requests
import json

client=discord.Client()

#returns a random quote from the api
def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  quote_json=json.loads(response.text)
  quote=quote_json[0]['q'] + " -" + quote_json[0]['a']
  return (quote)

#this event will be called when the bot is ready 
@client.event
async def on_ready():
  print('We have logged int as {0.user}'.format(client))

@client.event
async def on_message(message):

  #if the message is from the bot
  if message.author==client.user:
    return

  #if the message is a command
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!!!')

client.run(os.getenv('TOKEN'))

