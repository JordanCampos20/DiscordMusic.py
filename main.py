#DiscordBot - JordanBOT

#Bibliotecas
import discord
import random
import yt_dlp
import os
import re
import asyncio
from discord.ext import commands
from discord import Permissions

# Precisa do Modo Desenvolvedor Ativado - Discord / Configurações / Avançado / Modo Desenvolvedor = True
var_OWNERS = ['ID DO DISCORD']

#-------UM BOT-------

var_NAME = 'NOME DO BOT'
var_TOKEN = 'TOKEN DO BOT'
var_PREFIX = 'PREFIXO PARA O COMANDO DO BOT'
var_CLIENTID = 'ID DO BOT'

#-------DOIS OU MAIS BOT-------

# while(True):
#     escolha = input(f'1 Para BOT1 / 2 Para BOT2: ')
#
#     var_NAME = ''
#     var_TOKEN = ''
#     var_CLIENTID = ''
#     var_PREFIX = ''
#
#     if escolha == '1':
#         var_NAME = 'NOME DO BOT'
#         var_TOKEN = 'TOKEN DO BOT'
#         var_PREFIX = 'PREFIXO PARA O COMANDO DO BOT'
#         var_CLIENTID = 'ID DO BOT'
#         break
#     elif escolha == '2':
#         var_NAME = 'NOME DO BOT'
#         var_TOKEN = 'TOKEN DO BOT'
#         var_PREFIX = 'PREFIXO PARA O COMANDO DO BOT'
#         var_CLIENTID = 'ID DO BOT'
#         break
#     else:
#         continue

#-----------------------------------------------------------------------------------------------------------------------

token = var_TOKEN

#-----ALGUNS CHAMAM DE "client =" ou de "bot = ", Mude se Preferir
client = commands.Bot(command_prefix=f"{var_PREFIX}", owner_ids=set(var_OWNERS), help_command=None)

#----AO INICIAR MOSTRA:
@client.event
async def on_ready():
    print(f''' 

     ██╗ ██████╗ ██████╗ ██████╗  █████╗ ███╗   ██╗  ██████╗  ██████╗ ████████╗
     ██║██╔═══██╗██╔══██╗██╔══██╗██╔══██╗████╗  ██║  ██╔══██╗██╔═══██╗╚══██╔══╝  
     ██║██║   ██║██████╔╝██║  ██║███████║██╔██╗ ██║  ██████╔╝██║   ██║   ██║     
██   ██║██║   ██║██╔══██╗██║  ██║██╔══██║██║╚██╗██║  ██╔══██╗██║   ██║   ██║     
╚█████╔╝╚██████╔╝██║  ██║██████╔╝██║  ██║██║ ╚████║  ██████╔╝╚██████╔╝   ██║     
 ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═════╝  ╚═════╝    ╚═╝     


BOT: {var_NAME}
    
LINK: https://discord.com/api/oauth2/authorize?client_id={var_CLIENTID}&permissions=8&scope=bot

''')

#-----PARA MUDAR O STATUS DO BOT: status=discord.Status.{opção} / EXEMPLO: discord.Status.idle
    #ATIVIDADE DO BOT: Jogando
#    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"{var_PREFIX}help | {var_NAME}.com"))
#-----ATIVIDADE DO BOT: Stremando
#    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.streaming, name=f"{var_PREFIX}help | {var_NAME}.com"))

#-----A QUE ESTÁ SENDO UTILIZADA
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{var_PREFIX}help | {var_NAME}.com"))

#-----------------------------------------------------------------------------------------------------------------------

#-----TESTADOR DE EMBED, USE PARA VER COMO VAI FICAR
#----Comando: embed / Pode ser Usado com o Prefix e o aliases depois, Exemplo: !embed
@client.command(name='embed', aliases=['em', 'Em', 'Embed'])
async def embed(ctx):
    embed=discord.Embed(title=f"{var_NAME}", url=f"https://{var_NAME}.com", description=f"Server Tested: {ctx.guild.name}, Owner: <@{ctx.author.id}> {var_NAME} Working..", color=discord.Color.blue())
    await ctx.send(embed=embed)

