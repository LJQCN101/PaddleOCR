#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from apphelper.image import union_rbox
import re
class trainTicket:
    """
    火车票结构化识别
    """
    def __init__(self,result, img=None):
        self.result = union_rbox(result,0.2)
        self.img = img
        self.type = None
        self.N = len(self.result)
        self.res = {}
        self.address()
        self.time()
        self.price()
        self.customer_num()
        print(self.res)
        
    def address(self):
        station={}
        relevant_info = False
        occurence = 0
        current_y = 0
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')

            type_res = re.findall('CLP',txt)
            if len(type_res) > 0:
                self.type = 'CLP'

            if self.type == 'CLP':
                if float(self.result[i]['cx']) / float(self.img.shape[0]) < 0.48:
                    continue

            relevant_res = re.findall('[一-龥]+地址',txt), re.findall('圖文+[一-龥]',txt), re.findall('Towngas',txt), re.findall('Water',txt)
            if len(relevant_res[0]) > 0 or len(relevant_res[1]) > 0 or len(relevant_res[2]) > 0 or len(relevant_res[3]) > 0:
                relevant_info = True

            if relevant_info:
                res = re.findall('[A-Z]{2,50}', txt)
                if len(res)>0:
                    y = self.result[i]['cy']
                    if current_y < y - 3.0 or current_y > y + 3.0:
                        occurence += 1
                        station['Address' + str(occurence)] = ''
                        current_y = y
                    station['Address' + str(occurence)] += self.result[i]['text'] + ' '
                    self.res.update(station)
            if occurence >= 5:
                break
    
    def time(self):
        time={}
        relevant_info = False
        for i in range(self.N):
            if self.type == 'CLP':
                if float(self.result[i]['cx']) / float(self.img.shape[0]) < 0.48:
                    continue

            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            relevant_res = re.findall('請於', txt), re.findall('在此日期或之前+[一-龥]', txt),re.findall('限期', txt)
            if len(relevant_res[0]) or len(relevant_res[1]) > 0 or len(relevant_res[2]) > 0:
                relevant_info = True
            ##匹配日期

            if relevant_info:
                res1, res2, res3 = re.findall('[0-9]{1,4}年[0-9]{1,2}月[0-9]{1,2}日',txt),\
                                   re.findall('[0-9]{1,4}/[0-9]{1,2}/[0-9]{1,2}',txt),\
                                   re.findall('[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}',txt)
                if len(res1)>0:
                    time['date'] = res1[0]
                    self.res.update(time)
                    break
                if len(res2)>0:
                    time['date'] = res2[0]
                    self.res.update(time)
                    break
                if len(res3)>0:
                    time['date'] = res3[0]
                    self.res.update(time)
                    break
    
    def price(self):
        price={}
        relevant_info = False
        for i in range(self.N):
            if self.type == 'CLP':
                if float(self.result[i]['cx']) / float(self.img.shape[0]) < 0.48:
                    continue

            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            ##价格

            relevant_res = re.findall('付款通知', txt), re.findall('付+[一-龥]', txt), re.findall('缴款', txt), re.findall('總数', txt)
            if len(relevant_res[0]) or len(relevant_res[1]) > 0 or len(relevant_res[2]) > 0 or len(relevant_res[3]) > 0:
                relevant_info = True

            if relevant_info:
                res, res2 = re.findall('\$[0-9]{1,4}\.[0-9]{1,2}',txt), re.findall('[0-9]{1,4}\.[0-9]{1,2}',txt)
                if len(res)>0:
                    price['price']  =res[0].replace('$','')
                    self.res.update(price)
                    break
                if len(res2)>0:
                    price['price']  =res2[0]
                    self.res.update(price)
                    break

    def customer_num(self):
        customer_number = {}
        relevant_info = False
        for i in range(self.N):
            if self.type == 'CLP':
                if float(self.result[i]['cx']) / float(self.img.shape[0]) < 0.48:
                    continue

            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')

            relevant_res = re.findall('用户號', txt), re.findall('[一-龥]+號', txt)
            if len(relevant_res[0]) or len(relevant_res[1]) > 0:
                relevant_info = True

            if relevant_info:
                res = re.findall('[0-9]{1,5}-[0-9]{1,5}-[0-9]{1,2}', txt), re.findall('[0-9]{11,15}', txt)
                if len(res[0]) > 0:
                    customer_number['customer_number'] = res[0][0]
                    self.res.update(customer_number)
                    break

                if len(res[1]) > 0:
                    customer_number['customer_number'] = res[1][0]
                    self.res.update(customer_number)
                    break
                
                
        