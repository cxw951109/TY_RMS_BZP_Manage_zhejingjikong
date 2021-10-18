#! /usr/bin/env python
import cups
import time
import subprocess

conn = cups.Connection()
printers = conn.getPrinters()
printer_name = printers.keys()[0]

printerQueueLen = len(conn.getJobs())
if (printerQueueLen <= 1):
    time.sleep(1)
    printID = conn.printFile(printer_name, '/home/pi/src/pi_logo.png', 'ki',
                             {'fit-to-page': 'False', 'orientation-requested': '3'})


