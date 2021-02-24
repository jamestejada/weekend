import time
from datetime import datetime, timedelta
from modules.settings import LOCAL_PATH


class Chooser:
    """ base class for selecting which files to download from FTP
    """

    def __init__(self, 
        file_info_generator=None, which_file_set='latest', 
        local_list=None, dry_run=False):

        self.local_list = local_list
        self.dry_run = dry_run
        self.file_info_generator = file_info_generator or []
        self.which_file_set = which_file_set
        self.all_files = self._files_only_filter(self.file_info_generator)

        # time and date
        daylight_savings = time.localtime().tm_isdst
        self.mtime_offset = timedelta(hours=(7 if daylight_savings else 8))
        self.today = datetime.today()
        self.weekday = self.today.weekday()
        
        self.files_in_date_range = self.get_files_in_date_range(self.all_files)
        self.episode = self.get_episode(self.files_in_date_range)

    # main
    def files_to_get(self):
        return [
            file_name for file_name, modified_date in self.files_in_date_range
            if self._episode_check(file_name) 
            and self.is_newer(file_name, modified_date)
        ]
    
    def get_files_in_date_range(self, all_files):
        full_file_dict = self._merge_dicts(all_files)
        return [
            (file_name, modified_date) 
            for file_name, modified_date in full_file_dict.items()
            if self.date_compare(modified_date)
        ]

    def _episode_check(self, file_name):
        """ If episode strings are in the file names, this method will 
        check if the file is of the correct episode.
        """
        if self.episode:
            return (self.episode in file_name)
        return True

    def get_episode(self, file_list):
        """Returns string of desired episode number.
        """
        try:
            if file_list:
                # max() will choose the highest number episode in file_list
                episode_number = max([int(file_name.split('_')[1]) for file_name, _ in file_list])
                return str(episode_number)
        except IndexError:
            # file_name does not contain episode number
            pass
        return None
    
    def _files_only_filter(self, raw_file_info_gen):
        return [
            # {file_name: modified date}
            {file_name: info_dict.get('modify')}
            for file_name, info_dict in raw_file_info_gen
            if info_dict.get('type') == 'file'
            ]

    def _merge_dicts(self, dict_list):
        output_dict = {}
        for each_dict in dict_list:
            output_dict.update(each_dict)
        return output_dict
    
    def _get_remote_time(self, modified_date: str):
        return datetime.strptime(modified_date, '%Y%m%d%H%M%S')

    def date_compare(self, modified_date: str):
        remote_mtime = self._get_remote_time(modified_date)
        first_day, last_day = self._get_day_limit()

        return (first_day < remote_mtime <= last_day)
    
    def is_newer(self, file_name, modified_date: str, local_file_dir=LOCAL_PATH):
        local_path = local_file_dir.joinpath(file_name)
        remote_mtime = self._get_remote_time(modified_date)

        if local_path.exists():
            local_timestamp = local_path.stat().st_mtime
            local_mtime = datetime.fromtimestamp(local_timestamp) + self.mtime_offset
            if self.dry_run:
                self._debug_time(local_mtime, remote_mtime)
            return local_mtime < remote_mtime # or in desired episode
        return True

    def _debug_time(self, local_mtime, remote_mtime):
        strftime_string = '%m/%d/%y %H:%M:%S'
        local_string = local_mtime.strftime(strftime_string)
        remote_string = remote_mtime.strftime(strftime_string)
        print(
            f'{local_string} < {remote_string}: {local_mtime < remote_mtime}',
            f' | local - remote = {local_mtime-remote_mtime}'
            )

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


class Chooser_Latino_USA(Chooser):
    @property
    def first_day_offset(self):
        return timedelta(days=self.weekday + 3)


class Chooser_Reveal(Chooser):
    @property
    def first_day_offset(self):
        return timedelta(days=self.weekday + 2)
