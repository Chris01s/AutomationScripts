#!/usr/bin/python3

import os
import sys
import shutil 
import sys
import subprocess
from merge_pdf import PDF_Merge
from split_pdf import PDF_Split
import logging
from glob import glob
import threading


try:
	import PyPDF2
except:
	logging.info("[!!] Requires PyPDF2 reader library...")
	logging.info("e.g. pip install PyPDF2")
	sys.exit()


class PDF_Flatten:
	def __init__(self, in_pdfFile, out_pdfFile):
		self.in_pdf = in_pdfFile
		self.out_pdf = out_pdfFile
		self.folder_out = self.out_pdf.replace(".","_").replace(" ","")
		
	def check_if_imagemagick_installed(self):
		return "ImageMagick" in os.popen("convert --version").read()
	
	def create_temp_folder(self, folder_name):
		if not os.path.exists(folder_name):
			os.mkdir(folder_name)

	def split_pdf(self):
		self.create_temp_folder(
			folder_name = self.folder_out+"_pages"
		)
		pdf_splitter_obj = PDF_Split(
			fname  = self.in_pdf,
			folder_out = self.folder_out+"_pages",
			verbose = True
		)
		try:
			pdf_splitter_obj.split_pdf()
		except FileExistsError:
			logging.exception(
				"Error: File has already been split: split a new file or give new output filename",
				exc_info=True
			)
			os.system("python split_pdf.py --h")
			sys.exit()

	def convert_pdf_to_img(self, page):
		logging.info("[*] Converting {} to image...".format(page))
		run_imagemagick = subprocess.check_output(
			'convert -density 300 -flatten "{}" "{}"'.format(page, page+".pdf"), 
			shell=True
		)
		shutil.move(page+".pdf", self.folder_out+"_imgs")
		logging.info("[+] {} now in {}...".format(page+".pdf", self.folder_out+"_imgs"))
			
	def convert_pdf_pages_to_imgs(self):
		pdf_pages_filepaths = sorted(glob(self.folder_out+"_pages/*.pdf"))
		self.create_temp_folder(
			folder_name = self.folder_out+"_imgs"
		)
		for page in pdf_pages_filepaths:
			self.convert_pdf_to_img(page)
		
		
	def merge_images(self):
		pdf_merger_obj = PDF_Merge(
			folder_in  = self.folder_out+"_imgs",
			file_out = self.out_pdf
		)

		pdf_merger_obj.do_merge()
		
	
	def clean_up(self):
		logging.info("[+] Cleaning up...")
		shutil.rmtree(self.folder_out+"_pages")
		shutil.rmtree(self.folder_out+"_imgs")
		
		


if __name__ == "__main__":
	logging.basicConfig(
		format='%(asctime)s - %(message)s', 
		level=logging.INFO
	)
	
	if len(sys.argv) < 3:
		print("Usage: python3 {} [pdffile] [output.pdf]".format(sys.argv[0]))
		sys.exit()
		
	pdf_file = sys.argv[1]
	output_file = sys.argv[2]
	
	flatten_pdf_obj = PDF_Flatten(pdf_file, output_file)
	
	if not flatten_pdf_obj.check_if_imagemagick_installed():
		logging.info("[!!] ImageMagick needs to be installed...")
		sys.exit()
	
	flatten_pdf_obj.split_pdf()
	flatten_pdf_obj.convert_pdf_pages_to_imgs()
	flatten_pdf_obj.merge_images()
	flatten_pdf_obj.clean_up()
	
	logging.info("[+] Flatten Complete!!")
	

		
	
		
