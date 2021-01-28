from datetime import datetime, timedelta
from modules.settings import LOCAL_PATH, FOR_DROPBOX, FOR_FFA
from modules.process import Reveal

class Chooser:
    """ base class for selecting which files to download from FTP
    """
    def __init__(self, file_info_generator, which_file_set='latest', dry_run=False):
        self.file_info_generator = file_info_generator
        self.which_file_set = which_file_set
        self.all_files = self._files_only_filter(self.file_info_generator)
        self.today = datetime.today()
        self.weekday = self.today.weekday()

        self.dry_run = dry_run

    def files_to_get(self):
        files_only = self.all_files
        full_file_dict = self._merge_dicts(files_only)

        return [
            file_name for file_name, modified_date in full_file_dict.items()
            if self.date_compare(file_name, modified_date)
            ]
    
    def _files_only_filter(self, raw_file_info_gen):
        return [
            {file_name: info_dict.get('modify')}
            for file_name, info_dict in raw_file_info_gen
            if info_dict.get('type') == 'file'
            ]

    def _merge_dicts(self, dict_list):
        output_dict = {}
        for each_dict in dict_list:
            output_dict.update(each_dict)
        return output_dict

    def date_compare(self, file_name, modified_date: str):
        local_path = LOCAL_PATH.joinpath(file_name)

        remote_mtime = datetime.strptime(modified_date, '%Y%m%d%H%M%S')
        first_day, last_day = self._get_day_limit()

        if first_day < remote_mtime <= last_day:
            if local_path.exists():
                local_mtime = datetime.fromtimestamp(local_path.stat().st_mtime)
                return local_mtime < remote_mtime
            return True


    def _get_day_limit(self):

        week_offset_days = 7 if self.which_file_set == 'old' else 0
        week_offset = timedelta(days=week_offset_days)

        first_day = self.today - self.first_day_offset - week_offset
        last_day =  self.today + self.last_day_offset - week_offset

        return (first_day, last_day)

    @property
    def first_day_offset(self):
        return timedelta(days=self.weekday + 1)
    
    @property
    def last_day_offset(self):
        return timedelta(days=5 - self.weekday)


class Chooser_Snap_Judgment(Chooser):
    # override
    @property
    def first_day_offset(self):
        return timedelta(days=self.weekday + 3)


class Chooser_TAL(Chooser):
    # override
    @property
    def first_day_offset(self):
        # This gets Promos uploaded Saturday Evening.
        return timedelta(days=self.weekday + 2)


# class Chooser_Latino_USA(Chooser):
#     # override
#     @property
#     def first_day_offset(self):
#         return timedelta(days=self.weekday + 2)


CHOOSE_CLASS = {
    # Matches classes with ftp directory
    'LatinoUS': Chooser,
    'RevealWk': Chooser,
    'SaysYou1': Chooser,
    'SnapJudg': Chooser_Snap_Judgment,
    'THEMOTH': Chooser,
    'ThisAmer': Chooser_TAL
}

NOT_LATEST = ['RevealWk', 'THEMOTH']


def choose_files(ftp_dir, file_info_generator):
    if ftp_dir not in CHOOSE_CLASS.keys():
        return
    which_file_set = 'old' if ftp_dir in NOT_LATEST else 'latest'

    chooser = CHOOSE_CLASS.get(ftp_dir)(file_info_generator, which_file_set=which_file_set)
    return chooser.files_to_get()
