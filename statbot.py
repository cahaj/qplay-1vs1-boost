from javascript import require, On
import time
import random

mineflayer = require('mineflayer')

class StatBot():
  def __init__(self, username:str, statpass:str, victimlist:list, servers:list) -> None:
    self.username = username
    self.victim = victimlist
    self.servers = servers
    self.statpass = statpass

  def run(self):
    self.bot = mineflayer.createBot({
      'host': 'mc.qplay.cz',
      'port': 25565,
      'username': self.username,
      'version': "1.12.2"
    })

    print("Started stat bot")

    @On(self.bot, 'spawn')
    def handle(*args):
      print("Spawned")
      self.bot.chat(f"/register {self.statpass} {self.statpass}")
      self.bot.chat(f"/login {self.statpass}")


    @On(self.bot, 'chat')
    def handleMsg(this, sender, message, *args):
      print(sender, message)
      if "Connecting to Lobby-Main" in message:
        time.sleep(2)
        s = self._switchserver(self.servers)
        yield {"ServerChange": s}

      if "Winner" in message or "Winner" in sender:
        time.sleep(1)
        s = self._switchserver(self.servers)
        yield {"ServerChange": s}

      if "has joined the game" in message:
        time.sleep(1)
        if self.victim in message or self.username in message:
          yield {"FoundVictim": True}
        else:
          s = self._switchserver(self.servers)
          yield {"ServerChange": s}

      if "rank IRON II" in message:
        time.sleep(1)
        s = self._switchserver(self.servers)
        yield {"ServerChange": s}

    @On(self.bot, "end")
    def handle(*args):
      print("Bot ended!", args)

  def _switchserver(self, s:str = None):
    if s == None:
      s = random.choice(self.servers)
      self.bot.chat(f"/server {s}")
      return s
    else:
      self.bot.chat(f"/server {s}")
      return s