from modules.settings import LOCAL_PATH


class Download_Files:

    LOCAL_PATH = LOCAL_PATH

    def __init__(self, server, remote_dir: str, download_list: list):
        self.download_list = download_list
        self.remote_dir = remote_dir
        self.server = server
    
    def download_all(self):
        for each_file in self.download_list:
            self.download_one(each_file)

    def download_one(self, one_file):
        full_path = self.LOCAL_PATH.joinpath(one_file)
        with open(full_path, 'wb') as out_file:
            print(f'Downloading {one_file} ... ', end='')
            result = self.server.retrbinary(
                f'RETR /{self.remote_dir}/{one_file}', out_file.write
                )
            print(result)
            return ('226' in result)

