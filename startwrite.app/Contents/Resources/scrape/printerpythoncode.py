import cups
conn = cups.Connection()
printers = conn.getPrinters()
printer_name = printers.keys()[0]
conn.printFile(printer_name,'/home/pi/Desktop/a.pdf',"",{}) 




############ pycups ############