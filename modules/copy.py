from modules.settings import FFA_PATH, DROPBOX_PATH, FOR_FFA, FOR_DROPBOX
from modules.choose import Chooser
import shutil
from datetime import datetime, timedelta


def copy_all():
    for each_file in FOR_FFA.iterdir():
        modified_date = each_file.stat().st_mtime
        should_upload = Chooser().date_compare(
            each_file.name, 
            datetime.fromtimestamp(modified_date).strftime('%Y%m%d%H%M%S'),
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
        one_hour = timedelta(hours=1)

        should_upload = all([
            ((now - modified_date) < one_hour),
            each_file.suffix in ['.mp3', '.wav'],
            ])

        if should_upload:
            print(f'Copying {each_file.name} from {each_file.parent.stem} to DROPBOX')
            shutil.copyfile(
                str(each_file),
                str(DROPBOX_PATH.joinpath(each_file.name))
            )




