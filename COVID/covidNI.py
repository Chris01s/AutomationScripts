from bs4 import BeautifulSoup
import datetime
from requestSender import Request


class NI(Request):
	def __init__(self):
		self.url = "https://www.health-ni.gov.uk/news?search=%22Current+R+Number+estimate"
		Request.__init__(self, self.url)
	
	def get_articles(self):
		return self.soup.find_all("div",{"class":"columnItem"})
		
	def get_date_of_publication(self, article):
		return article.p.text.replace("Published","").strip()
	
	def convert_date_to_int(self, date):
		date = datetime.datetime.strptime(date, "%d %B %Y")
		date = date.strftime("%Y%m%d")
		return int(date)
	
	def get_links_and_publication_dates(self, articles):
		for article in articles:
			if "R NUMBER" in article.a.text.upper():
				publicationDate = self.get_date_of_publication(article)
				publicationDate = self.convert_date_to_int(publicationDate)
				self.publicationDates.append(publicationDate)
				
				link = article.a['href']
				self.links.append(link)
	
	def get_r_number(self):
		return self.soup.strong.text.strip()
		
	def covid_r_estimate(self):
		self.send_request()
		self.soup = BeautifulSoup(self.response.text, features = "html5lib")
		articles = self.get_articles()
		
		self.publicationDates = []
		self.links = []
		
		self.get_links_and_publication_dates(articles)
		
		latestPublicationDate = max(self.publicationDates)
		index_of_latest_publication_date = self.publicationDates.index(latestPublicationDate)
		latest_link = self.links[index_of_latest_publication_date]
		latest_link = self.parse_link(
			base_url = self.url, 
			link = latest_link
		)
		
		self.url = latest_link
		self.send_request()
		self.soup = BeautifulSoup(self.response.text, features = "html5lib")
		
		publicationDate = self.soup.find("span",{"class":"date-display-single"}).text
		r_number = self.get_r_number()
		print(f"\n\t\t\tAs of {publicationDate}\n\t\t\t{r_number}")
		

if __name__=="__main__":
	covidni_obj = NI()
	covidni_obj.covid_r_estimate()		

