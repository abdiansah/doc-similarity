#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 09:58:31 2020

@author: abdiansah (abdiansah@unsri.ac.id)

"""

import csv
from nltk import word_tokenize
import os, subprocess
from fpdf import FPDF
import math

class DocSimilarity:
    
    __cluster = []
    __threshold = 0
    
    def __cosine_similarity(self, teks1, teks2):
    
        x = word_tokenize(teks1)
        y = word_tokenize(teks2)
        
        x = set(x)
        y = set(y)
         
        l1 =[]
        l2 =[]
        
        rvector = x.union(y)  
        
        for w in rvector:
            if w in x:
                l1.append(1) # create a vector 
            else:
                l1.append(0)
        
            if w in y:
                l2.append(1)
            else:
                l2.append(0)
        c = 0
        for i in range(len(rvector)):
            c+= l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)
        
        return cosine
    
    def cek_kemiripan(self, data, threshold, verbose=False): # data2D [idx, teks]
        self.__cluster = [data[i][0] for i in range(0, len(data))]
        self.__threshold = threshold
        c = 1
        for i in range(0, len(data)):
            for j in range(i+1, len(data)):        
                sim = self.__cosine_similarity(data[i][1], data[j][1])
                if data[i][0] != data[j][0]:
                    if (sim >= self.__threshold):
                        self.__cluster[i]+=' {}'.format(data[j][0])
                    if verbose:
                        print('{}. Similarity({},{}): {:.2f}'.format(c, data[i][0], data[j][0], sim))
                    c+=1

    def tampilkan_hasil(self):
        print('Klaster kemiripan dengan nilai ambang batas = {}'.format(self.__threshold))
        c = 1
        for cls in self.__cluster:
            print('{}. {}'.format(c, cls))
            c+=1
    
    
    def ekstrak_csv(self, path_file, col_idx, col_text, pemisah=',', remove_header=True):
        data = []
        with open(path_file) as f:
            t = csv.reader(f, delimiter=pemisah)
            for r in t:
                data.append((r[col_idx],r[col_text])) # ambil idx dan teks
            if remove_header:
                data.remove((data[0][0], data[0][1])) # remove header (baris pertama)
            data = sorted(data)
        
        return data
    
    def ekstrak_filename(self, path, startpos, endpos): # nama idx dan text sama (mis. nim, nim.pdf)
        entries = os.listdir(path)
        rec = [] # [idx, nama_file pdf]
        
        for e in entries:
            clip = e[startpos: endpos]
            if str.isalnum(clip): # cek utk ambil angka saja (mis. nim)
                rec.append([clip,e]) # bisa dibuah sesuai kebutuhan
                
        return rec
    
    def ekstrak_pdf(self, path, rec):
        data = []
        for idx, filename in rec:
            args = ["/usr/bin/pdftotext",
                    '-enc',
                    'UTF-8',
                    "{}/{}".format(path, filename),
                    '-']
            res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = res.stdout.decode('utf-8')
            data.append([idx, output])
            
        return data
    
    def text2pdf(self, idx, teks, folder): # [idx, teks] - masih perlu perbaikan
        pdf = FPDF()
        pdf.add_page() 
        pdf.set_font('Arial', size = 10) 
        for d in teks.split('\n'):
            if len(d) > 84:                 # maks length teks = 84, jika lebih diturunkan ke bawah
                n = math.ceil(len(d)/84)
                s = 0
                e = 84
                for i in range(n):
                    t = d[s:e]
                    s = e
                    e = e + 84
                    pdf.cell(100, 5, t, ln = 1)
            else:
                pdf.cell(100, 5, d, ln = 1)
        pdf.output('{}/{}.pdf'.format(folder, idx)) # buat folder manual