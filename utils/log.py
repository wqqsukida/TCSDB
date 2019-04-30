# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 10/23/18 11:39 AM
# FileName: log.py

import logging.handlers
import os
from django.conf import settings

class Logger(object):
    def __init__(self):
        self.log_file_path = settings.LOG_FILE_PATH
        self.backup_count = settings.LOG_BACKUP_COUNT
        self.max_bytes = settings.LOG_MAX_BYTES
        self.log_file = os.path.join(self.log_file_path,'tcsdb.log')

        if not os.path.exists(self.log_file_path):
            os.makedirs(self.log_file_path)
            # f = open(self.log_file,'w')
            # f.close()
        file_handler = logging.handlers.RotatingFileHandler(self.log_file, 'a',
                                                            maxBytes=self.max_bytes,
                                                            backupCount=self.backup_count,
                                                            encoding='utf-8')
        # file_handler = logging.FileHandler(self.log_file, 'a', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s:  %(message)s"))

        self.logger = logging.Logger('tcsdb', level=logging.INFO)
        self.logger.addHandler(file_handler)

    def info(self,msg):
        self.logger.info(msg)
    def error(self,msg):
        self.logger.error(msg)


logger = Logger()