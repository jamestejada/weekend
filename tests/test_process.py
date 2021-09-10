from py import process
import pytest
from modules.process import Process
from modules.data import Show
from datetime import datetime, timedelta


FAKE_PATHS = [
            '/fakedir/weekend/files/downloads/14161.wav',
            '/fakedir/weekend/files/downloads/35233.wav',
            '/fakedir/weekend/files/downloads/35245.wav',
            '/fakedir/weekend/files/downloads/cached_hashes.json',
            '/fakedir/weekend/files/downloads/THEMOTH_445_PROM01.wav',
            '/fakedir/weekend/files/downloads/THEMOTH_445_SGMT01.wav',
            '/fakedir/weekend/files/downloads/ThisAmer_366_PROM01.wav',
            '/fakedir/weekend/files/downloads/ThisAmer_366_PROM02.wav',
            '/fakedir/weekend/files/downloads/test_bb32.wav',
            '/fakedir/weekend/files/downloads/test_6542.wav',
            '/fakedir/weekend/files/downloads/variable_test_.wav'
        ]

AIR_DAYS_NUMBERS = 6
MAX_SHOW_FILES = 3

@pytest.fixture
def air_day_string():
    today = datetime.today()
    return (today - timedelta(days=today.weekday()) + timedelta(days=6)).strftime('%b %-d')\


class Mock_File_Path:
    def __init__(self, path_string: str, exists:bool=True) -> None:
        self.path_string = path_string
        self._exists = exists

    @property
    def name(self):
        return self.path_string.split('/')[-1]
    
    @property
    def stem(self):
        return self.name.split('.')[0]
    
    @property
    def suffix(self):
        extension = self.name.split('.')[-1]
        return f'.{extension}'
    
    def exists(self):
        return self._exists

    def __str__(self) -> str:
        return str(self.path_string)


class Mock_Dirs:
    FAKE_PATHS = FAKE_PATHS
    def __init__(self, path_list:list=None, dir_path_string:str=None) -> None:
        self.fake_path_strings = path_list or self.FAKE_PATHS
        self.dir_path_string = dir_path_string or '/fakedir/weekend/files/downloads/'

    def iterdir(self):
        for each_path in self.fake_path_strings:
            yield Mock_File_Path(each_path)

    def joinpath(self, *args):
        path_list = self.dir_path_string.split('/')
        path_list = [each_path for each_path in path_list if each_path != '']
        for arg in args:
            path_list.append(arg)
        return Mock_File_Path('/' + '/'.join(path_list))


@pytest.fixture
def mock_dropbox_dir():
    return Mock_Dirs(dir_path_string='/fakedir/weekend/files/for_dropbox/')


@pytest.fixture
def mock_local_dir():
    return Mock_Dirs()


@pytest.fixture
def test_show():
    return Show(
        show_name='Test Show',
        show_match=['test_'],
        number_of_files=MAX_SHOW_FILES,
        remote_dir='test_',
        add_time_target=3060,
        first_day_offset_offset=1,
        air_days=[AIR_DAYS_NUMBERS],
        segment_match={
            'bb32': 'billboard',
            '_6542': 'segment_a',
            'variable_': 'segment_b'
        },
        cut_numbers={
            'billboard': '31337',
            'segment_a': '01531',
            'segment_b': '01492'
        }
    )


@pytest.fixture
def fake_process_list(mock_local_dir, test_show):
    return [
        file_path for file_path in mock_local_dir.iterdir()
        if any(
            bool(show_match_str in file_path.name) 
            for show_match_str in test_show.show_match
            )
        ]


@pytest.fixture
def processor(test_show, mock_local_dir, mock_dropbox_dir):
    return Process(
        test_show,
        _local_path=mock_local_dir, 
        _destination_path=mock_dropbox_dir
    )

@pytest.fixture
def force_processor(test_show, mock_local_dir, mock_dropbox_dir):
    return Process(
        test_show,
        _local_path=mock_local_dir, 
        _destination_path=mock_dropbox_dir,
        force=True
    )

