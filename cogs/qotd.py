import discord
from discord.ext import commands

from utils.schemas.QOTDSchema import QOTDSchema
from utils.constants import ADMIN_ID, JR_MOD_ID

from typing import Union
import sqlite3

class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(ADMIN_ID)
    async def qotdadd(self, ctx: commands.Context, *, question: str):
        
        db = sqlite3.connect(QOTDSchema.DB_PATH + QOTDSchema.DB_NAME + ".db")
        cursor = db.cursor()

        cursor.execute(f'''SELECT * FROM "QOTD"''')
        
        qotd = QOTDSchema(question)
        cursor.execute(*(qotd.insert()))
        db.commit()

        db.close()

        await ctx.reply("Successfuly added QOTD")
    
    @commands.command()
    @commands.has_role(JR_MOD_ID)
    async def qotdlist(self, ctx: commands.Context):
        db = sqlite3.connect(QOTDSchema.DB_PATH + QOTDSchema.DB_NAME + '.db')
        cursor = db.cursor()

        cursor.execute('''SELECT rowid, * FROM QOTD''')
        qotds = cursor.fetchall()

        message = ""
        if not qotds == []:
            for qotd in qotds:
                qotd = QOTDSchema.dict_from_tuple(qotd)
                question = qotd["question"]
                num = qotd["id"]
                message += f"`{num}` **{question}**\n"
        else:
            message = "The list is empty"
        
        embed = discord.Embed(
            title="All QOTD's:",
            description=message
        )

        db.close()

        await ctx.reply(embed=embed)
    
    @commands.command()
    @commands.has_role(ADMIN_ID)
    async def qotddel(self, ctx: commands.Context, num: int):
        db = sqlite3.connect(QOTDSchema.DB_PATH + QOTDSchema.DB_NAME + '.db')
        cursor = db.cursor()

        cursor.execute(f'''DELETE FROM "QOTD" WHERE rowid = {num}''')

        db.commit()

        await ctx.reply("Successfuly removed that QOTD")

def setup(bot):
    bot.add_cog(QOTD(bot))