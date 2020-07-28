#!/usr/bin/python3

import os
import shutil
import argparse
import logging
from PyPDF2 import PdfFileWriter, PdfFileReader


class ArgParser:
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            description="""Process for splitting up pdf file into seperate pages.
                                    Output is move to a new folder, specified by user or
                                    created by using the filename"""
        )

    def add_verbose(self):
        self.arg_parser.add_argument(
            "--verbose",
            help="monitor the output",
            required=False,
            default=False,
            type=bool
        )

    def add_input(self):
        self.arg_parser.add_argument(
            "--input",
            help="filepath to pdf to split",
            required=True,
            type=str
        )

    def add_output(self):
        self.arg_parser.add_argument(
            "--output",
            help="folder to put split pdfs",
            required=False,
            type=str
        )

    def get_args(self):
        self.add_verbose()
        self.add_input()
        self.add_output()



class PDF_Split:
    def __init__(self, fname, folder_out, verbose):
        self.fname = fname
        self.folder_out = folder_out
        self.verbose = verbose


    def read_pdf(self):
        try:
            self.pdf_file_obj = PdfFileReader(self.fname)
        except Exception as ex:
            logging.exception("[!] Something went wrong reading the pdf file", exc_info=True)
            sys.exit()


    def make_folder(self):
        if not self.folder_out:
            self.folder_out = self.fname.replace(".pdf", "_split")
        
        if not os.path.exists(self.folder_out):
        		os.mkdir(self.folder_out)
        
        if self.verbose:
            logging.info("[+] {} folder created for split pages".format(self.folder_out))


    def get_page_length(self):
        self.number_of_pages = self.pdf_file_obj.getNumPages()
        if self.verbose:
            logging.info("[*] No. of pages: {}".format(self.number_of_pages))


    def get_current_page(self):
        self.current_page = self.pdf_file_obj.getPage(self.page_number)


    def get_pdf_writer(self):
        self.pdf_writer_obj = PdfFileWriter()


    def add_page_to_pdf_writer(self):
        self.pdf_writer_obj.addPage(self.current_page)


    def write_pdf_page_to_file(self):
        if self.verbose:
                logging.info("[+] Splitting page {}".format(self.page_number+1))
        self.output_fname ="{}_page_{}.pdf".format(
        		self.fname, 
        		str(self.page_number+1).zfill(self.zfill_length)
        )
        with open(self.output_fname,"wb") as out:
            self.pdf_writer_obj.write(out)


    def move_page_to_folder_out(self):
        try:
            shutil.move(self.output_fname, self.folder_out)
        except Exception:
            logging.exception("[!] {} already exists".format(self.output_fname), exc_info=True)


    def print_verbose_output(self):
        self.output_fname = os.path.basename(self.output_fname)
        if self.verbose:
            logging.info("[+] Created: {}".format(self.output_fname))
            logging.info("[+] File moved to {}\n".format(self.folder_out))


    def split_pdf(self):
        self.read_pdf()
        self.get_page_length()
        self.zfill_length = len(str(self.number_of_pages))
        self.make_folder()
        for page in range(self.number_of_pages):
            self.page_number = page
            self.get_current_page()
            self.get_pdf_writer()
            self.add_page_to_pdf_writer()
            self.write_pdf_page_to_file()
            self.move_page_to_folder_out()
            self.print_verbose_output()
  


if __name__ == "__main__":
	logging.basicConfig(
		format='%(asctime)s - %(message)s', 
		level=logging.INFO
	)
	arg_parser_obj = ArgParser()
	arg_parser_obj.get_args()
	args = arg_parser_obj.arg_parser.parse_args()

	fname = args.input
	folder_out = args.output
	verbose = args.verbose
	pdf_splitter_obj = PDF_Split(
		fname  = fname,
		folder_out = folder_out,
		verbose = verbose
	)
	try:
		pdf_splitter_obj.split_pdf()
	except FileExistsError:
		logging.exception("Error: File has already been split: split a new file or give new custom folder\n", exc_info=True)
		os.system("python split_pdf.py --h")
		 
    




