import os
import json
import discord
from discord.ext import commands

class ReactRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Construct the path to reaction_roles.json relative to the bot_spheal directory
        self.config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reaction_roles.json")
        print(f"Loading config from: {self.config_file}")
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                self.reaction_roles = json.load(f)
            print("Loaded reaction_roles, use `!rr show` to check.")
        except FileNotFoundError:
            self.reaction_roles = {}
            print("reaction_roles.json not found, starting with an empty config.")

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.reaction_roles, f, indent=4)
        print("reaction_roles.json has been updated.")

    @commands.group(invoke_without_command=True)
    async def rr(self, ctx):
        await ctx.send("Use `!rr add`, `!rr remove`, `!rr show`, or `!rr clear` for reaction role management.")

    @rr.command(name='add')
    async def add_reaction_role(self, ctx, message_url, *args):
        channel_id, message_id = self.parse_message_url(message_url)
        message = await self.fetch_message(ctx.guild, channel_id, message_id)
        if not message:
            return await ctx.send("Message not found.")

        if message_id not in self.reaction_roles:
            self.reaction_roles[message_id] = {"channel_id": channel_id, "reactions": {}}

        pairs = zip(args[0::2], args[1::2])
        for emoji, role in pairs:
            role = await commands.RoleConverter().convert(ctx, role)
            await message.add_reaction(emoji)
            self.reaction_roles[message_id]["reactions"][emoji] = role.id

        self.save_config()
        await ctx.send("Reaction roles added.")

    @rr.command(name='remove')
    async def remove_reaction_role(self, ctx, message_url, *emojis):
        channel_id, message_id = self.parse_message_url(message_url)
        if message_id in self.reaction_roles:
            for emoji in emojis:
                if emoji in self.reaction_roles[message_id]["reactions"]:
                    del self.reaction_roles[message_id]["reactions"][emoji]
            if not self.reaction_roles[message_id]["reactions"]:
                del self.reaction_roles[message_id]  # Optionally remove the entry if empty
            self.save_config()
            await ctx.send("Reaction roles removed.")
        else:
            await ctx.send("No reaction roles found for this message.")

    @rr.command(name='show')
    async def show_reaction_roles(self, ctx):
        if not self.reaction_roles:
            await ctx.send("No reaction roles set in this guild.")
            return
        
        embed = discord.Embed(title="Reaction Roles Overview", color=0x00ff00)
        embed.description = "Below are the reaction roles set up in various messages:\n"

        for msg_id, details in self.reaction_roles.items():
            channel_id = details['channel_id']
            channel = ctx.guild.get_channel(int(channel_id))
            if channel:
                message_link = f"https://discord.com/channels/{ctx.guild.id}/{channel_id}/{msg_id}"
                roles_info = "\n".join(
                    f"{emoji}: {ctx.guild.get_role(role_id).mention}" if (role := ctx.guild.get_role(role_id)) else f"{emoji}: Role not found"
                    for emoji, role_id in details['reactions'].items())
                # Format the message section
                message_info = f"\n**Message in {channel.mention}: [Jump to message]({message_link})**\n{roles_info}"
                # Check if adding this message would exceed the embed limit
                if len(embed.description) + len(message_info) > 6000:
                    await ctx.send(embed=embed)
                    embed = discord.Embed(title="Reaction Roles Continued", color=0x00ff00)
                    embed.description = message_info  # Start a new embed if the limit is reached
                else:
                    embed.description += message_info
            else:
                embed.description += f"\n**Channel not found for message ID {msg_id}**"

        await ctx.send(embed=embed)


    @rr.command(name='clear')
    async def clear_reaction_roles(self, ctx, message_url):
        channel_id, message_id = self.parse_message_url(message_url)
        message = await self.fetch_message(ctx.guild, channel_id, message_id)
        if message and str(message_id) in self.reaction_roles:
            # Remove all bot reactions from the message
            reactions = self.reaction_roles[str(message_id)].get('reactions', {})
            for emoji in reactions.keys():
                try:
                    await message.clear_reaction(emoji)
                except discord.HTTPException as e:
                    print(f"Failed to remove reaction {emoji}: {str(e)}")

            # Remove the reaction roles from the config and save
            del self.reaction_roles[str(message_id)]
            self.save_config()
            await ctx.send(f"All reaction roles and reactions cleared for message ID {message_id}.")
        else:
            await ctx.send("No reaction roles found for this message, or message could not be accessed.")


    def parse_message_url(self, message_url):
        parts = message_url.split('/')
        return parts[-2], parts[-1]

    async def fetch_message(self, guild, channel_id, message_id):
        channel = guild.get_channel(int(channel_id))
        if channel:
            try:
                return await channel.fetch_message(int(message_id))
            except discord.NotFound:
                print("Message not found in the given channel.")
            except discord.Forbidden:
                print("Bot does not have permissions to access channel messages.")
        return None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = str(payload.message_id)
        if message_id in self.reaction_roles and str(payload.emoji) in self.reaction_roles[message_id]["reactions"]:
            guild = self.bot.get_guild(payload.guild_id)
            if not guild:
                return
            
            role_id = self.reaction_roles[message_id]["reactions"][str(payload.emoji)]
            role = guild.get_role(role_id)
            if not role:
                print(f"Role with ID {role_id} not found in guild {guild.name}.")
                return
            
            member = guild.get_member(payload.user_id)
            if not member:
                print(f"Member with ID {payload.user_id} not found in guild.")
                return
            
            try:
                await member.add_roles(role)
                print(f"Added {role.name} to {member.display_name} due to reaction.")
            except discord.Forbidden:
                print("Bot does not have permission to add roles.")
            except Exception as e:
                print(f"Failed to add role: {str(e)}")


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = str(payload.message_id)
        if message_id in self.reaction_roles and str(payload.emoji) in self.reaction_roles[message_id]["reactions"]:
            guild = self.bot.get_guild(payload.guild_id)
            if not guild:
                return
            
            role_id = self.reaction_roles[message_id]["reactions"][str(payload.emoji)]
            role = guild.get_role(role_id)
            if not role:
                print(f"Role with ID {role_id} not found in guild {guild.name}.")
                return
            
            member = guild.get_member(payload.user_id)
            if not member:
                print(f"Member with ID {payload.user_id} not found in guild.")
                return
            
            try:
                await member.remove_roles(role)
                print(f"Removed {role.name} from {member.display_name} due to reaction removal.")
            except discord.Forbidden:
                print("Bot does not have permission to remove roles.")
            except Exception as e:
                print(f"Failed to remove role: {str(e)}")


async def setup(bot):
    await bot.add_cog(ReactRoles(bot))
