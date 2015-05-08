__author__ = 'sybrandb'
from kerkelijkjaarlijst import *
import locale
import sys

from Tkinter import *
import tkFileDialog as filedialog
import os
import year2csv
daysPerWeek = 7
MA = 1
DI = 2
WO = 3
DO = 4
VR = 5
ZA = 6
ZO = 7

text = None


def my_date_range(start, end, step=week):
    while start < end:
        yield start
        start += step


def do_nothing():
    pass


def file_save():
    global text
    options = {'initialdir': 'C:\\users\\sybrandb\\documents',
               'filetypes': [
                    ("Comma Separated Values", "*.csv"),
                    ("PDF file", "*.pdf"),
                    ("All Files", "*.*")],
               'defaultextension': ".csv"}
    f = filedialog.asksaveasfile(mode='w', **options)
    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    fil, ext = os.path.splitext(f.name)
    print (fil, ext)

    return f


def main():
    # sets the locale in Python to the default locale of the user
    global text
    locale.setlocale(locale.LC_ALL, '')

    if len(sys.argv) == 2:
        kerkelijkjaar = int(sys.argv)
    else:
        kerkelijkjaar = date.today().year
    root = Tk("Overzicht kerkelijk jaar")
    root.geometry = "500x500"
    menubar = Menu(root)
    text = Text(root)
    text.pack()
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=do_nothing)
    filemenu.add_command(label="Open", command=do_nothing)
    filemenu.add_command(label="Save", command=file_save, accelerator="Ctrl+S")
    # filemenu.add_command(label="Save as...", command=file_save(root))
    filemenu.add_command(label="Close", command=do_nothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=do_nothing)
    helpmenu.add_command(label="About...", command=do_nothing())
    menubar.add_cascade(label="Help", menu=helpmenu)
    L1 = Label(root, text='Kerkelijk jaar', width=16)
    L1.pack(side=LEFT)
    guijaar = IntVar
    spinbox = Spinbox(root, from_=kerkelijkjaar-10, to=kerkelijkjaar+10,justify=RIGHT, textvariable=guijaar)
    spinbox.pack()
    root.config(menu=menubar)
    root.mainloop()
    # make a list of 52 sundays

    # Witte Donderdag, Goede Vrijdag, Stille Zaterdag en Hemelvaartsdag moeten er nog in gefrommeld worden
    # begin en eind van kerkeljaar nog ophalen uit klasse via method
    kj = KerkelijkJaarLijst(kerkelijkjaar)

    # this generates a list of sundays for a complete year
    # the +1 is necessary to make sure the last sunday is included
    dates = list(my_date_range(kj.eerste_zondag(), kj.laatste_zondag() + timedelta(1)))  # this generates a list of sundays for a complete year
    for d in dates:
        kj.add_sunday(d)
    pasen = kj.easter()
    kj.add_sunday(pasen - timedelta(1))
    kj.add_sunday(pasen - timedelta(2))
    kj.add_sunday(pasen - timedelta(3))
    kj.add_sunday(pasen + timedelta(39))
    print (kj)
    # TODO write kj variable to a file, or better still a PDF file
    lkj = kj.send2csvwriter()
    path = 'churchyear2015.csv'
    year2csv.csv_dict_writer(path, FeestDag.l_fieldnames, lkj)

main()