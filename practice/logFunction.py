import logging

# 日志功能
def getLogger(logFilePath):
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)

  # 生成log文件配置
  logfile = logFilePath
  fh = logging.FileHandler(logfile, mode='w')
  # fh.setLevel(logging.DEBUG)

  # 控制台输出log
  ch = logging.StreamHandler()
  # ch.setLevel(logging.INFO)

  # 格式化日志格式
  formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
  fh.setFormatter(formatter)
  ch.setFormatter(formatter)

  logger.addHandler(fh)
  logger.addHandler(ch)

  return logger