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
playwright install
```

```shell
make run
```

## Docker Image 빌드

```shell
make docker-build
```

## Docker Container 실행

```shell
make docker-run
```

## 참조

- [Playwright를 사용해서 HTML 페이지를 PDF로 만들기](https://markruler.github.io/posts/pdf/html-to-pdf/)
