# Ben Humphrey
# github.com/complexitydev
# ben@complexitydevelopment.com

import operator
import re

from bs4 import BeautifulSoup
from discord.ext import commands

from modules.aws_lambda import aws


class Commands:
    def __init__(self, client):
        self.client = client

    @staticmethod
    def parse_heroes(self, page):
        soup = BeautifulSoup(page)
        rows = soup.find_all('tr')
        table = {}
        for row in rows:
            hero = ''
            for cell in row.findChildren('td'):
                r = re.search('<td class=\"cell-icon\".{0,50}value=\"([\w\s]+)\"', str(cell))
                if r:
                    hero = r.group(1)
                    table[hero] = 0
                    continue
                r = re.search('value=\"([\d\.]+).{50,75}win', str(cell))
                if r:
                    table[hero] = r.group(1)
        sort = sorted(table.items(), key=operator.itemgetter(1), reverse=True)
        output = "```\n"
        for i in range(10):
            stat = sort[i]
            output += "{}, {}%\n".format(stat[0], stat[1])
        output += "```"
        return output

    @commands.command(pass_context=True)
    async def winrate(self, ctx, request):
        positions = ["mid", "off", "safe", "jungle", "roaming"]

        if not request or request not in positions:
            usage = "```Usage:\n.dotabuff [mid|off|safe|jungle|roaming]"
            await self.client.say(usage)

        output = self.parse_heroes(aws.process("dotabuff", request))
        await self.client.say(output)


def setup(client):
    client.add_cog(Commands(client))