#----Comando: help / Pode ser Usado com o Prefix e o aliases depois, Exemplo: !help
@client.command(name='help', aliases=['h', 'H', 'Help'])
async def help(ctx):
    await ctx.send(f"""
    ```css

[Music Help]

{var_PREFIX}(j)oin - Joins your current voice channel

{var_PREFIX}(p)lay [Song] - Plays and/or enqueues a song/playlist

{var_PREFIX}(l)eave - Leaves the voice channel

{var_PREFIX}(pa)use - Pause Song

{var_PREFIX}resume - Return Song

Examples:
    {var_PREFIX}play example song
    {var_PREFIX}join
    {var_PREFIX}pause
    {var_PREFIX}resume
    {var_PREFIX}leave

```""")

#----Comando: join / Pode ser Usado com o Prefix e o aliases depois, Exemplo: !join
@client.command(name='join', aliases=['j', 'J', 'Join'])
async def join(ctx):
    #----Se o Autor da Mensagem Não Estiver Em Nenhuma Sala
    if ctx.author.voice is None:
      #----Retorna Uma Resposta No Chat
      return await ctx.send("You are not connected to a voice channel")
    #----Se Não
    else:
      #----Pega o Canal do Autor e Cola na Variavel "channel"
      channel = ctx.author.voice.channel
      #----Conecta no "channel"
      await channel.connect()
      #----Imprimi Uma Mensagem no Console
      print(f"{var_NAME}: Connected in the room {channel}")

#----Comando: play / Pode ser Usado com o Prefix e o aliases depois, Exemplo: !play
@client.command(name='play', aliases=['p', 'P', 'Play'])
async def play(ctx, url=str('')):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'progress': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        res = re.findall(r'\w+', url)

        try:
            urlvideo = str(res[6])
        except:
            await ctx.send("You entered an invalid url")
            return

        urlyout = f"https://www.youtube.com/watch?v="

        urlfinal = f"{urlyout}{urlvideo}"

        if len(urlvideo) > 4:
            try:
                info_dict = ydl.extract_info(urlfinal, download=False)
                video_title = info_dict.get('title', None)
                ydl.download([urlfinal])
            except:
                return
        else:
            await ctx.send(
                'No results matching your query. Please try something else.')

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    try:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"@{ctx.author.voice.channel}")
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    except:
        await ctx.send("You are not connected to a voice channel")

    if urlfinal != '':

        if not voice is None:
            print(' \n ')
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            embed = discord.Embed(title=f":notes: {video_title}", description=f"[<@{ctx.author.id}>]", url=f"{url}",
                                  color=discord.Color.magenta())
            embed.add_field(name="**Queue**",
                            value=f"[View on {var_NAME}.com](https://{var_NAME}.com/server/{ctx.guild.id}/queue)", inline=False)
            print(f"{var_NAME}: Playing - {video_title}")
            await ctx.send(embed=embed)

        else:
            print(' \n ')
            channel = ctx.author.voice.channel
            await channel.connect()
            print(f"{var_NAME}: Connected {channel}")
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            embed = discord.Embed(title=f":notes: {video_title}",description=f"[<@{ctx.author.id}>]" , url=f"{url}", color=discord.Color.magenta())
            embed.add_field(name="**Queue**",value=f"[View on {var_NAME}.com](https://{var_NAME}.com/server/{ctx.guild.id}/queue)" , inline=False)
            print(f"{var_NAME}: Tocando - {video_title}")
            await ctx.send(embed=embed)

            while voice.is_playing():
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(90)
                while voice.is_playing():
                    break
                else:
                    await voice.disconnect()
                    print(f"{var_NAME}: It disconnected by itself because it wasn't playing music")
                    await ctx.send(
                        f":no_entry_sign: Left channel due to inactivity. Help support {var_NAME} and get some awesome perks with {var_NAME} PRO. https://{var_NAME}.com/")

    elif urlfinal == '':
        channel = ctx.author.voice.channel
        await channel.connect()
        print(f"{var_NAME}: Connected")

    else:
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel")
        else:
            await ctx.send("You entered an invalid url")

