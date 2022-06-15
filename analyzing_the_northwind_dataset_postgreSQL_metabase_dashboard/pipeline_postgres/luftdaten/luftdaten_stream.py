import requests
import time
from sqlalchemy import create_engine
import logging


SENSOR_URL = "http://api.luftdaten.info/static/v1/sensor/{}/"

HOST = 'mypg'
PORT = '5432' #port inside the container
DATABASE = 'postgres'
USER = 'postgres'
PASSWORD = 'postgres'

conn_string = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(conn_string)

create_query = '''
CREATE TABLE luftdaten(
    id SERIAL PRIMARY KEY,
    entry_date TEXT, 
    pm25 FLOAT,
    pm10 FLOAT);
'''
engine.execute('''DROP TABLE IF EXISTS luftdaten;''')
engine.execute(create_query)

def pick_luftdaten_values(sensor_id):
    result = requests.get(SENSOR_URL.format(sensor_id))
    data = result.json()
    time_stamp = data[0]['timestamp']
    PM25 = data[0]['sensordatavalues'][0]['value']
    PM10 = data[0]['sensordatavalues'][1]['value']
    return time_stamp, float(PM25), float(PM10)


if __name__ == '__main__':
    while True:
        time_stamp, PM25, PM10 = pick_luftdaten_values(7619)
        logging.critical(f"Air quality data at {time_stamp}: PM25 = {PM25}, PM10 = {PM10}")
        insert_query = f"INSERT INTO luftdaten (entry_date, pm25, pm10) VALUES ('{time_stamp}', '{PM25}', '{PM10}')"
        engine.execute(insert_query)
        logging.critical(f"Data written in database {DATABASE} in host {HOST}")
        time.sleep(10)