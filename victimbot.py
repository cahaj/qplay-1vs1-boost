from javascript import require, On
import time
import random

mineflayer = require('mineflayer')

class Victim():
    def __init__(self, username:str, victim:str, victimpass:str, servers:list, StatBotRun) -> None:
        self.username = username
        self.victim = victim
        self.servers = servers
        self.victimpass = victimpass

        self.statbotrun = StatBotRun

    def run(self):
        self.bot = mineflayer.createBot({
        'host': 'mc.qplay.cz',
        'port': 25565,
        'username': self.victim,
        'version': "1.12.2"
        })

        print("Started stat bot")
       
        @On(self.bot, 'login')
        def handle(*args):
            print("logged in")
            time.sleep(1)
            self.bot.chat(f"/register {self.victimpass} {self.victimpass}")
            self.bot.chat(f"/login {self.victimpass}")
            time.sleep(2)
            
            for i in self.statbotrun():
                if "ServerChange" in i.keys():
                    self._switchserver(s=i["ServerChange"])
                elif "FoundVictim" in i.keys():
                    self._switchserver(s=i["Lobby-OvsO1"])

    def _switchserver(self, s:str = None):
        if s == None:
            s = random.choice(self.servers)
            self.bot.chat(f"/server {s}")
            return s
        else:
            self.bot.chat(f"/server {s}")
            return s

