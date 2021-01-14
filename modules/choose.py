from datetime import datetime, timedelta

class Chooser:
    """ Base class for selecting which files to download from FTP
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

    def files_to_get(self, files_only_list=None):
        files_only = files_only_list or self.all_files
        full_file_dict = self._merge_dicts(files_only)

        sunday = self._get_day_limit()
        saturday = sunday + timedelta(weeks=1)

        return [
            (file_name, modified_date) for file_name, modified_date in full_file_dict.items()
            if (sunday < datetime.strptime(modified_date, '%Y%m%d%H%M%S') < saturday)
            ]

    def _get_day_limit(self, which_file_set=None):
        # have to change this when we go to specific dates.

        this_week = self.today - timedelta(days=self.weekday)
        last_week = self.today - timedelta(days=(7 + self.weekday))

        return {
            'latest': this_week,
            'old': last_week
        }.get(which_file_set or self.which_file_set)
