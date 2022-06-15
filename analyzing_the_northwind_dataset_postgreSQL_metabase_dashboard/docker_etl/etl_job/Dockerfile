FROM python:3.8
WORKDIR /app
COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY etl_skeleton.py /app
CMD ["python", "etl_skeleton.py"]