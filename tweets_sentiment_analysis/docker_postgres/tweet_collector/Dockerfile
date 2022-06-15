From python:3.6
WORKDIR /app
Copy requirements.txt /app
Copy credentials.py /app
Run pip install --upgrade pip
Run pip install -r requirements.txt
Copy get_tweets.py /app
CMD ["python", "get_tweets.py"]