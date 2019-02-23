#!/bin/python
import requests, json, sys, re
from bs4 import BeautifulSoup

def getJSONdata():
   ##open the json data for station codes
   json_data = requests.get("https://apis.opendatani.gov.uk/translink/")
   station_codes = json_data.json() 
   json_data.close()
   return station_codes
   
   
def filterForTermination(attr):
   for att in attr:
      if "Terminate" in att.text:
         term_idx = attr.index(att)
         attr.pop(term_idx)
         attr.pop(term_idx)


def getstationCode(station_codes,departure):
   for station in station_codes['stations']:
      if station[u'name'] == departure:
         file_code = str(station[u'code'])
   return file_code
   
 
def getWebPage(url):
   content = requests.get(url)
   if content.status_code != 200:
      print "could not get webpage"
      sys.exit()
   ##parse the webpage html code
   soup = BeautifulSoup(content.text,"html.parser")
   content.close() 
   return soup
   
def cleanOutput(string):
   return string.strip().replace('\r\n','').replace('  ','')
   
def printResults(main_details,callings):
   ##get the attributes by parsing the html
   t,d,p,i,e = ['Arrival Time','Destination','Platform','Incident', 'Expected']
   for detail,calling in zip(main_details,callings):
      toc = calling.find('span',class_='toc').text
      last_report = calling.find('span',class_='lr_text').text
      last_report_header = calling.find('span',class_='lr_header').text
      replacement_text = toc+last_report_header+last_report
      
      ##clean output
      calling = calling.text.replace(replacement_text,'')
      calling = cleanOutput(calling)
      replacement_text = cleanOutput(replacement_text) 
       
      if destination in calling:
         print t+":",detail.find('td',class_='time').text
         print d+":",detail.find('td',class_='dest').text
         print p+":",detail.find('td',class_='plat').text
         print i+":",detail.find('td',class_='incident').text
         print e+":",detail.find('td',class_='exp on_time').text
         print calling
         print replacement_text,'\n'


            

if __name__ == '__main__':
   ##get the departure and destination station
   departure = raw_input("departure station: ").title()
   destination = raw_input("destination station: ").title()
         
   station_codes = getJSONdata()
   file_code = getstationCode(station_codes,destination)

   ##request webpage with times using the code
   url = "https://apis.opendatani.gov.uk/translink/rendercis.asp?file="+file_code+".xml&width=full"
   soup = getWebPage(url)

   ##print the heading: "Departutres from station X info..."
   print "\n"
   heading = ' '.join(soup.find(class_='heading').text.split())
   print heading,":\n"

   ##get all the table rows, treat this as our top level
   top = soup.find_all('tr')
   ##now we can filter out results that terminate at that station
   filterForTermination(top)

   ##from the rows, get ETA,destination,platform etc for each journey
   main_details = top[1::2] 
   ##get the stations for all stops, and ETAs
   callings = top[2::2]     

   printResults(main_details,callings)
   
   sys.exit()




