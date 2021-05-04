import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from colorama import Fore

station_codes = {
	'Adelaide':'ADA',
	'Yorkgate': 'YGA',
	'Antrim':'ADA',
	'Whitehead':'WDA',
	'Ballycarry':'BCA',
	'Whiteabbey':'WBA',
	'Ballymena':'BAA',
	'University':'UVA',
	'Ballymoney':'BYA',
	'Trooperslane':'TEA',
	'Balmoral':'BLA',
	'Titanic Quarter':'BEA',
	'Bangor':'BRA',
	'Sydenham':'SYA',
	'Bangor West': 'BWA',
	'Seahill':'SLA',
	'Bellarina':'BNA',
	'Scarva':'SAA',
	'Botanic':'BTA',
	'Poyntzpass':'PSA',
	'Carnalea':'CAA',
	'Portrush':'PHA',
	'Carrickfergus':'CSA',
	'Portadown':'PDA',
	'Castlerock':'CKA',
	'Newry':'NYA',
	'Mossley West': 'MWA',
	'City Hospital':'CHA',
	'Clipperstown':'CPA',
	'Moira':'MRA',
	'Coleraine':'CEA',
	'Marino':'MOA',
	'Cullybackey':'CYA',
	'Magheramorne':'MMA',
	'Cultra':'CTA',
	'Lurgan':'LUA',
	'Derriaghy':'DHA',
	'Lisburn':'LBA',
	'Derry':'LYA',
	'Londonderry':'LYA',
	'Larne Town':'LNA',
	'Dhu Varren':'DVA',
	'Larne Harbour':'LRA',
	'Downshire':'DPA',
	'Lanyon Place':'CLA',
	'Drogheda':'DGA',
	'Lambeg':'LGA',
	'Dublin': 'DNA',
	'Jordanstown':'JNA',
	'Dundalk':'DKA',
	'Hollywood':'HWA',
	'Dunmurry':'DMA',
	'Hilden':'HDA',
	'Finaghy':'FYA',
	'Helens Bay':'HBA',
	'Glynn':'GNA',
	'Greenisland':'GDA',
	'Great Victoria Street':'GVA'
}
	
def get_destination_and_departure():
	print("\n")
	departure = input(Fore.LIGHTRED_EX+"Departure: "+Fore.RESET)
	destination = input(Fore.LIGHTGREEN_EX+"Destination: "+Fore.RESET)
	return departure, destination

def get_station_code(key):
	return station_codes[key.title()]

def get_request_headers():
	return { 'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0' }


def send_GET_request(headers, dest, dept):
	print(Fore.LIGHTGREEN_EX+"[+] "+Fore.RESET+f"Retrieving updates for {dept} to {dest}...")
	GET_response = requests.get(
		url = 'https://www.journeycheck.com/nirailways/route?from='+depart_code+'&to='+dest_code+'&action=search&savedRoute=',
		headers = headers
	)
	return GET_response


if __name__=="__main__":
	##input
	departure, destination = get_destination_and_departure()
	dest_code = get_station_code(destination)
	depart_code = get_station_code(departure)

	##GET request
	headers = get_request_headers()
	GET_response = send_GET_request(headers, destination, departure)

	results_table = PrettyTable([Fore.LIGHTGREEN_EX+'Scheduled','Expected','Origin'+Fore.RESET])

	##parse
	soup = BeautifulSoup(GET_response.text, features="html.parser")
	table_element = soup.find('div',{'id':'liveDeparturesBody'})

	for tr in table_element.find_all('tr',{'class':'callingPatternRow'}):
		tds = tr.find_all('td')
		results_table.add_row([tds[0].text.strip().split(" ")[0].split(" ")[0], tds[1].text.strip(), tds[2].text.strip()])

	##result
	print("\n")
	print(results_table)	
	print("\n")
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
