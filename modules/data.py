from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Show:
    show_name: str
    number_of_files: int
    remote_dir: str = None
    add_time_target: int = None
    first_day_offset_offset: int = 1
    show_match: List[str] = field(default_factory=list)
    air_days: List[int] = field(default_factory=list)
    segment_match: dict = field(default_factory=dict)
    cut_numbers: dict = field(default_factory=dict)
    timings: dict = field(default_factory=dict)
    add: List[str] = field(default_factory=list)

    def as_dict(self):
        return asdict(self)


REVEAL = Show(
    show_name='Reveal',
    first_day_offset_offset=2,
    number_of_files=9,
    show_match=['RevealWk_'],
    remote_dir='RevealWk',
    air_days=[4],
    segment_match={
        'PROM01': 'promo',
        'SGMT01': 'billboard',
        'SGMT03': 'segment_a',
        'SGMT05': 'segment_b',
        'SGMT07': 'segment_c',
        'SGMT04': 'music_bed_a',
        'SGMT06': 'music_bed_b',
        'SGMT02': 'music_bed_C'
    },
    cut_numbers={
        'promo': '17984',
        'billboard': '17978',
        'segment_a': '17979',
        'segment_b': '17981',
        'segment_c': '17983',
        'music_bed_a': '17980',
        'music_bed_b': '17982'
        # 'music_bed_c': 'NOT USED'
    },
    timings={
        '17984': 30,
        '17978': 60,
        '17980': 60,
        '17982': 60
    },
    add_time_target=3060,
    add=[
        '17979',
        '17981',
        '17983'
    ]
)

LATINO_USA = Show(
    show_name='Latino USA',
    first_day_offset_offset=3,
    remote_dir='LatinoUS',
    number_of_files=9,
    show_match=[str(num) for num in range(35232, 35249)],
    air_days=[6],
    segment_match={
        '35232': 'promo',
        '35242': 'billboard',
        '35244': 'segment_a',
        '35246': 'segment_b',
        '35248': 'segment_c',
        '35243': 'music_bed_a',
        '35245': 'music_bed_b',
        '35247': 'music_bed_c'
    },
    cut_numbers={
        'promo': '75292',
        'billboard': '17030',
        'segment_a': '17032',
        'segment_b': '17034',
        'segment_c': '17036',
        'music_bed_a': '17031',
        'music_bed_b': '17033',
        'music_bed_c': '17035'
    },
    timings={
        '75292': 30,
        '17030': 60,
        '17031': 30,
        '17033': 60,
        '17035': 60
    },
    add_time_target=3030,
    add=[
        '17032',
        '17034',
        '17036'
    ]
)

SAYS_YOU = Show(
    show_name='Says You',
    number_of_files=6,
    remote_dir='SaysYou1',
    show_match=['SaysYou1_'],
    air_days=[6],
    segment_match={
        'PROM01': 'promo',
        'SGMT01': 'billboard',
        'SGMT02': 'segment_a',
        'SGMT03': 'segment_b',
        'SGMT04': 'segment_c',
    },
    cut_numbers={
        'promo': '27305',
        'billboard': '27300',
        'segment_a': '27301',
        'segment_b': '27302',
        'segment_c': '27303'      
    },
    timings={
        '27305': 30,
        '27300': 60
    },
    add_time_target=3000,
    add=[
        '27301',
        '27302',
        '27303'
    ]

)

THE_MOTH = Show(
    show_name='The Moth',
    remote_dir='THEMOTH',
    show_match=['THEMOTH_'],
    number_of_files=7,
    air_days=[6],
    segment_match={
        'PROM01': 'promo',
        'SGMT01': 'billboard',
        'SGMT02': 'segment_a',
        'SGMT04': 'segment_b',
        'SGMT06': 'segment_c',
        'SGMT03': 'music_bed_a',
        'SGMT05': 'music_bed_b'
    },
    cut_numbers={
        'promo': '14172',
        'billboard': '14166',
        'segment_a': '14167',
        'segment_b': '14169',
        'segment_c': '14171',
        'music_bed_a': '14168',
        'music_bed_b': '14170'
    },
    timings={
        '14172': 30,
        '14166': 60,
        '14168': 60,
        '14170': 60
    },
    add_time_target=3060,
    add=[
        '14167',
        '14169',
        '14171'        
    ]
)

