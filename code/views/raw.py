import discord
from discord.ext import commands
from deserialize import TFFZ


class RerollView(discord.ui.View):
    def __init__(self, guy: discord.Member, bot: commands.Bot):
        self.guy = guy
        self.bot = bot
        super().__init__()

    @discord.ui.button(label="add", style=discord.ButtonStyle.success, emoji="🍀")
    async def apply_reroll_guy(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.guy.add_roles(TFFZ(self.bot).role)
        button.disabled = True
        await interaction.response.defer()


class RawView(discord.ui.View):
    def __init__(self, data, bot: commands.Bot):
        self.data = data
        self.bot = bot
        super().__init__()

        self.guild = TFFZ(self.bot).guild
        self.role = TFFZ(self.bot).role
        self.channel = TFFZ(self.bot).channel

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return TFFZ(self.bot).exhibitors in interaction.user.roles
        # return await super().interaction_check(interaction)

    @discord.ui.button(label="add", style=discord.ButtonStyle.success, emoji="🍀")
    async def apply_lucky_ones(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.data:
            # print(self.role.name, [m.name for m in self.role.members])
            # await interaction.response.send_message("\n".join(str(member) for member in self.role.members))
            for id in self.data['lucky_ones']:
                member: discord.Member = await self.guild.fetch_member(id)
                print('adding', member)
                await member.add_roles(self.role)

        await interaction.response.defer()
        # button.disabled = True
        # self.stop()

    @discord.ui.button(label="rm", style=discord.ButtonStyle.danger, emoji="✂")
    async def remove_lucky_ones(self, interaction: discord.Interaction, button: discord.ui.Button):
        for member in self.role.members:
            print('removing', str(member))
            await member.remove_roles(self.role)
        await interaction.response.defer()
        # await ctx.send("\n".join(str(member) for member in role.members))

    @discord.ui.button(label="@", style=discord.ButtonStyle.blurple, emoji="🔔")
    async def at_lucky_ones(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.channel.send(self.role.mention)
        # for member in self.role.members:
        #     await self.channel.send(member.mention)
        await interaction.response.defer()
