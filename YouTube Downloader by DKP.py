
import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog, simpledialog
from tkinter.ttk import Progressbar

import moviepy.editor as mergevid
from pytube import YouTube

root = Tk()

root.configure(background="lightblue")
root.geometry("600x600")

root.title("Youtube Downloader by DKP")

Title = Label(root, text=" Youtube Downloader by DKP",
              fg="green", bg="lightblue", font=("josh", 16))
Title.pack(pady=20)


LabelRes = Label(root, text="choose resolution", fg='white',
                 bg='green').pack(padx=20, pady=20)

select = StringVar()
options = [
    'low(360)', 'medium(720)', 'high(1080)', 'audio'
]

# select.set(options[0])
menu = OptionMenu(root, select, *options)
menu.pack(padx=20, pady=10)


def my_show(*args):

    select.set(select.get())


select.trace('w', my_show)


select.set('Resolution')
ShowRes2 = Label(root, textvariable=select, bg="lightblue",)
ShowRes2.pack(padx=20, pady=10)


Folder_Name = ""


class DownloadFile:

    def openlocation(self):
        global Folder_Name
        Folder_Name = filedialog.askdirectory()
        if (len(Folder_Name) > 1):
            LocationError.config(text=Folder_Name, fg="green")
        else:
            LocationError.config(text="Please choose a folder", fg="red")

    def get_link(self):
        link = simpledialog.askstring("Input Link", "Please Enter the URL")
        ftitle = YouTube(link)
        filename = Label(root, text=ftitle.title, font=("josh", 10))
        filename.pack(padx=20, pady=10)
        return link

    def increment(*args):
        Bar = Progressbar(root, orient="horizontal",
                          length=300, mode="indeterminate")
        Bar.pack(padx=20, pady=10)
        for i in range(100):
            Bar["value"] = i+1
            root.update()
            time.sleep(0.1)

    def Download(self):
        quality = select.get()
        print(quality)

        url = self.get_link()

        if(len(url) > 1):

            DownloadMsg.config(text="")
            yt = YouTube(url)

            progress = YouTube(url, on_progress_callback=threading.Thread(
                target=self.increment()), on_complete_callback=DownloadMsg.config(text="Downloaded !"))
            if (quality == options[0]):
                file = yt.streams.filter(progressive=True).get_by_itag(18)
                threading.Thread(target=file.download(Folder_Name))

            elif (quality == options[1]):
                file = yt.streams.filter(progressive=True).get_by_itag(22)
                threading.Thread(target=file.download(Folder_Name))

            elif (quality == options[2]):
                file1 = yt.streams.filter(only_audio=True).get_by_itag(140)
                time.sleep(2)

                try:

                    f1 = file1.download(Folder_Name)
                    base, ext = os.path.splitext(f1)
                    print("base=", base, "ext=", ext)
                    converted = base + '.mp3'
                    os.rename(f1, converted)

                    time.sleep(3)
                    file2 = yt.streams.filter(
                        progressive=False).get_by_itag(137)
                    f2 = file2.download(Folder_Name)

                    filename = f2.split('\\')

                    output = f"[1080p] {filename[-1]}"
                    audioclip = mergevid.AudioFileClip(converted)
                    videoclip = mergevid.VideoFileClip(f2)

                    convideo = videoclip.set_audio(audioclip)
                    convideo.write_videofile(output, fps=60)

                except Exception as e:
                    print(e)
                    tkinter.messagebox.showerror("Error", e)

            elif (quality == options[3]):
                file = yt.streams.filter(only_audio=True).get_by_itag(140)
                threading.Thread(target=file.download(Folder_Name))

            else:
                DownloadMsg.config(text="Try again", fg="red")
        else:
            DownloadMsg.config(text="Error", fg="red")


D = DownloadFile()


SaveLocation = Label(root, text="Save Location", fg="white",
                     bg="green", font=("josh", 10))
SaveLocation.pack(padx=20, pady=10)
LocationButton = Button(root, text="Choose Here", bg="white", fg="red",
                        width=10, command=D.openlocation, font=("josh", 8), bd=4)
LocationButton.pack(padx=20, pady=10)

LocationError = Label(root, text="Save location message",
                      fg="red", bg="lightblue", font=("josh", 10))
LocationError.pack(padx=20, pady=10)


DownloadButton = Button(root, text="Download Now",
                        bg="red", fg="black", command=D.Download)
DownloadButton.pack(padx=20, pady=10)


DownloadMsg = Label(root, text="Download Message", fg="red",
                    bg="lightblue", font=("josh", 10))
DownloadMsg.pack(padx=20, pady=10)


def About():
    about = Toplevel(root)
    about.geometry("400x400")
    about.title("About Developer")
    About = Label(
        about, text=" Hii ! This YouTube Downloader has following Features:\n\n 1.Download high quality youtube video. \n 2.1080p video Download Support. \n 3.Audio Download available. ", fg="green")
    About.pack(padx=20, pady=10)


AboutButton = Button(root, text="About", command=About).pack(padx=20, pady=10)
root.mainloop()
