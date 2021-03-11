import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import easyocr
from application import trainTicket
reader_ch = easyocr.Reader(['en', 'ch_tra']) # need to run only once to load model into memory
reader_en = easyocr.Reader(['en'])
result_en = reader_en.readtext('D:/dataset/invoice/7.jpg')
result_ch = reader_ch.readtext('D:/dataset/invoice/7.jpg')
assorted_results_ch = [{'box': bbox, 'txt': txt} for bbox, txt, _ in result_ch]
assorted_results_en = [{'box': bbox, 'txt': txt} for bbox, txt, _ in result_en]
res1 = trainTicket.trainTicket(assorted_results_ch)
res2 = trainTicket.trainTicket(assorted_results_en)
print(res1)
print(res2)