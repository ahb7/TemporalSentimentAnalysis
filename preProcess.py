# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 12:37:58 2016

@author: Abdullah
"""
import xlsxwriter

workbook = xlsxwriter.Workbook('AllComments.xlsx')
worksheet = workbook.add_worksheet()

fd = open('allComments.txt', 'r')

row = 0
col = 0
worksheet.write(row, col, "Author")
worksheet.write(row, col+1, "Comment")
worksheet.write(row, col+2, "Date")
worksheet.write(row, col+3, "Time")
worksheet.write(row, col+4, "Type")

row = 1
col = 0

while True:
    text = fd.readline()
    if not text:
        break
    
    if 'authorDisplayName' in text:
        list1 = text.split(":")
        author = list1[1]
        author = author.strip()
        author = author.lstrip('\" ,')
        author = author.rstrip('\" ,')
        worksheet.write(row, col, author)
    
    if 'publishedAt' in text:
        list1 = text.split(":")
        tmp1 = list1[1]
        min = list1[2]
        tmp2 = list1[3]
        
        list2 = tmp1.split("T")
        dt = list2[0]
        hr = list2[1]
        sec = tmp2.split(".")[0]
        
        tm = ":".join([hr, min, sec])
        dt = dt.strip()
        dt = dt.strip('\" ')
        worksheet.write(row, col+2, dt)
        worksheet.write(row, col+3, tm)
        
    if 'textDisplay' in text:
        list1 = text.split(":")
        cmnt = list1[1]
        cmnt = cmnt.strip()
        cmnt = cmnt.lstrip('\" ,')
        cmnt = cmnt.rstrip('\" ,')
        worksheet.write(row, col+1, cmnt)
        
    if 'topLevelComment' in text:
        type = 'Top Level'
        
    if 'replies' in text:
        type = 'Reply'
              
    if 'updatedAt' in text:
        worksheet.write(row, col+4, type)
        row += 1
        col = 0
    
workbook.close()
fd.close()
