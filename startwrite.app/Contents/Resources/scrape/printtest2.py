#!/usr/bin/env python
from tkinter import *
import sys, commands, os

root = Tk()
root.title('Printer Configuration')
root.config(bg="lightblue")

def getPrinter():
	nIndex = printerList.curselection()[0]

def setPrinter(printerVar):
	os.remove('printerSelection.py')
	file = open('printerSelection.py', 'w')
	sActivePrinter = printerList.get(nIndex)
	setPrinter(sActivePrinter)
	print >>file, 'PRINTER = '+printerVar
	quit()

def testPrinter():
	nIndex = printerList.curselection()[0]
	sActivePrinter = printerList.get(nIndex)
	printerControl = os.popen('lpr -P %s' % (sActivePrinter), 'w')
	printerControl.write('Laborder Configration Tool Test Print')
	printerControl.close()

frame1 = Frame(root)
frame1.config(bg="lightblue", padx=2, pady=2)
frame1.pack() 
frame2 = Frame(root)
frame2.config(bg="lightblue")
frame2.pack()

header = 'Laborder Printer Configuration Tool'
Label(frame1, bg="lightblue", text=header).grid(row=0)

printers = commands.getoutput('lpstat -p')
printers = printers.split('\n')
#printers.remove('\tPaused')
printerNames = []
for printer in printers:
	printer = printer.split(' ')
	printerNames.append(printer[1])
	
if len(printerNames) > 4:
	scrollPrinter = Scrollbar(frame1, orient=VERTICAL)
	printerList = Listbox(frame1, yscrollcommand=scrollPrinter.set, selectmode=SINGLE, selectbackground="yellow", height=4)
	scrollPrinter.config(command=printerList.yview)
	scrollPrinter.grid(row=1, column=1, rowspan=4, sticky=N+S)
else:
	printerList = Listbox(frame1, selectmode=SINGLE, selectbackground="yellow", height=4)

for printerName in printerNames:
	printerList.insert(END, printerName)

printerList.grid(row=1, column=0, rowspan=4, sticky=E+W)

Button(frame2, highlightbackground="lightblue", text="Test", command=testPrinter).grid(row=0, column=0)
Button(frame2, highlightbackground="lightblue", text="Set", command=getPrinter).grid(row=0, column=1)

root.mainloop()