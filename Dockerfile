FROM python:3.9.1-slim
WORKDIR /src
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "DegeneSix.py"]