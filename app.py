import os
import discord
from discord.ext import commands
import aiohttp

bot = commands.Bot(command_prefix='~')

api_base = "https://api.jikan.moe/v3/"

@bot.command()
async def search(ctx, *, query: str):
    async with aiohttp.ClientSession() as session:
        url = api_base+"search/anime?q="+query
        async with session.get(url) as resp:
            content = await resp.json()

            first_result = content['results'][0]

            embed = discord.Embed(
                title=first_result['title'],
                description=first_result['synopsis'],
                url=first_result['url']
            )
            embed.set_thumbnail(url=first_result['image_url'])

            await ctx.send(embed=embed)

bot.run(os.getenv('DISCORD_TOKEN'))