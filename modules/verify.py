from hashlib import md5
from modules.settings import LOCAL_PATH

# next add a check in 'for_dropbox' folder for proper show lengths
# also add a cache for the hashes to prevent rehashing remote files every time. 
#       maybe...store remote hashes in a file when files are downloaded. 

class Verify:
    LOCAL_PATH = LOCAL_PATH

    def __init__(self, ftp_server, ftp_dir, processor_class) -> None:
        self.ftp = ftp_server
        self.remote_dir = ftp_dir
        self.processor = processor_class()  # uses .match_show method
    
    def check_hashes(self):
        hash_doesnt_match_list = []
        for each_file in self.LOCAL_PATH.iterdir():
            file_name = each_file.name
            if self.processor.match_show(file_name):
                remote_hash = self.hash_remote(file_name)
                local_hash = self.hash_local(file_name) or remote_hash
                print()
                print(remote_hash, local_hash)
                if remote_hash != local_hash:
                    hash_doesnt_match_list.append(file_name)
        return hash_doesnt_match_list
    
    def hash_remote(self, file_name: str) -> str:
        md5_hash = md5()
        self.ftp.retrbinary(f'RETR /{self.remote_dir}/{file_name}', md5_hash.update)
        return md5_hash.hexdigest()
    
    def hash_local(self, file_name: str) -> str:
        local_file_path = self.LOCAL_PATH.joinpath(file_name)
        if not local_file_path.exists():
            return None
        with open(local_file_path, 'rb') as local_file:
            file_contents = local_file.read()
            return md5(file_contents).hexdigest()
