FROM python:3.8
WORKDIR /app
COPY requirements.txt /app
COPY credentials.py /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY get_recent_tweets.py /app
CMD ["python", "get_recent_tweets.py"]