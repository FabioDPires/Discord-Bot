import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client=discord.Client()
sad_words=["sad","depressed","unhappy","miserable","depressing"]

encouragments = ["Cheer up!","You are great"]

if "responding" not in db.keys():
  db["responding"]=True

#returns a random quote from the api
def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  quote_json=json.loads(response.text)
  quote=quote_json[0]['q'] + " -" + quote_json[0]['a']
  return (quote)

def add_encouragment(message):
  if "user_encouragments" in db.keys():
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
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):

  #if the message is from the bot
  if message.author==client.user:
    return

  msg= message.content

  #if the message is a command
  if msg.startswith('$inspire'):
    await message.channel.send(get_quote())

  if db["responding"]:
    options=encouragments
    if "user_encouragments" in db.keys():
      options=options + db["user_encouragments"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith('$add'):
    encouraging_message=msg.split("$add ",1)[1]
    add_encouragment(encouraging_message)
    author=str(message.author)
    author=author.split("#")[0]
    print(author)
    thanks="Thanks for contributting {} ".format(author) +"\U0001F601"
    await message.channel.send(thanks)

  if msg.startswith('$delete'):
    if discord.utils.get(message.author.roles, name="Admin") is None:
      author=str(message.author)
      author=author.split("#")[0]
      negate="What do you think you are doing {} ? Get the fu** out".format(author)+" \U0001F92C"
      await message.channel.send(negate)
    else:
      user_encouragments=[]
      if "user_encouragments" in db.keys():
        index=int(msg.split('$delete',1)[1])
        delete_encouragment(index)
        user_encouragments=db["user_encouragments"]
      
      if len(user_encouragments)>0:
        await message.channel.send(user_encouragments)

      else:
        await message.channel.send("There is no messages added by the server's users")
  
  if msg.startswith('$all'):
      user_encouragments=[]
      user_encouragments=db["user_encouragments"]
      if len(user_encouragments)>0:
        await message.channel.send(user_encouragments)
      else:
        await message.channel.send("There is no messages added by the server's users")
  
  if msg.startswith('$responding'):
    if discord.utils.get(message.author.roles, name="Admin") is None:
      await message.channel.send("You are not authorized to this action!")
    else:
      value=msg.split("$responding ",1)[1]
      if(value.lower()=="true"):
        db["responding"]=True
        await message.channel.send("The bot is now responding to messages")
      else:
        db["responding"]=False
        await message.channel.send("The bot is now not responding to messages")

  if msg.startswith('$delall'):
    if discord.utils.get(message.author.roles, name="Admin") is None:
      await message.channel.send("You are not authorized to this action!")
    else:
      db["user_encouragments"]=[]
      await message.channel.send("All the messages added by the users where deleted")

keep_alive()
client.run(os.getenv('TOKEN'))

