# ----24/7-HOSTING----
# from webserver import keep_alive
# --24/7-HOSTING-END--

# ----REQUIRED-LIBRARYS----
import discord
import instagramy.core.exceptions
from discord.ext import commands
from get_time import get_time, get_exact_time
from get_date import get_date, get_date_in_ten_years
from weather import get_weather, tell_weather
from gtts import gTTS
import os
from time import sleep
import requests
from mutagen.mp3 import MP3
from youtube_dl import YoutubeDL
import asyncio
# from replit import db
import wikipediaapi
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from instagramy import InstagramUser

# Test
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
# --REQUIRED-LIBRARYS-END--

# ----BOT-PREFIX----
prefix = "Alexa "
intents = discord.Intents().all()
client = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)
slash = SlashCommand(client, sync_commands=True)
# --BOT-PREFIX-END--

connected_guilds = []
# ------ON-READY------
@client.event
async def on_ready():
    on_ready.msg = f'------ Ready! Logged in as: {client.user} at {get_time()}, {get_date()} ------'
    print(on_ready.msg)
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Alexa help"))

    connected_guild_names_and_id = []
    server_count = 0
    for server in client.guilds:
        print(f"{get_time()}: connected to {server.name} - {server.id}")
        connected_guilds.append(server.id)
        connected_guild_names_and_id.append("Owner: <@" + str(server.owner_id) + ">, Server (id): " + server.name + " (" + str(server.id) + ")\n")
        server_count += 1

    on_client_ready = discord.Embed(title=f"{client.user} went online at {get_time()}, {get_date()}!", description=f"<@{str(client.user.id)}> is connected to {server_count} servers.", colour=discord.Color.green())
    on_client_ready.add_field(name="Server list:", value=''.join(connected_guild_names_and_id), inline=False)

    ceo = await client.fetch_user("503198701486080030")
    await ceo.send(embed=on_client_ready)
# ----ON-READY-END----


# ------LINUX-------
@client.command()
async def clear(ctx):
    clear = lambda: os.system('clear')
    if str(ctx.author.id) == "503198701486080030":
        clear()
        print(on_ready.msg)
        print(
            f"{get_time()} - {get_date()}: {ctx.author} cleared the console!")
    else:
        print(f"{get_time()}: {ctx.author} tried to clear the console!")

@client.command()
async def cmd(ctx, *, command):
    if str(ctx.author.id) == "503198701486080030":
        os.system(command)
        await ctx.send(f"\"{command}\" was executed.")
    else:
        await ctx.send(f"Dear {ctx.author}, you are NOT allowed to use: \"Alexa cmd {command}\"")
# -----LINUX--END-----


