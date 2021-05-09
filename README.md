# bot-chan

Returns information about anime obtained via MyAnimeList.com

## Instructions

[Create a Discord bot](https://discordpy.readthedocs.io/en/latest/discord.html) and add to a server with the "Send Messages" and "Embed Links" permissions.

Copy `.env.example` to a new file `.env` and fill with your Discord bot token.

Pull the image and run:

```
docker pull ryilliams/bot-chan
docker run -d --env-file ./.env bot-chan
```

Or to build locally:

```
docker-compose up
```

## Usage

```
​Commands:
  help     Shows this message
  schedule Returns the anime schedule for a given day (defaults to today)
  search   Returns the top three anime that match the given search parameter
  top      Returns the top 5 anime of all time according to MyAnimeList

Type ~help command for more info on a command.
You can also type ~help category for more info on a category.
```

All commands are prefixed with `~`.