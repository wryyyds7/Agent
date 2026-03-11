import os

from PIL.ImImagePlugin import split
from langchain_chroma import Chroma
from langchain_core.documents import Document
from sympy.physics.units import length
from tensorflow.python.types.doc_typealias import document

from utils.logger_handler import logger_agent
from model.factory import embedding_model
from utils.config_handler import chroma_conf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tools import get_abs_path
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name = chroma_conf["collection_name"],
            embedding_function=embedding_model,
            persist_directory=chroma_conf["persist_directory"]
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(
            search_kwargs={"k": chroma_conf["k"]}
        )

    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的MD5做去重
        :return: None
        """

        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]),"w",encoding="utf-8").close()
                return False

            with open(get_abs_path(chroma_conf["md5_hex_store"]),"r",encoding="utf-8") as f:
                for line in f.readline():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                return False

        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        allowed_files_path = listdir_with_allowed_type(
            chroma_conf["data_path"],
            tuple(chroma_conf["allow_knowledge_file_type"])
        )
        for path in allowed_files_path:
            # 获取文件md5
            md5_hex = get_file_md5_hex( path)
            if check_md5_hex(md5_hex):
                logger_agent.info(f"[加载知识库]{path}已存在与知识库中，跳过")
                continue

            try:
                documents: list[Document] = get_file_documents(path)
                if not documents:
                    logger_agent.warning(f"[加载知识库]文件解析错误为空: {path}")

                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger_agent.warning(f"[加载知识库]文件分片，唔有效实体内容: {path}")
                    continue

                self.vector_store.add_documents(split_document)

                #记录这个已经处理好的文件的md5，避免下次重复加载

                save_md5_hex(md5_hex)
                logger_agent.info(f"[加载知识库]文件处理完成: {path}")
            except Exception as e:
                # exc_info为True时，会记录详细的报错堆栈
                logger_agent.error(f"[加载知识库]文件处理错误: {path}\n{str(e)}", exc_info=True)
