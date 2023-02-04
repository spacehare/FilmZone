import discord
from discord.ext import commands
from typing import List, Optional
import json
import logging
from deserialize import json_cfg


class Zone(commands.Bot):
    extensions: List[str] = []

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        # intents = discord.Intents.all()
        super().__init__(
            command_prefix=json_cfg['prefix'],
            case_insensitive=True,
            intents=intents)
        self.extensions = [
            'cogs.filmzone',
            'cogs.owner'
        ]

    async def setup_hook(self) -> None:
        if __name__ == '__main__':
            for ext in self.extensions:
                await bot.load_extension(ext)
                print('loaded', ext)

    async def on_ready(self) -> None:
        # await discord.app_commands.CommandTree.sync(self=self)
        print('COMMANDS:', [c.name for c in self.commands])
        # cog = bot.get_cog('Greetings')
        # if cog:
        #     cmds = cog.get_commands()
        #     print([c.name for c in cmds])
        print(f'{self.user} ready')

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user\
                or not message.content.startswith(str(self.command_prefix)):
            # or message.author.bot\ # this is handle in the library's code already, i think
            return

        await message.add_reaction('<:sacabambaspis:970880902123126874>')
        # await self.process_commands(message)
        return await super().on_message(message)

    async def process_commands(self, message, /):
        # await message.add_reaction('<:sipsabmabacas:1001211851947905034>')
        return await super().process_commands(message)

    async def on_command_error(self, ctx: commands.Context, exception, /):
        if not ctx.interaction:
            await ctx.message.add_reaction('<:shockabambaspis:1001211310199025695>')
        return await super().on_command_error(ctx, exception)

        # <:shockabambaspis:1001211310199025695>

        # if message.content.startswith('help'):
        # await message.channel.send(self.command_prefix)
        #     await message.reply('Hello!', mention_author=True)


bot = Zone()
bot.run(json_cfg['token'])
