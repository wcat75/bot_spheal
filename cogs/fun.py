import random
import json
import discord
from discord.ext import commands
from discord import app_commands, Embed, Interaction
import os

class Choice(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None    

    @discord.ui.button(label="正面", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: Interaction
    ) -> None:
        self.value = "正面"
        self.stop()

    @discord.ui.button(label="反面", style=discord.ButtonStyle.blurple)
    async def cancel(
        self, button: discord.ui.Button, interaction: Interaction   
    ) -> None:
        self.value = "反面"
        self.stop()

class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot
        current_dir = os.path.dirname(__file__)  # Gets the directory where the current file is located
        json_path = os.path.join(current_dir, 'facts.json')  # Constructs the path to the JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            self.facts = json.load(f)          

    @app_commands.command(name="冷豹", description="豹～(告訴你一個冷知識🥶)")
    async def randomfact(self, interaction: Interaction) -> None:
        fact = random.choice(self.facts)['fact']
        embed = Embed(description=fact, color=0xD75BF4)
        embed.set_footer(text=f"今天水溫夠冷嗎🧐 by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="猜豹", description="海豹～（今天運氣如何？🎊）")
    async def coinflip(self, interaction: Interaction) -> None:
        buttons = Choice()
        embed = Embed(description="（猜猜是正面或反面）？", color=0xBEBEFE)
        await interaction.response.send_message(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["正面", "反面"])
        if buttons.value == result:
            embed = Embed(
                description=f"（恭喜🎉 你猜 `{buttons.value}`，結果是 `{result}`）",
                color=0xBEBEFE,
            )
            embed.set_footer(text=f"「今天運氣不錯😎」by {interaction.user.display_name}")
        else:
            embed = Embed(
                description=f"（蛙🐸 你猜 `{buttons.value}`，結果是 `{result}`...再試一次？）",
                color=0xE02B2B,
            )
            embed.set_footer(text=f"「今天運氣不太好😥」by {interaction.user.display_name}")

        await interaction.edit_original_response(embed=embed, view=None, content=None)


async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))
