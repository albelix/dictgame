from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'public_goods_pun'
    PLAYERS_PER_GROUP = 3
    NUM_OTHERS_PER_GROUP = PLAYERS_PER_GROUP - 1
    INSTRUCTIONS_TEMPLATE = 'public_goods_pun/Instructions.html'
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    MULTIPLIER = 1.8
    ENDOWMENT = 20
    EFFICIENCY_FACTOR = 1.6
    PUNISHMENT_ENDOWMENT = 10
    PUNISHMENT_FACTOR = 3

class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="How much will you contribute?"
    )


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
        group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )
    for p in players:
        p.payoff = C.ENDOWMENT - p.contribution + group.individual_share


# from otree.api import (
#     models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
#     Currency as c, currency_range
# )

#from django.db import models as djmodels

# author = "Philip Chapkovski, chapkovski@gmail.com"

# doc = """
# Public Good Game with Punishment (Fehr and Gaechter).
# Fehr, E. and Gachter, S., 2000.
#  Cooperation and punishment in public goods experiments. American Economic Review, 90(4), pp.980-994.
# """


class Constants(BaseConstants):
    name_in_url = 'pggfg'
    players_per_group = 3
    num_others_per_group = players_per_group - 1
    num_rounds = 20
    instructions_template = 'pggfg/Instructions.html'
    endowment = 20
    efficiency_factor = 1.6
    punishment_endowment = 10
    punishment_factor = 3


from django.db.models import Q, F


class Subsession(BaseSubsession):
    def creating_session(self):
        ps = []
        for p in self.get_players():
            for o in p.get_others_in_group():
                ps.append(Punishment(sender=p, receiver=o, ))
        Punishment.objects.bulk_create(ps)


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    average_contribution = models.FloatField()
    individual_share = models.CurrencyField()

    def set_pd_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.average_contribution = self.total_contribution / Constants.players_per_group
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.pd_payoff = sum([+ Constants.endowment,
                               - p.contribution,
                               + self.individual_share,
                               ])
            p.set_punishment_endowment()

    def set_punishments(self):
        for p in self.get_players():
            p.set_punishment()
        for p in self.get_players():
            p.set_payoff()


class Player(BasePlayer):
    contribution = models.PositiveIntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
        label="How much will you contribute to the project (from 0 to {})?".format(Constants.endowment)
    )
    punishment_sent = models.IntegerField()
    punishment_received = models.IntegerField()
    pd_payoff = models.CurrencyField(doc='to store payoff from contribution stage')
    punishment_endowment = models.IntegerField(initial=0, doc='punishment endowment')

    def set_payoff(self):
        self.payoff = self.pd_payoff - self.punishment_sent - self.punishment_received

    def set_punishment_endowment(self):
        assert self.pd_payoff is not None, 'You have to set pd_payoff before setting punishment endowment'
        self.punishment_endowment = min(self.pd_payoff, Constants.punishment_endowment)

    def set_punishment(self):
        self.punishment_sent = sum([i.amount for i in self.punishments_sent.all()])
        self.punishment_received = sum(
            [i.amount for i in self.punishments_received.all()]) * Constants.punishment_factor


class Punishment(djmodels.Model):
    sender = djmodels.ForeignKey(to=Player, related_name='punishments_sent', on_delete=djmodels.CASCADE)
    receiver = djmodels.ForeignKey(to=Player, related_name='punishments_received', on_delete=djmodels.CASCADE)
    amount = models.IntegerField(min=0)



# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


page_sequence = [Contribute, ResultsWaitPage, Results]
