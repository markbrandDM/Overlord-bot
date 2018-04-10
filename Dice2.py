import discord
import re
from discord.ext import commands
from random import randint


class Dice2:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["r"])
    async def roll(self, ctx):

        rollList = []
        conditionalRollList = []
        totalRollList = []
        match = "unknown"
        total = 0
        list = []
        symbol = ""
        author = ctx.message.author

        # define regex groups
        simpleRoll = re.compile('\d+')
        definedRoll = re.compile('d\d+')
        quantityRoll = re.compile('\d+d')
        modifier = re.compile('(\+|\-)\d+')
        conditional = re.compile('adv|dis')
        reroll = re.compile('reroll\d')
        drop = re.compile('drop\d')

        # log drop
        if not (re.search(drop, ctx.message.content)):
            dropOption = False
            print("No drop modifiers found")
        else:
            dropOption = re.search(drop, ctx.message.content).group()
            print(dropOption)
            dropValue = int(re.search(simpleRoll, dropOption).group())

        # log conditionals
        if not (re.search(conditional, ctx.message.content)):
            conditionalOption = False
            print("No conditional modifiers found")
        else:
            conditionalOption = re.search(conditional, ctx.message.content).group()
            print(conditionalOption)

        # log reroll
        if not (re.search(reroll, ctx.message.content)):
            rerollOption = False
            rerollValue = 0
            print("No reroll modifiers found")
        else:
            rerollOption = re.search(reroll, ctx.message.content).group()
            print(rerollOption)
            rerollValue = int(re.search(simpleRoll, rerollOption).group())

        # log simpleRoll
        if not (re.search(simpleRoll, ctx.message.content)):
            print("SimpleRoll not found, Default to 100")
            match = "100"
        else:
            match = re.search(simpleRoll, ctx.message.content).group()

        # log definedRoll
        if not(re.search(definedRoll, ctx.message.content)):
            print("DefinedRoll not found")
        else:
            match = re.search(definedRoll, ctx.message.content).group()
            print(re.search(simpleRoll, match).group())
            # print(match)

        # log quantityRoll
        if not(re.search(quantityRoll, ctx.message.content)):
            print("No match for quantityRoll found, defaulting to 1")
            quantityLoop = 1
        else:
            quantity = re.search(quantityRoll, ctx.message.content).group()
            quantityLoop = int(re.search(simpleRoll, quantity).group())
            print(re.search(simpleRoll, quantity).group())
            # print(quantity)

        # main logic loop
        for x in range(0, quantityLoop):
            rollList.append(self.getRoll(int(re.search(simpleRoll, match).group()), rerollOption, rerollValue))
            if (conditionalOption):
                conditionalRollList.append(self.getRoll(int(re.search(simpleRoll, match).group()), rerollOption, rerollValue))
                if (conditionalOption == "adv"):
                    if (rollList[x] <= conditionalRollList[x]):
                        totalRollList.append(conditionalRollList[x])
                    else:
                        totalRollList.append(rollList[x])
                if (conditionalOption == "dis"):
                    if (rollList[x] >= conditionalRollList[x]):
                        totalRollList.append(conditionalRollList[x])
                    else:
                        totalRollList.append(rollList[x])
            else:
                totalRollList = rollList
        print("RollList: {}", rollList)
        print("ConditionalRollList: {}", conditionalRollList)
        print("TotalRollList: {}", totalRollList)

        if (dropOption):
            totalRollList.sort()
            print(totalRollList)
            for x in range(0, dropValue):
                print("value being dropped", totalRollList[x])
                totalRollList.pop(x)
            print(totalRollList)

        # log modifier
        if not (re.search(modifier, ctx.message.content)):
            print("Modifier not found, defaulting to 0")
            modifierValue = "0"
        else:
            modifierValue = re.search(modifier, ctx.message.content).group()
            print(modifierValue)
            if (modifierValue.startswith('+')):
                modifierValue = re.search(simpleRoll, modifierValue).group()
                # print(re.search(simpleRoll, modifierValue).group())
                symbol = "+"

        # calculate Total
        for x in range(len(totalRollList)):
            total += totalRollList[x]
        print (total)
        total += int(modifierValue)
        print (total)

        # print out the results
        for x in range(len(totalRollList)):
            if (conditionalOption):
                list.append("{}[{},{}]".format(totalRollList[x], rollList[x], conditionalRollList[x]))
            else:
                list = totalRollList
        await self.bot.say("{} Rolls :game_die: Total: {} :game_die: {}, {}{}"
                           .format(author, total, list, symbol, modifierValue))

    def getRoll(self, roll, rerollOption, rerollValue):
        value = randint(1, roll)
        if (rerollOption):
            while (value <= rerollValue):
                print("value:{},rerollValue:{}", value, rerollValue)
                value = randint(1, roll)
        return value


def setup(bot):
    bot.add_cog(Dice2(bot))
