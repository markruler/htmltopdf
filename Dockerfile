FROM python:3.11-bookworm

WORKDIR /server
COPY . /server

# Timezone: KST 설정
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Playwright: browser and OS dependencies are installed with a single command
RUN playwright install --with-deps chromium

CMD ["uvicorn", "htmltopdf:app", "--host", "0.0.0.0", "--port", "38000"]
