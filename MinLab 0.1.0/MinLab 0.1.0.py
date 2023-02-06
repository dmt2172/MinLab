"""
MinLab Alpha 0.1.0

This is the first "release" of MinLab. I have finally gotten it to a point 
where all the features which exist have been implemented. Many more need to be added
which have been discovered along the way. As each feature is added, an additional
number will be added to the 3rd decimal. MinLab 0.1.1 is the next update. 
MinLab 0.2.0 will be when the Beta begins and I send it to people other than Ben and Wyatt

date: Jan 01 2022
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

from PIL import Image as IM
from PIL import ImageDraw as ID
from PIL import ImageFont as IF



#Get Current directory, set as cd.
cd = os.getcwd()

#empty save directory
savedir = ''

#Condition Checker. 0 if not met, 1 if met
CC = [0,0,0,0,0,0]

'''
1. Spreadsheet chosen?
2. Template chosed?
3. Option/Preset chosen?
4. Indeces chosen?
5. Savename format chosen?
6. Save directory chosen?
'''

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
root.title('MinLab Alpha 0.1.0')

#Create Frames
selectionframe = Frame(root)
templateframe = Frame(root)
placementframe = Frame(root)
itemframe = Frame(root)


#Place Frames
selectionframe.grid(row=0, column=0)
templateframe.grid(row=0, column=1)
placementframe.grid(row=1, column=0)
itemframe.grid(row=1, column=1)

#Commands go here

#Browse for a spreadsheet in the Spreadsheets directory
def BrowseSheet():
    
    #global variables
    global cd
    global sheetDataFrame
    global sheet_label
    global columns
    global cpos
    global cpos_menu
    global option
    global index_var
    global index_menu
    global save_box
    
    #uses filedialog to open the file. 
    sheet = filedialog.askopenfilename(title="Open a Spreadsheet", initialdir=cd+"/Spreadsheets", filetypes=(('csv files', '*.csv'), ('xlsx files', '*.xlsx')))
    
    #if user cancels then do nothing
    if sheet == '':
        pass
    
    #otherwise proceed
    else:
        #if the file is a .csv, process it into a pandas dataframe
        if Path(sheet).suffix == '.csv':
            sheetDataFrame = pd.read_csv(sheet)
        
        #if the file is a .xlsx process it into a pandas dataframe
        elif Path(sheet).suffix == '.xlsx':
            sheetDataFrame = pd.read_excel(sheet)
         
        #resets the selected sheet label
        sheet_label.grid_forget()
       
        #Selects just the name of the sheet, not the whole directory
        sheetname = Path(sheet).name
                
        #displays the condensed filename as a label.     
        sheet_label = Label(selectionframe, text='Selected Sheet: ' +sheetname)
        sheet_label.grid(row=1, column=0, columnspan=2)
    
        #get the indexes
        columns = sheetDataFrame.columns
    
        #fill in the drop down menu for placement frame
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
        
        #Activates inactive widgets in item frame
        showop_lab['state'] = NORMAL
        saveop_lab['state'] = NORMAL
        text_lab['state'] = NORMAL
        example_lab['state'] = NORMAL
        index_menu['state'] = NORMAL
        option_box['state'] = NORMAL
        save_box['state'] = NORMAL
        
        #fill in index menu in item frame
        index_menu.grid_forget()
        index_var.set('Select Index')
        index_menu = OptionMenu(itemframe, index_var, *columns, command=selectIndex)
        index_menu.grid(row=0, column=1)
        
        #fill in the listbox for choosing a save name
        save_names_list = [columns[0] + ' + ' + columns[1], columns[0] + ' Only', columns[1] + ' + ' + columns[3], columns[0] + ' Label']
        
       #convert this list into a StringVar for the list to process 
        save_names_var = StringVar(value=save_names_list)
            
        #Update save box with all the options for items to select
        save_box.grid_forget()
        save_box= Listbox(itemframe, width=40, height=4, listvariable=save_names_var, selectmode=BROWSE)
        save_box.grid(row=5, column=0, columnspan=2)
        save_box.bind("<<ListboxSelect>>", selectSaveFormat)
        
        #updates Condition Checker
        CC[0] = 1
        if sum(CC)==6:
            go_btn['state']=NORMAL

    
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
        canvas_label.configure(image=img)
        canvas_label.image=img
        
        #Updates Condition Checker
        CC[1] = 1
        if sum(CC)==6:
            go_btn['state']=NORMAL 
#looks for a directory to save labels into
def BrowseSave():
    #global variables
    global save_filename
    global savedir_label
    
    #uses filedialog to select a template image file
    save_filename = filedialog.askdirectory(title="Select Save Directory", initialdir=cd+"/Saves")
    
    #allows for the cancel option
    if save_filename == '':
        pass
    
    #If there is a choice, proceed
    else:
        #resets the selected sheet label
        savedir_label.grid_forget()
       
        #Selects just the name of the sheet, not the whole directory
        template_name = Path(save_filename).name
                
        #displays the condensed filename as a label.     
        savedir_label = Label(selectionframe, text='Save Folder: ' +template_name)
        savedir_label.grid(row=5, column=0, columnspan=2)
        
        #Updates the Condition Checker
        CC[5] = 1
        if sum(CC)==6:
            go_btn['state']=NORMAL
#When an Option is selected, update the placement frame to reflect the parameters of that specific option     
def SelectOption(selection):
    
    #global variables
    global columns
    global cposition
    global font_label
    global savedir
    global option
    
    #determine what the current position is
    for i in range(len(columns)):
        if selection == columns[i]:
            cposition = i
    
    #updates Condition Checker
    CC[3] = 1
    if sum(CC)==6:
            go_btn['state']=NORMAL
            
    #Enable all the widgets in Placement Frame
    font_label['state'] = NORMAL
    size_label['state'] = NORMAL
    caps_label['state'] = NORMAL
    sci_label['state'] = NORMAL
    xpos_label['state'] = NORMAL
    ypos_label['state'] = NORMAL
    maxw_label['state'] = NORMAL
    font_btn['state'] = NORMAL
    saveas_btn['state'] = NORMAL
    cent_btn['state'] = NORMAL
    ex_btn['state'] = NORMAL
    caps_btn['state'] = NORMAL
    sci_btn['state'] = NORMAL
    size_box['state'] = NORMAL
    xpos_box['state'] = NORMAL
    ypos_box['state'] = NORMAL
    maxw_box['state'] = NORMAL
    
    #Updates font label to reflect the current position
    if option.a[cposition].font == '' :
        font_label.grid_forget()
        font_label = Label(placementframe, text = 'Select Font:')
        font_label.grid(row=1, column=1)
    
    else:
        #Selects just the name of the font, not the whole directory
        font = Path(option.a[cposition].font).stem
        
        #Updates the font label
        font_label.grid_forget()
        font_label = Label(placementframe, text = 'Font: '+font)
        font_label.grid(row=1, column=1)
        
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
    
    #updates the boxes to show the current selection
    size_box.delete(0,END)
    xpos_box.delete(0,END)
    ypos_box.delete(0,END)
    maxw_box.delete(0,END)
    
    size_box.insert(0, option.a[cposition].size)
    xpos_box.insert(0, option.a[cposition].xpos)
    ypos_box.insert(0, option.a[cposition].ypos)
    maxw_box.insert(0, option.a[cposition].maxw)
    
        
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
        option.a[cposition].font = Path(font_filename).name
        
        #Selects just the name of the font, not the whole directory
        font = Path(font_filename).stem
        
        #updates the font label
        font_label.grid_forget()
        font_label = Label(placementframe, text = 'Font: '+font)
        font_label.grid(row=1, column=1)
        
         #updates the preview
        if template_filename != '': 
            Preview()

#updates the value of the Caps variable
def updateCaps():
    #global variables
    global cposition
    
    #updates the value of the caps variable
    option.a[cposition].caps = caps_var.get()
    
     #updates the preview
    if template_filename != '': 
        Preview()
    

#updates the value of the Sci variable
def updateSci():
    #global variables
    global cposition
    
    #updates the value of the caps variable
    option.a[cposition].sci = sci_var.get()
    
    #updates the preview
    if template_filename != '': 
        Preview()

#updates the value of the vaps variable when a Radio Button is hit.
def updateRadio():
    #global variables
    global cposition
    
    #updates the value of the caps variable
    option.a[cposition].cent = cent_var.get()
    
    #updates the preview
    if template_filename != '': 
        Preview()

#Updates the size variable whenever an input is made into the box
def updateSize():
    #global variables
    global cposition
    
    #updates the values of size
    option.a[cposition].size = size_box.get()
    
    #updates the preview
    if template_filename != '': 
        Preview()
    
#Updates the xpos variable whenever an input is made into the box
def updateXpos():
    #global variables
    global cposition
    
    #updates the values of Xpos
    option.a[cposition].xpos = xpos_box.get()
    
     #updates the preview
    if template_filename != '': 
        Preview()
    
#Updates the ypos variable whenever an input is made into the box
def updateYpos():
    #global variables
    global cposition
    
    #updates the values of Ypos
    option.a[cposition].ypos = ypos_box.get()
    
    #updates the preview
    if template_filename != '': 
        Preview()
    
#Updates the maxw variable whenever an input is made into the box
def updateMaxW():
    #global variables
    global cposition
    
    #updates the values of Maxw
    option.a[cposition].maxw = maxw_box.get()
    
    #updates the preview
    if template_filename != '': 
        Preview()

#Updates Object instances to reflect the values stored in a preset, or do nothing if 'no preset' is selected
def choosePreset(choice):
    
    #global variables
    global savedir
    global presetDataFrame
    global columns
    global option
    global cposition
    global save_btn
    global font_label
    global size_var
    global canvas_label
    
    try: cposition
    except NameError: cposition = 1
    
    #if no preset selected
    if preset.get() == 'No Preset':
        return
    
    #if a choice is made
    else:
        #open the preset file
        presetdir = cd + '/Presets/' + preset.get()
        savedir = presetdir
        presetDataFrame = pd.read_csv(presetdir)
        
        #update the objects
        for i in range(len(columns)):
            option.a[i].name = presetDataFrame['name'][i]
            option.a[i].xpos = presetDataFrame['xpos'][i]
            option.a[i].ypos = presetDataFrame['ypos'][i]
            option.a[i].cent = presetDataFrame['cent'][i]
            option.a[i].maxw = presetDataFrame['maxw'][i]
            option.a[i].size = presetDataFrame['size'][i]
            option.a[i].caps = presetDataFrame['caps'][i]
            option.a[i].sci = presetDataFrame['sci'][i]
        
            if type(presetDataFrame['font'][i]) == str:
                option.a[i].font = presetDataFrame['font'][i]
            else: 
                option.a[i].font = ''
                
        #updates the widgets
        #Updates font label to reflect the current position
        if option.a[cposition].font == '' :
            font_label.grid_forget()
            font_label = Label(placementframe, text = 'Select Font:')
            font_label.grid(row=1, column=1)
        
        else:
            #Selects just the name of the font, not the whole directory
            font = Path(option.a[cposition].font).stem
            
            #Updates the font label
            font_label.grid_forget()
            font_label = Label(placementframe, text = 'Font: '+font)
            font_label.grid(row=1, column=1)
            
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
            
        #size_box.delete(0,END)
        xpos_box.delete(0,END)
        ypos_box.delete(0,END)
        maxw_box.delete(0,END)
        
        
        #size_box.insert(0, option.a[cposition].size)
        xpos_box.insert(0, option.a[cposition].xpos)
        ypos_box.insert(0, option.a[cposition].ypos)
        maxw_box.insert(0, option.a[cposition].maxw)
        
        size_var.set(option.a[cposition].size)
        
        #activate save button
        save_btn['state'] = NORMAL
        
        #updates Condition Checker
        CC[2] = 1
        if sum(CC)==6:
            go_btn['state']=NORMAL
        
         #updates the preview
        if template_filename != '': 
            Preview()
        
#saves the current options to the selected preset directory
def Save():
    
    #global variables
    global savedir
    global columns
    global option
    
    #allows for the option where savedir is empty to skip
    if savedir is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    
    #creates a list of list of the objects
    savelist = []
    for i in range(len(columns)):
        savelist.append([option.a[i].name,
                         option.a[i].xpos,
                         option.a[i].ypos,
                         option.a[i].cent,
                         option.a[i].maxw,
                         option.a[i].font,
                         option.a[i].size,
                         option.a[i].caps,
                         option.a[i].sci])
    
    #creates a list with the indexes for the save file
    savecolumns = ['name','xpos','ypos','cent','maxw','font','size','caps','sci']
    
    #createsa pandas database with the Object data and Indexes
    saveDataFrame = pd.DataFrame(savelist, columns=savecolumns)
    
    #saves this database to the indicated save directory
    saveDataFrame.to_csv(savedir)

#saves the options and values to a .csv file.
def Saveas():
    
    #global variables
    global columns
    global saveDataFrame
    global save_btn
    global preset_menu
    global result
    global preset
    
    #prompts user to select location and name of the preset they wish to create
    savedir = filedialog.asksaveasfilename(defaultextension=".csv", initialdir=cd+"/Presets")
    if savedir is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    
    #creates a list of list of the objects
    savelist = []
    for i in range(len(columns)):
        savelist.append([option.a[i].name,
                         option.a[i].xpos,
                         option.a[i].ypos,
                         option.a[i].cent,
                         option.a[i].maxw,
                         option.a[i].font,
                         option.a[i].size,
                         option.a[i].caps,
                         option.a[i].sci])
    
    #creates a list with the indexes for the save file
    savecolumns = ['name','xpos','ypos','cent','maxw','font','size','caps','sci']
    
    #createsa pandas database with the Object data and Indexes
    saveDataFrame = pd.DataFrame(savelist, columns=savecolumns)
    
    #saves this database to the indicated save directory
    saveDataFrame.to_csv(savedir)
    
    #Activates the regular save button if it has not been updated already
    save_btn['state'] = NORMAL
    
    #updates the list of presets to reflect the addition of the new preset
    path = cd + "/Presets"
    extension = 'csv'
    os.chdir(path)
    result = glob.glob('*.{}'.format(extension))
    result.sort()
    
    #updates the preset menu to show the new file is selected
    preset.set(Path(savedir).stem)
    preset_menu.grid_forget()
    preset_menu = OptionMenu(placementframe, preset,'No Preset', *result)
    preset_menu.grid(row=0, column=3)

#populates the option box with items to choose from based on the selected Index
def selectIndex(selection):
    
    #global variables
    global option_box
    global selected
    global item_list
    global selected_items
    
    #pass name of selection onwards
    selected = selection
    
    #make a list of all the elements under the selected index from the sheetDataFrame
    item_list = []
    for i in range(len(sheetDataFrame[selection])):
        #if the position is nan, convert it to ''
        if type(sheetDataFrame.iloc[i][selection]) == float:
            sheetDataFrame.iloc[i][selection] = ''
        
        #if the name of the item is taken already
        if sheetDataFrame.iloc[i][selection] in item_list:
            #and the item is not ''
            if sheetDataFrame.iloc[i][selection] != '':
                #count the number of duplicates and add a number for it
                duplicates = ' ' + str(str(item_list).count(sheetDataFrame.iloc[i][selection])+1)
                item_list.append(sheetDataFrame.iloc[i][selection]+duplicates)
            
            #otherwise, just add '', duplicates of that dont matter
            elif sheetDataFrame.iloc[i][selection] == '':
                item_list.append('')
        
        #if it is not a duplicate name, just add it normally
        elif sheetDataFrame.iloc[i][selection] not in item_list:
            item_list.append(sheetDataFrame.iloc[i][selection])
     
    #convert this list into a StringVar for the option box to process
    itemlist_var = StringVar(value=item_list)
        
    #Update option box with all the options for items to select
    option_box.grid_forget()
    option_box= Listbox(itemframe, width=40, height=9, listvariable=itemlist_var, selectmode=EXTENDED)
    option_box.grid(row=1, column=0, columnspan=2)
    
    #update the text box to reflect the change in index
    selected_list = []
    for i in range(len(selected_items)):
        selected_list.append(item_list[selected_items[i]])
    
    text_box['state'] = NORMAL
    text_box.delete('1.0', END)
    text_box.insert(INSERT, selected_list)
    text_box['state'] = DISABLED
    
    add_btn['state'] = NORMAL
    remove_btn['state'] = NORMAL
    clear_btn['state'] = NORMAL
    all_btn['state'] = NORMAL

#adds the selected item/items to the list of items to be made into labels
def addItem():
    
    #global variable
    global option_box
    global selected_items
    global selected
    global selected_list
    global item_list
    global positions_list
    
    #makes a tuple of the current selected items
    item_tup = option_box.curselection()
    
    #For every item that is selected, add it to the selected items list
    for i in range(len(item_tup)):
        #checks for duplicates
        if item_tup[i] not in selected_items:
            selected_items.append(item_tup[i])
            selected_items.sort()
    
    #makes a list of the names of the selected items
    for i in range(len(item_tup)):
        position = item_tup[i]
        if item_list[position] not in selected_list:
            selected_list.append(item_list[position])
    
    #Updates the Text Box
    text_box['state'] = NORMAL
    text_box.delete('1.0', END)
    text_box.insert(INSERT, selected_list)
    text_box['state'] = DISABLED
    
    #updates Condition Checker
    CC[3] = 1
    if sum(CC)==6:
            go_btn['state']=NORMAL

#removes the selected item/items from the list of items to be made into labels
def removeItem():
    
    #global variables
    global option_box
    global selected_items
    global selected
    global selected_list
    
    #makes a tuple of the current selected items
    item_tup = option_box.curselection()
    
    #For every item that is selected, remove it from the selected items list
    for i in range(len(item_tup)):
        if item_tup[i] in selected_items:
            selected_items.remove(item_tup[i])
            
    #makes a list of the names of the selected items
    for i in range(len(item_tup)):
        position = item_tup[i]
        print(selected_list)
        if item_list[position] in selected_list:
            selected_list.remove(item_list[position])
    
    #Updates the Text Box
    text_box['state'] = NORMAL
    text_box.delete('1.0', END)
    text_box.insert(INSERT, selected_list)
    text_box['state'] = DISABLED
    

#removes ALL items from the list of items to be made into labels
def clearItem():
    
    #global variables
    global option_box
    global selected_items
    global selected
    global selected_list
    
    #updates the 2 lists associated
    selected_items = []
    selected_list = []
    
    #Updates the Text Box
    text_box['state'] = NORMAL
    text_box.delete('1.0', END)
    text_box.insert(INSERT, selected_list)
    text_box['state'] = DISABLED
    
    #updates Condition Checker
    CC[3] = 0
    go_btn['state']=DISABLED
    
    pass

#adds ALL items to the list of items to be made into labels
def allItem():
    
    #global variables
    global option_box
    global selected_items
    global selected
    global selected_list
    global item_list
    
    #updates the 2 lists associated
    selected_items = list(range(len(item_list)))
    selected_list = item_list
    
    #Updates the Text Box
    text_box['state'] = NORMAL
    text_box.delete('1.0', END)
    text_box.insert(INSERT, selected_list)
    text_box['state'] = DISABLED
    
    #updates Condition Checker
    CC[3] = 1
    if sum(CC)==6:
            go_btn['state']=NORMAL

#When an option for the save format of each label is chosen from the list box, update the variable, and example
def selectSaveFormat(virtualevent):
    
    #global variables
    global example_lab
    
    #For whatever is selected, update the example label.
    if save_box.curselection() == (0,):
        example = sheetDataFrame.iloc[0][0] +' '+ sheetDataFrame.iloc[0][1] + '.jpg'
    
    elif save_box.curselection() == (1,):
        example = sheetDataFrame.iloc[0][0] + '.jpg'
    
    elif save_box.curselection() == (2,):
        example = sheetDataFrame.iloc[0][1] +' '+ sheetDataFrame.iloc[0][3] + '.jpg'
        
    elif save_box.curselection() == (3,):
        example = sheetDataFrame.iloc[0][0] + ' Label' + '.jpg'
    
    #Update the example label to reflect the choice
    example_lab.grid_forget()
    example_lab = Label(itemframe, text= 'Example: '+example)
    example_lab.grid(row=6, column=0, columnspan=2)   
    
    #updates Condition Checker
    CC[4] = 1
    if sum(CC)==6:
            go_btn['state']=NORMAL

#The ultimate command. Checks to see if all preconditions are met, then creates labels.
def createLabels():
    
    #creates save list for sheets
    savelist = []
    
    #loop for each row
    for i in range(len(selected_items)):
        
        #initializes the template
        image = IM.open(template_filename)
        img_w, img_h = image.size
        draw = ID.Draw(image)
        
        #loop for each column
        for j in range(len(sheetDataFrame.iloc[0])):
    
            #checks for NaN, if value exists continue
            if pd.isna(sheetDataFrame.iloc[selected_items[i]][j]) == False:
    
                #sets color as black --- NEEDS TO BECOME AN OPTION
                Color = 'rgb(0,0,0)'
                
                #makes a size variable
                size = int(option.a[j].size)
                
                #makes a Font variable
                Font = IF.truetype(cd+"/Fonts/"+option.a[j].font, size)
                print(sheetDataFrame.iloc[i][j])
                
                #If CAPS lock is on, replace with full caps
                if option.a[j].caps == 1:
                    sheetDataFrame.iloc[i][j]=sheetDataFrame.iloc[i][j].upper()
                
                #checks size, if size is wider than maxW then reduce size
                w,h = draw.textsize(str(sheetDataFrame.iloc[selected_items[i]][j]),font=Font)
                while w > int(option.a[j].maxw):
                    #reduce size
                    size = size - 1
                    #resize Font
                    Font = IF.truetype(cd+"/Fonts/"+option.a[j].font, size)
                    #new width and hiegth variables to check
                    w,h = draw.textsize(str(sheetDataFrame.iloc[selected_items[i]][j]),font=Font)
                
                #If exact position, (X,Y) is exact
                if int(option.a[j].cent) == 1:
                    (x,y) = (int(option.a[j].xpos) , int(option.a[j].ypos))
                
                #If Centerered, (X,Y) is centered
                elif option.a[j].cent == 0:
                    (x,y) = (((img_w-w)/2)+(int(option.a[j].xpos)-(img_w/2)), int(option.a[j].ypos))
                    
                draw.text((x,y), str(sheetDataFrame.iloc[i][j]), fill=Color, font=Font)
    
        if save_box.curselection() == (0,):
            Filename = sheetDataFrame.iloc[i][0] +' '+ sheetDataFrame.iloc[i][1] + '.jpg'
    
        elif save_box.curselection() == (1,):
            Filename = sheetDataFrame.iloc[i][0] + '.jpg'
        
        elif save_box.curselection() == (2,):
            Filename = sheetDataFrame.iloc[i][1] +' '+ sheetDataFrame.iloc[i][3] + '.jpg'
            
        elif save_box.curselection() == (3,):
            Filename = sheetDataFrame.iloc[i][0] + ' Label' + '.jpg'
        
        #saves image
        save = save_filename + '/' + Filename
        savelist.append(save)
        image.save(save)
        
    sheetlist(savelist)

def sheetlist(list):
    background = IM.new('RGBA', (2550, 3300), (255, 255, 255, 255))
    bg_w, bg_h = background.size
    space = 50
    
    
    offset = (space,space)
    page = 1
    for i in range(len(list)):
        img = IM.open(list[i],'r')
        img_w, img_h = img.size
        distance = (offset[0]+img_w,offset[1]+img_h)
        
        nextoffset = (offset[0]+space+img_w, offset[1])
        nextdistance = (nextoffset[0]+img_w,nextoffset[1]+img_h)
        
        background.paste(img,offset)
        
        if nextdistance[0] > bg_w:
            nextoffset = (space, offset[1]+space+img_h)
            nextdistance = (nextoffset[0]+img_w,nextoffset[1]+img_h)
            if nextdistance[1] >= bg_h: 
                save = save_filename + '/Sheet Page ' + str(page) + '.png'
                print('Sheet ' + str(page) + ' created.')
                background.save(save)
                if i == len(list)-1:
                    break
                page = page + 1
                background = IM.new('RGBA', (2550, 3300), (255, 255, 255, 255))
                nextoffset = (space,space)
        
        offset = nextoffset
        distance = nextdistance
    
    save = save_filename + '/Sheet Page ' + str(page) + '.png'
    if not os.path.exists(save):
        background.save(save)
        print('Sheet ' + str(page) + ' created.')
    print('Sheets created :D')




#updates the preview
def Preview():
    #global variables
    global template_filename
    global canvas_label
    
    #checks to see if there is a template already
    if template_filename != '':
        
        #initializes the template
        image = IM.open(template_filename)
        img_w, img_h = image.size
        draw = ID.Draw(image)
        
        #loop for each column
        for i in range(len(sheetDataFrame.columns)):
            
            #checks for NaN, if value exists continue
            if pd.isna(sheetDataFrame.columns[i]) == False:
        
            #sets color as black --- NEEDS TO BECOME AN OPTION
                Color = 'rgb(0,0,0)'
                
                #makes a size variable
                size = int(option.a[i].size)
                
                #makes a Font variable
                Font = IF.truetype(cd+"/Fonts/"+option.a[i].font, size)
                
                #checks size, if size is wider than maxW then reduce size
                w,h = draw.textsize(sheetDataFrame.columns[i],font=Font)
                while w > int(option.a[i].maxw):
                    #reduce size
                    size = size - 1
                    #resize Font
                    Font = IF.truetype(cd+"/Fonts/"+option.a[i].font, size)
                    #new width and hiegth variables to check
                    w,h = draw.textsize(sheetDataFrame.columns[i],font=Font)
                
                #If exact position, (X,Y) is exact
                if int(option.a[i].cent) == 1:
                    (x,y) = (int(option.a[i].xpos),int(option.a[i].ypos))
                
                #If Centerered, (X,Y) is centered
                elif int(option.a[i].cent) == 0:
                    (x,y) = (((img_w-w)/2)+(int(option.a[i].xpos)-(img_w/2)), int(option.a[i].ypos))
                    
                printer = sheetDataFrame.columns[i]
                
                #places the text
                draw.text((x,y), printer, fill=Color, font=Font)
        
    else: 
        pass
    
    #saves temporary image
    savename = cd + '/Preview/Preview.jpg'
    image.save(savename)
    
    #reopens image in tkinter
    img2 = ImageTk.PhotoImage(Image.open(cd+'/Preview/Preview.jpg'))

    #display the new preview
    canvas_label.configure(image=img2)
    canvas_label.photo = img2

#create widgets for selection frame
    
    #Labels
ss_label = Label(selectionframe, text= "Choose a Spreadsheet:")
sheet_label = Label(selectionframe, text='')
t_label = Label(selectionframe, text= "Choose a Template:")
temp_label = Label(selectionframe, text='')
sav_label = Label(selectionframe, text='Choose a Save Directory')
savedir_label = Label(selectionframe, text='')

    #Buttons
ss_btn = Button(selectionframe, text= "Browse", command = BrowseSheet)
t_btn = Button(selectionframe, text="Browse", command=BrowseTemplate)
sav_btn = Button(selectionframe, text="Browse", command=BrowseSave)

#place widgets for selection frame

    #labels
ss_label.grid(row=0, column=0)
sheet_label.grid(row=1, column=0, columnspan=2)
t_label.grid(row=2, column=0)
temp_label.grid(row=3, column=0, columnspan=2)
sav_label.grid(row=4, column=0)
savedir_label.grid(row=5, column=0, columnspan=2)

    #buttons
ss_btn.grid(row=0, column=1)
t_btn.grid(row=2, column=1)
sav_btn.grid(row=4, column=1)

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
result.sort()

size_var = StringVar(value=0)
xpos_var = StringVar(value=0)
ypos_var = StringVar(value=0)
maxw_var = StringVar(value=0)

cent_var = IntVar()
caps_var = IntVar()
sci_var = IntVar()
    
    #Buttons
font_btn = Button(placementframe, text= 'Browse', command=SelectFont)
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
preset_menu = OptionMenu(placementframe, preset,'No Preset', *result, command=choosePreset)
    
    #Spin boxes
size_box = Spinbox(placementframe,from_=0, to=10000, textvariable=size_var, command=updateSize)
xpos_box = Spinbox(placementframe,from_=0, to=10000, textvariable=xpos_var, command=updateXpos)
ypos_box = Spinbox(placementframe,from_=0, to=10000, textvariable=ypos_var, command=updateYpos)
maxw_box = Spinbox(placementframe,from_=0, to=10000, textvariable=maxw_var, command=updateMaxW)

#Place widgets in placement frame
    
    #Labels
cpos_label.grid(row=0 , column=0)
preset_label.grid(row=0 , column=2 )
font_label.grid(row=1 , column=1 )
size_label.grid(row=2 , column=0 )
caps_label.grid(row=5 , column=0 )
sci_label.grid(row=5 , column=2 )
xpos_label.grid(row=3 , column=0 )
ypos_label.grid(row=3 , column=2 )
maxw_label.grid(row=2 , column=2 )
    
    
    #Buttons
font_btn.grid(row=1 , column=2)
#update_btn.grid(row=6 , column=1)
save_btn.grid(row=6 , column=2)
saveas_btn.grid(row=6 , column=3)

    #Radio Buttons
cent_btn.grid(row=4 , column=1)
ex_btn.grid(row=4 , column=2)

    #Check Buttons
caps_btn.grid(row=5, column=1)
sci_btn.grid(row=5, column=3) 

    #Option Menus
cpos_menu.grid(row=0, column=1)
preset_menu.grid(row=0, column=3)
    
    #Spin Boxes
size_box.grid(row=2, column=1)
xpos_box.grid(row=3, column=1)
ypos_box.grid(row=3, column=3)
maxw_box.grid(row=2, column=3)
    
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
#update_btn['state'] = DISABLED
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

    #Spin Boxes
size_box['state'] = DISABLED
xpos_box['state'] = DISABLED
ypos_box['state'] = DISABLED
maxw_box['state'] = DISABLED

#Create Widgets in item frame

    #Labels
showop_lab = Label(itemframe, text='Show by Index:')
saveop_lab = Label(itemframe, text='Save Name Format:')
text_lab = Label(itemframe, text='Selected Items:')
example_lab = Label(itemframe, text='Example: >Choose a Format<')

    #Variables
index_var = StringVar()
index_var.set('Choose a Spreadsheet first')
selected_items = []
selected_list = []
positions_list = []
    
    #Buttons
add_btn = Button(itemframe, text='Add', command=addItem)
remove_btn = Button(itemframe, text='Remove', command=removeItem)
clear_btn = Button(itemframe, text='Clear', command=clearItem)
all_btn = Button(itemframe, text = 'All', command=allItem)
go_btn = Button(itemframe, text='Create Labels', command=createLabels)


    #Option Menus
index_menu = OptionMenu(itemframe, index_var, index_var, *columns, command=selectIndex)
    
    #List Boxes
option_box= Listbox(itemframe, width=40, height=9)
save_box= Listbox(itemframe, width=40, height=4)
save_box.bind("<<ListboxSelect>>", selectSaveFormat)
    
    #Text Box
text_box = Text(itemframe, width=25, height=10, bd=1, relief='solid', wrap=WORD)
#Place Widgets in item frame

    #Labels
showop_lab.grid(row=0 , column=0)
saveop_lab.grid(row=4 , column=0, columnspan=2)
text_lab.grid(row=0 , column=3)
example_lab.grid(row=6, column=0, columnspan=2)
    
    #Buttons
add_btn.grid(row=2 , column=0)
remove_btn.grid(row=2 , column=1)
clear_btn.grid(row=3 , column=1)
all_btn.grid(row=3, column=0)
go_btn.grid(row=2 , column=3, rowspan=4)

    #Option Menus
index_menu.grid(row=0, column=1)

    #List Boxes
option_box.grid(row=1 , column=0, columnspan=2)
save_box.grid(row=5 , column=0, columnspan=2)
    
    #Text Box
text_box.grid(row=1, column=3)

    
#Disables inactive widgets in item frame
    
    #Labels
showop_lab['state'] = DISABLED
saveop_lab['state'] = DISABLED
text_lab['state'] = DISABLED
example_lab['state'] = DISABLED
    
    #Buttons
add_btn['state'] = DISABLED
remove_btn['state'] = DISABLED
clear_btn['state'] = DISABLED
all_btn['state'] = DISABLED
go_btn['state'] = DISABLED

    #Option Menus
index_menu['state'] = DISABLED

    #List Boxes
option_box['state'] = DISABLED
save_box['state'] = DISABLED 
   
    #Text Box
text_box['state'] = DISABLED

#establishes the mainloop of the tkinter root
root.mainloop()