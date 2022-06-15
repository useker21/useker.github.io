# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory in the container to /my_folder
WORKDIR /app_folder

# Copy the requirements file and verything else in this folder i
COPY . /app_folder

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# What should be executed when the contrainer is built/started: Run luftdaten_stream.py
CMD ["python", "luftdaten_stream.py"]