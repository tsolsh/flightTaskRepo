import shutil
from tempfile import NamedTemporaryFile
import datetime
import csv


def read_csv():
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


read_csv()
