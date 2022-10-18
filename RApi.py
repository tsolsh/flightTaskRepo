from flask import Flask, request, jsonify
import shutil
from tempfile import NamedTemporaryFile
import datetime
import csv
import json

app = Flask(__name__)

flights = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1018},
]


def _find_next_id():
    return max(country["id"] for country in flights) + 1


@app.get("/flights")
def get_flights():
    csvFilePath = 'flight.csv'
    data = []

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            data.append(rows)

    return json.dumps(data, indent=4)


@app.get("/flights/<flight_id>")
def get_flight(flight_id):
    csvFilePath = 'flight.csv'

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            if row['flight ID'] == flight_id:
                data = row
                break

    return json.dumps(data, indent=4)


@app.post("/flights")
def update_file():
    filename = 'flight.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    fields = ['flight ID', ' Arrival', ' Departure ', 'success']

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        writer.writerow(dict((heads, heads) for heads in fields))
        for rows in reader:
            if rows['flight ID'] == 'flight ID':
                continue
            arrival = rows[' Arrival'].strip()
            departure = rows[' Departure '].strip()
            time_delta = datetime.datetime.strptime(departure, '%H:%M') - datetime.datetime.strptime(arrival, '%H:%M')
            total_seconds = time_delta.total_seconds()
            minutes = total_seconds / 60
            if minutes >= 180:
                row = {'flight ID': rows['flight ID'].strip(), ' Arrival': arrival, ' Departure ': departure,
                       'success': 'success'}
            else:
                row = {'flight ID': rows['flight ID'].strip(), ' Arrival': arrival, ' Departure ': departure,
                       'success': 'fail'}
            writer.writerow(row)

    shutil.move(tempfile.name, filename)
    return {"error": "Request must be JSON"}, 415
