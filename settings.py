from os import environ


SESSION_CONFIGS = [
    # dict(
    #     name='dictator',
    #     display_name="dictator",
    #     app_sequence=['dictator'],
    #     num_demo_participants=4,
    # ),
    dict(
        name='public_goods_simple',
        display_name="public_goods_simple",
        app_sequence=['public_goods_simple'],
        num_demo_participants=7,
    ),
    dict(
        name='public_goods_threshold',
        display_name="public_goods_threshold",
        app_sequence=['public_goods_simple','public_goods_threshold'],
        num_demo_participants=7,
    ),
    # dict(
    #     name='dictCG',
    #     display_name="dictCG",
    #     app_sequence=['dictCG'],
    #     num_demo_participants=4,
    # ),
    dict(
        name='guess_two_thirds',
        display_name="Guess 2/3 of the Average",
        app_sequence=['guess_two_thirds', 'payment_info'],
        num_demo_participants=3,
    ),
    dict(
        name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    ),
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ru'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(
        name='live_demo',
        display_name='Room for live demo (no participant labels)'),
    dict(
        name='7players',
        display_name='We are 7',
        participant_label_file='_rooms/PlayerList7.txt',
    ),

]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '1183708141756'

INSTALLED_APPS = ['otree']
