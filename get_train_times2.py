#!/bin/python

import xml.etree.cElementTree as ETc
import json, requests, os
from prettytable import PrettyTable




def getStationCodesFromTranslinkAPI():
   json_data = requests.get("https://apis.opendatani.gov.uk/translink/")
   station_codes = json_data.json() 
   json_data.close()
   return station_codes
   


def downloadXMLcodeFromTranslinkAPI():
   url = 'https://apis.opendatani.gov.uk/translink/'+file_code+'.xml'
   os.system('wget -O translink_data.xml '+url)

     
     
def getStationCodeForDeparturePoint(station_codes,departure_station):
   for station in station_codes['stations']:
      if station[u'name'] == departure_station:
         file_code = str(station[u'code'])
         return file_code
   
   

def checkIfServiceIsTerminating(service):
   service_type = service.find('ServiceType').attrib['Type']
   return service_type != 'Terminating'



def getItemsOfInterest(service):
   destination = service.find('Destination1').attrib
   arrival_time = service.find('ArriveTime').attrib
   platform = service.find('Platform').attrib
   departure_time = service.find('DepartTime').attrib
   last_report = service.find('LastReport').attrib
   return destination,arrival_time,platform,departure_time,last_report
   
   
   
def checkIfDestinationInListOfCallingPoints(requested_destination,destination,calling_points):
   names = [calling_point.attrib['Name'] for calling_point in calling_points] 
   return (requested_destination in names) or (requested_destination==destination['name'])



def printTopLevelResults(destination,arrival_time,platform,departure_time,last_report):
   print 'Destination:',destination['name']
   print "Arrival time:",arrival_time['time']
   print "Arrived:",arrival_time['Arrived']
   print "Departure Time:",departure_time['time']
   print 'Destination time:',destination['ttarr']
   print "Platform:",platform['Number']
   print "Platform Changed:",platform['Changed']
   print getLatestUpdate(last_report)
   print checkForDelays(service)
   print("Calling at:...\n")
   


def getLatestUpdate(last_report):
   if last_report['station1']=="":
      return "No report"
   else:
      return "Last Report: at "+last_report['station1']+" ("+last_report['time']+')'
      
      

def checkForDelays(service):
   delays = service.find('Delay').attrib
   if delays['Minutes'] != "0":
      delays_cause = service.find('DelayCause').attrib
      return "Delayed by: "+delays['Minutes']+" mins; "+delays_cause.text 
   else:
      return "Delays: No delays"
         

         
def buildTableForCallingPoints(calling_point,results_table):
   station = calling_point['Name']
   arrival_time = calling_point['ttarr']
   departure_time = calling_point['ttdep']
   eta = calling_point['etarr']
   etd = calling_point['etdep']
   results_table.add_row([station,arrival_time,departure_time,eta,etd])



def printTableResults(calling_points,results_table):             
   for calling_point in calling_points:
      buildTableForCallingPoints(calling_point.attrib,results_table)
   print(results_table)
   print("\n")




if __name__ == '__main__':

   ##get the departure and destination station
   departure_station = raw_input("departure station: ").strip().title()
   requested_destination = raw_input("destination station: ").strip().title()

   ##request station codes
   station_codes = getStationCodesFromTranslinkAPI()
   file_code = getStationCodeForDeparturePoint(station_codes,departure_station)

   downloadXMLcodeFromTranslinkAPI()

   ##get top level tags
   tree = ETc.parse('translink_data.xml')
   services = tree.findall('Service')

   for service in services:
      if checkIfServiceIsTerminating(service):
         calling_points = service.find('Dest1CallingPoints')
         destination,arrival_time,platform,departure_time,last_report = getItemsOfInterest(service)
         
         if checkIfDestinationInListOfCallingPoints(requested_destination,destination,calling_points): 
            results_table = PrettyTable(['Station','arrival','departure','ETA','ETD'])
            printTopLevelResults(destination,arrival_time,platform,departure_time,last_report)
            printTableResults(calling_points,results_table)

            
            
            

