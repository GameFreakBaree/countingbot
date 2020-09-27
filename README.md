# CountingBot
CountingBot is a Discord Bot just for one purpose. To make a minigame that players can count in. The purpose is to make a very customizable bot without a advanced configuration. We also made the bot 100% free for everyone to use. Once we reach 500 guilds we will make a premium bot.

## Suggestions, bugs, feature requests
Want to contribute? Great, we love that! Please take your time on [opening a new issue](https://github.com/GameFreakBaree/countingbot/issues).

## Commands
### Commands for Everyone
* **c!ping** - Get the ping in milliseconds of the bot.
* **c!info** - Get all the information about the bot.
* **c!invite** - Get an invite to add the bot.
* **c!leaderboard** - Get a leaderboard with members that counted the most.
* **c!userinfo** - See how many times you counted in the server.
* **c!help** - A help command with all commands displayed.
* **c!currentcount** - Tells you on which number the count is.

### Commands for users' with MANAGE_SERVER permission
* **c!autosetup** - Run this command and it will setup a channel automatically. You can change the name and position of the channel without problems.
* **c!setup** - Run this command in the channel you want to count in.
* **c!unlink** - Run this command in the channel you want stop counting in.
* **c!config** - Here you can configurate the bot however you like.
* **c!toggle** - Pause/Unpause the channel from counting in it.
* **c!settopic** - Set the topic of the channel.
* **c!resetscore {user}** - Reset a user's score.
* **c!mute {user}** - Mute a user from counting in the channel.
* **c!unmute {user}** - Unmute a user from counting in the channel.

### Commands for the Owner of the guild
* **c!resetall** - Remove all data from the bot in the guild.

## Config (c!config)
* **c!config** - See all possible commands in config.
* **c!config maxcount {number}** - Change the maximum count. Min 50, Max 2147483647 [Default: 2147483647]
* **c!config resetonfail {enabled/disabled}** - Reset count if someone types the wrong number. [Default: disabled]
* **c!config emotereact {enabled/disabled}** - React on every count message. [Default: enabled]
* **c!config resetscore {user}** - Reset a user's score.

## License
This project is licensed under the GNU GPLv3-license. I love to see that other developers learn from my code. You can use it but cannot claim it as yours.
> You may copy, distribute and modify the software as long as you track changes/dates in source files. Any modifications to or software including (via compiler) GPL-licensed code must also be made available under the GPL along with build & install instructions.  

Fetched from [TLDRLegal](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)), please also read the [license](https://github.com/GameFreakBaree/countingbot/blob/master/LICENSE) if you plan on using the source code. This is only a short summary. Please also take note of that we are not forced to help you, and we won't help you host it yourself as we do not recommend you doing so.
