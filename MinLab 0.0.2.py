"""
MinLab Alpha 0.0.2

This is the second iteration of the framework of MinLab, a mineral label making tool. 
The goal is to create a GUI which allows the user to quickly create many mineral labels
using a spreadsheet, a template, and a preset

date: Oct 1 2021
@author: daveedo
"""

#Importation of important modules
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from pathlib import Path
import pandas as pd
import numpy as np
import sys 
import random
import os
import glob

pathlib.Path('/Users/David 1/Desktop/Tkinter Labels/Presets/Preset 1.csv').suffix

#Get Current directory, set as cd.
cd = os.getcwd()

#empty save directory
savedir = ''

#Empty Object Class with 9 parameters
class Parameters:
    def __init__(self,name,xpos,ypos,cent,maxw,font,size,caps,sci):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.cent = cent
        self.maxw = maxw
        self.font = font
        self.size = size
        self.caps = caps
        self.sci = sci
    
#Used to iterate an empty object for each column in the selected Spreadsheet
class Option:
    def __init__(self,tup):
        self.a = [Parameters(*d) for d in tup]


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
    global cpos
    global cpos_menu
    global option
    
    #uses filedialog to open the file. 
    sheet = filedialog.askopenfilename(title="Open a Spreadsheet", initialdir=cd+"/Spreadsheets", filetypes=(('csv files', '*.csv'), ('xlsx files', '*.xlsx')))
    
    #if user cancels then do nothing
    if sheet == '':
        pass
    
    #otherwise proceed
    else:
        pathlib.Path(sheet).suffix
        #if the file is a .csv, process it into a pandas dataframe
        if pathlib.Path(sheet).suffix == '.csv':
            df = pd.read_csv(sheet)
        
        #if the file is a .xlsx process it into a pandas dataframe
        elif pathlib.Path(sheet).suffix == '.xlsx':
            df = pd.read_excel(sheet)
         
        #resets the selected sheet label
        sheet_label.grid_forget()
       
        #Selects just the name of the sheet, not the whole directory
        sheetname = Path(sheet).name
                
        #displays the condensed filename as a label.     
        sheet_label = Label(selectionframe, text='Selected Sheet: ' +sheetname)
        sheet_label.grid(row=1, column=0, columnspan=2)
    
        #get the indexes
        columns = df.columns
    
        #fill in the drop down menu
        cpos_menu.grid_forget()
        cpos.set('Select Option')
        cpos_menu = OptionMenu(placementframe, cpos, *columns, command=SelectOption)
        cpos_menu.grid(row=0, column=1)
        
    #Creates Objects and Empty Instances based on the column names
        #creates a new list to be modified
        newcolumns = list(columns)
        
        #for each position on the new list, make a list in that spot with 9 empty slots
        for i in range(len(columns)):
            newcolumns[i] = [newcolumns[i],0,0,0,0,'',0,0,0]
        
        #make that list of lists into a tuple
        tup = tuple(newcolumns)
        
        #creates the multiple blank objects       
        option = Option(tup)    
    
    #Enables some elements of the placement window:
        preset_menu['state'] = NORMAL
        cpos_label['state'] = NORMAL
        preset_label['state'] = NORMAL

    
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
        template_name = Path(template_filename).name
                
        #displays the condensed filename as a label.     
        temp_label = Label(selectionframe, text='Selected Template: ' +template_name)
        temp_label.grid(row=3, column=0, columnspan=2)
        
        #preview template in the template frame
        canvas_label.grid_forget()
        canvas_label= Label(templateframe, image = img)
        canvas_label.grid(row=0, column=0)
   
