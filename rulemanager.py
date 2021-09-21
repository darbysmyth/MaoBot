import json
import random as r

# rules.json just stores the base rules for the game as well as a spot for new rules to be added
# and is loaded each time a new game is started to redeclare the RULES variable in this file
# all rules are wiped from the previous game except for the base rules

# as of now the rule manager only handles rules relating to playing cards
# rules like "no asking questions" "saying 'POI' to talk" "no saying 'MAO'" etc will be handled separately
# in the @bot.event on_message event handler
with open("rules.json") as f:
    RULES = json.load(f)


class RuleManager():

    def givecard(self, ctx, deck, gm):
        player_name = str(ctx.author).split("#")[0]
        drawn_card = r.choice(deck)
        deck.remove(drawn_card)
        gm.players[player_name]["hand"].append(drawn_card)

    def checkbaserules(self, playedcard):
        try:
            #check rules for input card by searching rule dictionary
            pass
        except IndexError:
            # if there is no rule for that card, ignore
            pass
        pass