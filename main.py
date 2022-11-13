import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions
from youtube_dl import YoutubeDL
import yfinance as yf
import requests
import random
import datetime
import array

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command("help")

YDL_Config = {'format': 'bestaudio/best',
              'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
              'restrictfilenames': True,
              'noplaylist': True,
              'nocheckcertificate': True,
              'ignoreerrors': False,
              'logtostderr': False,
              'quiet': True,
              'no_warnings': True,
              'default_search': 'auto',
              'source_address': '0.0.0.0'}

FFMPEG_Config = {'before_options': '-reconnect 1 '
                                   '-reconnect_streamed 1 '
                                   '-reconnect_delay_max 5',
                 'options': '-vn'}

reaction_embed = discord.Embed(
    title='Welcome to this server!',
    description='To get role, put the reaction below \n\n'
                ':gun: CS:GO\n'
                ':dodo: Dota2\n'
                ':warning: CoD: Warzone 2\n'
                ':goat: Valorant',
    color=0x8f5abb
)


@bot.event
async def on_ready():
    print('Bot is live!')
    print('SE-2203 THE BEST\n\n')


@bot.event
async def on_member_join(member):
    print(member)
    embed = discord.Embed(title=f"Welcome, {member.name}!", description=f"Thanks for joining **{member.guild.name}**!",
                          color=0x8f5abb)
    embed.set_footer(text='🔥 Tundra* powered by Karen, Adilet and Yelnur from SE-2203')
    embed.set_thumbnail(url='https://i.imgur.com/XHfTk8D.png')
    role = discord.utils.get(member.guild.roles, name="member")
    await member.add_roles(role)
    await member.send(embed=embed)


@bot.command()
@has_permissions(administrator=True, manage_messages=True, manage_roles=True)
async def admin(ctx, member: discord.Member):
    adminka = discord.utils.get(member.guild.roles, name="admin")
    await member.add_roles(adminka)
    print(f'{member} now is admin')
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=discord.Embed(title='Successful!', description=f'{member} now is admin!', color=0x00ff00),
                   delete_after=10)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == reactionroles_message:
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if str(payload.emoji) == '🔫':
            role = discord.utils.get(message.guild.roles, name="CSGO")
            await payload.member.add_roles(role)
        if str(payload.emoji) == '🦤':
            role = discord.utils.get(message.guild.roles, name="Dota2")
            await payload.member.add_roles(role)
        if str(payload.emoji) == '⚠️':
            role = discord.utils.get(message.guild.roles, name="Warzone")
            await payload.member.add_roles(role)
        if str(payload.emoji) == '🐐':
            role = discord.utils.get(message.guild.roles, name="Valorant")
            await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == reactionroles_message:
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        guild = await(bot.fetch_guild(payload.guild_id))
        member = await(guild.fetch_member(payload.user_id))
        if str(payload.emoji) == '🔫':
            role = discord.utils.get(message.guild.roles, name="CSGO")
            await member.remove_roles(role)
        if str(payload.emoji) == '🦤':
            role = discord.utils.get(message.guild.roles, name="Dota2")
            await member.remove_roles(role)
        if str(payload.emoji) == '⚠️':
            role = discord.utils.get(message.guild.roles, name="Warzone")
            await member.remove_roles(role)
        if str(payload.emoji) == '🐐':
            role = discord.utils.get(message.guild.roles, name="Valorant")
            await member.remove_roles(role)


@bot.command()
async def clear(ctx, message_count: int):
    await ctx.channel.purge(limit=message_count + 1)
    clear_embed = discord.Embed(description=f"{ctx.message.author.mention} just deleted {message_count} messages",
                                color=0x8f5abb)
    await ctx.send(embed=clear_embed, delete_after=10)


@bot.command(aliases=['h', 'хелп'])
async def help(ctx):
    embed = discord.Embed(title='**Tundra`s** commands',
                          description='• **clear** (value)  —  clears (value) messages in the channel\n'
                                      '• **play** (url or name)  —  plays music in the voice channel\n'
                                      '• **join**  —  connects Tundra to the voice channel\n'
                                      '• **pause**  —  pauses music\n'
                                      '• **resume**  —  resumes music\n'
                                      '• **ban** (member, time, reason)  —  bans chosen member\n'
                                      '• **kick** (member)  —  kicks member from the server\n'
                                      '• **mute** (member)  —  mutes member\n'
                                      '• **unmute** (member)  —  unmutes member\n'
                                      '• **finance** (ticker)  —  finds and information about ticker\n'
                                      '• **roll** (start, end)  —  generates random number from \n'
                                      '• **coinflip**  —  flips the coin\n'
                                      '• **password** (length) (0 or 1)  —  generates hard(1) or medium(0) '
                                      'password\n'
                                      '• **admin** (member)   —  gives admin role to chosen member', color=0x8f5abb)
    embed.set_footer(text='🔥 Tundra* powered by Karen, Adilet and Yelnur from SE-2203')
    embed.set_thumbnail(url='https://i.imgur.com/XHfTk8D.png')
    await ctx.send(embed=embed)
    return