#When an Option is selected, update the placement frame to reflect the parameters of that specific option     
def SelectOption(selection):
    
    #global variables
    global columns
    global cposition
    global font_label
    global savedir
    
    
    #determine what the current position is
    for i in range(len(columns)):
        if selection == columns[i]:
            cposition = i
    
    #Enable all the widgets in Placement Frame
    font_label['state'] = NORMAL
    size_label['state'] = NORMAL
    caps_label['state'] = NORMAL
    sci_label['state'] = NORMAL
    xpos_label['state'] = NORMAL
    ypos_label['state'] = NORMAL
    maxw_label['state'] = NORMAL
    font_btn['state'] = NORMAL
    update_btn['state'] = NORMAL
    saveas_btn['state'] = NORMAL
    cent_btn['state'] = NORMAL
    ex_btn['state'] = NORMAL
    caps_btn['state'] = NORMAL
    sci_btn['state'] = NORMAL
    size_ent['state'] = NORMAL
    xpos_ent['state'] = NORMAL
    ypos_ent['state'] = NORMAL
    maxw_ent['state'] = NORMAL
    
    #Updates font label to reflect the current position
    if option.a[cposition].font == '' :
        font_label.grid_forget()
        font_label = Label(placementframe, text = 'Select Font:')
        font_label.grid(row=1, column=0)
    
    else:
        #Selects just the name of the font, not the whole directory
        font = Path(option.a[cposition].font).stem
        
        #Updates the font label
        font_label.grid_forget()
        font_label = Label(placementframe, text = 'Font: '+font)
        font_label.grid(row=1, column=0)
        
    #Updates the Caps button to be on or off
    if option.a[cposition].caps == 0:
        caps_btn.deselect()
        
    else: 
        caps_btn.select()
        
    #Updates the Sci button to be on or off
    if option.a[cposition].sci == 0:
        sci_btn.deselect()
        
    else: 
        sci_btn.select()
        
    #Updates the Radio Buttons to be on the corresponding button based on cent
    if option.a[cposition].cent == 0:
        cent_btn.select()
        
    else: 
        ex_btn.select()
        
    size_ent.delete(0,END)
    xpos_ent.delete(0,END)
    ypos_ent.delete(0,END)
    maxw_ent.delete(0,END)
    
    size_ent.insert(0, option.a[cposition].size)
    xpos_ent.insert(0, option.a[cposition].xpos)
    ypos_ent.insert(0, option.a[cposition].ypos)
    maxw_ent.insert(0, option.a[cposition].maxw)
        
    
        
#Selects font when font browse button is clicked
def SelectFont():
    
    #global variables
    global cposition
    global font_label
    
    #filedialog determines the filename
    font_filename = filedialog.askopenfilename(title="Select Font", initialdir=cd+"/Fonts", )
    
    #cancel option
    if font_filename == '':
        pass
    
    #If there is a selection, proceed:
    else:
        #updates the option to reflect the selected font
        option.a[cposition].font = font_filename
        
        #Selects just the name of the font, not the whole directory
        font = Path(font_filename).stem
        
        #updates the font label
        font_label.grid_forget()
        font_label = Label(placementframe, text = 'Font: '+font)
        font_label.grid(row=1, column=0)

# function to validate mark entry
def only_numbers(char):
    return char.isdigit()
validation = root.register(only_numbers)

#updates the value of the Caps variable
def updateCaps():
    #global variables
    global cposition
    
    #updates the value of the caps variable
    option.a[cposition].caps = caps_var.get()

#updates the value of the Sci variable
def updateSci():
    #global variables
    global cposition
    
    #updates the value of the caps variable
    option.a[cposition].sci = sci_var.get()

def updateRadio():
    #global variables
    global cposition
    
    #updates the value of the caps variable
    option.a[cposition].cent = cent_var.get()
    
def Update():
    #global variables
    global cposition
    
    #updates the values of each respective variable
    option.a[cposition].size = size_ent.get()
    option.a[cposition].xpos = xpos_ent.get()
    option.a[cposition].ypos = ypos_ent.get()
    option.a[cposition].maxw = maxw_ent.get()

#Updates Object instances to reflect the values stored in a preset, or do nothing if 'no preset' is selected
def Preset():
    
    #global variables
    
    pass 
def Save():
    pass

#saves the options and values to a .csv file.
def Saveas():
    
    #global variables
    global f
    global columns
    global sf
    global save_btn
    
    #prompts user to select location and name of the preset they wish to create
    savedir = filedialog.asksaveasfilename(defaultextension=".csv", initialdir=cd+"/Presets")
    if savedir is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    
    #creates a list of list of the objects
    savelist = []
    for i in range(len(columns)):
        savelist.append([option.a[i].name,option.a[i].xpos,option.a[i].ypos,option.a[i].cent,option.a[i].maxw,option.a[i].font,option.a[i].size,option.a[i].caps,option.a[i].sci])
    
    #creates a list with the indexes for the save file
    savecolumns = ['name','xpos','ypos','cent','maxw','font','size','caps','sci']
    
    #createsa pandas database with the Object data and Indexes
    sf = pd.DataFrame(savelist, columns=savecolumns)
    
    #saves this database to the indicated save directory
    sf.to_csv(savedir)
    
    #Activates the regular save button if it has not been updated already
    save_btn['state'] = NORMAL

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
cpos_label = Label(placementframe, text='Choose Option to edit:')
preset_label = Label(placementframe, text='Choose Preset:')
font_label = Label(placementframe, text='Select Font:')
size_label = Label(placementframe, text='Size:')
caps_label = Label(placementframe, text='All Caps?')
sci_label = Label(placementframe, text='Scientific Formula?')
xpos_label = Label(placementframe, text='X Position:')
ypos_label = Label(placementframe, text='Y Position:')
maxw_label = Label(placementframe, text='Maximum Width:')


    #Variables
