# Ben Humphrey
# github.com/complexitydev
# ben@complexitydevelopment.com

import re

from discord.ext import commands

from modules.aws_lambda import aws


class Commands:
    def __init__(self, client):
        self.client = client

    def parse_heroes(self, page):
        m = re.search('<tbody>(.+)?<\/tbody>', page.rstrip('\n'), re.IGNORECASE)
        table = m.group(1)
        filename = "test.txt"
        file = open(filename)
        file.write(table)
        # Group 1 hero name, Group 2 win rate
        pattern = re.compile(
            '<tr>.{0,750}value=\\"(\w+)\\\">.{500,900}value=\\\"([\d\.]+)\\\">.{0,250}segment-win.{0,600}<\/tr>',
            re.IGNORECASE)
        for (name, winrate) in re.findall(pattern, table):
            print(name, winrate)

    @commands.command(pass_context=True)
    async def winrate(self, ctx, request):
        positions = ["mid", "off", "safe", "jungle", "roaming"]

        if not request or request not in positions:
            usage = "```Usage:\n.dotabuff [mid|off|safe|jungle|roaming]"
            await self.client.say(usage)
        await self.client.say("Processing winrate request for position {}".format(request))

        self.parse_heroes(aws.process("dotabuff", request))


def setup(client):
    client.add_cog(Commands(client))
