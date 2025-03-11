"""
ChromaDB 클라이언트 연결 관리 모듈
"""

import logging
import time
from typing import Optional

import chromadb

from ..core.config import settings

# 로깅 설정
logger = logging.getLogger(__name__)


class ChromaDBClient:
    """
    ChromaDB 클라이언트 연결을 관리하는 클래스
    """

    _instance: Optional["ChromaDBClient"] = None
    _client: Optional[chromadb.Client] = None
    _last_connection_time: float = 0
    _max_connection_age: int = None

    def __new__(cls):
        """
        객체가 생성될 때 __init__ 이전에 호출되는 메소드
        클래스 자체를 첫 번째 매개변수로 받는다.
        """

        if cls._instance is None:
            cls._instance = super(ChromaDBClient, cls).__new__(cls)
            cls._max_connection_age = settings.CHROMA_MAX_CONNECTION_AGE

        return cls._instance  # 항상 인스턴스를 반환

    def get_client(self) -> chromadb.Client:
        """
        ChromaDB 클라이언트 인스턴스를 반환하는 메소드
        필요시 새로운 연결을 생성하거나 연결을 갱신함
        """
        current_time = time.time()

        # 클라이언트가 없거나 너무 오래된 연결이면 재연결을 검토한다.
        if (
            self._client is None
            or (current_time - self._last_connection_time) > self._max_connection_age
        ):
            try:
                # 기존 연결이 있으면 상태를 확인한다.
                if self._client is not None:
                    try:
                        # 연결 상태를 확인한다 (간단한 쿼리 실행)
                        self._client.list_collections()
                        # 연결이 정상이면 타임스탬프만 갱신한다.
                        self._last_connection_time = current_time
                        return self._client
                    except Exception as conn_err:  # pylint: disable=broad-except
                        logger.warning(
                            "ChromaDB 연결 오류 감지: %s, 재연결을 시도합니다...",
                            str(conn_err),
                        )

                # 새 클라이언트를 생성한다.
                self._client = chromadb.Client()
                # 마지막 연결 시각을 갱신한다.
                self._last_connection_time = current_time
                logger.info("ChromaDB 새 연결 수립 완료")
            except Exception as e:  # pylint: disable=broad-except
                logger.error("ChromaDB 연결 실패: %s", str(e))
                if self._client is None:
                    raise ConnectionError("ChromaDB에 연결할 수 없습니다") from e
        return self._client

    def initialize(self) -> None:
        """
        ChromaDB 연결을 초기화하는 메소드
        """
        try:
            self.get_client()
            logger.info("ChromaDB 연결 초기화 완료")
        except ConnectionError as e:
            logger.error("ChromaDB 초기 연결 실패: %s", str(e))

    def close(self) -> None:
        """
        ChromaDB 연결을 종료하는 메소드
        """
        self._client = None
        logger.info("ChromaDB 연결 종료")


# ChromaDB 연결 인스턴스 생성
chroma_db = ChromaDBClient()
