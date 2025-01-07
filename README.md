# HTML to PDF

## 사용 모듈

- ~~[wkhtmltopdf](https://github.com/wkhtmltopdf/wkhtmltopdf)~~
- ~~[puppeteer](https://github.com/puppeteer/puppeteer)~~
- [microsoft/playwright](https://github.com/microsoft/playwright-python)

## Local 실행

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps # chromium, firefox, webkit, etc.
```

```shell
make run
```

## 백그라운드 실행

```shell
nohup venv/bin/python3 app.py > /dev/null 2>&1 &
```

## Docker Image 빌드

```shell
make docker-build
```

## Docker Container 실행

> Docker에서 사용 시 좀비 프로세스(`headless-shell <defunct>`)가 쌓이는 문제가 있음.

```shell
make docker-run
```

## 참조

- [Playwright를 사용해서 HTML 페이지를 PDF로 만들기](https://markruler.github.io/posts/pdf/html-to-pdf/)
