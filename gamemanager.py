import random as r
from player import Player
from rulemanager import RuleManager

# can add functions that use the same methods and stuff from the discord class
# without importing the discord class

DECK = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS',
        'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC',
        'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH',
        'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD',
        'JOK', 'JOK',
        'HOWTO', 'HOWTO']
RM = RuleManager()


class GameManager:

    def __init__(self):
        self.cur_card = None
        self.players = {}
        self.cur_turn = ""
        self.turnorder = []
        self.turndir = "R"

    def nextplayer(self, skipamount):
        if self.turndir == "R":
            next_player_index = self.turnorder.index(self.cur_turn) + skipamount
            print(next_player_index)
            try:
                self.cur_turn = self.turnorder[next_player_index]
            except IndexError:
                self.cur_turn = self.turnorder[0]
        else:
            next_player_index = self.turnorder.index(self.cur_turn) - skipamount
            self.cur_turn = self.turnorder[next_player_index]

    async def deal(self, bot, ctx, args):
        global DECK
        for player in args:
            user_id = int("".join([i for i in player if i.isdigit()]))
            user = bot.get_user(user_id)
            player_name = user.name
            self.turnorder.append(player_name)
            self.players[player_name] = {}
            self.players[player_name]["hand"] = []
            self.players[player_name]["id"] = user_id
            for i in range(7):
                card = r.choice(DECK)
                DECK.remove(card)
                self.players[player_name]["hand"].append(card)
            await user.send(f"``` Here is your hand\n"
                            " Don't Touch!\n"
                            f"{self.players[player_name]['hand']}```")
        self.cur_card = r.choice(DECK)
        await ctx.send(f"current card: {self.cur_card}\nFirst up is {args[0]}")
        self.cur_turn = self.turnorder[0]
        print(DECK)

    async def play(self, ctx, args):
        played_card = args[0]
        player_name = str(ctx.author).split("#")[0]
        if played_card[0] == self.cur_card[0] or played_card[1] == self.cur_card[1] \
                or self.cur_card == "JOK" or self.cur_card == "HOWTO" \
                or played_card == "JOK" or played_card == "HOWTO":
            self.cur_card = played_card
            for player in self.players:
                if player == player_name:
                    if played_card not in self.players[player]["hand"]:
                        await ctx.author.send("You don't have that card\ntry again")
                        return
                    self.players[player]["hand"].remove(played_card)
                    await ctx.author.send(f"{self.players[player]['hand']}")
                    await ctx.send(f"current card: {self.cur_card}")
                    self.nextplayer(1)
                    if len(self.players[player]["hand"]) == 0:
                        ctx.send(f"Congrats <@!{self.players[player]['id']}>! you have won the game!")
        else:
            await ctx.author.send("Invalid play")

    async def draw(self, ctx):
        RM.givecard(ctx, DECK, self)

    async def showhand(self, ctx):
        player_name = str(ctx.author.name)
        await ctx.author.send(self.players[player_name]["hand"])
        print(DECK)