# Music bot
@bot.command(aliases=['play', 'add'])
async def p(ctx, *, url):
    print(url)

    if not ctx.message.author.voice:
        await ctx.send('You must be in a voice channel ¯\_(ツ)_/¯')

    if not ctx.voice_client:
        playmusic = await ctx.message.author.voice.channel.connect()
    else:
        playmusic = ctx.voice_client

    with YoutubeDL(YDL_Config) as ydl:
        if 'https://' in url:
            info = ydl.extract_info(url, download=False)
        else:
            info = ydl.extract_info(f'ytsearch:{url}', download=False)['entries'][0]

    link = info['formats'][0]['url']
    playmusic.play(discord.FFmpegPCMAudio(executable='ffmpeg\\ffmpeg.exe', source=link, **FFMPEG_Config))
    await ctx.send(embed=discord.Embed(description=f'Bot started playing {url}', color=0x8f5abb))


@bot.command(aliases=['exit'])
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send(embed=discord.Embed(description="Bot has left channel", color=0x8f5abb))
    else:
        await ctx.send(embed=discord.Embed(description="Bot is not in a voice channel", color=0x8f5abb))


@bot.command(aliases=['connect', 'enter'])
async def join(ctx):
    if not ctx.voice_client:
        await ctx.message.author.voice.channel.connect()
        await ctx.send(embed=discord.Embed(description="Bot has joined channel", color=0x8f5abb))
    else:
        await ctx.send(embed=discord.Embed(description="Bot is already in a voice channel", color=0x8f5abb))


@bot.command(aliases=['unpause'])
async def resume(ctx):
    if not ctx.voice_client.is_playing():
        ctx.voice_client.resume()
        await ctx.send(embed=discord.Embed(description="Bot has been unpaused", color=0x8f5abb))
    else:
        await ctx.send(embed=discord.Embed(description="Bot is not paused", color=0x8f5abb))


@bot.command()
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send(embed=discord.Embed(description="Bot has been paused", color=0x8f5abb))
    else:
        await ctx.send(embed=discord.Embed(description="Bot is not playing", color=0x8f5abb))


@bot.command()
@has_permissions(administrator=True, manage_messages=True, manage_roles=True)
async def reactionroles(ctx):
    await ctx.channel.purge(limit=1)
    message = await ctx.send(embed=reaction_embed)
    await message.add_reaction('🔫')
    await message.add_reaction('🦤')
    await message.add_reaction('⚠️')
    await message.add_reaction('🐐')
    global reactionroles_message
    reactionroles_message = message.id
    print(f'new reactionroles message id: {reactionroles_message}')


@bot.command()
@has_permissions(administrator=True, manage_messages=True, manage_roles=True)
async def ban(ctx, member: discord.Member = None, time=None, *, reason: str = None):
    async def unb(member):
        async for ban_user in ctx.guild.bans():
            if ban_user.user == member:
                await ctx.guild.unban(ban_user.user)

    if member:
        if time:
            time_letter = time[-1:]
            time_numbers = int(time[:-1])

            def t(time_letter):
                if time_letter == 's':
                    return 1
                if time_letter == 'm':
                    return 60
                if time_letter == 'h':
                    return 60 * 60
                if time_letter == 'd':
                    return 60 * 60 * 24

            if reason:
                await member.ban(reason=reason)
                await ctx.send(embed=discord.Embed(
                    description=f'User {member.mention} has been banned \nTime: {time} \nReason: {reason}',
                    color=0x8f5abb))

                await asyncio.sleep(time_numbers * t(time_letter))

                await unb(member)
                await ctx.send(
                    embed=discord.Embed(description=f'User {member.mention} has been unbanned', color=0x8f5abb))
            else:
                await member.ban()
                await ctx.send(embed=discord.Embed(description=f'User {member.mention} has been banned \nTime: {time}',
                                                   color=0x8f5abb))

                await asyncio.sleep(time_numbers * t(time_letter))

                await unb(member)
                await ctx.send(
                    embed=discord.Embed(description=f'User {member.mention} has been unbanned', color=0x8f5abb))
        else:
            await member.ban()
            await ctx.send(embed=discord.Embed(description=f'User {member.mention} has been banned', color=0x8f5abb))
    else:
        await ctx.send(embed=discord.Embed(title='Error 404', description='Enter username', color=0x8f5abb))


@bot.command()
@has_permissions(administrator=True, manage_messages=True, manage_roles=True)
async def kick(ctx, member: discord.Member = None, *, reason: str = None):
    if member:
        if reason:
            await member.kick(reason=reason)
            await ctx.send(embed=discord.Embed(description=f'User {member.mention} has been kicked \nReason: {reason}',
                                               color=0x8f5abb))
        else:
            await member.kick()
            await ctx.send(embed=discord.Embed(description=f'User {member.mention} has been kicked', color=0x8f5abb))
    else:
        await ctx.send('Enter user`s name')


