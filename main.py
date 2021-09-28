import discord
import os
from gamemanager import GameManager
import random as r
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="!", help_command=None)

GAME_IN_PLAY = False


GM = GameManager()

@bot.command()
async def help(ctx, *args):
    args = [arg.lower() for arg in args]
    # context refers to the channel the message will be sent in i think
    if len(args) == 0:
        await ctx.send("```pls stop ur hurting me```")
    if "mao" in args:
        await ctx.send("`It's against the rules to tell you the rules`")
    if "game" in args:
        # put help info for all commands used for playing the game
        pass


# remember to change to redacted when we play

@bot.command()
async def dealme(ctx, *args):
    global GAME_IN_PLAY
    GAME_IN_PLAY = True
    await GM.deal(bot, ctx, args)


@bot.command()
async def play(ctx, *args):
    global GAME_IN_PLAY
    if GAME_IN_PLAY:
        await GM.play(ctx, args)
    else:
        ctx.send("Game hasn't started yet")


@bot.command()
async def draw(ctx):
    global GAME_IN_PLAY
    if GAME_IN_PLAY:
        await GM.draw(ctx)
    else:
        ctx.send("Game hasn't started yet")

@bot.command()
async def showhand(ctx):
    global GAME_IN_PLAY
    if GAME_IN_PLAY:
        await GM.showhand(ctx)
    else:
        ctx.send("Game hasn't started yet")


@bot.event
async def on_message(message):
    global GAME_IN_PLAY
    if message.author == bot.user:
        return
    if GAME_IN_PLAY and message.content[0] != "!":
        await message.channel.send("No Talking during Mao!")
    await bot.process_commands(message)


bot.run(TOKEN)
