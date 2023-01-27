from keep_alive import keep_alive
import discord
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, check
import os
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
from discord_slash.utils.manage_commands import create_option, create_choice
from itertools import cycle
# ^^ All of our necessary imports
import wikipediaapi

#Define our bot
client = discord.Client()

client = commands.Bot(
    command_prefix="!"
)  #put your own prefix here, but it wont matter since slash commands default to /
slash = SlashCommand(client, sync_commands=True)

status = cycle(['Super', 'Idol'])


@client.event
async def on_ready():
    change_status.start()
    print("Your bot is ready")


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


#Send message "pong" when user sends /ping
@slash.slash(name="ping", description="Ping Pong")
async def _help(ctx: SlashContext):
    await ctx.send(content="pong!")


# Space given text by user
@slash.slash(
    name="space",
    description="Space your text",
    options=[
        create_option(  #create an arg
            name="text",  #Name the arg as "text"
            description="The text to space",  #Describe arg
            option_type=3,  #option_type 3 is string
            required=True  #Make arg required
        )
    ])
async def _space(ctx: SlashContext, sentence):
    newword = ""  #define new sentence
    for char in sentence:  #For each character in given sentence
        newword = newword + char + "   "  #Add to new sentence  with space
    await ctx.send(content=newword)  #send mew sentence


# Get Wiki page summary
@slash.slash(
    name="getWiki",
    description="Get Wiki Page Summary",
    options=[
        create_option(  #create an arg
            name="page_name",  #Name the arg as "text"
            description="Name of Wiki page",  #Describe arg
            option_type=3,  #option_type 3 is string
            required=True,  #Make arg required
        ),
        create_option(
            name="displayOption",  #Name the arg as "text"
            description="Display page summary or whole page",  #Describe arg
            option_type=3,  #option_type 3 is string
            required=True,  #Make arg required
            choices=[
                create_choice(  #create an arg
                    name="Summary",  #Name the arg as "text"
                    value="Summary"),
                create_choice(  #create an arg
                    name="Page",  #Name the arg as "text"
                    value="Page"),
            ])
    ])
async def _getWiki(ctx: SlashContext, page_name, option):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(page_name)
    if (option == "Summary"):
        await ctx.send(content=page_py.summary)
    elif (option == "Page"):
        await ctx.send(content=page_py.text)
    #send mew sentence


# exports chat of channel in txt file
@client.command()
async def test(ctx):
    filename = f"{ctx.channel.name}.txt"
    with open(filename, "w") as file:
        async for msg in ctx.channel.history(limit=None):
            file.write(
                f"{msg.created_at} - {msg.author.display_name}: {msg.clean_content}\n"
            )


#Run our webserver, this is what we will ping
keep_alive()

#Run our bot
client.run(os.getenv("TOKEN"))
