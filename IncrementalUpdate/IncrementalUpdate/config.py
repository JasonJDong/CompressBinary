import logging
import os
import sys
import ConfigParser
import string
import urllib2

class Config:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        with open(os.path.join(self._get_dir_path(),'config.cfg'), 'r') as cfg_file:
            config.readfp(cfg_file)
            self.service_host = config.get('local', 'server_host')
            self.service_port = config.get('local', 'server_port')
            self.block_storage = config.get('local', 'block_storage')
            block_size = config.get('local', 'block_size')
            self.block_size = 16   if block_size == '' else int(block_size) 
            self.minimap = {}
            self.loggingLevel = logging.ERROR

            #TEST
            self.server_folder = config.get('test', 'server_folder')
            self.client_folder = config.get('test', 'client_folder')

            try:
                level = config.get('log', 'level')
                if hasattr(logging, level):
                    self.loggingLevel = getattr(logging, level)
            except:
                pass
        self._init_logger()
        self._init_minimap()

    def _init_minimap(self):
        with open(os.path.join(self._get_dir_path(),'minemap.txt'), 'r') as f:
            for line in f:
                temp = line.split(' = ')
                if len(temp) == 2:
                    self.minimap[str(temp[0].strip())] = temp[1].strip()

    def _init_logger(self):
        logger = logging.getLogger('incremental-update-client')
        logger.setLevel(self.loggingLevel)
        ch = logging.StreamHandler()
        cf = logging.FileHandler(os.path.join(self._get_dir_path(),'app.log'))
        ch.setLevel(self.loggingLevel)
        cf.setLevel(self.loggingLevel)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s : %(message)s')
        ch.setFormatter(formatter)
        cf.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(cf)

    def _get_dir_path(self):
        return os.path.dirname(os.path.abspath(sys.argv[0]))

    def _str2list(self,str):
        try:
            split = str.split(',')
            dirs = []
            for dir in split:
                dirs.append(dir)
            return dirs
        except:
            return []

config = Config()
log = logging.getLogger('incremental-update-client')