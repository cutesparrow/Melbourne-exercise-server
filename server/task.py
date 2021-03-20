#timely task
from urllib.request import urlopen
import json


def update_dataset():
    download_sensor_location()
    download_Hourly_count_dataset()


def download_file(url, filename):
    try:
        content = urlopen(url, timeout=15).read()
        jsonContent = json.loads(content.decode('utf-8'))
        with open('../resources/' + filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jsonContent))
    except Exception as err:
        print(err)
        print(url)


def download_Hourly_count_dataset():
    try:
        download_file(
            "https://data.melbourne.vic.gov.au/resource/d6mv-s43h.json",
            'pedestrian_count_dataset.json')
    except Exception as err:
        print(err)


def download_sensor_location():
    try:
        download_file(
            "https://data.melbourne.vic.gov.au/resource/h57g-5234.json",
            'pedestrian_sensor_location.json')
    except Exception as err:
        print(err)
