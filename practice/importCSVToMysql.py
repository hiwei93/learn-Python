#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'zhangwei'
import pymysql
import csv
import re
import os
from logFunction import getLogger

# 日志
logFilePath = './log/import.log'
logger = getLogger(logFilePath)

logger.info('getLogger is success')

# 将csv中的数据转换到数据库
def importToDB(csvFileName, tableName):
  # 打开csv文件
  csvFileDir = 'E:\\Class\\imooc\\Python\\practice\\CVSorExcelFileExecute\\work\\'
  csvFileName = csvFileName
  cvsFileSuf = '.csv'
  csvFullPath = csvFileDir + csvFileName + cvsFileSuf

  logger.info('csv file full path is ' + csvFullPath)
  
  # 连接数据库
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

  with open(csvFullPath, newline='', encoding='utf-8') as f:
    logger.info('CSV file ' + f.name + ' open success')

    # 读取csv表头
    reader = csv.reader(f)

    # 获取表头字段
    header = next(reader)
    logger.info('get the table head is ' + ', '.join(header))

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
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8''' % ((tableName,) + tuple(header) + (header[0],))
    # logger.info('the sql statement is ' + sql)

    try:
      with connection.cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS `' + tableName + '`')
        if cursor.execute(sql) >= 0:
          logger.info('create table ' + tableName + " success")
        else:
          logger.info('create table ' + tableName + " faile")

      # 读取csv文件中的数据，向数据库中导入数据
      with connection.cursor() as cursor:
        total = 0
        for row in reader:
          values = []
          i = 0
          for value in row:
            if i == 5 or i == 6 or i == 9:
              if value == "" or re.match(r'[\sa-z]', value):
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

          # 向数据库写入数据
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
                  )''' % ((tableName,) + tuple(values))
          # logger.info('The insert sql is: ' + sql)
          total += cursor.execute(sql)
      logger.info('total data have ' + str(reader.line_num - 1))
      logger.info('import date have ' + str(total))
      connection.commit()
    finally:
      connection.close()

# 将csv数据导入到MySQL
# importToDB('8', 'table1')