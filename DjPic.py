import cv2
import numpy as np
import exifread
import checksumdir
import os
from tkinter import *
from tkinter import filedialog
from myDb import Db


database = Db("C:/temp/test.db")

#print (sys.version)

def get_selected_row(event):
    global selected_tuple
    index=l1.curselection()[0]
    selected_tuple=l1.get(index)
    print (selected_tuple)

def readExif():
    directoryInput = "C:/temp"
    for filename in os.listdir(directoryInput):
        if filename.endswith('.jpg'):
            try:
                with open("%s/%s" % (directoryInput, filename), 'rb') as image: # file path and name
                    exif = exifread.process_file(image)
                    dt = str(exif['EXIF DateTimeOriginal'])  # might be different
                    # segment string dt into date and time
                    day, dtime = dt.split(" ", 1)
                    # segment time into hour, minute, second
                    hour, minute, second = dtime.split(":", 2)
                    print (dt)
            except:
                print (image)

def listDirs():
    for dirpath, dirs,files in os.walk("c:/temp"):
        hash = checksumdir.dirhash(dirpath)
    #    database.insertDir(dirpath,hash)
        print (dirpath + " " + hash)

def listFiles():
    l1.delete(0,END)
    topdir = 'c:/temp'
    exten = '.jpg'
    for dirpath, dirnames, files in os.walk(topdir):
        for name in files:
            if name.lower().endswith(exten):
                file = os.path.join(dirpath, name)
                l1.insert(END,file)

def viewDb():
    database.view()

def comImg(f_name,v_comp):
    img = cv2.imread(f_name, 1)
    print("compressing ...\n")
    n_name = f_name.split(".")[0] + '.resized.jpg'
    cv2.imwrite(n_name,img,[cv2.IMWRITE_JPEG_QUALITY, v_comp])
    print("Done ...\n")

def remImg(f_name,v_reszie):
    img=cv2.imread(f_name,1)
    resized=cv2.resize(img,(int(img.shape[1]*(v_reszie/100)),int(img.shape[0]*(v_reszie/100))))
    n_name = f_name.split(".")[0] + '.resized.jpg'
    print ("resizing ...\n")
    cv2.imwrite(n_name,resized)

#   cv2.imshow("img",resized)
#   cv2.waitKey(0)
#   cv2.destroyAllWindows()

def brows():
   root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("jpeg files", "*.jp*"), ("all files", "*.*")))
   if not root.filename:
       return
   if (c1var.get() != 0):
      remImg(root.filename,int(w1var.get()))
   if (c2var.get() != 0):
      comImg(root.filename,int(w2var.get()))

readExif()
root = Tk()
b1=Button(root,text="Open",command=brows)
b1.grid(row=0,column=0,sticky=(N, S, E, W))
b2=Button(root,text="ListF",command=listFiles)
b2.grid(row=1,column=0, sticky=(N, S, E, W))
b3=Button(root,text="ListD",command=listDirs)
b3.grid(row=2,column=0, sticky=(N, S, E, W))
b4=Button(root,text="ListDB",command=viewDb)
b4.grid(row=3,column=0, sticky=(N, S, E, W))

w1var= DoubleVar()
w1=Scale(root, from_=1, to=100 ,orient=HORIZONTAL,variable = w1var)
w1.set(50)
w1.grid(row=0,column=1)

w2var= DoubleVar()
w2=Scale(root, from_=1, to=100 ,orient=HORIZONTAL,variable = w2var)
w2.set(50)
w2.grid(row=0,column=3)

c1var = IntVar()
c1=Checkbutton(root, text="Resize %", variable=c1var)
c1.grid(row=0,column=2, sticky=(N, S, E, W))

c2var = IntVar()
c2=Checkbutton(root, text="Compress %", variable=c2var)
c2.grid(row=0,column=4, sticky=(N, S, E, W))

l1=Listbox(root,height=10,width=40)
l1.grid(row=1,column=1,rowspan=6,columnspan=2)

sb1=Scrollbar(root)
sb1.grid(row=1,column=3,rowspan=6,sticky=(W,S,N))

l1.configure(yscrollcommand=sb1.set)
sb1.configure(command=l1.yview)

l1.bind('<<ListboxSelect>>',get_selected_row)


root.mainloop()
