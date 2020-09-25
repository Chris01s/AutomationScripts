from bs4 import BeautifulSoup
import datetime
from requestSender import Request


class ENG(Request):
	def __init__(self):
		self.url = "https://www.gov.uk/guidance/the-r-number-in-the-uk"
		Request.__init__(self, self.url)
	
	def get_main_update_panel(self):
		return self.soup.find("div", {"class":"govspeak"})
	
	def get_r_number(self):
		headline_element = self.update_panel.find("aside")
		return headline_element.p.text
		
	def get_date_of_latest_update(self):
		return self.update_panel.p.text
	
	def get_table(self):
		return self.soup.table
		
	def get_table_header(self, table):
		return table.thead
		
	def get_table_body(self, table):
		return table.tbody
	
	def print_table_head(self, table_head):
		for value in table_head.find_all("th"):
			print("  "+value.text, end="\t")
		print("\n")
		
	def print_row_values(self, row):
		print("  "+row.th.text, end="\t")
		for value in row.find_all("td"):
			print("  "+value.text,end="\t")
		print("\n")
		
	def covid_r_estimate(self):
		self.send_request()
		self.soup = BeautifulSoup(self.response.text, features = "html5lib")
		
		self.update_panel = self.get_main_update_panel()
		date_of_last_update = self.get_date_of_latest_update()
		r_number = self.get_r_number()
		print(f"\n\t\t\t{date_of_last_update}\n\t\t\t{r_number}")
		
		regional_table = self.get_table()
		table_head = self.get_table_header(regional_table)
		self.print_table_head(table_head)
		
		table_body = self.get_table_body(regional_table)
		for row in table_body:
			try:
				self.print_row_values(row)
			except:
				pass

if __name__=="__main__":
	covidni_obj = ENG()
	covidni_obj.covid_r_estimate()		

