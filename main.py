import discord

client=discord.Client()

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
    await message.channel.send('Hello')


