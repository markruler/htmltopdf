import logging
import time

from playwright.async_api import async_playwright, Browser


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
    logging.info(url)
    async with async_playwright() as playwright:
        logging.debug('headless Chromium 브라우저 시작')
        # https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch
        browser: Browser = await playwright.chromium.launch(
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

        try:
            logging.debug('새 페이지 열기')
            page = await browser.new_page()

            # https://playwright.dev/python/docs/api/class-page#page-goto
            logging.debug('URL로 이동')
            await page.goto(
                url=url,
                timeout=10_000,
                wait_until='load'  # domcontentloaded, load, networkidle
            )

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
        except Exception as e:
            logging.error(e)
        finally:
            logging.debug('브라우저 종료')

            # https://playwright.dev/python/docs/api/class-browser#browser-close
            # if browser is not None:
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
        logging.debug('headless Chromium 브라우저 시작')
        # https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch
        browser: Browser = await playwright.chromium.launch(
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
        try:
            logging.debug('새 페이지 열기')
            page = await browser.new_page()

            # https://playwright.dev/python/docs/api/class-page#page-goto
            logging.debug('Content 생성')
            await page.set_content(
                html=html,
                timeout=10_000,
                # load로 해야 img.src가 로드됨.
                wait_until='load'  # domcontentloaded, load, networkidle
            )

            time.sleep(1.0)  # seconds (wait for rendering)

            if css is not None:
                logging.info('CSS 추가')
                # # for testing: addStyleTag가 적용되는지 확인
                # color = '#ff000091'
                # css += (f'\nbody {{ background-color: {color}; }}'
                #         f'\n#printzone {{ background-color: {color}; }}'
                #         f'\n.subpage {{ background-color: {color}; }}')
                # logging.debug(css)
                await page.add_style_tag(
                    content=css
                )

            # https://playwright.dev/python/docs/api/class-page#page-pdf
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
        except Exception as e:
            logging.error(e)
        finally:
            logging.debug('브라우저 종료')

            # https://playwright.dev/python/docs/api/class-browser#browser-close
            # if browser is not None:
            await browser.close()
