import discord
import random
from discord.ext import commands
from discord import app_commands, Embed, Interaction, Member

class RockPaperScissors(discord.ui.Select):
    def __init__(self, participants):
        self.participants = participants
        options = [
            discord.SelectOption(label="小火龍", description="火龍～！", emoji="<:charmander:1234085837214584852>"),
            discord.SelectOption(label="傑尼龜", description="傑尼傑尼", emoji="<:squirtle:1234085840590864465>"),
            discord.SelectOption(label="妙蛙種子", description="種子種子", emoji="<:bulbasaur:1234085832340668438>"),
        ]
        super().__init__(placeholder="請選擇......", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if interaction.user not in self.participants:
            await interaction.response.send_message("（你不是參賽者👾\n使用「/戰豹」來發起挑戰！）", ephemeral=True)
            return
        if interaction.user in self.view.responses:
            # User has already made a selection, send an ephemeral message
            await interaction.response.send_message("（你已經做出選擇～請等待其他參賽者）", ephemeral=True)
            return
        
        self.view.responses[interaction.user] = self.values[0]
        await interaction.response.edit_message(view=self.view)
        await self.view.update_followup()
        await self.view.check_completion()

class RockPaperScissorsView(discord.ui.View):
    def __init__(self, participants):
        super().__init__(timeout=60)
        self.participants = participants
        self.responses = {}
        self.followup_message = None
        self.message = None
        self.add_item(RockPaperScissors(participants))

    async def bot_responses(self, interaction):
        embed = discord.Embed(description="（正在佈置場地...）", color=0x00ffcc)
        for participant in self.participants:
            if participant.bot:
                self.responses[participant] = random.choice(["小火龍", "傑尼龜", "妙蛙種子"])
        self.followup_message = await interaction.followup.send(embed=embed)
        await self.update_followup()

    async def on_timeout(self):
        for participant in self.participants:
            if participant not in self.responses:
                self.responses[participant] = "未回應"

        embed = Embed(title="時間到！", description="（結果處理中...）", color=0xffcccc)
        for item in self.children:
            item.disabled = True
        if self.followup_message:
            await self.followup_message.edit(embed=embed)
        await self.message.edit(view=self) 
        await self.update_followup(final=True)

    async def update_followup(self, final=False):
        choices_to_emojis = {
            "小火龍": "<:charmander:1234085837214584852>",  # Scissors
            "傑尼龜": "<:squirtle:1234085840590864465>",  # Rock
            "妙蛙種子": "<:bulbasaur:1234085832340668438>",    # Paper
            "未回應":"`逃走了`"
        }

        embed = discord.Embed(title="即時戰況", color=0x00DB00)  
        if final:
            embed.title = "挑戰結果"
            embed.color = 0xFFD306
            results_text = self.determine_winner()
            participants_status = "｜".join(
                f"{user.display_name}{choices_to_emojis.get(choice)}"
                for user, choice in self.responses.items()
            )
            embed.description = f"（{results_text}）\n\n{participants_status}"
            self.stop()
        else:
            participants_status = "｜".join(
                f"{user.display_name}{'`🟢已選擇`' if user in self.responses else '`🔴等待中`'}"
                for user in self.participants
            )
            embed.description = f"{participants_status}"
            embed.set_footer(text="正在等待其他參賽者...")

        if not self.followup_message:
            self.followup_message = await self.interaction.followup.send(embed=embed)
        else:
            await self.followup_message.edit(embed=embed)

    async def check_completion(self):
        if len(self.responses) == len(self.participants):
            for item in self.children:
                item.disabled = True  # Disable all select options
            await self.message.edit(view=self) 
            await self.update_followup(final=True)
            self.stop()
        else:
            pass

    def determine_winner(self):
        # Filter out non-responders
        active_responses = {user: choice for user, choice in self.responses.items() if choice != "未回應"}
        
        # Check if only one participant responded
        if len(active_responses) == 1:
            sole_responder = next(iter(active_responses))
            return f"**獲勝者是**👑{sole_responder.mention}——因為大家都棄拳了🫥"

        # Determine the types of responses
        response_types = set(active_responses.values())

        # Check for ties based on the types of responses
        if len(response_types) == 3 or len(response_types) == 1:
            return "平手～💫"

        # Custom rules based on missing responses
        if "小火龍" not in response_types:  # No scissors
            winners = [user.mention for user, choice in active_responses.items() if choice == "妙蛙種子"]  # Paper wins
        elif "妙蛙種子" not in response_types:  # No paper
            winners = [user.mention for user, choice in active_responses.items() if choice == "傑尼龜"]  # Rock wins
        elif "傑尼龜" not in response_types:  # No rock
            winners = [user.mention for user, choice in active_responses.items() if choice == "小火龍"]  # Scissors wins
        else:
            return "平手～💫"  # Fallback tie if none of the conditions are met

        # Format the winning result
        if len(winners) == 1:
            return f"**獲勝者是**👑{winners[0]}"
        else:
            return f"{'和'.join(winners)}平手💫"


class Rps(commands.Cog, name="rps"):
    def __init__(self, bot) -> None:
        self.bot = bot         

    @app_commands.command(name="戰豹", description="海豹豹！（來對戰吧👊🖐✌）")
    @app_commands.describe(
        rival1="指定你的對手，最多可選4位，也可以選擇小幫手🤖️",
        rival2="選擇更多對手(非必填)",
        rival3="選擇更多對手(非必填)",
        rival4="選擇更多對手(非必填)"
    )
    @app_commands.rename(rival1="對手1", rival2="對手2", rival3="對手3", rival4="對手4")
    async def challenge_command(self, interaction: Interaction, rival1: Member, rival2: Member = None, rival3: Member = None, rival4: Member = None):
        rivals = [rival1, rival2, rival3, rival4]  # List of all specified rivals
        # Filter out None and remove the interaction user from rivals list
        filtered_rivals = list(filter(lambda x: x is not None and x != interaction.user, rivals))

        # Check for duplicates by comparing the length of the list with and without duplicates
        if len(filtered_rivals) != len(set(filtered_rivals)):
            # Send an error message to the user
            return await interaction.response.send_message("（你指定了重複的對手，請重新輸入。）", ephemeral=True)

        if not filtered_rivals:
            return await interaction.response.send_message("（你必須選擇至少一位對手，且不能挑戰自己！）", ephemeral=True)

        participants = [interaction.user] + filtered_rivals
        view = RockPaperScissorsView(participants)
   
        await interaction.response.send_message(f"{'、'.join(rival.mention for rival in filtered_rivals)}（接受{interaction.user.mention}的挑戰吧！）", view=view)
        message = await interaction.original_response()
        view.message = message
        await view.bot_responses(interaction)


async def setup(bot) -> None:
    await bot.add_cog(Rps(bot))
