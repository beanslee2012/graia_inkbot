import configparser

def get_conf(key):
  config = configparser.ConfigParser()   # 创建对象
  config.read("./config/bot.conf", encoding="utf-8")  # 读取配置文件，如果配置文件不存在则创建
  val = config.get('bot', key)  
  return val