@bot.command(pass_context=True)
@has_permissions(administrator=True, manage_messages=True, manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(member.guild.roles, name='Muted')
    await member.add_roles(role)
    embed = discord.Embed(title="User Muted!",
                          description="**{0}** was muted by **{1}**!".format(member, ctx.message.author),
                          color=0x8f5abb)
    await ctx.send(embed=embed)


@bot.command()
async def test(ctx):
    await ctx.send('test')


@bot.command(aliases=['unm'])
@has_permissions(administrator=True, manage_messages=True, manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(member.guild.roles, name='Muted')
    await member.remove_roles(role)
    await ctx.send(embed=discord.Embed(title="User Muted!",
                                       description=f"{member.mention} was unmuted by {ctx.message.author.mention}",
                                       color=0x8f5abb))


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if "idiot" in message.content:
        await message.channel.purge(limit=1)
        await message.channel.send(embed=discord.Embed(title="User Muted!",
                                                       description=f"{message.author.mention} was unmuted for using bad word",
                                                       color=0x8f5abb))
        muted_role = discord.utils.get(message.guild.roles, name="Muted")
        await message.author.add_roles(muted_role)
    await bot.process_commands(message)


@bot.command(aliases=['stock', 'price', 'yfinance', 'stocks'])
async def finance(ctx, name=None):
    if name is None:
        await ctx.send(embed=discord.Embed(title='Error 404', description='Write a ticker', color=0x8f5abb))
        return

    stock = yf.Ticker(name)
    if stock.info['regularMarketPrice'] is None:
        await ctx.send(embed=discord.Embed(title='Not found', description='This ticker wasn`t found', color=0xff0000))
        return

    count_difference = int(stock.info['regularMarketPrice']) - int(stock.info['previousClose'])
    color = 0xff0000

    if count_difference >= 0:
        color = 0x00ff00

    embed = discord.Embed(title=f"{stock.info['shortName']}",
                          description=f"**Market price for stock:** ${stock.info['regularMarketPrice']} \n"
                                      f"**Day Highest price:** ${stock.info['dayHigh']}\n"
                                      f"**Day Lowest price:** ${stock.info['dayLow']}\n"
                                      f"**Market Cap:** ${stock.info['marketCap']}\n\n"
                                      f"**Ticker:** {stock.info['symbol']}",
                          timestamp=datetime.datetime.utcnow(), color=color)

    embed.set_footer(text='powered by Yahoo Finance API', icon_url="https://i.imgur.com/uZIlRnK.png")
    embed.set_thumbnail(url=stock.info['logo_url'])
    await ctx.send(embed=embed)


@bot.command()
async def roll(ctx, start: int = None, end: int = None):
    if start is None and end is None:
        start = 1
        end = 100
    if end is None:
        end = start
        start = 1
    if end < start or start < 0:
        await ctx.send(embed=discord.Embed(title=f'Wrong input!', color=0x8f5abb))
        return
    answer = random.randint(start, end)
    print(answer)
    await ctx.send(embed=discord.Embed(title=f'Number generated from {start} to {end}', description=f'**{answer}**',
                                       color=0x8f5abb))


@bot.command(aliases=['flip', 'coin', 'coinf', 'cflip'])
async def coinflip(ctx):
    if random.randint(0, 1) == 0:
        answer = "Heads"
    else:
        answer = "Tails"

    await ctx.send(embed=discord.Embed(title=f'Coinflip', description=f'Result: **{answer}**',
                                       color=0x8f5abb))


@bot.command()
async def password(ctx, length: int = 10, strong:int = 0):
    MAX_LEN = int(length)

    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    lowercase_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    uppercase_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                            'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    symbols = ['@', '$', '%', '=', '?', '.', '*']

    if strong == 1:
        combined_list = digits + lowercase_characters + uppercase_characters + symbols
        rand_digit = random.choice(digits)
        rand_upper = random.choice(uppercase_characters)
        rand_lower = random.choice(lowercase_characters)
        rand_symbol = random.choice(symbols)
        temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    else:
        combined_list = digits + lowercase_characters + uppercase_characters
        rand_digit = random.choice(digits)
        rand_upper = random.choice(uppercase_characters)
        rand_lower = random.choice(lowercase_characters)
        temp_pass = rand_digit + rand_upper + rand_lower

    for x in range(MAX_LEN - 4):
        temp_pass += random.choice(combined_list)
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    passw = ""
    for x in temp_pass_list:
        passw += x

    if strong == 0:
        hard = 'medium'
    else:
        hard = 'hard'
    await ctx.message.author.send(embed=discord.Embed(title=f'Your generated {hard} password is: ',
                                       description=f'{passw}\n', color=0x8f5abb))
    await ctx.send(embed=discord.Embed(description=f'Your password has been generated in direct messages',
                                       color=0x8f5abb))
    return


bot.run('MTAzMTg1MTEzMjYyMTk2NzM4Mg.GKMoco.bO30G5BuiT-2NosHDd-HR8Z-vtaSXDW8Mbi_BQ')