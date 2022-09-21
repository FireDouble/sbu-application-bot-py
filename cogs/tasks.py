import discord
from discord.ext import commands, tasks

from utils.constants import GUILDS, TOTAL_MEMBERS_ID, SERVER_MEMBERS_ID, SERVER_ID, QOTD_ID, QOTD_ROLE_ID, MOD_CHAT_ID, ADMIN_ID
from utils.schemas.QOTDSchema import QOTDSchema

import requests
import tarfile
import os
import sqlite3

from asyncio import sleep

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_members.start()
        self.backup_db.start()
        self.send_qotd.start()

    def cog_unload(self):
        self.update_members.cancel()
        self.backup_db.cancel()
        self.send_qotd.cancel()
    
    @tasks.loop(hours=24)
    async def send_qotd(self):
        db = sqlite3.connect(QOTDSchema.DB_PATH + QOTDSchema.DB_NAME + '.db')
        cursor = db.cursor()

        cursor.execute(f'''SELECT rowid, * FROM QOTD WHERE rowid IS NOT NULL ORDER BY rowid ASC''')
        
        data = cursor.fetchone()

        if data is None:
            channel = self.bot.get_channel(MOD_CHAT_ID)
            role = channel.guild.get_role(ADMIN_ID)
            await channel.send(f"{role.mention} The bot has ran out of QOTD's!")
            return
        
        qotd = data[1]
        rowid = data[0]

        channel = self.bot.get_channel(QOTD_ID)
        role = channel.guild.get_role(QOTD_ROLE_ID)
        await channel.send(qotd + f"\n{role.mention}")

        cursor.execute(f'''DELETE FROM QOTD WHERE rowid = {rowid}''')
        db.commit()

        cursor.execute('''SELECT rowid FROM QOTD''')
        data = cursor.fetchall()
        if len(data) < 2:
            channel = self.bot.get_channel(MOD_CHAT_ID)
            role = channel.guild.get_role(ADMIN_ID)
            await channel.send(f"{role.mention} The bot is running out of QOTD's!")

    @send_qotd.before_loop
    async def wait_one_hour(self):
        await sleep(3600)



    @tasks.loop(hours=1)
    async def update_members(self):
        total = 0
        for num, guild in enumerate(GUILDS.keys()):
            uuid = GUILDS[guild]["uuid"]
            info = requests.get(f"https://api.slothpixel.me/api/guilds/id/{uuid}").json()
            members = len(info["members"])

            vc = self.bot.get_channel(int(GUILDS[guild]["vc"]))
            await vc.edit(reason="Update members", name=f"{guild}: {members}")

            total = total + members
        
        vc = self.bot.get_channel(TOTAL_MEMBERS_ID)
        await vc.edit(reason="Update members", name=f"Total Members: {total}")

        vc = self.bot.get_channel(SERVER_MEMBERS_ID)
        guild = self.bot.get_guild(SERVER_ID)
        await vc.edit(reason="Update members", name=f"Server Members: {guild.member_count}")
    
    @tasks.loop(hours=24)
    async def backup_db(self):
        with tarfile.open("./backup/backup.tar.gz", "w:gz") as tar_handle:
            for root, dirs, files in os.walk("./data"):
                for file in files:
                    if file.endswith(".db"):
                        tar_handle.add(os.path.join(root, file), arcname=file)

def setup(bot):
    bot.add_cog(Tasks(bot))