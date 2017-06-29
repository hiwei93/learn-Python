#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'zhangwei'
import os
import hashlib
from logFunction import getLogger
from importCSVToMysql import importToDB

# 日志
logFilePath = 'log/execute.log'
logger = getLogger(logFilePath)

logger.info('getLogger is success')

fileDic = {} # 用于存放文件关系的字典
parentPath = 'E:\\Tsinghua\\20170623\\任务'
pSeparator = '\\' # path分隔符
# print(files)

# 获取哈希值
def getHexString(string):
  md5 = hashlib.md5()
  md5.update(string.encode('utf8'))
  return md5.hexdigest()

# 处理传入的path，根据path的类型跟别处理
def dealWithDir(fullPath):
  if not os.path.exists(fullPath):
    logger.info('this path dose not exist!')
    return
  
  if os.path.isdir(fullPath):
    logger.info('path: ' + fullPath + 'is a directory！')
    executDir(fullPath)

  if os.path.isfile(fullPath):
    logger.info('path: ' + fullPath + 'is a file！')
    executFile(fullPath)

# 处理文件
def executeFile(dirName, mapping):
  if dirName in fileDic:
    fileDic[dirName].update(mapping)
  else:
    fileDic[dirName] = mapping

# 处理目录
def executDir(dirPath):
  # 获取目录的名字
  dnBegin = dirPath.rfind('\\') + 1
  dirName = dirPath[dnBegin:]
  logger.info('dirName is ' + dirName)

  # 获取目录中的文件
  files = os.listdir(dirPath)
  logger.info('have file number is ' + str(len(files)))
  # 遍历文件
  for file in files:
    # 如果是目录，则递归
    if os.path.isdir(dirPath + pSeparator  + file):
      executDir(dirPath + pSeparator + file)
    # 如果是文件，处理文件
    if os.path.isfile(dirPath + pSeparator + file):
      # 获取文件名
      if file.endswith('csv'):
        # fileDic.update({dirName: {}})
        fnEnd = file.rfind('.csv')
        fileName = file[:fnEnd]
        tableName = getHexString(fileName)
        # 生成文件映射，有助于生成xls文件和文件夹
        executeFile(dirName, {fileName: tableName})
        # fileDic[dirName].update({fileName: tableName})
        # logger.info('file name is ' + fileName)
        # logger.info('file dictionary like ' + str(fileDic))
      else:
        logger.error('type of file ' + file + ' is not CVS');


dealWithDir(parentPath)
logger.info('final file dictionary like ' + str(fileDic))
# for dirs, files in fileDic.items():
#   print('directory ' + dirs +' has files: ' )
#   for file, hexStr in files:
#     print('----file: ' + file )
    