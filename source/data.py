import csv
import math
from FlightInfo import FlightInfo
from collections import *
from util import *

# For testing csv.reader
def no_filter(fname):
	filtered_rows = [];
	fromfile = csv.reader(open(fname, 'rb'), delimiter=",")
	for row in fromfile:
		filtered_rows.append(row)
	return filtered_rows

date_to_filtered_rows = None

# Filter rows by date
def filter_rows_by_date(fname, date_string):
	global date_to_filtered_rows
	if date_to_filtered_rows is None:
		date_to_filtered_rows = defaultdict(list)

		fromfile = csv.reader(open(fname, 'rb'), delimiter=",")
		for row in fromfile:
			if row[0] == 'FL_DATE': # skip header
				continue
			# Filter away rows with missing fields
			if (not((row[3] == "") or
					(row[4] == "") or
					(row[6] == "") or
					(row[7] == ""))): 
				date_to_filtered_rows[row[0]].append(row)
	return date_to_filtered_rows[date_string]

# Partition filtered rows into respective airports
def split_rows_into_airports(filtered_rows):
	dict = {}
	for row in filtered_rows:
		if (row[1] not in dict): # Depart from current airport
			dict[row[1]] = []
		if (row[2] not in dict): # Arrive at current airport
			dict[row[2]] = []
		dict[row[1]].append(row)
		dict[row[2]].append(row)
	return dict

# Flight_info = [(index, departure?, scheduled time, actual time), ...]
# Index starts from 0
def airports_to_flight_info(dict):
	airports_info = {}
	for airport, rows in dict.items():
		airports_info[airport] = []
		index = 0
		for row in rows:
			if (row[1] == airport):
				departure = True
			elif (row[2] == airport):
				departure = False
			else:
				return "Error in airports_to_flight_info: Unable to determine whether flight is departure or arrival."
			
			scheduled = time_to_minutes(row[3])
			actual = time_to_minutes(row[4])
			
			airports_info[airport].append(FlightInfo(index, departure, scheduled, actual))
			index += 1
	return airports_info

# Keep only airports that have at least min_flights number of flights
def filter_airport_size(airports, min_flights):
	filtered = {}
	for airport, flight_info in airports.items():
		if len(flight_info) >= min_flights:
			filtered[airport] = flight_info
	return filtered

# Returns a dictionary of airports to flight_info, for given date
def get_airports_from_date(fname, date_string, min_flights):
	filtered_rows = filter_rows_by_date(fname, date_string)
	airports_dict = split_rows_into_airports(filtered_rows)
	airports_info = airports_to_flight_info(airports_dict)
	filtered_airports_info = filter_airport_size(airports_info, min_flights)
	return filtered_airports_info

# Returns the flight informations at the busiest airport, for a given date
def get_busiest_airport_from_date(fname, date_string, min_flights):
	airports_info = get_airports_from_date(fname, date_string, min_flights)
	busiest_airport = []
	for airport, flights in airports_info.items():
		if len(flights) > len(busiest_airport):
			busiest_airport = flights
	return busiest_airport

# Returns the flight informations at the busiest airport, for the entire month of Janurary
def get_busiest_airport_from_month(fname, min_flights):
	busiest = []
	for i in xrange(1, 32):
		day = str(i)
		if i < 10:
			day = '0' + day
		date = '2014-01-' + day
		# print date
		intervals = get_busiest_airport_from_date(fname, date, min_flights)
		if len(intervals) > len(busiest):
			busiest = intervals
	return busiest

