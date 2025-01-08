import logging
import time

from playwright.async_api import async_playwright, Browser, Playwright


async def generate_pdf(page, orientation: str):
    """
    PDF 생성
    https://playwright.dev/python/docs/api/class-page#page-pdf
    :param page: Playwright page object
    :param orientation: 용지 방향 (portrait, landscape)
    :return: PDF 바이너리
    """
    logging.debug('PDF로 변환 및 저장')
    _pdf = await page.pdf(
        format='A4',
        landscape=orientation == 'landscape',
        print_background=True,
        display_header_footer=False,
        margin={
            'top': '10mm',
            'bottom': '10mm',
            'left': '10mm',
            'right': '10mm',
        }
    )
    return _pdf


async def launch_browser(playwright: Playwright):
    """
    Playwright 브라우저 시작
    # https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch
    :return: Playwright browser object
    """
    logging.debug('headless Chromium 브라우저 시작')
    return await playwright.chromium.launch(
        headless=True,
        timeout=10_000,  # (ms)
        args=[
            # https://peter.sh/experiments/chromium-command-line-switches/
            "--no-sandbox",
            # "--single-process",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-zygote",
        ],
        # avoid "signal only works in main thread of the main interpreter"
        handle_sigint=False,
        handle_sigterm=False,
        handle_sighup=False,
    )


async def url_to_pdf(
        url: str,
        orientation: str,
):
    """
    페이지 URL로 PDF 생성
    :param url: 페이지 URL
    :param orientation: 용지 방향 (portrait, landscape)
    :return: PDF 바이너리
    """
    logging.info(f'URL to PDF: {url}')
    async with async_playwright() as playwright:
        browser: Browser = await launch_browser(playwright)
        try:
            logging.debug('새 페이지 열기')
            page = await browser.new_page()
            # https://playwright.dev/python/docs/api/class-page#page-goto
            logging.debug('URL로 이동')
            await page.goto(url=url, timeout=10_000, wait_until='load')  # domcontentloaded, load, networkidle
            return await generate_pdf(page, orientation)
        except Exception as e:
            logging.error(e)
        finally:
            logging.debug('브라우저 종료')
            # https://playwright.dev/python/docs/api/class-browser#browser-close
            await browser.close()


async def content_to_pdf(
        html: str,
        css: str,
        orientation: str = 'portrait',
):
    """
    HTML, CSS로 PDF 생성
    :param html: HTML Content
    :param css: CSS Content
    :param orientation: 용지 방향 (portrait, landscape)
    :return: PDF 바이너리
    """
    async with async_playwright() as playwright:
        browser: Browser = await launch_browser(playwright)
        try:
            logging.debug('새 페이지 열기')
            page = await browser.new_page()
            # https://playwright.dev/python/docs/api/class-page#page-goto
            logging.debug('Content 생성')
            # load로 해야 img.src가 로드됨.
            await page.set_content(html=html, timeout=10_000, wait_until='load')  # domcontentloaded, load, networkidle
            time.sleep(1.0)  # seconds (wait for rendering)
            if css is not None:
                logging.debug('CSS 추가')
                await page.add_style_tag(content=css)

            return await generate_pdf(page, orientation)
        except Exception as e:
            logging.error(e)
        finally:
            logging.debug('브라우저 종료')
            # https://playwright.dev/python/docs/api/class-browser#browser-close
            await browser.close()
