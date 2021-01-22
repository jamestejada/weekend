from datetime import datetime, timedelta


class Chooser:
    """ class for selecting which files to download from FTP
    """

    def __init__(self, file_info_generator, which_file_set='latest'):
        self.file_info_generator = file_info_generator
        self.which_file_set = which_file_set
        self.all_files = self._files_only_filter(self.file_info_generator)
        self.today = datetime.today()
        self.weekday = self.today.weekday()
    
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

    def files_to_get(self):
        files_only = self.all_files
        full_file_dict = self._merge_dicts(files_only)

        sunday = self._get_day_limit()
        saturday = sunday + timedelta(weeks=1)

        return [
            file_name for file_name, modified_date in full_file_dict.items()
            if (sunday < datetime.strptime(modified_date, '%Y%m%d%H%M%S') < saturday)
            ]

    def _get_day_limit(self, which_file_set=None):
        this_week = self.today - timedelta(days=self.weekday + 1)
        last_week = self.today - timedelta(days=(8 + self.weekday))

        return {
            'latest': this_week,
            'old': last_week
        }.get(which_file_set or self.which_file_set)


class Chooser_Snap_Judgment(Chooser):
    # override
    def files_to_get(self):
        files_only = self.all_files
        full_file_dict = self._merge_dicts(files_only)
        return [file_name for file_name in full_file_dict.keys()]

class Chooser_TAL(Chooser):
    # override
    def _get_day_limit(self, which_file_set=None):
        return self.today - timedelta(days=self.weekday + 2)


CHOOSE_CLASS = {
    # Matches classes with ftp directory
    'LatinoUS': Chooser,
    'RevealWk': Chooser,
    'SaysYou1': Chooser,
    'SnapJudg': Chooser_Snap_Judgment,
    'THEMOTH': Chooser,
    'ThisAmer': Chooser_TAL
}

NOT_LATEST = ['RevealWk']


def choose_files(ftp_dir, file_info_generator):
    which_file_set = 'old' if ftp_dir in NOT_LATEST else 'latest'

    chooser = CHOOSE_CLASS.get(ftp_dir)(file_info_generator, which_file_set=which_file_set)
    return chooser.files_to_get()
