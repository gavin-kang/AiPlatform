FROM python

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com --no-cache-dir -r requirements.txt

COPY app.py .
COPY gunicorn.conf.py .

CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]