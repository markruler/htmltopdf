import logging
import sys
from io import BytesIO
from typing import Optional, Annotated

from fastapi import FastAPI, Form
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.pdf_from_content import get_pdf_from_content
from api.pdf_from_url import get_pdf_from_url
from libs.perf import log_execution_time

# uvicorn htmltopdf:app --reload

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging_format = '%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(name)s:%(module)s] - %(message)s'
fileHandler = logging.FileHandler(
    filename='logs/htmltopdf.log',
    mode='a+',  # 'a': append, 'w': overwrite
)
stream_handler = logging.StreamHandler(
    stream=sys.stdout,
)
logging.basicConfig(
    level=logging.DEBUG,
    format=logging_format,
    handlers=[
        fileHandler,
        stream_handler,
    ]
)


@app.middleware("http")
async def execution_time_middleware(request, call_next):
    return await log_execution_time(request, call_next)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    logging.error(exc)
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logging.error(exc)
    return await request_validation_exception_handler(request, exc)


@app.get("/health")
async def healthcheck():
    return "OK"


@app.get("/pdf/url")
async def url_to_pdf(
        url: str,
        orientation: Optional[str] = "portrait",
        filename: Optional[str] = "out",
):
    pdf = await get_pdf_from_url(url, orientation)
    return StreamingResponse(
        content=BytesIO(pdf),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment;filename={filename}.pdf"
        },
    )


@app.post("/pdf/content")
async def content_to_pdf(
        html: Annotated[str, Form()],
        css: Annotated[str, Form()] = None,
        orientation: Annotated[str, Form()] = "portrait",
        filename: Annotated[str, Form()] = "out",
):
    pdf = await get_pdf_from_content(html, css, orientation)
    return StreamingResponse(
        content=BytesIO(pdf),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment;filename={filename}.pdf"
        },
    )
