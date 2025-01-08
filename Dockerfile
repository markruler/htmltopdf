FROM mcr.microsoft.com/playwright/python:v1.49.1-noble
# Playwright: browser and OS dependencies are installed with a single command
# RUN playwright install --with-deps chromium

WORKDIR /server
COPY . /server

# Timezone: KST 설정
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "htmltopdf:app", "--host", "0.0.0.0", "--port", "38000"]
