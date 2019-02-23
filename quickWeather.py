import json,requests,sys,pprint

#get location from commandline arguments
if len(sys.argv) < 2:
   print "Usage: quickWeather.py location"
   sys.exit()
 
location = ''.join(sys.argv[1:])
appid_key = '0f3a11e987f854c89289f94b33ddec5c'

#: download json data from openweathermap.org api
url = 'https://api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s'%(location,appid_key)
response = requests.get(url)
response.raise_for_status()

#: load json data into python variable
weatherData = json.loads(response.text)

#print weather desc
w = weatherData['list']
print "Current weather in %s:"%(location)
print w[0]['weather'][0]['main'],'-',w[0]['weather'][0]['description']
print '\n'
print 'Tomorrow:'
print w[1]['weather'][0]['main'],'-',w[1]['weather'][0]['description']
print '\n'
print 'Day after tomorrow:'
print w[2]['weather'][0]['main'],'-',w[2]['weather'][0]['description']
