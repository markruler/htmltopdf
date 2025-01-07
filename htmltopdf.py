import asyncio
import logging
import sys
from typing import Optional

from api.pdf_from_url import get_pdf_from_url

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


async def url_to_pdf(
        url: str,
        orientation: Optional[str] = "portrait",
):
    pdf = await get_pdf_from_url(url, orientation)
    logging.info(pdf[:2])


async def main():
    tasks = [
        url_to_pdf(
            url="https://www.google.com",
            orientation="portrait",
        )
        for _ in range(20)
    ]
    await asyncio.gather(*tasks)
    await asyncio.sleep(3600)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