cpos = StringVar()
cpos.set('Choose a Spreadsheet')
columns = []

preset = StringVar()
preset.set('Choose a Preset')
path = cd + "/Presets"
extension = 'csv'
os.chdir(path)
result = glob.glob('*.{}'.format(extension))

cent_var = IntVar()
caps_var = IntVar()
sci_var = IntVar()
    
    #Buttons
font_btn = Button(placementframe, text= 'Browse', command=SelectFont)
update_btn = Button(placementframe, text='Update' , command=Update)
save_btn = Button(placementframe, text='Save' , command=Save)
saveas_btn = Button(placementframe, text='Save as' , command=Saveas)

    #Radio Buttons
cent_btn = Radiobutton(placementframe, text="Centered around point", variable=cent_var, value=0, command=updateRadio)
ex_btn = Radiobutton(placementframe, text="Exact Point", variable=cent_var, value=1, command=updateRadio)

    #Check Buttons
caps_btn = Checkbutton(placementframe, variable=caps_var, command=updateCaps)
sci_btn = Checkbutton(placementframe, variable=sci_var, command=updateSci)
    
    #Option  menu
cpos_menu = OptionMenu(placementframe, cpos, cpos, *columns, command=SelectOption)
preset_menu = OptionMenu(placementframe, preset,'No Preset', *result)
    
    #Entry boxes
size_ent = Entry(placementframe, validate='key', validatecommand=(validation, '%S'))
xpos_ent = Entry(placementframe, validate='key', validatecommand=(validation, '%S'))
ypos_ent = Entry(placementframe, validate='key', validatecommand=(validation, '%S'))
maxw_ent = Entry(placementframe, validate='key', validatecommand=(validation, '%S'))

#place widgets in placement frame
    
    #Labels
cpos_label.grid(row=0 , column=0)
preset_label.grid(row=0 , column=2 )
font_label.grid(row=1 , column=0 )
size_label.grid(row=1 , column=2 )
caps_label.grid(row=1 , column=4 )
sci_label.grid(row=1 , column=6 )
xpos_label.grid(row=2 , column=0 )
ypos_label.grid(row=2 , column=2 )
maxw_label.grid(row=2 , column=4 )
    
    
    #Buttons
font_btn.grid(row=1 , column=1)
update_btn.grid(row=4 , column=5)
save_btn.grid(row=4 , column=6)
saveas_btn.grid(row=4 , column=7)

    #Radio Buttons
cent_btn.grid(row=3 , column=0)
ex_btn.grid(row=3 , column=1)

    #Check Buttons
caps_btn.grid(row=1, column=5)
sci_btn.grid(row=1, column=7) 

    #Option Menus
cpos_menu.grid(row=0, column=1)
preset_menu.grid(row=0, column=3)
    
    #Entry Boxes
size_ent.grid(row=1, column=3)
xpos_ent.grid(row=2, column=1)
ypos_ent.grid(row=2, column=3)
maxw_ent.grid(row=2, column=5)
    
#Disables inactive widgets in Placement Frame
    
    #Labels
cpos_label['state'] = DISABLED
preset_label['state'] = DISABLED
font_label['state'] = DISABLED
size_label['state'] = DISABLED
caps_label['state'] = DISABLED
sci_label['state'] = DISABLED
xpos_label['state'] = DISABLED
ypos_label['state'] = DISABLED
maxw_label['state'] = DISABLED

    #Buttons
font_btn['state'] = DISABLED
update_btn['state'] = DISABLED
save_btn['state'] = DISABLED
saveas_btn['state'] = DISABLED

    #Radio Buttons
cent_btn['state'] = DISABLED
ex_btn['state'] = DISABLED

    #Check Buttons
caps_btn['state'] = DISABLED
sci_btn['state'] = DISABLED

    #Option Menu
cpos_menu['state'] = DISABLED
preset_menu['state'] = DISABLED

    #Entry Boxes
size_ent['state'] = DISABLED
xpos_ent['state'] = DISABLED
ypos_ent['state'] = DISABLED
maxw_ent['state'] = DISABLED

#established the mainloop of the tkinter root
root.mainloop()