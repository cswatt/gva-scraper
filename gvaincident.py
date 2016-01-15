#!/usr/bin/python
from bs4 import BeautifulSoup
from datetime import datetime
import requests, re

class GVAIncident:
	def __init__(self, iid, date, state, city, no_k, no_i, event_url):
		self.iid = iid
		self.date = self.format_date(date)
		self.state = str(state)
		self.city = str(city)
		self.no_k = int(no_k)
		self.no_i = int(no_i)
		self.incident_url = "http://gunviolencearchive.org/incident/" + iid
		self.event_url = str(event_url)
		self.lat, self.long = self.locate()

	def __repr__(self):
		return "%r,%r,%r,%r,%r,%r,%r,%r,%r,%r" %(self.iid, self.date, self.state, self.city, self.no_k, self.no_i, self.incident_url, self.event_url, self.lat, self.long)

	def format_date(self, date):
		d = datetime.strptime(date, "%B %d, %Y")
		return datetime.strftime(d, "%Y-%m-%d")

	def locate(self):
		result = requests.get(self.incident_url)

		c = result.content
		soup = BeautifulSoup(c)

		span = soup.find_all("span")
		spans = []
		for x in span:
			spans.append(x.string)

		found = False
		for y in spans:
			if y and y.startswith('Geolocation'):
				found = True
				latlong = y[13:]
				return [float(z.strip()) for z in latlong.split(',')]
		if not found:
			return [0, 0]
