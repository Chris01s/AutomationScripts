#!/bin/python 

from bs4 import BeautifulSoup
from .requests_class import GetRequests


class GetSoup(GetRequests):
	def get_soup(self):
		if self.status_code == 200:
			self.soup = BeautifulSoup(
				markup = self.response.text,
				features = "html.parser"
			)
		else:
			print("Something went wrong", self.response.reason)
			sys.exit()
