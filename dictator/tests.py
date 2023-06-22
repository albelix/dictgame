from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random


class PlayerBot(Bot):
    def play_round(self):
        yield Introduction

        if self.player.id_in_group == 1:
            val=random.randint(0,100)
            yield Offer, dict(kept=cu(val))
#            expect(self.player.payoff, cu(val))
        else:
            pass #expect(self.player.payoff, cu(1))

        if self.player.round_number == 2 & self.player.id_in_group == 1:
            val2=random.randint(0,100)-random.lognormvariate(val,0.5)
            yield Offer, dict(kept=cu(val2))
        else:
            pass
        yield Results

