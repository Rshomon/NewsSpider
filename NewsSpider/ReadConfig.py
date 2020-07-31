from configparser import ConfigParser
import os
'''
读取配置文件信息
配置文件位置：./config/test.ini
'''


class ReadConfigFile(object):
    def read_config(self):
        conn = ConfigParser()
        patha = os.path.join(os.path.join(
            os.path.dirname(__file__), "config"), "test.ini")
        if not os.path.isfile(patha):
            raise FileNotFoundError("文件不存在")
        # 读取配置文件
        conn.read(patha)
        # 获取单个配置信息
        url = conn.get("api", "url")
        method = conn.get("api", "method")
        name = conn.get("api", "name")
        age = conn.get("api", "age")
        phoneNum = conn.get("api", "phoneNum")
        return [url, method, name, age, phoneNum]


if __name__ == "__main__":
    readconfigfile = ReadConfigFile()
    print(readconfigfile.read_config())