# --------TEST--------
@client.command(aliases=["Nickname", "NICKNAME"])
async def nickname(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    await ctx.send(user.display_name)
'''
@slash.slash(name="img", description="Returns your profile picture url.", guild_ids=connected_guilds)
async def img(ctx: SlashContext):
    embed = discord.Embed(title="your profile picture", url=str(ctx.author.avatar_url))
    await ctx.send(embed=embed)
'''
# ------TEST-END------


# -----Instagram------
@client.command(aliases=["Instagram", "insta", "Insta"])
async def instagram(ctx, *, profile_name):
    if profile_name == "":
        return
    else:
        try:
            user = InstagramUser(profile_name, from_cache=True)
        except:
            session_id = "5680559859%3ADdJpPeGaxyPrMY%3A24"
            user = InstagramUser(profile_name, sessionid=session_id, from_cache=True)
        def verified():
            if user.is_verified:
                name = "@" + profile_name + ":ballot_box_with_check:"
            else:
                name = "@" + profile_name
            return name
        profile_embed = discord.Embed(title=verified(), description=user.biography, url=f"https://instagram.com/{profile_name}/")
        profile_embed.set_thumbnail(url=user.profile_picture_url)
        profile_embed.add_field(name="Posts:", value=user.number_of_posts, inline=True)
        profile_embed.add_field(name="Followers:", value=user.number_of_followers, inline=True)
        profile_embed.add_field(name="Following:", value=user.number_of_followings, inline=True)
        if user.website is not None:
            profile_embed.add_field(name="Link in biography:", value=user.website, inline=False)
        await ctx.send(embed=profile_embed)
# ---Instagram-END----


# ---------ID---------
@slash.slash(name="ausweis",
             description="Creates a german identity card.",
             guild_ids=connected_guilds,
             options=[
                 create_option(
                     name="user",
                     description="Choose a user!",
                     required=True,
                     option_type=6
                 ),
                 create_option(
                     name="first_name",
                     description="First name from person.",
                     required=True,
                     option_type=3
                 ),
                 create_option(
                     name="last_name",
                     description="Last name from person.",
                     required=True,
                     option_type=3
                 )
             ]
             )
async def ausweis(ctx: SlashContext, user, first_name, last_name):
    user = await client.fetch_user(user.id)
    url = str(user.avatar_url)
    url = url.split("?")
    url = url[0] + "?size=512"
    r = requests.get(url, allow_redirects=False)

    open('german_id_user.png', 'wb').write(r.content)

    im1 = Image.open('german_id.png')
    im2 = Image.open('german_id_user.png')
    white_space = Image.open('blank_space_253x70.png')
    letter_white_space = Image.open('blank_space_12x18.png')
    if str(im2.size) != "(253, 253)":
        im2 = im2.resize((253, 253))
        try:
            os.remove('german_id_user.png')
            im2.save('german_id_user.png')
        except:
            pass

    back_im = im1.copy()
    back_im.paste(im2, (27, 86))
    back_im.paste(white_space, (27, 339))

    # last name
    x = 313
    for i in range(12):
        back_im.paste(letter_white_space, (x, 113))
        x += 12

    length_last_name = len(last_name)
    if length_last_name > 12:
        x = 457
        extra_letters = length_last_name - 12
        for i in range(extra_letters):
            back_im.paste(letter_white_space, (x, 113))
            x += 12

    # first name - part 1
    x = 313
    for i in range(7):
        back_im.paste(letter_white_space, (x, 140))
        x += 12

    length_last_name = len(first_name)
    if length_last_name > 7:
        x = 385
        extra_letters = length_last_name - 7
        for i in range(extra_letters):
            back_im.paste(letter_white_space, (x, 140))
            x += 12

    # first name - part 2
    x = 298
    for i in range(6):
        back_im.paste(letter_white_space, (x, 181))
        x += 12

    if length_last_name > 6:
        x = 370
        extra_letters = length_last_name - 6
        for i in range(extra_letters):
            back_im.paste(letter_white_space, (x, 181))
            x += 12

    # date of expiration
    x = 298
    for i in range(11):
        back_im.paste(letter_white_space, (x, 335))
        x += 12

    draw = ImageDraw.Draw(back_im)
    font = ImageFont.truetype("CourierprimecodeRegular-vx0M.ttf", 20)
    draw.text((313, 113), last_name, (0, 0, 0), font=font)  # last name
    draw.text((313, 140), first_name, (0, 0, 0), font=font)  # first name - part 1
    draw.text((298, 181), first_name, (0, 0, 0), font=font)  # first name - part 2
    draw.text((298, 335), get_date_in_ten_years(), (0, 0, 0), font=font)  # date of expiration

    try:
        os.remove("german_user_id.png")
    except:
        pass

    back_im.save('german_user_id.png', quality=100)

    await ctx.send(file=discord.File('german_user_id.png'))
    print(f"{get_time()}: {ctx.author} created a german id for {user}.")
# -------ID-END-------


# --------SIMP--------
@client.command(aliases=["Simp", "SIMP"])
async def simp(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    url = str(user.avatar_url)
    url = url.split("?")
    url = url[0] + "?size=512"
    r = requests.get(url, allow_redirects=False)

    open('simp_user.png', 'wb').write(r.content)

    im1 = Image.open('simp_card.png')
    im2 = Image.open('simp_user.png')
    if str(im2.size) != "(512, 512)":
        im2 = im2.resize((512, 512))
        try:
            os.remove('simp_user.png')
            im2.save('simp_user.png')
        except:
            pass
    mask_im = Image.new("L", im2.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((120, 10, 430, 430), fill=255)
    mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(10))

    back_im = im1.copy()
    back_im.paste(im2, (-20, 375), mask_im_blur)

    try:
        os.remove("simp_card_id.png")
    except:
        pass

    back_im.save('simp_card_id.png', quality=100)
    await ctx.send(file=discord.File('simp_card_id.png'))
    print(f"{get_time()}: {ctx.author} created a simp card for {user}.")
# ------SIMP-END------


# -----SIMP-RATE------
@client.command(aliases=["Simprate", "SIMPRATE"])
async def simprate(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    rate = discord.Embed(title=f"{user.display_name} is {str(random.randint(0, 100))}% a simp :sweat_drops:", colour=discord.Color.orange())
    await ctx.send(embed=rate)
    print(f"{get_time()}: {ctx.author} simp rated {user}.")
# ---SIMP-RATE-END----


# ---------PP---------
@client.command(aliases=["PP"])
async def pp(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    whole_username = user
    size = random.randint(0, 25)
    if size == 0:
        graph = "No penis. Maybe you are a girl :smirk:"
    elif size == 25:
        graph = "8" + "=" * size + "D \nCongratulations! You have a **BBC**. :tada:"
    else:
        graph = "8" + "=" * size + "D"
    rate = discord.Embed(title=f"{user.display_name}'s penis size is {str(size)}cm", description=graph, colour=ctx.author.color)
    await ctx.send(embed=rate)
    print(f"{get_time()}: {ctx.author} requested the penis size from {whole_username}")
# -------PP-END-------


# ------GAY-RATE------
@client.command(aliases=["Gayrate", "GAYRATE"])
async def gayrate(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    rate = discord.Embed(title=f"{user.display_name} is {str(random.randint(0, 100))}% gay :rainbow_flag:", colour=discord.Color.orange())
    await ctx.send(embed=rate)
    print(f"{get_time()}: {ctx.author} gay rated {user}.")
# ----GAY-RATE-END----


# ------YES-NO------
@client.command(aliases=["Yes/no", "yes/no", "y/n", "Y/N", "Yes/No", "yes/No"])
async def yes_no(ctx):
    yes_no = ["Yes", "No"]
    embed = discord.Embed(title=f"{yes_no[random.randint(0, 1)]}")
    await ctx.send(embed=embed)
    print(f"{get_time()}: {ctx.author} requested a yes/no answer.")
# ----YES-NO-END---


# ------JA-NEIN-----
@client.command(aliases=["J/N", "j/n", "Ja/Nein", "ja/nein", "Ja/nein", "ja/Nein", "Jein", "Jaein"])
async def ja_nein(ctx):
    ja_nein = ["Ja", "Nein"]
    embed = discord.Embed(title=f"{ja_nein[random.randint(0, 1)]}")
    await ctx.send(embed=embed)
    print(f"{get_time()}: {ctx.author} hat Ja/Nein angefragt.")
# ----JA-NEIN-END---


# -----9c-CLASS------
@client.command(aliases=["10c", "class_member"])
async def class_random(ctx):
    try:
        if str(ctx.guild.id) == "960125484488851476":
            class_nine_c = [
                "Arya", "Cheayu", "Christos", "Esther", "Gökhan", "Gurman", "Sohan",
                "Leo", "Marina", "Mirela", "Munib", "Nisrin", "Nora", "Patrik",
                "Karthig", "Rohan", "Simon", "Sneha", "Sofia", "Viyal", "Vladimir"
            ]
            number = random.randint(0, 21)
            embed = discord.Embed(title=f"Random 10c Member: {class_nine_c[number]}")
            await ctx.send(embed=embed)
            print(f"{get_time()}: {ctx.author} requested a 10c student.")
        else:
            await ctx.send("This command is only allowed on the 10c server.")
            print(f"{get_time()}: {ctx.author} tried to request a 10c student.")
    except:
        await ctx.send("This command is only allowed on the 10c server.")
        print(f"{get_time()}: {ctx.author} tried to request a 10c student.")
# ---9c-CLASS-END----


# --------MATH--------
@client.command(aliases=["Math", "Calc", "calc", "Calculate", "calculate", "Calculator", "calculator"])
async def math(ctx, *, task):
    try:
        solution = str(eval(task))
        embed = discord.Embed(title=f"{task} = **{solution}**", color=discord.Color.green())
        await ctx.reply(embed=embed, mention_author=False)
        print(f"{get_time()}: {ctx.author} calculated: {task} = {solution}")
    except:
        solution = discord.Embed(title="Syntax ERROR", color=discord.Color.red())
        solution.add_field(name='Please use only this math operations:', value="**+** Addition \n**-** Subtraction \n***** Multiplication \n**/** Division \n**()** Bracket \n**.** Decimal", inline=False)
        await ctx.reply(embed=solution, mention_author=False)
        print(f"{get_time()}: {ctx.author} used wrong math operations")
# ------MATH-END------


# -----WIKIPEDIA-----
@client.command(aliases=["Wikipedia", "Wiki", "wiki"])
async def wikipedia(ctx, *, user_message):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(user_message)
    if page_py.exists():
        embed = discord.Embed(title=f"{user_message} - Wikipedia", url=page_py.fullurl, timestamp=ctx.message.created_at)
        embed.add_field(name='500 words summary:', value=page_py.summary[0:500], inline=False)
        embed.set_footer(text='Wikipedia')
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{user_message} not found!")
# ---WIKIPEDIA-END---


# -----NEWSLETTER-----
@client.command(aliases=["Newsletter", "NEWSLETTER"])
async def newsletter(ctx, *, user_message):
    newsletter = db["newsletter"]
    if user_message == "on":
        if str(ctx.author.id) in db["newsletter"]:
            await ctx.send(f"Newsletter already activated for {ctx.author}!")
        else:
            newsletter.append(str(ctx.author.id))
            await ctx.send(f"Newsletter activated for {ctx.author}!")
    elif user_message == "off":
        if str(ctx.author.id) in db["newsletter"]:
            newsletter.remove(str(ctx.author.id))
            await ctx.send(f"Newsletter deactivated for {ctx.author}!")
        else:
            await ctx.send(f"Newsletter already deactivated for {ctx.author}!")
    else:
        await ctx.send(f"Error occured while activating newsletter!")


@client.command()
async def send_newsletter(ctx, *, user_message):
    if str(ctx.author.id) == "503198701486080030":
        newsletter = discord.Embed(title=f"{client.user} Newsletter", url="https://amazon-alexa-discord-bot.patrikmartic1.repl.co/", colour=discord.Color.blue(), timestamp=ctx.message.created_at)
        newsletter.set_thumbnail(url="https://cdn.discordapp.com/avatars/896060431578329108/69425534ece260e2130c69eb7c6bd786.webp?size=1024")
        newsletter.set_footer(text=f'Alexa newsletter on/off')
        newsletter.add_field(name='New feature(s):', value=user_message, inline=False)
        newsletter_user = db["newsletter"]
        message = 0
        for user in newsletter_user:
            user_id = await client.fetch_user(str(newsletter_user[message]))
            await user_id.send(embed=newsletter)
            message += 1
# ---NEWSLETTER-END---


# --------DM----------
@client.command(aliases=["DM", "Dm", "dM"])
async def dm(ctx, user: discord.Member = None, *, user_message):
    try:
        embed = discord.Embed(title=user_message, colour=discord.Color.blue())
        await user.send(embed=embed)
        embed_success = discord.Embed(title=f"{ctx.author} sent dm to {str(user)} | Message: {user_message}", colour=discord.Color.green())
        ceo = await client.fetch_user("503198701486080030")
        await ceo.send(embed=embed_success)
        # print("Message sent to CEO.")
        print(f"{get_time()}: {ctx.author} sent dm to {str(user)} | Message: {user_message}")
    except:
        embed_error = discord.Embed(
            title=
            f"{ctx.author} tried to sent \"{user_message}\" to {str(user)}.",
            colour=discord.Color.red())
        await ceo.send(embed=embed_error)
        print(f"{get_time()}: {ctx.author} tried to sent \"{user_message}\" to {str(user)}.")


'''
@client.event
async def on_message(ctx):
  commands = ["date", "time", "joke", "witz", "weather", "news", "info", "dm", "server", "tell", "play", "pause", "stop", "resume", "say", "sag"]
  if not ctx.guild and ctx.author != client.user and not commands in ctx.content:
    ceo = await client.fetch_user("503198701486080030")
    await ceo.send(f"{ctx.author} replied with: {ctx.content}")
'''
# -------DM-END--------

# ------SETUP------
'''
@client.command()
async def setup(ctx, *, user_message):
    bot_name = str(client.user)
    bot_name = bot_name.split("#")
    embed = discord.Embed(
        title=f"{bot_name[0]} Dashboard",
        color=discord.Color.blue()
    )
    embed.add_field(name=f"{bot_name[0]}", value=f"{user_message}", inline=False)

    new_embed = discord.Embed(
        title=f"{bot_name[0]} Dashboard",
        color=discord.Color.blue()
    )
    new_embed.add_field(name=f"{bot_name[0]}", value=f"{user_message}", inline=False)
    dashboard = await ctx.send(embed=embed)
    await dashboard.edit(embed=new_embed)
'''


@client.command()
async def create_text_channel(ctx, *, name=None):
    guild = ctx.message.guild
    if name == None:
        await ctx.send('Sorry, but you have to insert a name. Try again, but do it like this: `Alexa create_text_channel [channel name]`')
    else:
        await guild.create_text_channel(name)
        await ctx.send(f"Text channel {name} created.")
        print(f"{get_time()}: Text channel created on {ctx.guild.name} named {name} by {ctx.author}.")


@client.command()
async def create_voice_channel(ctx, *, name=None):
    guild = ctx.message.guild
    if name == None:
        await ctx.send('Sorry, but you have to insert a name. Try again, but do it like this: `Alexa create_voice_channel [channel name]`')
    else:
        await guild.create_voice_channel(name)
        await ctx.send(f"Voice channel {name} created.")
        print(f"{get_time()}: Voice channel created on {ctx.guild.name} named {name} by {ctx.author}.")
# ----SETUP-END----


# ------NEWS------
@client.command(aliases=["News", "NEWS", "gnews", "Gnews", "GNews", "gNews", "GNEWS"])
async def news(ctx, *, user_message):
    response = requests.get(f"https://gnews.io/api/v4/search?q={user_message}&sortby=relevance&token=2fbb31f6574c1d84332d8451cd14d69a")
    n = response.json()
    article = 0
    embeds = []
    try:
        for i in range(10):
            news = n["articles"]
            article_no = news[article]
            article_title = article_no["title"]
            article_content = article_no["content"]
            article_url = article_no["url"]
            article_image = article_no["image"]
            embed = discord.Embed(title=article_title, url=article_url, description=article_content, color=0xFF5733)
            embed.set_thumbnail(url=article_image)
            embeds.append([embed])
            article += 1
    except:
        pass
    pages = article
    cur_page = 1
    selected_embed = embeds[cur_page - 1]
    selected_embed = selected_embed[0]
    message = await ctx.send(embed=selected_embed)
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

    # This makes sure nobody except the command sender can interact with the "menu"

    print(f"{get_time()}: News requested. Topic: {user_message} | by {ctx.author}")
    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=120, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                selected_embed = embeds[cur_page - 1]
                selected_embed = selected_embed[0]
                await message.edit(embed=selected_embed)
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                selected_embed = embeds[cur_page - 1]
                selected_embed = selected_embed[0]
                await message.edit(embed=selected_embed)
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
            # removes reactions if the user tries to go forward on the last page or
            # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            break
        # ending the loop if user doesn't react after x seconds
# ----NEWS-END----


# -----MUSIC-PLAYER-----  '''
@client.command(aliases=['Stop'])
async def stop(ctx):
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.stop()
        print(f"{get_time()}: Stopped playing any audio by {ctx.author}")
    else:
        await ctx.send("Nothing is beeing played.")


@client.command(aliases=['Pause'])
async def pause(ctx):
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.pause()
        print(f"{get_time()}: Paused playing any audio by {ctx.author}")
    else:
        await ctx.send("Nothing is beeing played.")


@client.command(aliases=['Resume'])
async def resume(ctx):
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice_client.is_playing():
        voice_client.resume()
        print(f"{get_time()}: Resumed playing any audio by {ctx.author}")
    else:
        await ctx.send("Nothing is beeing played.")


@client.command(aliases=['Play'])
async def play(ctx, *, url):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
        print(f"{get_time()}: joined {ctx.author.voice.channel}")
    except:
        pass

    YDL_OPTIONS = {
        'format': 'bestaudio',
        'noplaylist': 'True'
    }  # , 'noplaylist': 'True'
    FFMPEG_OPTIONS = {
        'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice_client.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                requests.get(url)
            except:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
            else:
                info = ydl.extract_info(url, download=False)
        URL = info['url']
        audio_source = discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
        sleep(1.0)
        voice_client.play(discord.PCMVolumeTransformer(audio_source, volume=0.08))  # after=None
        print(f"{get_time()}: {ctx.author} started playing: {url}")
        navbar = ['⏯️', '⏹️']
        for navbar in navbar:
            await ctx.message.add_reaction(navbar)
    else:
        await ctx.send("Bot is already playing")
        return


@client.event
async def on_reaction_add(reaction, user):
    if user != client.user:
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=user.guild)
        if str(reaction.emoji) == "⏯️":
            if voice_client.is_playing():
                voice_client.pause()
                await reaction.remove(user)
            else:
                voice_client.resume()
                await reaction.remove(user)
        if str(reaction.emoji) == "⏹️":
            voice_client.stop()
            await reaction.remove(user)
# --MUSIC-PLAYER-END--


# - ------VOICE-------
@client.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        # Exiting if the bot it's not connected to a voice channel
        return

    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()
        print(f"{get_time()}: {voice_state.channel} left due to missing members.")


@client.command(aliases=['Join'])
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    print(f"{get_time()}: joined {ctx.author.voice.channel}")


@client.command(aliases=['Leave', 'Exit', 'exit', 'Remove', 'remove'])
async def leave(ctx):
    await ctx.voice_client.disconnect()
    print(f"{get_time()}: removed from {ctx.author.voice.channel} by {ctx.author}")


@client.command(aliases=['Say'])
async def say(ctx, *, user_message):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
        print(f"{get_time()}: joined {ctx.author.voice.channel}")
    except:
        pass
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)

    print(f"{get_time()}: {ctx.author} said: {user_message}")
    tts = gTTS(user_message)
    tts.save('temp.mp3')
    audio_source = discord.FFmpegPCMAudio('temp.mp3')  # HIER!!!!!!!!!!
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)


@client.command(aliases=['Sag'])
async def sag(ctx, *, user_message):
    try:
        os.system(f"mkdir audios-de")
    except:
        pass
    message_time = get_exact_time()
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
        print(f"{get_time()}: joined {ctx.author.voice.channel}")
    except:
        pass
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)

    print(f"{get_time()}: {ctx.author} hat gesagt: ({message_time}) {user_message}")
    language = 'de'
    tts = gTTS(text=user_message, lang=language, slow=False)
    audio_queue = []
    audio_name = str(ctx.author) + "-" + message_time + ".mp3"
    try:
        tts.save(f"{os.getcwd()}/audios-de/{audio_name}")
        audio_queue.append(audio_name)
        print(audio_queue)
    except:
        pass
    print(audio_queue)
    while len(os.listdir(f"{os.getcwd()}/audios-de/")) != 0:
        if len(os.listdir(f"{os.getcwd()}/audios-de/")) == 0:
            break
        current_audio = audio_queue[0]
        audio_source = discord.FFmpegPCMAudio(f"{os.getcwd()}/audios-de/{current_audio}")
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            delay = int(MP3(f"{os.getcwd()}/audios-de/{current_audio}").info.length)
            sleep(delay)
            if os.path.isfile(f"{os.getcwd()}/audios-de/{current_audio}"):
                os.remove(f"{os.getcwd()}/audios-de/{current_audio}")
                del audio_queue[0]


@client.command(aliases=['Tell', 'TELL'])
async def tell(ctx, *, user_message):
    message = str(user_message)
    message = message.lower()

    try:
        channel = ctx.author.voice.channel
        await channel.connect()
        print(f"{get_time()}: joined {ctx.author.voice.channel}")
    except:
        pass
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if "weather" in message:
        city = user_message.split(" ")
        del city[0]
        city = ' '.join(str(e) for e in city)
        if len(city) != 0:
            weather_mp3 = tell_weather(city)
            if os.path.exists("weather.mp3"):
                os.remove("weather.mp3")
            tts = gTTS(weather_mp3)
            tts.save('weather.mp3')
            audio_source = discord.FFmpegPCMAudio('weather.mp3')
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=None)
                delay = int(MP3(f"{os.getcwd()}/weather.mp3").info.length)
                sleep(delay)
                if os.path.isfile(f"{os.getcwd()}/weather.mp3"):
                    os.remove(f"{os.getcwd()}/weather.mp3")
        else:
            await ctx.send("I think you forgot to enter the city.")

    if "joke" in message:
        await ctx.send("Alexa is searching for a joke ... :mag:")
        if os.path.exists("joke.mp3"):
            os.remove("joke.mp3")
        r = requests.get('https://v2.jokeapi.dev/joke/Any?type=single').json()
        joke = r['joke']
        tts = gTTS("Here a joke. " + joke)
        tts.save('joke.mp3')
        audio_source = discord.FFmpegPCMAudio('joke.mp3')
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            delay = int(MP3(f"{os.getcwd()}/joke.mp3").info.length)
            sleep(delay)
            if os.path.isfile(f"{os.getcwd()}/joke.mp3"):
                os.remove(f"{os.getcwd()}/joke.mp3")
    if "witz" in message:
        await ctx.send("Alexa sucht nach einem Witz ... :mag:")
        if os.path.exists("joke-de.mp3"):
            os.remove("joke-de.mp3")
        language = 'de'
        r = requests.get('https://v2.jokeapi.dev/joke/Any?lang=de&type=single').json()
        witz = r['joke']
        tts = gTTS(text="Hier ist ein Witz. " + witz,
                   lang=language,
                   slow=False)
        tts.save('joke-de.mp3')
        audio_source = discord.FFmpegPCMAudio('joke-de.mp3')
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            delay = int(MP3(f"{os.getcwd()}/joke-de.mp3").info.length)
            sleep(delay)
            if os.path.isfile(f"{os.getcwd()}/joke-de.mp3"):
                os.remove(f"{os.getcwd()}/joke-de.mp3")

    if "time" in message:
        if os.path.exists("time.mp3"):
            os.remove("time.mp3")
        tts = gTTS("The current time is " + get_time())
        tts.save('time.mp3')
        audio_source = discord.FFmpegPCMAudio('time.mp3')
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            delay = int(MP3(f"{os.getcwd()}/time.mp3").info.length)
            sleep(delay)
            if os.path.isfile(f"{os.getcwd()}/time.mp3"):
                os.remove(f"{os.getcwd()}/time.mp3")

    if "date" in message:
        # if os.path.exists("date.mp3"):
        try:
            os.remove("date.mp3")
        except:
            pass
        tts = gTTS("Today is the " + get_date())
        tts.save('date.mp3')
        audio_source = discord.FFmpegPCMAudio('date.mp3')
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            delay = int(MP3(f"{os.getcwd()}/date.mp3").info.length)
            sleep(delay)
            if os.path.isfile(f"{os.getcwd()}/date.mp3"):
                os.remove(f"{os.getcwd()}/date.mp3")
# ------VOICE-END-----


# --------TIME--------
@client.command(aliases=['Time'])
async def time(ctx):
    current_time = get_time()
    await ctx.send(current_time)
    print(f"{get_time()}: Time sent " + current_time)
# ------TIME-END------


# --------DATE--------
@client.command(aliases=['Date'])
async def date(ctx):
    current_date = get_date()
    await ctx.send(current_date)
    print(f"{get_time()}: Date sent " + current_date)
# ------DATE-END------


# --------JOKE--------
@client.command(aliases=['Joke'])
async def joke(ctx):
    await ctx.send("Alexa is searching for a joke ... :mag:")
    r = requests.get('https://v2.jokeapi.dev/joke/Any?type=single').json()
    joke = r['joke']
    await ctx.send(joke)
    print(f"{get_time()}: Joke sent - " + joke)


@client.command(aliases=['Witz'])
async def witz(ctx):
    await ctx.send("Alexa sucht nach einem Witz ... :mag:")
    r = requests.get('https://v2.jokeapi.dev/joke/Any?lang=de&type=single').json()
    joke = r['joke']
    await ctx.send(joke)
    print(f"{get_time()}: Witz sent - " + joke)
# ------JOKE-END------


# ------Weather-------
@client.command(aliases=['Weather'])
async def weather(ctx, *, location):
    try:
        weather, city, country = get_weather(ctx, location)
        await ctx.send(embed=weather)
        print(f"{get_time()}: Weather requested for {city}, {country}")
    except:
        weather, status = get_weather(ctx, location)
        await ctx.send(embed=weather)
        print(f"{get_time()}: Weather errorcode: {status}")

@slash.slash(name="weather",
             description="Request current weather for a location.",
             guild_ids=connected_guilds,
             options=[
                 create_option(
                     name="city",
                     description="Choose a city!",
                     required=True,
                     option_type=3
                 )
             ]
             )
async def slash_weather(ctx: SlashContext, city):
    try:
        weather, location, country = get_weather(ctx, city)
        await ctx.send(embed=weather)
        print(f"{get_time()}: Weather requested for {location}, {country}")
    except:
        weather, status = get_weather(ctx, city)
        await ctx.send(embed=weather)
        print(f"{get_time()}: Weather errorcode: {status}")
# ----Weather--END-----


# --------ECHO--------
@client.command(aliases=['Echo', 'ECHO'])
async def echo(ctx, *, user_message):
    await ctx.send(f'{ctx.author}: {user_message}')
    print(f"{get_time()}: Message returned: {ctx.author}: {user_message}")
# ------ECHO-END------


# -------WHO-IS-------
@client.command(aliases=["Info", "Whois", "whois"])
async def info(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    rlist = []
    for role in user.roles:
        if role.name != "@everyone":
            rlist.append(role.mention)

    b = ", ".join(rlist)

    embed = discord.Embed(colour=user.color)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    # embed.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)

    embed.add_field(name='Profile (ID):', value=f"<@{user.id}> \n({user.id})", inline=False)

    account_created = str(user.created_at)
    account_created = account_created.split(".")
    del account_created[1]
    account_created = ''.join(str(e) for e in account_created)
    embed.add_field(name='Account created at:', value=account_created, inline=False)
    try:
        joined_server = str(user.joined_at)
        joined_server = joined_server.split(".")
        del joined_server[1]
        joined_server = ''.join(str(e) for e in joined_server)
    except:
        joined_server = "/"
    try:
        embed.add_field(name=f'Joined {ctx.guild.name} at:', value=joined_server, inline=False)
    except:
        pass
    if user.bot == True:
        user_bot = "Yes"
    elif user.bot == False:
        user_bot = "No"
    else:
        user_bot = "Unknown"
    embed.add_field(name=f'Is {user} a Bot?', value=f"- {user_bot}", inline=False)

    if len(rlist) == 1:
        embed.add_field(name=f'{len(rlist)} Role:', value=''.join([b]), inline=False)
    else:
        embed.add_field(name=f'{len(rlist)} Roles:', value=''.join([b]), inline=False)

    embed.add_field(name='Top Role:', value=user.top_role.mention, inline=False)

    await ctx.send(embed=embed)
    print(f"{get_time()}: User info requested for {user}(<@{user.id}>) by {ctx.author}(<@{ctx.author.id}>)")
# -----WHO-IS-END-----


# --------HELP--------
@client.command(aliases=['Commands', 'commands', 'Commandlist', 'commandlist', 'Helplist', 'helplist', 'Help', '?'])
async def help(ctx):
    embed = discord.Embed(title=f"Command list for {client.user}", colour=discord.Color.blue(), timestamp=ctx.message.created_at)

    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/896060431578329108/69425534ece260e2130c69eb7c6bd786.webp?size=1024")
    embed.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)

    # embed.add_field(name=f'Prefix: {prefix} ...', value='\u200b', inline=False)

    embed.add_field(name='Text channel:', value=f"╔ {prefix} date \n╠ {prefix} dm [@user] [message] \n╠ {prefix} gayrate [@user] \n╠ /ausweis[@user][fname][lname] \n╠ {prefix} info [@user] \n╠ {prefix} insta [acc] \n╠ {prefix} joke \n╠ {prefix} math [task] \n╠ {prefix} news [topic] \n╠ {prefix} pp [@user] \n╠ {prefix} server \n╠ {prefix} simp [@user] \n╠ {prefix} simprate [@user] \n╠ {prefix} time \n╠ {prefix} weather [city] \n╠ {prefix} witz \n╠ {prefix} wikipedia [topic] \n╚ {prefix} y/n", inline=True)

    embed.add_field(name='Voice channel:', value=f"╔ {prefix} play [YT URL/name] \n╠ {prefix} tell date \n╠ {prefix} tell joke \n╠ {prefix} say [message] \n╠ {prefix} sag [Nachricht] \n╠ {prefix} tell time \n╠ {prefix} tell weather [city] \n╚ {prefix} tell witz", inline=True)

    try:
        if str(ctx.guild.id) == "960125484488851476":
            embed.add_field(name=f'Special features on {ctx.guild.name}:', value=f"╔ {prefix} 10c - Zufälliger Schüler der 10c \n╚ {prefix} j/n - Zufällige Antwort mit Ja oder Nein", inline=False)
    except:
        pass

    embed.add_field(name='Information:', value="╔ Used language: Python 3.9.7 \n╠ Developed by: <@503198701486080030>\n╠ Bot shutdown: November 28th, 2022 \n╚ Hosted with: https://www.heroku.com/home", inline=False)

    await ctx.send(embed=embed)
    print(f"{get_time()}: {ctx.author} requested help.")
# ------HELP-END------


# -------SERVER-------
@client.command(aliases=['Server'])
async def server(ctx):
    owner = str(ctx.guild.owner_id)
    # region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    # desc=ctx.guild.description

    embed = discord.Embed(title=ctx.guild.name + " Server Information", color=discord.Color.blue())  # description=desc
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=f"<@{owner}>", inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    # embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)
    print(f"{get_time()}: Server information requested for {ctx.guild.name} - {ctx.guild.id} by {ctx.author}")


'''
    members=[]
    async for member in ctx.guild.fetch_members(limit=150) :
      await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name,str(member.status),str(member.joined_at)))
'''
# -----SERVER-END-----

# ----REQUIRED-STUFF----
# keep_alive() # required if hosted on https://repl.it/ via ping by https://uptimerobot.com/
# try:
client.run("ODk2MDYwNDMxNTc4MzI5MTA4.YWBnTg.rQAMcupKCYrRrQJ3xlZMyfoLn8c")
# except:
    # client.run("OTU5MDg1NDQ2Mjg0MDYyNzQw.YkWv7Q.CNnPw_37GLWfuVqTLkRAArzvStk")
# --REQUIRED-STUFF-END--