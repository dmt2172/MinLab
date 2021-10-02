#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 02:02:53 2021

@author: daveedo
"""


from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import pandas as pd
import numpy as np
import sys 
import random
import os
import glob


#Get Current directory, set as cd.
cd = os.getcwd()


#establish root for tkinter
root = Tk()
root.geometry("1440x900")
root.title('MinLab Alpha 0.0.2')

#Create Frames
selectionframe = Frame(root)
templateframe = Frame(root)
placementframe = Frame(root)


#Place Frames
selectionframe.grid(row=0, column=0)
templateframe.grid(row=0, column=1)
placementframe.grid(row=1, column=0, columnspan=2)

#Commands go here

#Browse for a spreadsheet in the Spreadsheets directory
def BrowseSheet():
    
    #global variables
    global cd
    global df
    global sheet_label
    global columns
    
    #uses filedialog to open the file. 
    sheet = filedialog.askopenfilename(title="Open a Spreadsheet", initialdir=cd+"/Spreadsheets", filetypes=(('csv files', '*.csv'), ('xlsx files', '*.xlsx')))
    
    #if user cancels then do nothing
    if sheet == '':
        pass
    
    #otherwise proceed
    else:
        #if the file is a .csv, process it into a pandas dataframe
        if sheet[-4:-1] == '.cs':
            df = pd.read_csv(sheet)
        
        #if the file is a .xlsx process it into a pandas dataframe
        elif sheet[-5:-1] == '.xls':
            df = pd.read_excel(sheet)
         
        #resets the selected sheet label
        sheet_label.grid_forget()
       
        #Selects just the name of the sheet, not the whole directory
        j=0
        while j<1:
            for i in range(len(sheet)):
                if sheet[len(sheet)-1-i] == '/':
                    sheetname = sheet[len(sheet)-i:len(sheet)]
                    j=1
                    break
                else:
                    pass
                
        #displays the condensed filename as a label.     
        sheet_label = Label(selectionframe, text='Selected Sheet: ' +sheetname)
        sheet_label.grid(row=1, column=0, columnspan=2)
    
        #get the indexes
        columns = df.columns
    
    #fill in the drop down menu
    
#Looks for a template image file and opens
def BrowseTemplate():
    #global variables
    global canvas_label
    global template_filename
    global img
    global temp_label
    
    #uses filedialog to select a template image file
    template_filename = filedialog.askopenfilename(title="Select Template Image", initialdir=cd+"/Templates", filetypes=(('jpg files', '*.jpg'), ('png files', '*.png')))
    
    #allows for the cancel option
    if template_filename == '':
        pass
    
    #If there is a choice, proceed
    else:
        #opens the image using the selected filename
        img = ImageTk.PhotoImage(Image.open(template_filename))  
        
        #resets the selected sheet label
        temp_label.grid_forget()
       
        #Selects just the name of the sheet, not the whole directory
        j=0
        while j<1:
            for i in range(len(template_filename)):
                if template_filename[len(template_filename)-1-i] == '/':
                    template_name = template_filename[len(template_filename)-i:len(template_filename)]
                    j=1
                    break
                else:
                    pass
                
        #displays the condensed filename as a label.     
        temp_label = Label(selectionframe, text='Selected Template: ' +template_name)
        temp_label.grid(row=3, column=0, columnspan=2)
        
        #preview template in the template frame
        canvas_label.grid_forget()
        canvas_label= Label(templateframe, image = img)
        canvas_label.grid(row=0, column=0)

#create widgets for selection frame
    
    #Labels
ss_label = Label(selectionframe, text= "Choose a Spreadsheet:")
sheet_label = Label(selectionframe, text='')
t_label = Label(selectionframe, text= "Choose a Template:")
temp_label = Label(selectionframe, text='')


    
    #Buttons
ss_btn = Button(selectionframe, text= "Browse", command = BrowseSheet)
t_btn = Button(selectionframe, text="Browse", command=BrowseTemplate)

#place widgets for selection frame

    #labels
ss_label.grid(row=0, column=0)
sheet_label.grid(row=1, column=0, columnspan=2)
t_label.grid(row=2, column=0)
temp_label.grid(row=3, column=0, columnspan=2)

    #buttons
ss_btn.grid(row=0, column=1)
t_btn.grid(row=2, column=1)

    

#create widgets for template frame
canvas_label = Label(templateframe)

#place widgets for template frame
canvas_label.grid(row=0, column=0)

#create widgets in placement frame

    #Labels
    
    #Variables
    
    #Buttons
    
    #Radio buttons
    
    #Check buttons
    
    #Entry boxes

#place widgets in placement frame

root.mainloop()