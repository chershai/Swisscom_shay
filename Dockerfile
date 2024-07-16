FROM python:3.12
WORKDIR /app
COPY . /app
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["sh", "-c", "python -m unittest ./test/client_unittest.py"]