import discord
import os
import requests
import json
import random
from replit import db

client=discord.Client()
sad_words=["sad","depressed","unhappy","miserable","depressing"]

encouragments = ["Cheer up!","You are great"]

#returns a random quote from the api
def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  quote_json=json.loads(response.text)
  quote=quote_json[0]['q'] + " -" + quote_json[0]['a']
  return (quote)

def add_encouragment(message):
  if "user_encouragments" in db.Keys:
    user_encouragments = db["user_encouragments"]
    user_encouragments.append(message)
    db["user_encouragments"]=user_encouragments
  else:
    db["user_encouragments"]=[message]

def delete_encouragment(index):
  user_encouragments=db["user_encouragments"]

  if len(user_encouragments)>index:
    del user_encouragments[index]
    db["user_encouragments"]=user_encouragments


#this event will be called when the bot is ready 
@client.event
async def on_ready():
  print('We have logged int as {0.user}'.format(client))

@client.event
async def on_message(message):

  #if the message is from the bot
  if message.author==client.user:
    return

  msg= message.content

  #if the message is a command
  if msg.startswith('$inspire'):
    await message.channel.send(get_quote())

  options=encouragments
  if "user_encouragments" in db.Keys():
    options=options + db["user_encouragments"]

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

client.run(os.getenv('TOKEN'))

