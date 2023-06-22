from otree.api import *



class C(BaseConstants):
    NAME_IN_URL = 'public_goods_threshold'
    PLAYERS_PER_GROUP = 7
    NUM_ROUNDS = 8
    ENDOWMENT = cu(100)
    LOSS = 0.75
    KEPT = 0.25
    THRESHOLD = cu(3200)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    round_num = models.IntegerField()
    current_share = models.FloatField()
    global_contribution = models.CurrencyField()
#    success = models.BooleanField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="Сколько очков Вы готовы внести на общий счет?")
#    payoff = models.CurrencyField()
    my_contribution = models.CurrencyField(doc="""The amount contributed by the player""", )
    my_payoff = models.CurrencyField()
    my_cut_payoff = models.CurrencyField()

# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    group.total_contribution = sum([p.contribution for p in players])
    group.global_contribution = sum([sum([pp.contribution for pp in p.in_all_rounds()]) for p in players])
#    sum([sum([p.payoff for p in pp.in_all_rounds()]) for pp in allplayers])
    group.current_share = int(float(group.global_contribution*100/C.THRESHOLD))

    for p in players:
        p.payoff = C.ENDOWMENT - p.contribution
        p.my_contribution = sum([pp.contribution for pp in p.in_all_rounds()])
        p.my_payoff = sum([pp.payoff for pp in p.in_all_rounds()])
        p.my_cut_payoff = p.my_payoff * C.KEPT

    #individual_share = sum(contributions)
    # group.individual_share = (
    #     group.total_contribution * C.EFFICIENCY_FACTOR / C.PLAYERS_PER_GROUP
    # )
    # for p in players:
    #     p.payoff = C.ENDOWMENT - p.contribution + group.individual_share
#        total_payoff = sum([sum([p.payoff for p in pp.in_all_rounds()]) for pp in allplayers])

        # p.my_payoff = sum([p.payoff for p in players.in_all_rounds()])

# def my_method(player: Player):
#     # players = player.group.get_players()
#     my_contribution = sum([p.contribution for p in player.in_all_rounds()])
#     my_payoff = sum([p.payoff for p in player.in_all_rounds()])

# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    # after_all_players_arrive = [my_method]

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(others=player.get_others_in_group())


class ResultsSummary(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    def vars_for_template(player: Player):
        return {
            'total_payoff_full': sum(
                [p.payoff for p in player.in_all_rounds()]),
            'total_payoff_cut':  sum(
                [p.payoff for p in player.in_all_rounds()])*C.KEPT,
            'player_in_all_rounds': player.in_all_rounds(),
        }


page_sequence = [Contribute, ResultsWaitPage, Results, ResultsSummary]
