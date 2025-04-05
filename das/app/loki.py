"""
Loki 로깅 설정을 위한 모듈
"""

import logging
import sys

import logging_loki

from app.config import LOKI_URL


def setup_logging():
    """
    루트 로거를 설정하고 콘솔 및 Loki 핸들러를 추가합니다.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d %(levelname)5s 1 --- [%(threadName)s] "
        "%(name)-40.40s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    try:
        loki_handler = logging_loki.LokiHandler(
            url=LOKI_URL,
            tags={"service": "DAS-SERVER"},
            version="1",
        )
        loki_handler.setLevel(logging.INFO)
        loki_handler.setFormatter(formatter)
        root_logger.addHandler(loki_handler)
        logging.info("Loki 로깅 핸들러가 성공적으로 설정되었습니다.")
    except (ConnectionError, ValueError, IOError) as e:
        logging.error("Loki 로깅 핸들러 설정 중 오류 발생: %s", str(e))

    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        module_logger = logging.getLogger(logger_name)
        module_logger.handlers = []
        module_logger.propagate = True

    return logging.getLogger("das")
