FROM python:3.8

COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3","api.py"]