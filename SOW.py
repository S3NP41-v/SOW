import discord
import re
import subprocess
from time import time
import os
from socket import gethostname
from json import loads, dumps
import TPManager


with open("config.json", 'r') as f:
    token = loads(f.read())["client-token"]
    f.close()


class Client(discord.Client):
    async def on_ready(self):
        with open("config.json", 'r') as f:
            self.configdata: dict
            self.configdata = loads(f.read())

        if self.configdata["login"] == "DEFAULT":
            self.login = gethostname()
        else:
            self.login = self.configdata["login"]

        self.lastused = ""
        self.TPManager = TPManager.TimePassword()
        self.trusted = None
        self.log = self.configdata['log']

        self.pause = False

        print(f"{self.user} | {self.login} listening on servers: ")
        for server in client.guilds:
            print(f"\t{server.name} :: {server.id}")
        else:
            print('\n', end='')

    async def on_message(self, message):
        message.content: str
        if message.author == self.user:
            return

        # if we don't have a trusted IE a connected user
        if not self.trusted:
            # initiating connecting
            conn = re.findall("(?:sow|SOW) (.*)@(.*)", message.content)
            if conn:
                conn = conn[0]
                # someone tried to connect to us
                if conn[0] == str(self.login):

                    # checking password, not accepting last used because someone might accidentally end their session, and we don't want the password to be re-used
                    paswd = self.TPManager.genpass()
                    if conn[1] == paswd and paswd != self.lastused:
                        # adding the user as a trusted one for the time of the connection
                        self.trusted = client.get_user(message.author.id)
                        self.lastused = paswd
                        mess = f"Confirmed connection from user {self.trusted}\n" \
                               f"Last connection by ID:{self.log[-1][0]} on {self.log[-1][1]}\n" \
                               f"SOW specific commands `::[command] [!args]` type `::help` for more info"
                        self.TPManager.addlog(int(message.author.id))

                        await self.trusted.send(mess)

        # we have an active connection
        else:
            # ignore all other messages
            if message.author.id != self.trusted.id:
                return

            if message.content[:2] == "::":
                # TODO SOW specific commands
                if message.content.startswith("::help"):
                    mess = "```\n" \
                           "::help   --  display this message\n" \
                           "::pause  --  pause/unpause the interpretation of messages as commands\n" \
                           "::exit   --  terminate the connection\n" \
                           "```"
                    await self.trusted.send(mess)

                elif message.content.startswith("::pause"):
                    self.pause = not self.pause

                elif message.content.startswith("::exit"):
                    self.trusted = None

                elif message.content.startswith("::sk"):
                    pass

                return
            else:
                if not self.pause:
                    try:
                        out = subprocess.check_output(message.content, shell=True)
                        print(message.content, message.author)

                    except subprocess.CalledProcessError as e:
                        await self.trusted.send(f"{e}\n")
                    except BaseException as e:
                        await self.trusted.send(f"{e}\n")
                    else:
                        await self.trusted.send(f"```\n{out.decode('UTF-8').rstrip()}```")


intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = Client(intents=intents)

client.run(token)


# TODO: see below
"""
- a portable password generator
- SOW specific commands
    -sk [send key]          -- send a keypress to the terminal
    -rfile [receive file]   -- get a file
    -sfile [send file]      -- send a file
"""
