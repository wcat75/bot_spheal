""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

def is_owner_or_admin():
    async def predicate(ctx: Context) -> bool:
        # Bot 擁有者
        owner_id = getattr(ctx.bot, "owner_id", None)
        is_owner = owner_id is not None and ctx.author.id == owner_id

        # admin_ids 清單
        owner_cog = ctx.bot.get_cog("owner")
        is_admin = False
        if owner_cog and hasattr(owner_cog, "admin_ids"):
            is_admin = ctx.author.id in owner_cog.admin_ids

        # 管理員身分組 ID 列表
        allowed_role_ids = [1138373306165248142]  # ✅ 替換成你自己的身分組ID
        is_role_ok = any(role.id in allowed_role_ids for role in ctx.author.roles)

        return is_owner or is_admin or is_role_ok

    return commands.check(predicate)

class Owner(commands.Cog, name="owner"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        name="sync",
        description="Synchonizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global` or `guild`.
        """

        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally synchronized.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been synchronized in this guild.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
        name="unsync",
        description="Unsynchonizes the slash commands.",
    )
    @app_commands.describe(
        scope="The scope of the sync. Can be `global`, `current_guild` or `guild`"
    )
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        Unsynchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global`, `current_guild` or `guild`.
        """

        if scope == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally unsynchronized.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been unsynchronized in this guild.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
        name="load",
        description="Load a cog",
    )
    @app_commands.describe(cog="The name of the cog to load")
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        The bot will load the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to load.
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not load the `{cog}` cog.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully loaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.command(
        name="unload",
        description="Unloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        The bot will unload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to unload.
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not unload the `{cog}` cog.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully unloaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.command(
        name="reload",
        description="Reloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        The bot will reload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to reload.
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not reload the `{cog}` cog.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully reloaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(description="Shutting down. Bye! :wave:", color=0xBEBEFE)
        await context.send(embed=embed)
        await self.bot.close()


    """
    Below can be used by given admin.
    """

    @commands.command(
        name="say",
        description="The bot will say anything you want.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @is_owner_or_admin()
    async def say(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        await context.send(message)

    @commands.command(
        name="sayin",
        description="The bot will say anything you want in a specific channel.",
    )
    @app_commands.describe(channel="The channel where the message should be sent",
                       message="The message that should be repeated by the bot")
    @is_owner_or_admin()
    async def sayin(self, context: commands.Context, channel: discord.TextChannel, *, message: str) -> None:
        """
        Send a message to a specified channel.

        Parameters:
            channel (discord.TextChannel): The channel to send the message to.
            message (str): The message to send.
        """
        try:
            await channel.send(message)
            await context.send(f"Message sent to {channel.mention}")
        except discord.Forbidden:
            await context.send("I do not have permission to send messages in that channel.")
        except Exception as e:
            await context.send(f"An error occurred: {e}")

    @commands.command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @is_owner_or_admin()
    async def embed(self, context: commands.Context, *, args: str):
        """
        The bot will say anything you want, but using embeds, with optional title and footer.

        :param context: The hybrid command context.
        :param args: The full string containing message, title, and footer.
        """
        # Default values
        title = None
        footer = None
        message = args

        # Simple parsing for 'title=' and 'footer=' in the command input
        if "title=" in args:
            parts = args.split("title=")
            message = parts[0].strip()
            title = parts[1].split("footer=")[0].strip()

        if "footer=" in args:
            parts = args.split("footer=")
            message = parts[0].strip() if "title=" not in args else message
            footer = parts[1].strip()

        # Create embed with parsed data
        embed = discord.Embed(description=message, color=0x000000)
        if title:
            embed.title = title
        if footer:
            embed.set_footer(text=footer)
        
        try:
            await context.send(embed=embed)
        except Exception as e:
            await context.send(f"An error occurred: {e}")

    @commands.command(
        name="embedin",
        description="The bot will say anything you want in an embed in a specific channel.",
    )
    @is_owner_or_admin()
    async def embedin(self, context: commands.Context, channel: discord.TextChannel, *, args: str):
        """
        Send a message within an embed to a specified channel, with optional title and footer.

        Parameters:
            channel (discord.TextChannel): The channel to send the message to.
            args (str): The full string containing message, title, and footer.
        """
        # Default values
        title = None
        footer = None
        message = args

        # Simple parsing for 'title=' and 'footer=' in the command input
        if "title=" in args:
            parts = args.split("title=")
            message = parts[0].strip()
            title = parts[1].split("footer=")[0].strip()

        if "footer=" in args:
            parts = args.split("footer=")
            message = parts[0].strip() if "title=" not in args else message
            footer = parts[1].strip()

        # Create embed with parsed data
        embed = discord.Embed(description=message, color=0x000000)
        if title:
            embed.title = title
        if footer:
            embed.set_footer(text=footer)

        try:
            await channel.send(embed=embed)
            await context.send(f"Embed sent to {channel.mention}")
        except discord.Forbidden:
            await context.send("I do not have permission to send messages in that channel.")
        except Exception as e:
            await context.send(f"An error occurred: {e}")


    @commands.command(
        name="edit",
        description="Edit a message that the bot has sent.",
    )
    @is_owner_or_admin()
    async def edit(self, context: commands.Context, *, args: str):
        """
        Edit a message sent by the bot.

        Parameters:
            args (str): The new content to update the message with, optionally including a channel mention, message ID,
                        and 'title=' and 'footer='.
        """
        try:
            # Default channel is the current context's channel
            channel = context.channel

            # Check if a channel mention was included
            if args.startswith('<#') and '>' in args:
                channel_mention_end = args.find('>')
                channel_id = int(args[2:channel_mention_end])  # Extract channel ID from mention
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    await context.send("Channel not found.")
                    return

                # Remove the mention from args and get the message ID
                args = args[channel_mention_end + 1:].strip()
                message_id_str, args = args.split(" ", 1)
                message_id = int(message_id_str.strip())
            else:
                # If no channel mention, assume current channel and extract message ID
                message_id_str, args = args.split(" ", 1)
                message_id = int(message_id_str.strip())

            # Fetch the message
            message = await channel.fetch_message(message_id)
            if not message:
                await context.send("Message not found.")
                return

            # Default values for title and footer
            title = None
            footer = None
            new_content = args

            # Parsing for 'title=' and 'footer=' in the command input
            if "title=" in args:
                parts = args.split("title=")
                new_content = parts[0].strip()
                title = parts[1].split("footer=")[0].strip()

            if "footer=" in args:
                parts = args.split("footer=")
                new_content = parts[0].strip() if "title=" not in args else new_content
                footer = parts[1].strip()

            # Check if the message is an embed or plain text
            if message.embeds:
                embed = message.embeds[0]
                embed.description = new_content
                if title:
                    embed.title = title
                if footer:
                    embed.set_footer(text=footer)
                await message.edit(embed=embed)
            else:
                await message.edit(content=new_content)

            await context.send(f"Message in {channel.mention} has been edited.")

        except discord.Forbidden:
            await context.send("I do not have permission to edit messages in that channel.")
        except discord.NotFound:
            await context.send("Message not found.")
        except Exception as e:
            await context.send(f"An error occurred: {e}")


async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
