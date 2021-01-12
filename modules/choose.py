from datetime import datetime, timedelta

class Chooser:
    """ Base class for selecting which files to download from FTP
    """

    def __init__(self, file_info_generator, which_file_set='latest'):
        self.file_info_generator = file_info_generator
        self.which_file_set = which_file_set
        self.all_files = self._files_only_filter(self.file_info_generator)
    
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

        # !!!:  change to specific date logic with function
        #       that calculates dates when 
        start_limit, end_limit = self._get_timedelta_tuple()
        lower_limit = timedelta(weeks=start_limit)
        upper_limit = timedelta(weeks=end_limit)

        today = datetime.today()

        return [
            (file_name, modified_date) for file_name, modified_date in full_file_dict.items()
            if (lower_limit < (today - datetime.strptime(modified_date, '%Y%m%d%H%M%S')) < upper_limit)
            ]
    
    
    def _get_timedelta_tuple(self, which_file_set=None):
        return {
            'latest': (0, 1),
            'old': (1, 3)
        }.get(which_file_set or self.which_file_set)
