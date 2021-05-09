import os
import discord
from discord.ext import commands
import aiohttp
from datetime import date
from dateutil.parser import isoparse
import calendar

bot = commands.Bot(command_prefix='~')

api_base = "https://api.jikan.moe/v3/"

def get_current_day():
    weekday = date.today().weekday()
    day_str = calendar.day_name[weekday]
    return day_str.lower()

def timestamp_to_formatted_time(timestamp):
    date = isoparse(timestamp)
    return date.strftime('%-I:%M %p')

@bot.command()
async def search(ctx, *, query: str):
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
async def schedule(ctx):
    async with aiohttp.ClientSession() as session:
        day = get_current_day()

        url = api_base + "schedule/" + day
        async with session.get(url) as resp:
            content = await resp.json()

            message = 'Here\'s today\'s schedule:\n'

            for result in content[day]:
                time = timestamp_to_formatted_time(result['airing_start'])
                message += f"\n{result['title']} ({time})"

            await ctx.send(message)


bot.run(os.getenv('DISCORD_TOKEN'))