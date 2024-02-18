from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from pafy import *
import time
from pathlib import Path
from os import path
import threading
import clipboard
#################################################################################################################################

def mycb(total, recvd, ratio, rate, eta):
    
    rate=str(round(rate))+" KB/s"
    prc = round((recvd*100)/total)
    #print("[",str(prc)+"% ] --","[",rate,"] --","[",eta,"s]")
    progress['value']= prc
    screen.update_idletasks()
    vb['state'] = DISABLED
    ab['state'] = DISABLED
    
#################################################################################################################################

def done_audio():
    getdata = threading.Thread(target=download_audio)
    getdata.start()
    
def download_audio ():
    name1=name.get()
    for p in ('|', '?', '\\', '/', ':', '*', '<', '>', '\"'):
        name1 = name1.replace(p, '_')
    url1=url.get()
    video = pafy.new(url1)
    if len(name1)==0:
        name1=video.title
    video = video.getbestaudio(preftype="m4a")
    if path.exists(folder_loc+"/"+name1+".m4a")==True:#the download doesn't work if there's a file with the same name, so this line is to change the name to start download.
        i=1
        while 1:
            name1=name1+"("+str(i)+")"
            i+=1
            if path.exists(folder_loc+"/"+name1+".m4a")==False:
                break
            else:
                name1=name1[:-3]
        if folder_loc == str(Path.home() / "Downloads"):
            video.download(filepath=folder_loc+"\\"+name1+".m4a" ,quiet=True,callback=mycb)
        else:
            video.download(filepath=folder_loc+"/"+name1+".m4a" ,quiet=True,callback=mycb)
    else:
        if folder_loc == str(Path.home() / "Downloads"):
            video.download(filepath=folder_loc+"\\"+name1+".m4a" ,quiet=True,callback=mycb)
        else:
            video.download(filepath=folder_loc+"/"+name1+".m4a" ,quiet=True,callback=mycb)
    vb['state'] = NORMAL
    ab['state'] = NORMAL
    time.sleep(0.5)
    progress['value']=0
    url_entry.delete(0,END)
    name_entry.delete(0,END)
    
#################################################################################################################################

def done_video():
    getdata = threading.Thread(target=download_video)
    getdata.start()

def download_video ():
    name1=name.get()
    for p in ('|', '?', '\\', '/', ':', '*', '<', '>', '\"'):
        name1 = name1.replace(p, '_')
    url1=url.get()
    video = pafy.new(url1)
    if len(name1)==0:
        name1=video.title
    video = video.getbest(preftype="mp4")
    if path.exists(folder_loc+"/"+name1+".mp4")==True:#the download doesn't work if there's a file with the same name, so this line is to change the name to start download.
        i=1
        while 1:
            name1=name1+"("+str(i)+")"
            i+=1
            if path.exists(folder_loc+"/"+name1+".mp4")==False:
                break
            else:
                name1=name1[:-3]
        if folder_loc == str(Path.home() / "Downloads"):
            video.download(filepath=folder_loc+"\\"+name1+".mp4" ,quiet=True,callback=mycb)
        else:
            video.download(filepath=folder_loc+"/"+name1+".mp4" ,quiet=True,callback=mycb)
    else:
        if folder_loc == str(Path.home() / "Downloads"):
            video.download(filepath=folder_loc+"\\"+name1+".mp4" ,quiet=True,callback=mycb)
        else:
            video.download(filepath=folder_loc+"/"+name1+".mp4" ,quiet=True,callback=mycb)
    ab['state'] = NORMAL
    vb['state'] = NORMAL
    time.sleep(0.5)
    progress['value']=0
    url_entry.delete(0,END)
    name_entry.delete(0,END)
    
#################################################################################################################################

def location ():
    global folder_loc
    folder_loc = filedialog.askdirectory()
    
#################################################################################################################################

def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
        
#################################################################################################################################

def paste_text():
    url.set(clipboard.paste())

#################################################################################################################################

#window settings#################################################################################################################################

screen = Tk()
screen.title("YouTube Downloader 5.0")
screen.geometry("800x600")
screen.resizable(False,False)

#background image#################################################################################################################################

bgimage=PhotoImage(file="YouTube downloader background.png")
bgLabel=Label(screen,image=bgimage)
bgLabel.pack()
screen.iconbitmap('icon 4.ico')

#menu(when you right-click)########################################################################################################################

m = Menu(screen, tearoff = 0)
m.add_command(label ="Paste",command=paste_text)

#url entry#################################################################################################################################

url = StringVar()
url_entry = Entry(textvariable=url,width=19,bd=3,font=("Segoe UI", 22))
url_entry.place(x=25,y=115)

#paste button#######################################################################################################################################

paste_btn = Button(text="Paste",fg="white",bg="red3",height=1,pady=7,width=10,font=("Segoe UI", 12),command=paste_text)
paste_btn.place(x=350,y=113)

#file_name entry#################################################################################################################################

name = StringVar()
name_entry = Entry(textvariable=name,width=26,bd=3,font=("Segoe UI", 22))
name_entry.place(x=25,y=210)

#progress bar#################################################################################################################################

progress = Progressbar(screen, orient = HORIZONTAL, length = 300, mode = 'determinate',)
progress.place(x=81,y=490)

#choose_folder button#################################################################################################################################

folder_loc = str(Path.home() / "Downloads")
cf = Button(text="Folder",fg="white",bg="red3",height=1,pady=7,width=10,font=("Segoe UI", 12),command = location)
cf.place(x=180,y=300)

#video button#################################################################################################################################

vb = Button(text="Video",fg="white",bg="red3",height=1,pady=7,width=10,font=("Segoe UI", 12),command=done_video)
vb.place(x=125,y=393)

#audio button#################################################################################################################################

ab = Button(text="Audio",fg="white",bg="red3",height=1,pady=7,width=10,font=("Segoe UI", 12),command=done_audio)
ab.place(x=235,y=393)


url_entry.bind("<Button-3>", do_popup)
screen.mainloop()
