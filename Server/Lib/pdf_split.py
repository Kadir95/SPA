# -*- coding: utf-8 -*-
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

import cv2
import zipfile
import numpy as np
from pyzbar import pyzbar

data_path = "/home/mzp7/workspace/MEF/SPA/Server/data"
result_path="results/"

def is_zip_done(exam_uuid):
    path = os.path.join(data_path, exam_uuid)
    zip_path = os.path.join(path, "result.zip")
    if os.path.isfile(zip_path):
        return True
    return False

def zip_results(exam_uuid):
    path = os.path.join(data_path, exam_uuid)
    walk_path = os.path.join(path, result_path)
    zip_path = os.path.join(path, "result.zip")
    zipf = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(walk_path):
        for file in files:
            zipf.write(os.path.join(root, file), arcname=file)

def pdf_qrcode_reader(exam_uuid):
    path = os.path.join(data_path, exam_uuid, "original_file")
    fname = os.path.splitext(os.path.basename(path))[0]

    os.makedirs(os.path.join(data_path, exam_uuid, result_path))

    pdf = PdfFileReader(path)
    pdf_images = convert_from_path(path)
    pp=0
    barcodeData=""
    
    for page in range(pdf.getNumPages()):
        
        im = cv2.cvtColor(np.array(pdf_images[page]), cv2.COLOR_RGB2BGR)
        ## im = cv2.resize(im, None, fx=0.5, fy=0.5)
        barcodes = pyzbar.decode(im)
        barcodeData=""
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")

        if barcodeData != "":
            if pp==0:
                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(page))
                pp=1
                filename=barcodeData
            else:
                output_filename = '{}.pdf'.format(filename)
                output_filename = os.path.join(data_path, exam_uuid, result_path, output_filename)
         
                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)

                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(page))
                filename=barcodeData
        else:
            pdf_writer.addPage(pdf.getPage(page))

    output_filename = '{}.pdf'.format(filename)
    output_filename = os.path.join(data_path, exam_uuid, result_path, output_filename)

    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)