#----Comando: leave / Pode ser Usado com o Prefix e o aliases depois, Exemplo: !leave
@client.command(name='leave', aliases=['l', 'L', 'Leave'])
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_connected():
            embed = discord.Embed(description=":no_entry: Left and unbound channels.", color=discord.Color.magenta())
            await ctx.send(embed=embed)
            await voice.disconnect()
            print(f"{var_NAME}: Disconnected")
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    except:
        await ctx.send("The bot is not connected to a voice channel.")
        return

#----Comando: pause / Pode ser Usado com o Prefix e o aliases depois, Exemplo: !pause
@client.command(name='pause', aliases=['pa', 'Pa', 'Pause'])
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing():
            voice.pause()
            print(f"{var_NAME}: Paused the music")
        else:
            await ctx.send("Currently no audio is playing.")
    except:
        await ctx.send("Currently no audio is playing..")
        return

#----Comando: resume / Pode ser Usado com o Prefix e o aliases depois, Exemplo: !resume
@client.command(name='resume', aliases=['r', 'R', 'Resume'])
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_paused():
            voice.resume()
            print(f"{var_NAME}: The audio is paused")
        else:
            await ctx.send("The audio is not paused.")
    except:
        await ctx.send("The audio is not paused.")
        return

#----Comando: stop / Pode ser Usado com o Prefix e o aliases depois, Exemplo: !stop
@client.command(name='stop', aliases=['s', 'S', 'Stop'])
async def stop(ctx):
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if not voice is None:
            print(f"{var_NAME}: Stop the music")
            voice.stop()
    except:
        await ctx.send("Could not stop the music.")
        return

#----Comando: mute / Pode ser Usado com o Prefix e o aliases depois, Exemplo: !mute
@client.command(name='mute', aliases=['Mute'])
async def mute(ctx, member:discord.Member=None, reason=None):
    try:
        if member == None or member == ctx.message.author:
            await ctx.channel.send("You can't silence yourself!")
            print(f"{var_NAME}: {member} You can't silence yourself.")
            return
        if reason == None:
            reason = "REASON!"
        message = f"Sorry ae, but, you were {member.name} was mutated by {reason}"
        await member.send(message)
        await member.edit(mute=True)
        await ctx.channel.send(f"{member} has been silence!")
        print(f"{var_NAME}: The {member} has been silence by {reason}")
    except:
        await ctx.send(f"It was not possible to silence the {member.name}.")
        return

#----Comando: unmute / Pode ser Usado com o Prefix e o aliases depois, Exemplo: !unmute
@client.command(name='unmute', aliases=['Unmute'])
async def unmute(ctx, member:discord.Member=None):
    try:
        if member == None:
            await ctx.channel.send("Can't silence nothing!")
            print(f"{var_NAME}: {member} Can't silence nothing.")
            return
        await member.edit(mute=False)
        await ctx.channel.send(f"{member} It was unmuted!")
        print(f"{var_NAME}: {member.name} It was unmuted!")
    except:
        await ctx.send(f"It was not possible to unmute the {member.name}.")
        return

#-----Executa o BOT
try:
    client.run(token, bot=True)
except:
    print(f''' 

     ██╗ ██████╗ ██████╗ ██████╗  █████╗ ███╗   ██╗  ██████╗  ██████╗ ████████╗
     ██║██╔═══██╗██╔══██╗██╔══██╗██╔══██╗████╗  ██║  ██╔══██╗██╔═══██╗╚══██╔══╝  
     ██║██║   ██║██████╔╝██║  ██║███████║██╔██╗ ██║  ██████╔╝██║   ██║   ██║     
██   ██║██║   ██║██╔══██╗██║  ██║██╔══██║██║╚██╗██║  ██╔══██╗██║   ██║   ██║     
╚█████╔╝╚██████╔╝██║  ██║██████╔╝██║  ██║██║ ╚████║  ██████╔╝╚██████╔╝   ██║     
 ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═════╝  ╚═════╝    ╚═╝     

Precisa Mudar as "Settings" Para Funcionar, São Elas:

    var_NAME = {var_NAME}
    var_TOKEN = {var_TOKEN}
    var_PREFIX = {var_PREFIX}
    var_CLIENTID = {var_CLIENTID}
    
''')