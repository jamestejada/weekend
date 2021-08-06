from py import process
import pytest
from modules.process import Process
from modules.data import Show
from datetime import datetime, timedelta


@pytest.fixture
def test_show():
    return Show(
        show_name='Test Show',
        show_match=['test_'],
        number_of_files=3,
        remote_dir='test_',
        add_time_target=3060,
        first_day_offset_offset=1,
        air_days=[6]
    )


@pytest.fixture
def processor(test_show):
    return Process(test_show)


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


FAKE_PATHS = [
            '/fakedir/weekend/files/downloads/14161.wav',
            '/fakedir/weekend/files/downloads/35233.wav',
            '/fakedir/weekend/files/downloads/35245.wav',
            '/fakedir/weekend/files/downloads/cached_hashes.json',
            '/fakedir/weekend/files/downloads/THEMOTH_445_PROM01.wav',
            '/fakedir/weekend/files/downloads/THEMOTH_445_SGMT01.wav',
            '/fakedir/weekend/files/downloads/ThisAmer_366_PROM01.wav',
            '/fakedir/weekend/files/downloads/ThisAmer_366_PROM02.wav',
            '/fakedir/weekend/files/downloads/test_.wav',
            '/fakedir/weekend/files/downloads/test_6542.wav',
            '/fakedir/weekend/files/downloads/variable_test_.wav'
        ]


class Mock_File_Path:
    def __init__(self, path_string: str) -> None:
        self.path_string = path_string    

    @property
    def name(self):
        return self.path_string.split('/')[-1]
    
    @property
    def stem(self):
        return self.name.split('.')[0]

    def __str__(self) -> str:
        return str(self.path_string)


class Mock_Dirs:
    FAKE_PATHS = FAKE_PATHS
    def __init__(self, path_list:list=None) -> None:
        self.fake_path_strings = path_list or self.FAKE_PATHS
        self.dir_path_string = '/fakedir/weekend/files/downloads/'

    def iterdir(self):
        for each_path in self.fake_path_strings:
            yield Mock_File_Path(each_path)

    def joinpath(self, *args):
        path_list = self.dir_path_string.split('/')
        path_list = [each_path for each_path in path_list if each_path != '']
        for arg in args:
            path_list.append(arg)
        return Mock_File_Path('/' + '/'.join(path_list))


def test_Process_get_file_list_without_process_list(processor):
    expected_show_list = [show_file for show_file in Mock_Dirs().iterdir() if processor.match_show(show_file.name)]
    fake_pathlib_dir = Mock_Dirs()
    actual_show_list = processor.get_file_list(_local_path=fake_pathlib_dir)
    for fake, actual in zip(expected_show_list, actual_show_list):
        assert str(fake) == str(actual)


def test_Process_get_file_list_with_process_list(processor):
    fake_process_list = [file_path for file_path in Mock_Dirs().iterdir() if processor.match_show(file_path.name)]
    fake_pathlib_dir = Mock_Dirs()
    expected = [show_file for show_file in fake_process_list if processor.match_show(show_file.name)]
    actual = processor.get_file_list(process_list=fake_process_list, _local_path=fake_pathlib_dir)
    for actual_file, expected_file in zip(actual, expected):
        assert str(actual_file) == str(expected_file)