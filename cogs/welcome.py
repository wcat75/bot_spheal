import discord
from discord.ext import commands

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = 1138373306614026353  # Replace with the ID of the channel where welcome messages should go

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Sends a welcome message in a designated welcome channel, directing new members to the rules channel."""
        welcome_channel_id = 1138373306614026353  # Replace with the ID of your welcome channel
        rules_channel_id = 1138373306165248144  # Replace with the ID of your "#須知" channel

        welcome_channel = self.bot.get_channel(welcome_channel_id)
        rules_channel = self.bot.get_channel(rules_channel_id)

        if welcome_channel and rules_channel:
            embed = discord.Embed(
                description=f"歡迎{member.mention}🥳\n記得詳閱{rules_channel.mention}哦海豹～",
                color=0x000000 # You can choose any color
            )
            embed.set_footer(text="(已使用翻譯年糕)")
            print(f"{member.display_name} has joined the server!")
            await welcome_channel.send(embed=embed)
        else:
            print("Channel not found.")


async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
