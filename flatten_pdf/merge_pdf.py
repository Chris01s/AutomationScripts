#!/usr/bin/python3

import os
import time
import shutil
import glob
import argparse
from PyPDF2 import PdfFileMerger
import logging

class ArgParser:
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            description="""Process for splitting up pdf file into seperate pages.
                                    Output is move to a new folder, specified by user or
                                    created by using the filename"""
        )

    def add_input(self):
        self.arg_parser.add_argument(
            "--input",
            help="filepath to folder of pdfs to merge",
            required=True,
            type=str
        )

    def add_output(self):
        self.arg_parser.add_argument(
            "--output",
            help="Filename to put merged pdfs",
            required=False,
            type=str
        )

    def get_args(self):
        self.add_input()
        self.add_output()



class PDF_Merge:
	def __init__(self, folder_in, file_out):
		self.folder_in = folder_in
		self.file_out = file_out
		self.pdf_merger = PdfFileMerger()


	def get_pdf_filenames(self):
		try:
			self.pdf_filenames = sorted(glob.glob(self.folder_in+"/*.pdf"))
		except Exception as ex:
			logging.info("[+] Something went wrong reading the pdf file", exc_info=True)
			sys.exit()


	def merge_pdf_files(self):
		for pdf in self.pdf_filenames:
			logging.info("[+] Merging: {}".format(pdf))
			self.pdf_merger.append(pdf)
	
	
	def write_new_merged_pdf(self):
		self.pdf_merger.write(self.file_out)
		logging.info("[+] Merged files complete...")
		logging.info("[+] Merged to {}".format(self.file_out))


	def do_merge(self):
		self.get_pdf_filenames()
		self.merge_pdf_files()
		self.write_new_merged_pdf()



if __name__ == "__main__":
	logging.basicConfig(
		format='%(asctime)s - %(message)s', 
		level=logging.INFO
	)
	arg_parser_obj = ArgParser()
	arg_parser_obj.get_args()
	args = arg_parser_obj.arg_parser.parse_args()

	folder_in = args.input
	file_out = args.output

	pdf_merger_obj = PDF_Merge(
		folder_in  = folder_in,
		file_out = file_out
	)

	pdf_merger_obj.do_merge()

    
    




