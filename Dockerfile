FROM gcr.io/kaggle-images/python@sha256:00a659cc16b91a6956ef066063a9083b6a70859e5882046f3251632f4927149e

EXPOSE 8888 8501
WORKDIR /project

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
