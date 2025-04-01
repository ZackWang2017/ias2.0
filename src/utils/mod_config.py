#encoding:utf-8
#name:mod_config.py

import configparser
import os

#获取config配置文件
def get_config(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/sys.conf'
    config.read(path,encoding="UTF-8")
    return config.get(section, key)

#其中 os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录