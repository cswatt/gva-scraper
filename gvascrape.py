from bs4 import BeautifulSoup
from gvaincident import GVAIncident
import requests, sys

output_file = sys.argv[1]

def scrape(results, soup):
	table = soup.find("table")
	for row in table.find_all('tr')[1:]:
		col = row.find_all('td')

		date = col[0].string
		state= col[1].string
		city = col[2].string
		killed = col[4].string
		injured = col[5].string
		incident_url = col[6].ul.li.a.get('href')
		incident_id = incident_url[-6:]
		event_url = col[6].ul.li.findNext('li').a.get('href')
		
		record = GVAIncident(incident_id, date, state, city, killed, injured, event_url)
		# print record
		results.append(record)

def write_csv(results):
	target = open(output_file, 'a')
	for r in results:
		target.write(repr(r))
		target.write("\n")
	target.close()

def main():
	results = []
	base_url = 'http://www.gunviolencearchive.org'
	next_url = '/mass-shooting'
	while next_url:
		print base_url+next_url
		next_page = requests.get(base_url + next_url)
		c = next_page.content
		soup = BeautifulSoup(c)
		scrape(results, soup)
		next_url = soup.find('a', {'title': 'Go to next page'})
		if next_url:
			next_url = next_url.get('href')
	write_csv(results)

if __name__ == "__main__":
	main()
