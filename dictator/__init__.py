from otree.api import *

doc = """
One player decides how to divide a certain amount between himself and the other
player. Then players at random swap their roles.
Of interest is the behaviour of player who was dictator and became receiver, etc.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.
"""

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    import random
    for p in subsession.get_players():
        p.value = random.randint(0, 100)

class C(BaseConstants):
    NAME_IN_URL = 'dictatorNS'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 2
    # Initial amount allocated to the dictator
    ENDOWMENT = cu(100)


# class C(BaseConstants):
#     NAME_IN_URL = 'public_goods_simple'
#     PLAYERS_PER_GROUP = 4
#     NUM_ROUNDS = 1
#     ENDOWMENT = 100
#     MULTIPLIER = 2


# class Subsession(BaseSubsession):
#     pass


def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    print('in group_by_arrival_time_method')
    players_byexample = [p for p in waiting_players if p.participant.treatment == 'byexample']
    players_else = [p for p in waiting_players if p.participant.treatment == 'else']

    for p in waiting_players:
        if len(players_byexample) >= 4:
            print('about to create a group')
            return [players_byexample[0], players_byexample[1], players_byexample[2], players_byexample[3]]

        elif len(players_else) >= 4:
            print('about to create a group')
            return [players_else[0], players_else[1], players_else[2], players_else[3]]

        else:
            print('not enough players yet to create a group')


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    number_of_leaders = models.IntegerField()
    recom = models.IntegerField(blank=True)
    expl = models.LongStringField()
    contr = models.IntegerField(blank=True)
    smb_dropedout = models.BooleanField(initial=False)


def is_dropout(group: Group):
    for p in group.get_players():
        if p.is_dropout == True:
            group.smb_dropedout = True


def set_payoffs(group: Group):
    for p in group.get_players():
        if group.smb_dropedout == True:
            p.individual_payoff = 200
            p.group.total_contribution = 0
        else:
            contributions = [p.contribution for p in group.get_players()]
            group.total_contribution = sum(contributions)
            p.individual_payoff = (C.ENDOWMENT - p.contribution + group.total_contribution / 2)


def set_leader(group: Group):
    for p in group.get_players():
        p.chosen_role = p.participant.chosen_role
    players = group.get_players()
    player_yes = [p for p in players if p.chosen_role == 1]
    roles = [p.chosen_role for p in players]
    group.number_of_leaders = sum(roles)
    import random
    if group.number_of_leaders >= 1:
        leader = random.choice(player_yes)
        leader.is_leader = True
    elif group.number_of_leaders < 1:
        leader_by_chance = random.choice(players)
        leader_by_chance.is_leader = True


def recom_function(group: Group):
    session = group.session
    subsession = group.subsession
    for g in subsession.get_groups():
        for p in group.get_players():
            recommendation = p.field_maybe_none('recommendation')
            recommendation = p.participant.recommendation
            if p.is_leader == True:
                recommen = g.field_maybe_none('recom')
                recommen = recommendation


def expl_function(group: Group):
    session = group.session
    subsession = group.subsession
    for g in subsession.get_groups():
        for p in group.get_players():
            p.explanation = p.participant.explanationсв
            if p.is_leader == True:
                g.expl = p.explanation


def contr_function(group: Group):
    session = group.session
    subsession = group.subsession
    for g in subsession.get_groups():
        for p in group.get_players():
            p.contribution_leader = p.participant.contribution_leader
            if p.is_leader == True:
                g.contr = p.contribution_leader


def participant_function(group: Group):
    for p in group.get_players():
        contribution = p.field_maybe_none('contribution')
        if contribution is None:
            contribution = p.participant.contribution_leader
        p.participant.contribution = contribution
        p.participant.individual_payoff = p.individual_payoff
        p.participant.total_contribution = p.group.total_contribution


class Group(BaseGroup):
    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        max=C.ENDOWMENT,
        label="I will keep",
    )


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = C.ENDOWMENT - group.kept


# PAGES
class Introduction(Page):
    pass


class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(offer=C.ENDOWMENT - group.kept)


page_sequence = [Introduction, Offer, ResultsWaitPage, Results]
