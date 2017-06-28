#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
import csv
import logging
import re

# connection = pymysql.connect(host='localhost',
#                       user = 'root',
#                       password = 'root',
#                       db = 'dbgirl',
#                       charset = 'utf8')

# with connection.cursor() as cursor:
#   sql = 'SELECT * FROM girl'
#   cursor.execute(sql)
#   results = cursor.fetchall()
#   for row in results:
#     print(row)

# 日志配置
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logfile = './log/execute.log'
fh = logging.FileHandler(logfile, mode='w')
# fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# csv数据导入到MySQL中
# 获取数据库连接
host = 'localhost'
username = 'root'
password = 'root'
dbName = 'work'
charset = 'utf8'

connection = pymysql.connect(host = host,
                             user = username,
                             password = password,
                             db = dbName,
                             charset = charset)

with open(r'E:\Class\imooc\Python\practice\CVSorExcelFileExecute\Construction engineering management culture shift- Is the lowest tender offer dead-.csv', 
          newline='', encoding='utf-8') as f:
  # 获取文件名
  fileFullPath = f.name;
  print(fileFullPath)
  fnBegin = fileFullPath.rfind('\\')
  fnEnd = fileFullPath.rfind('.csv')
  # fileName = fileFullPath[fnBegin + 1:fnEnd]
  fileName = 'table2'
  logger.info('current filename is ' + fileName)

  # 读取csv文件
  reader = csv.reader(f)

  # 获取表头字段(可要可不要)
  header = next(reader) 
  logger.info('get the header: ' + ','.join(header)) 

  # 创建数据库
  sql = '''CREATE TABLE `%s` (
            `%s` VARCHAR (225) NOT NULL,
            `%s` VARCHAR (255) NULL,
            `%s` VARCHAR (1000) NULL,
            `%s` VARCHAR (255) NULL,
            `%s` VARCHAR (255) NULL,
            `%s` DOUBLE NULL,
            `%s` INT (255) NULL,
            `%s` VARCHAR (1000) NULL,
            `%s` VARCHAR (255) NULL,
            `%s` DOUBLE NULL,
            `%s` VARCHAR (255) NULL,
            PRIMARY KEY (`%s`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8''' % ((fileName,) + tuple(header) + (header[0],))
  logger.info('the sql statement is ' + sql)

  with connection.cursor() as cursor:
    cursor.execute('DROP TABLE IF EXISTS `' + fileName + '`')
    if cursor.execute(sql) >= 0:
      logger.info('create table ' + fileName + " success")
    else:
      logger.info('create table ' + fileName + " faile")

    # 读取csv文件中的数据，向数据库中导入数据
    for row in reader:
      values = []
      i = 0
      
      # 读取数据并且转换数据类型
      for value in row:
        if i == 5 or i == 6 or i == 9:
          if value == "" or re.match(r'[a-zA-Z]+', value):
            value = 'null'
          elif i == 5 or i == 9:
            logger.info('value transfored by float is : ' + value)
            value = float(value)
          elif i == 6:
            logger.info('value transfored by int is : ' + value)
            value = int(value)
        else:
          logger.info('value transfored by escape_string is : ' + value)
          value = pymysql.escape_string(value)
        values.append(value)
        i += 1

      # for value in values:
      #   print(value)
      
      sql = '''INSERT INTO `%s` (
              `ID`,
              `Name`,
              `Aff`,
              `Email`,
              `Extracted`,
              `score`,
              `H-index`,
              `Keyword`,
              `Language`,
              `Relevance`,
              `Cag`
            )
            VALUES
              (
                '%s',
                '%s',
                '%s',
                '%s',
                '%s',
                %s,
                %s,
                '%s',
                '%s',
                %s,
                '%s'
              )''' % ((fileName,) + tuple(values))
      logger.info('The insert sql is: ' + sql)
      print(cursor.execute(sql))
  connection.commit()