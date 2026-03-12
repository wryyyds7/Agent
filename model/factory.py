from abc import ABC, abstractproperty, abstractmethod
from typing import Optional
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_community.chat_models.tongyi import ChatTongyi

from utils.config_handler import rag_conf


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_conf["chat_model_name"], api_key=rag_conf["api_key"])

class EmbeddingFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"], dashscope_api_key=rag_conf["dashscope_api_key"])

chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingFactory().generator()