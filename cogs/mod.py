import discord
from discord.ext import commands

from utils.constants import JR_MOD_ID, MOD_ID, INVITE_CHANNEL
from utils.schemas.WarnedMember import WarnedMember

import humanfriendly
import sqlite3
import datetime

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_role(MOD_ID)
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason=None):
        try:
            await ctx.guild.ban(user=user, delete_message_days=0, reason=reason)
        except discord.Forbidden:
            await ctx.reply(f"The bot doesn't have permissions to ban this user!")
            return
        
        message = f"{user} was Successfuly banned"

        try:
            await user.send(f"You've been banned from {ctx.guild.name}\n```reason: {reason}```")
        except discord.HTTPException:
            message += ", failed to dm"

        await ctx.reply(message)

    @ban.error
    async def ban_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.BadArgument) or isinstance(exception, commands.MissingRequiredArgument):
            await ctx.reply("Invalid format. Use `+ban <@member> [reason]")

    
    @commands.command()
    @commands.has_role(MOD_ID)
    async def unban(self, ctx: commands.Context, user: discord.User, *, reason=None):
        try:
            await ctx.guild.unban(user=user, reason=reason)
        except discord.Forbidden:
            await ctx.reply(f"The bot doesn't have permissions to unban this user!")
            return
        except discord.NotFound:
            await ctx.reply(f"This user isn't banned!")
            return

        message = f"{user} was Successfuly banned"

        try:
            link = await bot.get_channel(INVITE_CHANNEL).create_invite()
            await user.send(f"You have been unbanned from {ctx.guild.name}\n{link}")
        except discord.HTTPException:
            message += ", failed to dm" 
        except Exception as exception:
            await log_error(ctx, exception)
        
        await ctx.reply(message)
    
    @unban.error
    async def unban_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.BadArgument) or isinstance(exception, commands.MissingRequiredArgument):
            await ctx.reply("Invalid format. Use `+unban <@member> [reason]")
    
    
    @commands.command()
    @commands.has_role(JR_MOD_ID)
    async def mute(self, ctx: commands.Context, member: discord.Member, time: str, *, reason=None):
        try:
            time = humanfriendly.parse_timespan(time)
        except humanfriendly.InvalidTimespan:
            raise commands.BadArgument

        if time > (30 * 86400):
            await ctx.reply("Max mute duration is 30 days!")
            return
        
        duration = datetime.timedelta(seconds=time)

        try:
            await member.timeout_for(duration=duration, reason=reason)
        except discord.Forbidden:
            await ctx.reply("The bot doesn't have permissions to mute this member!")

    @mute.error
    async def mute_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.BadArgument) or isinstance(exception, commands.MissingRequiredArgument):
            await ctx.reply("Invalid format. Use `+mute <@member> <time> [reason]")


    @commands.command()
    @commands.has_role(JR_MOD_ID)
    async def unmute(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        try:
            await member.remove_timeout(reason=reason)
        except discord.Forbidden:
            await ctx.reply("The bot doesn't have permissions to unmute this member!")
    

    @commands.command()
    @commands.has_role(JR_MOD_ID)
    async def warn(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        member_id = member.id

        db = sqlite3.connect(WarnedMember.DB_PATH + WarnedMember.DB_NAME + '.db')
        cursor = db.cursor()

        time = int(datetime.datetime.now().timestamp())
            
        cursor.execute(f'''SELECT * FROM "WARNS" WHERE guild={ctx.guild.id} AND member={member_id}''')
        warn_id = 1
        for warn in cursor.fetchall():
            warn_id += 1


        warn = WarnedMember(member_id, ctx.guild.id, reason, ctx.author.id, time, warn_id)

        cursor.execute(*(warn.insert()))
        db.commit()

        cursor.execute(f'''SELECT * FROM "WARNS" WHERE guild={ctx.guild.id} AND member={member_id}''')

        warns = []
        for warn in cursor.fetchall():
            warns.append(warn)

        print(warns)

        db.close()

        await ctx.reply(f"Successfuly warned {member}")


    @commands.command()
    @commands.has_role(JR_MOD_ID)
    async def infractions(self, ctx: commands.Context, member: discord.Member):
        db = sqlite3.connect(WarnedMember.DB_PATH + WarnedMember.DB_NAME + '.db')
        cursor = db.cursor()

        cursor.execute(f'''SELECT * FROM "WARNS" WHERE guild={ctx.guild.id} AND member={member.id}''')

        warns = ""
        num = 0
        for warn in cursor.fetchall():
            if num == 10:
                break
            warn = WarnedMember.dict_from_tuple(warn)
            warns += f"**{warn['reason']}** - <t:{warn['time']}:R> ID: {warn['id']}\n"
            num += 1;
        
        embed = discord.Embed(
            title=f"{member.display_name}'s infractions",
            color=0x1e1e1e
        )
        if warns == "":
            warns = "This user doesnt have any infractions"
        embed.add_field(name="**Last 10 infractions**", value=warns, inline=True)

        await ctx.reply(embed=embed)
    
    @commands.command()
    @commands.has_role(MOD_ID)
    async def del_warn(self, ctx: commands.Context, member: discord.Member, warn_id: int):
        db = sqlite3.connect(WarnedMember.DB_PATH + WarnedMember.DB_NAME + '.db')
        cursor = db.cursor()

        cursor.execute(f'''SELECT rowid FROM "WARNS" WHERE guild = {ctx.guild.id} AND member = {member.id} AND id = {warn_id}''')
        rowid = cursor.fetchone()

        if rowid is None:
            return await ctx.reply("Invalid warn ID")
        
        rowid = rowid[0]
        
        cursor.execute(f'''DELETE FROM "WARNS" WHERE rowid = {rowid}''')
        db.commit()

        await ctx.reply("Successfuly removed this warn")




def setup(bot):
    bot.add_cog(Mod(bot))