import json
from hashlib import md5
from modules.settings import LOCAL_PATH

# next add a check in 'for_dropbox' folder for proper show lengths

class Verifier:
    LOCAL_PATH = LOCAL_PATH
    CACHED_HASHES_FILE = 'cached_hashes.json'

    def __init__(self, ftp_server, remote_dir, processor_class=None) -> None:
        self.ftp_server = ftp_server
        self.remote_dir = remote_dir
        self.processor = processor_class  # uses .match_show method
        self.cached_hashes = self._read_cached_hashes() or {}
    
    # Main
    def check_hashes(self):
        hash_doesnt_match_list = []
        for each_file in self.LOCAL_PATH.iterdir():
            file_name = each_file.name
            if self.processor().match_show(file_name):

                remote_hash = self.hash_remote(file_name)
                local_hash = self.hash_local(file_name) or remote_hash

                if remote_hash != local_hash:
                    hash_doesnt_match_list.append(file_name)
        
        self._write_cached_hashes()
        return hash_doesnt_match_list
    
    def hash_remote(self, file_name: str) -> str:
        if self.in_cache(file_name):
            return self.cached_hashes.get(file_name)

        md5_hash = md5()
        self.ftp_server.retrbinary(
            f'RETR /{self.remote_dir}/{file_name}', md5_hash.update
            )
        file_hash = md5_hash.hexdigest()
        self.cached_hashes.update({file_name: file_hash})
        return file_hash
    
    def hash_local(self, file_name: str) -> str:
        local_file_path = self.LOCAL_PATH.joinpath(file_name)
        if not local_file_path.exists():
            return None
        with open(local_file_path, 'rb') as local_file:
            file_contents = local_file.read()
            return md5(file_contents).hexdigest()

    def in_cache(self, file_name):
        return file_name in self.cached_hashes.keys()

    def _read_cached_hashes(self):
        if not self.LOCAL_PATH.joinpath(self.CACHED_HASHES_FILE).exists():
            return None
        with open(self.LOCAL_PATH.joinpath(self.CACHED_HASHES_FILE), 'r') as infile:
            try:
                return json.load(infile)
            except json.JSONDecodeError:
                return None

    def _write_cached_hashes(self):
        with open(self.LOCAL_PATH.joinpath(self.CACHED_HASHES_FILE), 'w+') as outfile:
            json.dump(self.cached_hashes, outfile)
    
