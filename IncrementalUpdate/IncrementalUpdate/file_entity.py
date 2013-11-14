import os
import hashlib
from Utils.util import FileUtil

class FileEntity:

    def __init__(self,file_path,lazy_init=True):
        self.file_path = file_path
        self.sha256 = ''
        self.virtual_path = ''
        #
        self.blocks = []
        if not lazy_init:
            computeSHA256()

    def computeSHA256(self):
        self.sha256 = FileUtil.compute_file_Sha256(self.file_path)


