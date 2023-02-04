from discord.ext import commands
from json import load

json_cfg = {}
with open('configuration/bot.json', 'r') as f:
    json_cfg = load(f)


class TFFZ():
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.guild = self.bot.get_guild(json_cfg['tffz_guild'])
        self.role = self.guild.get_role(json_cfg['lucky ones']['role'])
        self.exhibitors = self.guild.get_role(json_cfg['exhibitors'])
        self.channel = self.guild.get_channel(
            json_cfg['lucky ones']['channel'])
