from modules.process import Process


""" This module gets promos from satellite to process and
transfer to FFA for continuity producers.
"""

class Process_Satellite(Process):
    # Develop something to catch generic promos in segment matches later

    # override
    def process_for_ffa(self, key='promo'):
        super().process_for_ffa(key=key)
        # process then deletes source in 'for_dropbox'
        # (it is no longer needed because already delivers via satellite)
        dropbox_file_path = self.destination_paths.get(key)
        download_path = self.source_paths.get(key)

        # cleanup files that are not needed
        if dropbox_file_path:
            dropbox_file_path.unlink()
        if download_path:
            download_path.unlink()

    # override
    def _should_skip(self, destination):
        # Don't skip any...process all satellite files.
        return False
