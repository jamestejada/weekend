from modules.settings import FFA_PATH, DROPBOX_PATH, FOR_FFA, FOR_DROPBOX
from modules.choose import Chooser
import shutil
from datetime import datetime, timedelta


def copy_all():
    for each_file in FOR_FFA.iterdir():
        modified_date = each_file.stat().st_mtime
        modified_date_str = datetime.fromtimestamp(modified_date).strftime('%Y%m%d%H%M%S')
        static_chooser = Chooser()
        should_upload = static_chooser.date_compare(
                    modified_date_str
                ) and static_chooser.is_newer(
                    each_file.name,
                    modified_date_str,
                    local_file_dir=FFA_PATH
                )
        
        if should_upload and each_file.suffix in ['.mp3', '.wav']:
            print(f'Copying {each_file.name} from {each_file.parent.stem} to FFA')
            shutil.copyfile(
                str(each_file),
                str(FFA_PATH.joinpath(each_file.name))
            )

    for each_file in FOR_DROPBOX.iterdir():
        modified_date = datetime.fromtimestamp(each_file.stat().st_mtime)
        now = datetime.now()
        thirty_minutes = timedelta(minutes=30)

        should_upload = all([
            ((now - modified_date) < thirty_minutes),
            each_file.suffix in ['.mp3', '.wav'],
            ])

        if should_upload:
            print(f'Copying {each_file.name} from {each_file.parent.stem} to DROPBOX')
            shutil.copyfile(
                str(each_file),
                str(DROPBOX_PATH.joinpath(each_file.name))
            )