SNAP_JUDGMENT = Show(
    show_name='Snap Judgment',
    remote_dir='SnapJudg',
    show_match=[str(num) for num in range(14155, 14162)],
    number_of_files=7,
    air_days=[6],
    segment_match={
        '14161': 'promo',
        '14155': 'billboard',
        '14156': 'segment_a',
        '14158': 'segment_b',
        '14160': 'segment_c',
        '14157': 'music_bed_a',
        '14159': 'music_bed_b'
    },
    cut_numbers={
        'promo': '14161',
        'billboard': '14155',
        'segment_a': '14156',
        'segment_b': '14158',
        'segment_c': '14160',
        'music_bed_a': '14157',
        'music_bed_b': '14159'
    },
    timings={
        '14161': 30,
        '14155': 60,
        '14157': 90,
        '14159': 90
    },
    add_time_target=3000,
    add=[
        '14156',
        '14158',
        '14160'
    ]
)

THIS_AMERICAN_LIFE = Show(
    show_name='This American Life',
    remote_dir='ThisAmer',
    number_of_files=5,
    add_time_target=3480,
    first_day_offset_offset=2,
    show_match=['ThisAmer_'],
    air_days=[5,6],
    segment_match={
        'PROM01': 'promo',
        'PROM02': 'promo_today',
        'SGMT01': 'segment_a',
        'SGMT03': 'segment_b',
        'SGMT02': 'music_bed_a'
    },
    cut_numbers={
        'promo': '25321',
        'segment_a': '17040',
        'segment_b': '17042',
        'music_bed_a': '17041'
    },
    timings={
        '25321': 30,
        '17041': 60
    },
    add=[
        '17040',
        '17042'
    ]

)

# Satellite
ITS_BEEN_A_MINUTE = Show(
    show_name='It\'s Been a Minute',
    show_match=['ItsBeen1_'],
    number_of_files=1,
    air_days=[5],
    segment_match={'SGMT01': 'promo'},
    cut_numbers={'promo': '17790'}
)

ASK_ME_ANOTHER = Show(
    show_name='Ask Me Another',
    show_match=['AskMeA1_'],
    number_of_files=1,
    air_days=[6],
    segment_match={'SGMT01': 'promo'},
    cut_numbers={'promo': '17020'}
)

HIDDEN_BRAIN = Show(
    show_name='Hidden Brain',
    show_match=['HiddenB1_'],
    number_of_files=1,
    air_days=[6],
    segment_match={'SGMT01': 'promo'},
    cut_numbers={'promo': '18120'}
)

WAIT_WAIT = Show(
    show_name='Wait Wait... Don\'t Tell Me!',
    show_match=['WaitWa2_'],
    number_of_files=2,
    air_days=[5, 6],
    segment_match={'SGMT02': 'promo'},
    cut_numbers={'promo': '25366'}
)

WESUN = Show(
    show_name='Weekend Edition Sunday',
    show_match=['Weeken20_'],
    number_of_files=1,
    air_days=[6],
    segment_match={'SGMT01': 'promo'},
    cut_numbers={'promo': '25389'}
)

DATA_LIST = [REVEAL, LATINO_USA, SAYS_YOU, SNAP_JUDGMENT, THE_MOTH, THIS_AMERICAN_LIFE]
SATELLITE_DATA_LIST = [ITS_BEEN_A_MINUTE, ASK_ME_ANOTHER, HIDDEN_BRAIN, WAIT_WAIT, WESUN]
