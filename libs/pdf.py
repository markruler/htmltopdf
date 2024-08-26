import time

from flask import current_app as app

from libs.browser import BrowserInstance


def url_to_pdf(
        url: str,
        orientation: str = 'portrait',
):
    """
    페이지 URL로 PDF 생성
    :param url: 페이지 URL
    :param orientation: 용지 방향 (portrait, landscape)
    :return: PDF 바이너리
    """
    app.logger.info(url)

    browser_instance = BrowserInstance(orientation=orientation)
    browser = browser_instance.start()
    page = browser.new_page()

    # https://playwright.dev/python/docs/api/class-page#page-goto
    app.logger.debug('URL로 이동')
    page.goto(
        url=url,
        timeout=10_000,
        wait_until='load'  # domcontentloaded, load, networkidle
    )

    _pdf = browser.pdf()

    browser.stop()

    return _pdf


def content_to_pdf(
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
    browser_instance = BrowserInstance(orientation=orientation)
    browser = browser_instance.start()
    page = browser.new_page()

    # https://playwright.dev/python/docs/api/class-page#page-goto
    app.logger.debug('Content 생성')
    page.set_content(
        html=html,
        timeout=10_000,
        # load로 해야 img.src가 로드됨.
        wait_until='load'  # domcontentloaded, load, networkidle
    )

    time.sleep(1.0)  # seconds (wait for rendering)

    if css is not None:
        app.logger.info('CSS 추가')
        # # for testing: addStyleTag가 적용되는지 확인
        # color = '#ff000091'
        # css += (f'\nbody {{ background-color: {color}; }}'
        #         f'\n#printzone {{ background-color: {color}; }}'
        #         f'\n.subpage {{ background-color: {color}; }}')
        # app.logger.debug(css)
        page.add_style_tag(
            content=css
        )

    _pdf = browser.pdf()

    browser.stop()

    return _pdf
