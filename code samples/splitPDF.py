import os
from sys import exit
from PyPDF2 import PdfFileReader, PdfFileWriter

from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
 
import cv2
import numpy as np
from pytesseract import image_to_string

def pdf_splitter(path,pp):
    fname = os.path.splitext(os.path.basename(path))[0]
    ## exit(0) 

    pdf = PdfFileReader(path)
    os.chdir("C:\Python27\GDrive\Exams")
    for page in range(pdf.getNumPages()/pp):
        pdf_writer = PdfFileWriter()
        
        for p in range(pp):
            pdf_writer.addPage(pdf.getPage(page*pp+p))
 
        output_filename = '{}_page_{}.pdf'.format(
            fname, page+1)
 
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
 
        print('Created: {}'.format(output_filename))

        images = convert_from_path(output_filename)

        # Convert to cv2 and resize        
        im = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
        im = cv2.resize(im, None, fx=0.5, fy=0.5)
        
        # Select ROI
        if page==0:
            r = cv2.selectROI(im)
         
        # Crop image
        imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        # cv2.imshow("Resulting Image with Rectangular ROIs", imCrop)
        # cv2.waitKey()

        print('r0: {}, r1: {}, r2: {}, r3: {}'.format(r[0],r[1],r[2],r[3]))

        # Print the text in ROI
        name=image_to_string(imCrop, lang='eng')
        name.replace(' ', '')
        print name
        
        try:
            os.rename(output_filename, '{}.pdf'.format(name))
        except:
            pass


         
if __name__ == '__main__':
    path = 'Quiz1-SE-2019.pdf'
    pdf_splitter(path,2)
