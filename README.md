# Radia Production
IPL Production Stack

Radia Production is a stack of applications made by
[IPL Production](https://iplabs.work) for the of production related tasks.

## Features
- Auto Detection of commentators in Discord Voice Chat
- Ability to set commentator profiles (Name, Twitter handle, Pronouns)
- Set tournament information and bracket link
- Twitch bot for view to run command to see commentators' information
- REST API for requesting information for use on overlays and other services
- Custom Twitch Command support, for custom commands

## stack
This mono-repository containing multiple components that make up the production
system.

- **`discordBot`**: A Discord Bot used for querying information from Discord
- **`twitchBot`**: A Twitch bot that connects and handles Twitch IRC commands
- **`RestAPI`**: A REST API for querying information.

## Requirements

- MongoDB Database
- Twitch Bot Account
- Discord bot profile

## Setup
Each application in the stack requires its own .env file located in the **Root**
directory, they are as follows.

It's recommended that you have separate username and password URI for MongoDB

It's recommended you use docker-compose to deploy your stack as it handles the
other requirements such as Redis for DB caching for you.

### **Sentry Disclosure**

If you enable `SENTRY` in the `.env` file, if your instance has an error, IPL's
Production team will receive a copy of the error via Sentry for
debugging purposes.

### `discord.env` for Discord bot
```
DISCORDTOKEN=Discord.bot.token
MONGODBURI=Mongo.DB.Connection.URI
SENTRY = "System Environment"  # Optional
DEBUG = 1  # Optional
REDISURL = "REDIURI" # Used in testing only for sepecify where the redisDB is 
```

### `twitch.env` for Twitch Bot
```
TWITCHCLIENTID=Twitch.application.client.id
TWITCHOAUTH=Twitch.oath.token
TWITCHNICK=Twitch.bot.username
TWITCHCHANNELS=Channel.to.connect.to.seperated.by.comma (e.g vlee111,iplsplatoon)
MONGODBURI=Mongo.DB.Connection.URI
SENTRY = "System Environment"  # Optional
DEBUG = 1  # Optional
REDISURL = "REDIURI" # Used in testing only for sepecify where the redisDB is hosted  
```

### `restapi.env` for REST API
```
MONGODBURI=Mongo.DB.Connection.URI
SENTRY = "System Environment"  # Optional
DEBUG = 1  # Optional
REDISURL = "REDIURI" # Used in testing only for sepecify where the redisDB is 
```

### `docker-compose.yml` edits
For [traefik](https://traefik.io/traefik/) to setup Lets' Encrypt SSL
certificate correctly you need to edit the docker compose file.

1. Replace `api.website.com` in `traefik.http.routers.whoami.rule=Host`
attached to the `rest-api`'s labels with the link you want to use to your REST API.

2. Replace `security@website.com` in `--certificatesresolvers.myresolver.acme.email=`
attached to `traefik` commands with the email you want to give to let's encrypt,
for security notifications'.

After setting up these `.env` files up and edited the `docker-compose.yml` file,
you can run `docker-compose up` to start the stack

When started, the REST API Docs will be available at `https://your-website.com/docs`

## Credits

Written by [Vincent Lee](https://github.com/vlee489) & [LeptoFlare](https://github.com/LeptoFlare)

This bot was inspried by the [EGtv-Bot](https://github.com/NintenZone/EGtv-Bot)
by NintenZone
