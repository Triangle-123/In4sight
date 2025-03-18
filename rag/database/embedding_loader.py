"""
ChromaDB에 임베딩할 모델을 로딩하는 클래스
"""

import logging
from typing import Callable, List, Optional

from chromadb.api.types import Documents, EmbeddingFunction
from sentence_transformers import SentenceTransformer

from rag.core.config import settings

logger = logging.getLogger(__name__)


class SentenceTransformerEmbeddings(EmbeddingFunction):
    """
    ChromaDB의 EmbeddingFunction 인터페이스를 구현한 클래스
    """

    def __init__(self, model_name: str):
        """
        SentenceTransformerEmbeddings 초기화

        Args:
            model_name: 사용할 SentenceTransformer 모델 이름
        """
        self.model_name = model_name
        self._model = None

    def _get_model(self) -> SentenceTransformer:
        """
        모델 인스턴스 로드 및 캐싱
        """
        if self._model is None:
            try:
                logger.info("임베딩 모델 '%s' 로드 중...", self.model_name)
                self._model = SentenceTransformer(self.model_name)
                logger.info("임베딩 모델 로드 완료")
            except Exception as e:
                logger.error("임베딩 모델 로드 실패: %s", str(e))
                raise
        return self._model

    def __call__(self, text: Documents) -> List[List[float]]:
        """
        ChromaDB의 EmbeddingFunction 인터페이스에 맞춘 호출 메서드

        Args:
            input: 임베딩할 텍스트 리스트

        Returns:
            임베딩 벡터 리스트
        """
        model = self._get_model()
        embeddings = model.encode(text)
        return embeddings.tolist()


class EmbeddingModelLoader:
    """
    ChromaDB 임베딩 모델을 관리하고 로드하는 클래스
    """

    # 올바른 타입 힌트 방식
    INSTANCE: Optional["EmbeddingModelLoader"] = None
    model: Optional[SentenceTransformer] = None

    def __new__(cls):
        """
        클래스 초기화
        """
        if cls.INSTANCE is None:
            cls.INSTANCE = super(EmbeddingModelLoader, cls).__new__(cls)
            cls.model_name = getattr(
                settings,
                "EMBEDDING_MODEL_NAME",
                "paraphrase-multilingual-mpnet-base-v2",
            )

        return cls.INSTANCE

    def get_model(self) -> SentenceTransformer:
        """
        임베딩 모델 인스턴스를 리턴하는 메소드
        """

        if self.model is None:
            try:
                logger.info("임베딩 모델 '%s' 로드 중...", self.model_name)
                self.model = SentenceTransformer(self.model_name)
                logger.info("임베딩 모델 로드 완료")
            except Exception as e:
                logger.error("임베딩 모델 로드 실패: %s", str(e))
                raise

        return self.model

    def encode(self, texts: List[str]) -> List[List[float]]:
        """
        텍스트 리스트를 임베딩 벡터로 변환

        Args:
            texts: 임베딩할 텍스트 리스트

        Returns:
            임베딩 벡터 리스트
        """
        model = self.get_model()
        embeddings = model.encode(texts)
        return embeddings.tolist()

    def get_embedding_function(self) -> Callable[[List[str]], List[List[float]]]:
        """
        ChromaDB에서 사용할 수 있는 임베딩 함수 반환
        """
        return SentenceTransformerEmbeddings(self.encode)


embedding_loader = EmbeddingModelLoader()
