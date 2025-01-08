# HTML to PDF

API server to generate PDF from HTML.

## Prerequisites

- Python 3.9+

## Usage

### Running with Docker

```shell
make docker-build
```

```shell
make docker-run
```

### Running locally

```shell
python -m venv .venv
source .venv/bin/activate
pip install --no-cache-dir --upgrade -r requirements.txt
playwright install --with-deps # chromium, firefox, webkit, etc.
```

```shell
make run
```

Running as a background process:

```shell
nohup .venv/bin/uvicorn htmltopdf:app --host=0.0.0.0 --port=38000 > /dev/null 2>&1 &
```

## References

- To avoid zombie processes
  - [Suggested configuration](https://playwright.dev/docs/ci#docker) - Playwright
  - [Docker](https://playwright.dev/docs/docker) - Playwright
- [Playwright를 사용해서 HTML 페이지를 PDF로 만들기](https://markruler.github.io/posts/pdf/html-to-pdf/)
