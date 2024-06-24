import os
from common.logger import logger

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # 基础路径
file_path = os.path.join(BASE_PATH, "config", "testfile.txt")  # 配置文件路径


def convert_to_binary_and_get_size(file_path):
    # 确保文件存在
    if not os.path.exists(file_path):
        logger.error(f"文件 {file_path} 不存在。")
        return None, None

    try:
        # 以二进制模式打开文件
        with open(file_path, 'rb') as file:
            binary_content = file.read()
            # 获取文件大小
            file_size = os.path.getsize(file_path)
            return binary_content, file_size
    except IOError as e:
        logger.error(f"读取文件时发生错误: {e}")
        return None, None


# 示例
if __name__ == "__main__":
    file_path = file_path  # 替换为你的文件路径
    binary_content, file_size = convert_to_binary_and_get_size(file_path)

    if binary_content is not None and file_size is not None:
        logger.info(f"文件大小: {file_size} 字节")
        # 如果你想查看二进制内容，取消注释下面一行
        # print(binary_content)
    else:
        logger.error("无法转换文件或获取大小。")
