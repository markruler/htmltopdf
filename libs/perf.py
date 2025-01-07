import threading
import time
from fastapi import Request
import logging

async def log_execution_time(request: Request, call_next):
    # 시작 시간 기록
    start_time = time.time()

    # 요청 처리
    response = await call_next(request)

    # 끝난 시간 기록
    process_time = time.time() - start_time

    # 로그 출력
    logging.info(f"{request.method} {request.url.path} 처리 시간: {process_time:.4f} 초")
    logging.debug(f"threading.active_count(): {threading.active_count()}")

    return response
