import discord
from discord.ext import commands
import requests
import json
import random
import logging
import os
import pypokedex
from keep_alive import keep_alive

from calculator.simple import SimpleCalculator
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!',intents=intents)
c = SimpleCalculator()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "\n- " + json_data[0]['a'] 
  return (quote)

#check if the bot has logged on to the discord server
@client.event
async def on_ready():
 
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Anime"))
  print('logged in as')
  print(client.user.name)
  print(client.user.id)
  print('-----')


#This event is used to check a member on discord has joined
@client.event
async def on_member_join(member):
  channel = client.get_channel(841046339181477940)
  await channel.send('Welcome to the Server Use .help for more information '+member.mention)
  print(member.mention+'has joined')

#this event is used to check if a member of discord has been removed
@client.event
async def on_member_remove(member):
  channel = client.get_channel(841046339181477940)
  await channel.send(member.mention+' has left the server')
  print(member.mention+'has Left The server')

#This event is used to check if a message has been sent and will log messages to a specific channel 
@client.event
async def on_message(message):
#use this message to prevent the bot from recursively send messages
  if message.author == client.user:
    return
  author = message.author
  content = message.content
  channel = message.channel
  channel2 = client.get_channel(847988731767423006)
  await channel2.send('{} : "{}" : {}'.format(author,content,channel))
  await client.process_commands(message)

 
#This event is used to check what messages have been deleted from the server
@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    channel3 = client.get_channel(848107253865119755)
    await channel3.send('Deleted {} : "{}" : {}'.format(author,content,channel))

#This event is used to check what messages have been edited and will show the before and after changes in the messages
@client.event
async def on_message_edit(before, after):
  author = before.author
  channel = before.channel
  content = before.content
  content2 = after.content
  channel2 = client.get_channel(848108844411519006)
  await channel2.send('Edit {} : Before: "{}" After: {} : {}'.format(author,content,content2,channel))


@client.command()
async def test(ctx, arg):
  await ctx.send("HI")
# This command is used to access and search for a twtich user so as long as they exist 
@client.command()
async def twitch(ctx,arg):
  await ctx.send(embed=discord.Embed(title=arg, url="https://www.twitch.tv/"+arg, description=arg, color=0x800080))


#This command is used to get the ping of a user 
@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! In {round(client.latency * 1000)}ms')

#This command is used as a calculator 
@client.command()
async def calc(ctx,*,arg):
  c.run(arg)
  await ctx.send('The Answer is {}'.format(c.lcd))
#This command is used to flip a coin whether it being heads or tails
@client.command()
async def coin(ctx):
  randomvar = random.randint(1,2)
  if(randomvar==1):
    await ctx.send('Heads!',file = discord.File('heads.png'))
  else:
    await ctx.send('Tails!',file=discord.File('tails.png'))
#this comamand is used to clear messages depending on the number entered 
@client.command()
async def clear(ctx,arg):
  if(arg=='all'):
    await ctx.channel.purge(limit=10000000000)
  else:
    await ctx.channel.purge(limit = int(arg))  
#This command will take the poke api and call it which will display the info about a certain pokemon
@client.command()
async def poke(ctx,arg):
  nameDex = arg
  poke = pypokedex.get(name = nameDex)
  title  = poke.name
  title2 = title.upper()
  
  embed = discord.Embed(title = title2,description = 'Pokemon',color=0xffcb05)
  url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{poke.dex}.png"
  embed.set_image(url=url)
  embed.set_thumbnail(url=url)  
  embed.add_field(name='Dex',value = '# '+str(poke.dex),inline = True)
  embed.add_field(name='Height',value = str(poke.height)+'`',inline = True)
  embed.add_field(name='Weight',value = str(poke.weight)+' lbs',inline = True)
  embed.add_field(name='Types',value = '\n'.join(map(str, poke.types)),inline = True)
  embed.add_field(name='Base Experience',value = poke.base_experience,inline = False)
  embed.add_field(name='Abilites',value = '\n'.join(map(str, poke.abilities)),inline = True)
  embed.add_field(name='Base Stats',value = str(poke.base_stats)[10:-1],inline = False)
  await ctx.send(embed = embed)
#This command is used to show the list of commands to the user
@client.command()
async def commands(ctx):
  embed = discord.Embed(title = '!command ',description = 'List of commands',color = 0x7289da)
  embed.add_field(name='!twitch <twitch channel name>',value = 'Gets the user/channel from twitch',inline = False)
  embed.add_field(name='!calc <operations>',value = 'Basic Calculator can do addition,subtraction,mutlplction,divison and mod with each number and opperand spaced',inline = False)
  embed.add_field(name='!ping',value = 'Gets the user Ping',inline = False)
  embed.add_field(name='!clear',value = 'Clears the most recent 100 messages only avaliable to admins',inline = False)
  embed.add_field(name='!coin',value = 'Flips a coin either landing on heads or tails',inline = False)
  embed.add_field(name='!poke<pokemon <name> or <dex>',value = 'Shows the stats of a speciifc pokemon',inline = False)
  await ctx.send(embed = embed)
#this command is used to kick members
@client.command()
async def kick(ctx,member : discord.Member,*,reason = 'none'):
  await member.kick(reason = reason)
#this command is used to ban members
@client.command()
async def ban(ctx,member : discord.Member,*,reason = 'none'):
   await member.ban(reason = reason)

@client.command()
async def quote(ctx):
  quote = get_quote()
  await ctx.send(quote);

@client.command()
async def assignrole(ctx, user: discord.Member, role: discord.Role):
  await user.add_roles(role)
  await ctx.send(f"hey {user.name} has been giving a role called: {role.name}")

@client.command()
async def removerole(ctx, user: discord.Member, role: discord.Role):
  await user.remove_roles(role)
  await ctx.send(f"{user.name} has been removed a role called: {role.name}")


keep_alive()
client.run(os.getenv('TOKEN'))
