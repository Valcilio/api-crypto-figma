FROM python:3.10.4

WORKDIR /app

ARG request_domain

ENV request_domain=$TOKEN_FIGMA_CRYPTO_KEY

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

COPY ./main.py /app/main.py

COPY ./.proj_root /.proj_root

COPY ./tests /app/tests

COPY ./domain /app/domain

COPY ./resources /app/resources

RUN pytest

ENTRYPOINT ["python"]

CMD ["main.py"]
