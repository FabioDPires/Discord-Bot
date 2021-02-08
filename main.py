import discord

client=discord.Client()

#this event will be called when the bot is ready 
@client.event
async def on_ready():
  print('We have logged int as {0.user}'.format(client))
