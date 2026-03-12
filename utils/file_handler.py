import os,hashlib
from idlelib.iomenu import encoding
from importlib.metadata import files

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from utils.logger_handler import logger_agent

def get_file_md5_hex(filepath: str): # 获取文件md5的十六进制字符串
    if not os.path.exists(filepath):
        logger_agent.error(f"[md5计算]文件不存在: {filepath}")
        return

    if not os.path.isfile(filepath):
        logger_agent.error(f"[md5计算]路径不是文件: {filepath}")
        return
    md5_obj = hashlib.md5()
    chunk_size = 4096
    try:
        with open(filepath, "rb") as f: # 二进制打开
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            """
            等效于
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)
            """
            return md5_obj.hexdigest()
    except Exception as e:
        logger_agent.error(f"[md5计算]文件计算错误: {filepath}")
        return



def listdir_with_allowed_type(path: str, allowed_type: tuple[str] = None): # 返回文件夹内部的文件列表
    files = []
    if not os.path.isdir(path):
        logger_agent.error(f"[listdir_with_allowed_type]路径不是文件夹: {path}")
        return allowed_type

    for f in os.listdir(path):
        if f.endswith(allowed_type):
            files.append(os.path.join(path,f))

    return tuple(files)

def pdf_loader(filepath: str,passwd: str = None):
    return PyPDFLoader(filepath, passwd).load()


# TODO: 这里真的能这么写吗？自产的时候注意一下看看怎么测试
def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()

