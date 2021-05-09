import os
import discord
from discord.ext import commands
import aiohttp
from datetime import date
from dateutil.parser import isoparse
import calendar
from typing import Optional

api_base = "https://api.jikan.moe/v3/"

def get_current_day():
    weekday = date.today().weekday()
    day_str = calendar.day_name[weekday]
    return day_str.lower()

def timestamp_to_formatted_time(timestamp):
    date = isoparse(timestamp)
    return date.strftime('%-I:%M %p')

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(
    command_prefix='~',
    help_command = help_command,
    description = "Returns information about anime obtained via MyAnimeList.com"
)

@bot.command()
async def search(ctx, *, query: str):
    """Returns the top three anime that match the given search parameter"""

    async with aiohttp.ClientSession() as session:
        url = api_base+"search/anime?q="+query
        async with session.get(url) as resp:
            content = await resp.json()

            await ctx.send('Here\'s the top 3 results:')

            for result in content['results'][:3]:
                embed = discord.Embed(
                    title=result['title'],
                    description=result['synopsis'],
                    url=result['url']
                )
                embed.set_thumbnail(url=result['image_url'])

                await ctx.send(embed=embed)

@bot.command()
async def top(ctx):
    """Returns the top 5 anime of all time according to MyAnimeList"""

    async with aiohttp.ClientSession() as session:
        url = api_base+"top/anime"
        async with session.get(url) as resp:
            content = await resp.json()

            await ctx.send('Here\'s the top 5 anime of all time:')

            for result in content['top'][:5]:
                embed = discord.Embed(
                    title=result['title'],
                    description=f"Rank: {result['rank']}\nScore: {result['score']}",
                    url=result['url']
                )
                embed.set_thumbnail(url=result['image_url'])

                await ctx.send(embed=embed)

@bot.command()
async def schedule(ctx, day: Optional[str] = get_current_day()):
    """Returns the anime schedule for a given day (defaults to today)"""

    async with aiohttp.ClientSession() as session:
        url = api_base + "schedule/" + day
        async with session.get(url) as resp:
            content = await resp.json()

            message = f'Here\'s {day}\'s schedule:\n'

            for result in content[day]:
                time = timestamp_to_formatted_time(result['airing_start'])
                message += f"\n{result['title']} ({time})"

            await ctx.send(message)


bot.run(os.getenv('DISCORD_TOKEN'))