@pytest.fixture
def process_list_processor(test_show, mock_local_dir, mock_dropbox_dir, fake_process_list):
    return Process(
        test_show,
        process_list=fake_process_list,
        _local_path=mock_local_dir, 
        _destination_path=mock_dropbox_dir
    )


@pytest.mark.parametrize('air_weekday_list', [[5,6], [6,7], [6], [7]])
def test_Process_get_days_string(processor, air_weekday_list):
    today = datetime.today()
    expected_string = ' and '.join(
        [
            (
                today - timedelta(days=today.weekday()) + timedelta(days=day)
            ).strftime('%b %-d')
            for day in air_weekday_list
        ]
    )
    assert expected_string == processor.get_days_string(air_weekday_list)


@pytest.mark.parametrize('file_name', ['test_', 'test_6542', 'variable_test_'])
def test_Process_match_show_true(processor, file_name):
    assert processor.match_show(file_name)


@pytest.mark.parametrize('file_name', ['not_a_match', 'neither_this', 'nor_that'])
def test_Process_match_show_false(processor, file_name):
    assert not processor.match_show(file_name)


def test_Process_get_file_list_without_process_list(processor, mock_local_dir):
    expected_show_list = [show_file for show_file in mock_local_dir.iterdir() if processor.match_show(show_file.name)]
    actual_show_list = processor.get_file_list()
    for fake, actual in zip(expected_show_list, actual_show_list):
        assert str(fake) == str(actual)


def test_Process_get_file_list_with_process_list(processor, fake_process_list):
    expected = [show_file for show_file in fake_process_list if processor.match_show(show_file.name)]
    actual = processor.get_file_list(process_list=fake_process_list)
    for actual_file, expected_file in zip(actual, expected):
        assert str(actual_file) == str(expected_file)


def test_Process_get_source_paths(processor):
    expected = {
            'billboard': Mock_File_Path('/fakedir/weekend/files/downloads/test_bb32.wav'),
            'segment_a': Mock_File_Path('/fakedir/weekend/files/downloads/test_6542.wav'),
            'segment_b': Mock_File_Path('/fakedir/weekend/files/downloads/variable_test_.wav')
    }
    actual = processor.get_source_paths()
    assert actual.keys() == expected.keys()
    for key in expected.keys():
        assert str(actual.get(key)) == str(expected.get(key))


def test_Process_get_destination_paths(processor, air_day_string):

    expected = {
            'billboard': Mock_File_Path(f'/fakedir/weekend/files/for_dropbox/31337_Test Show BILLBOARD {air_day_string}.wav'),
            'segment_a': Mock_File_Path(f'/fakedir/weekend/files/for_dropbox/01531_Test Show SEGMENT A {air_day_string}.wav'),
            'segment_b': Mock_File_Path(f'/fakedir/weekend/files/for_dropbox/01492_Test Show SEGMENT B {air_day_string}.wav')
    }
    actual = processor.get_destination_paths()
    assert actual.keys() == expected.keys()
    for key in expected.keys():
        assert str(actual.get(key)) == str(expected.get(key))


def test_Process_check_number_of_files(processor):
    assert processor._check_number_of_files(FAKE_PATHS) == []
    correct_length_list = [x for x in range(MAX_SHOW_FILES)]
    assert processor._check_number_of_files(correct_length_list) == correct_length_list


def test_Process_should_skip_true(processor):
    fake_file_path = Mock_File_Path('/fakedir/weekend/files/downloads/variable_test_.wav')
    assert processor._should_skip(fake_file_path)

def test_Process_should_skip_false(force_processor, process_list_processor):
    fake_file_path = Mock_File_Path('/fakedir/weekend/files/downloads/variable_test_.wav')
    assert not force_processor._should_skip(fake_file_path)
    assert not process_list_processor._should_skip(fake_file_path)
