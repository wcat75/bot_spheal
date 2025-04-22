import os
import random
import discord
from openai import OpenAI
from discord.ext import commands
from discord import app_commands, Embed, Interaction

client = OpenAI(api_key=os.getenv("APIKEY"))

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def analyze_tone(self, user_message: str) -> str:
        system_prompt = (
            "你是一隻可愛體貼的海豹球寶可夢，會根據使用者的語氣給予一個反應，"
            "請根據語氣判斷並回應一段簡短的海豹式語句（例如：海豹！、豹～？、海海、海豹...、球～、豹豹）。"
            "不要解釋，只可以用「海」、「豹」、「球」等三個字排列組合及表情符號進行回應，表情符號不可以用人臉。"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=15
        )

        return response.choices[0].message.content.strip() # type: ignore

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author.bot:
            return
        
        # 檢查是否有提及機器人
        if self.bot.user in message.mentions:
            ctx = await self.bot.get_context(message)
            if ctx.valid:
                return  # 如果是有效指令就不回應
            reply = await self.analyze_tone(message.content)
            await message.channel.send(reply)

    @app_commands.command(name="問豹", description="海豹？（問我任何問題🤓）")
    @app_commands.describe(question="你想問的問題")
    @app_commands.rename(question="問題")
    async def eight_ball(self, interaction: Interaction, *, question: str) -> None:
        system_prompt = (
            "你是一隻可愛體貼的海豹球寶可夢，會用簡短可愛的方式回答問題。\n"
            "請根據使用者的提問語氣與內容，生成一段簡短有趣、帶點情緒、風格像括號內那樣的回應，例如：\n"
            "（當然可以～） （我覺得不行！） （再問一次看看？） （我不太懂耶～）\n"
            "語助詞可以包含：～、喔、啦、耶、或表情符號，但不能超過10個字，表情符號不可以用人臉。"
            "每個回答都要包含前後括號，禁止多餘說明，也禁止回傳原始問題內容。"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=20,
        )

        reply = response.choices[0].message.content.strip()

        embed = Embed(
            description=reply,
            color=0xBEBEFE,
        )
        embed.set_footer(text=f"「{question}🤔」by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="選豹", description="海？(選擇困難🤔幫你選🥰)")
    @app_commands.describe(
        option1="選項1",
        option2="選項2",
        option3="選項3 (可選)",
        option4="選項4 (可選)",
        option5="選項5 (可選)"
    )
    @app_commands.rename(option1="選項1", option2="選項2", option3="選項3", option4="選項4", option5="選項5")
    async def choose_one(self, interaction: discord.Interaction, 
                        option1: str, 
                        option2: str, 
                        option3: str = None, 
                        option4: str = None, 
                        option5: str = None):

        options = [option1, option2, option3, option4, option5]
        options = [option for option in options if option is not None]
        choice = random.choice(options)

        # Process mentions into display names
        def convert_mention(option):
            if option.startswith('<@') and option.endswith('>'):
                user_id = int(option.strip('<@!>'))
                member = interaction.guild.get_member(user_id)
                if member:
                    return member.display_name
            return option

        options = [convert_mention(option) for option in options if option is not None]

        options_text = "｜".join([f"{option}" for option in options])
        embed = Embed(description=f"（我選擇 ✨**{choice}**✨）",color=0x46A3FF) 
        embed.set_footer(text=f"「{options_text}」by {interaction.user.display_name}")

        # Send the embed message
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="吃豹", description="球？（宵夜吃什麼？）",)
    # @app_commands.describe(meal_type="選擇時段：早餐、午餐、晚餐、宵夜")
    # @app_commands.choices(meal_type=[
    #     app_commands.Choice(name="早餐", value="早餐"),
    #     app_commands.Choice(name="午餐", value="午餐"),
    #     app_commands.Choice(name="晚餐", value="晚餐"),
    #     app_commands.Choice(name="宵夜", value="宵夜")
    # ])
    # @app_commands.rename(meal_type="時段")
    async def eat_wheel(self, interaction: Interaction) -> None: #, meal_type: str

        restaurants = [
            "白帝城",
            "海底撈",
            "錢都",
            "上賀",
            "金鋒滷肉飯",
            "天香臭豆腐",
            "台一牛奶冰",
            "鴉片粉圓",
            "台電大樓永和豆漿",
            "廣東粥",
            "鍋in",
            "師園鹽酥雞",
            "炎弟鐵板燒",
            "麥當勞",
            "阿薄朗",
            "龍泉深海魚",
            "麻小麵",
            "安居街",
            "麥當勞",
            "瑞安街永和豆漿",
            "大埔鐵板燒",
            "莫宰羊",
            "すき家",
            "玉欣珍"
        ]
        embed = Embed(description=f"（我想吃 **{random.choice(restaurants)}**😋）",color=0x46A3FF) 
        embed.set_footer(text=f"宵夜吃什麼？ by {interaction.user.display_name}") #{meal_type}
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Chat(bot))
