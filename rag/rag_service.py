"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from rag.vector_store import VectorStoreService
from model.factory import chat_model
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()        # 向量存储器
        self.retriever = self.vector_store.get_retriever() # 检索器
        self.prompt_text = load_rag_prompts() #
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)  #
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        return self.prompt_template | self.model | StrOutputParser()

    def retriever_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"[参考资料{counter}]: {doc.page_content}  |  [参考元数据]: {doc.metadata}"
        return self.chain.invoke(
            {
                "input": query,
                "context": context,
                # TODO: 记得加上历史记录！在rag_service里面改就行！
                # "history": history
            }
        )
if __name__ == "__main__":
    rag_service = RagSummarizeService()
    print(rag_service.rag_summarize("如何使用RAG服务,中文回答我"))