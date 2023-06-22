# models.py
# import random
# from otree.api import models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer
# import extends as extends
from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'dictCG'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    # Initial amount allocated to each player
    ENDOWMENT = cu(100)


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
           self.group_randomly()
        else:
           self.group_like_round(1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.CurrencyField()


# templates.py


# pages.py
# from otree.api import Currency as c, currency_range
# from . import models
# from ._builtin import Page, WaitPage
# from .models import Constants


class Introduction(Page):
    pass



class Decision(Page):
    form_model = 'group'
    form_fields = ['keep']

    # only show the page to the first player in the group
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


# wait page so both players can catch up
class ResultsWaitPage(WaitPage):
    pass

    # when both get here
    @staticmethod
    def after_all_players_arrive(group: Group):
        # grab the first player, payoff is what they kept for themselves
        group.get_player_by_id(1).payoff = group.keep
        # grab the second player, payoff is the part of the budget the other one didn't keep
        group.get_player_by_id(2).payoff = C.BUDGET - group.keep


class Results(Page):
    pass






class Round1(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'ENDOWMENT': self.session.config['ENDOWMENT']}

    form_model = 'player'
    form_fields = ['transfer']

    def before_next_page(self):
        if self.round_number == 1:
            players = self.group.get_players()
            for p in players:
                p.role = 'Dictator' if self.random.randint(0, 1) == 0 else 'Receiver'
                p.participant.vars['role'] = p.role



class Round2(Page):
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        prev_round = self.player.in_round(self.round_number - 1)
        return {'prev_round': prev_round}

    def byefore_next_page(self):
        if self.round_number == 2:
            prev_round = self.player.in_round(self.round_number - 1)
            prev_player = prev_round.get_others_in_group()[0]
            self.player.payoff = prev_player.endowment


class Results(Page):
    def is_displayed(self):
       return self.round_number == C.NUM_ROUNDS


page_sequence = [
    Introduction,
    Round1,
    Round2,
    Results,
]
