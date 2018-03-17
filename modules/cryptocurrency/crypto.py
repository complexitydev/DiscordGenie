# Ben Humphrey
# github.com/complexitydev
# ben@complexitydevelopment.com

import json

from discord.ext import commands

from modules.aws_lambda import aws


def get_info(request):
    info = json.loads(aws.process("crypto", request))
    if 'error' in info['message']:
        return "error"

    message = '```\n{}:\nUSD: {}\nBTC: {}\n24 Hour Change: {}%\n```'.format(
        info['message'][0]['name'],
        info['message'][0]['price_usd'],
        info['message'][0]['price_btc'],
        info['message'][0]['percent_change_24h'])
    return message


class Commands:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def check(self, ctx, request):
        if ctx.message.channel.id != "422504096990494741":
            return
        message = get_info(request)
        if message == "error":
            await self.client.say("Error processing. Don't use the symbol name!")

        await self.client.say(message)


def setup(client):
    client.add_cog(Commands(client))
