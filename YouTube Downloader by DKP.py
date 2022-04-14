import os
import threading
from time import sleep
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import tkinter
import io
import webbrowser
import requests
from pytube import YouTube, Playlist
import moviepy.editor as mergevid
from PIL import Image, ImageTk


root = Tk()

root.configure(background="lightblue")
root.geometry("600x650+400+100")
root.resizable(False, False)
root.title("YouTube Downloader by DKP")
root.config(bg="lightblue")

# Application title
Title = Label(root, text="Youtube Downloader", fg="cyan", bg="#121110", font=(
    "josh", 16), padx=30, pady=5).place(x=30, y=10, width=540, height=30)
Footer = Label(root, text="Devloped by DKP", fg="cyan", bg="#121110", font=(
    "times 15", 16), padx=30, pady=5).place(x=30, y=595, width=540, height=30)

# Frame for asking details
frame1 = Frame(root, bg="white").place(x=30, y=50, width=540, height=540)


# Resolution choose Function
LabelRes = Label(root, text="Choose Resolution", fg='white', bg='#22C5B4', padx=10,
                 pady=5, font=("josh", 10, "bold")).place(x=32, y=80, width=200, height=30)

select = StringVar()
options = [
    'low(360)', 'medium(720)', 'high(1080)', 'audio', 'playlist(720p)', 'multivideo(720p)', 'multiaudio'
]

select.set(options[0])
menu = OptionMenu(root, select, *options)
menu.place(x=250, y=80, width=130, height=30)


Folder_Name = ""
# Saving location funtion


def openlocation():
    global Folder_Name
    Folder_Name = filedialog.askdirectory()
    if (len(Folder_Name) > 1):
        LocationError.config(text=Folder_Name, fg="green")
    else:
        LocationError.config(text="Please choose a folder", fg="red")


# Saving file location
SaveLocation = Label(root, text="Save Location", fg="white",
                     bg="#22C5B4", font=("josh", 10, "bold"), padx=10, pady=5)
SaveLocation.place(x=32, y=120, width=200, height=30)

LocationButton = Button(root, text="Choose Here", bg="white",
                        fg="black", width=10, command=openlocation, font=("josh", 8), bd=2)
LocationButton.place(x=250, y=120, width=130, height=30)

LocationError = Label(root, text="No dictory selected",
                      fg="red", bg="white", font=("josh", 10))
LocationError.place(x=390, y=120, width=180, height=30)


# Asking Video URL funtion
link_var = StringVar()
link_label = Label(root, text='Youtube URL(s)', fg="white", bg="#22C5B4", font=(
    'calibre', 10, 'bold'), padx=10, pady=5).place(x=32, y=160, width=200, height=30)

link_entry = Entry(root, textvariable=link_var, font=('calibre', 10, 'normal'),
                   relief="solid", borderwidth=1).place(x=250, y=160, width=314, height=30)


# Frame for video details
frame2 = Frame(root, bg="pink").place(x=32, y=200, width=535, height=387)

# Video Title Label
video_title = Label(root, text="Video Title", bg="#457DEA", fg="white", font=(
    'josh', 10, 'bold'), padx=10, pady=5, anchor=NW)
video_title.place(x=32, y=200, width=535, height=30)

# Video description Label
video_desc = Text(root, borderwidth=1, relief="solid", font=(
    'calibre', 10, 'bold'), fg="black", bg="white")
video_desc.place(x=32, y=230, width=370, height=215)

# Video thumbnail Label
video_thumb = Label(root, text="Thumbnail", bg="white", fg="black", font=(
    'times 12', 10,), relief="solid", borderwidth=1)
video_thumb.place(x=390, y=230, width=177, height=215)

# video filesize Label
video_size = Label(root, text="File Size:", font=('times 15', 10),
                   bg="#22C5B4", fg="black", borderwidth=2, anchor=NW, padx=10, pady=5)
video_size.place(x=32, y=450, width=80, height=30)

size = Label(root, font=('times 15', 10), bg="#22C5B4", fg="black",
             borderwidth=2, anchor=NW, padx=10, pady=5)
size.place(x=112, y=450, width=90, height=30)


# About Funtion
def About():
    about = Toplevel(root)
    about.geometry("400x400")
    about.title("About Us")
    about.resizable(False, False)
    About = Label(
        about, text=" Hii !, This YouTube Downloader has following features:", fg="#F4CE0B", bg="#615E4F", font=("times 17", 10, "bold"))
    About.pack(padx=10, pady=10)
    features = Label(about, text="1.Download high quality youtube video. \n 2.1080p video Download Support. \n 3.Audio Download available. \n 4.Download multiple video,audio and playlist in one click",
                     fg="black", font=("times 15", 10, "bold"))
    features.pack(padx=10, pady=20)

    def callback(url):
        webbrowser.open_new(url)
    link1 = Label(about, text="Github Source", fg="#2D1DF0",
                  cursor="hand2", font=("josh", 10, "bold"))
    link1.pack(padx=5, pady=100)
    link1.bind(
        "<Button-1>", lambda e: callback("https://github.com/Codewithdkp/YouTube-Downloader"))


# About Button
AboutButton = Button(root, text="About", command=About).place(
    x=230, y=550, width=150, height=30)


class DownloadFile:

    def __init__(self, Folder_Name) -> None:
        self.folder = Folder_Name

    # Youtube Thumbnail workspace
    def thumbnail(self, url):
        yt = YouTube(url)
        video_title.config(text=yt.title)

        video_desc.delete('1.0', END)
        video_desc.insert(END, yt.description[:250])

        readIMG = requests.get(yt.thumbnail_url)
        imgio = io.BytesIO(readIMG.content)

        load = Image.open(imgio)
        load = load.resize((185, 164), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        video_thumb.config(image=render)
        video_thumb.image = render

    def filesize(self, file):
        size.config(
            text=f"{round(((file.filesize)/1024/1024),2)}MB", bg="white", fg="black",)
        # print(file.filesize)

    def Download(self):
        url = link_var.get()
        quality = select.get()
        progress.config(text="Downloding", fg="black")
        if(len(url) == 0):
            tkinter.messagebox.showerror("URL Not Found", "Please enter a url")

        # condition for youtube playlist (720p)
        elif((len(url) > 1) & (quality == options[4])):
            p = Playlist(url)
            for video in p.videos:
                x = threading.Thread(target=self.thumbnail, args=(video,))
                x.start()
                sleep(5)
                x.join()
                file = video.streams.filter(progressive=True).get_by_itag(22)
                self.filesize(file)
                file.download(Folder_Name)
                progress.config(text=f"Download Completed{file}")
        # condtion for multiple video (720p)
        elif((len(url) > 1) & (quality == options[5])):
            url_List = (url).split(',')
            for url in url_List:
                yt = YouTube(url)
                x = threading.Thread(target=self.thumbnail, args=(url,))
                file = yt.streams.filter(progressive=True).get_by_itag(22)
                self.filesize(file)
                file.download(Folder_Name)
                progress.config(text=f"Download Completed{file}")
        # condtion for multiple audio
        elif((len(url) > 1) & (quality == options[6])):
            url_List = url.split(',')
            for url in url_List:
                yt = YouTube(url)
                x = threading.Thread(target=self.thumbnail, args=(url,))
                x.start()
                sleep(5)
                x.join()
                file = yt.streams.filter(only_audio=True).get_by_itag(140)
                self.filesize(file)
                file.download(Folder_Name)
                progress.config(
                    text=f"Download Completed! \n {file.default_filename}")

        elif(len(url) > 1):

            yt = YouTube(url)
            x = threading.Thread(target=self.thumbnail, args=(url,))
            x.start()
            x.join()

            if(quality == options[0]):
                file = yt.streams.filter(progressive=True).get_by_itag(18)
                self.filesize(file)
                file.download(Folder_Name)
                progress.config(text=f"Download Completed{file}")
            elif(quality == options[1]):
                file = yt.streams.filter(progressive=True).get_by_itag(22)
                self.filesize(file)
                file.download(Folder_Name)
                progress.config(text=f"Download Completed{file}")
            elif(quality == options[2]):
                file1 = yt.streams.filter(only_audio=True).get_by_itag(140)
                try:
                    f1 = file1.download(Folder_Name)
                    base, ext = os.path.splitext(f1)
                    converted = base + '.mp3'  # converted extention to mp3
                    os.rename(f1, converted)

                    file2 = yt.streams.filter(
                        progressive=False).get_by_itag(137)
                    f2 = file2.download(Folder_Name)
                    self.filesize(f2)
                    filename = f2.split('\\')
                    print(filename)
                    output = f"[1080p] {filename[-1]}"
                    print(output)

                    audioclip = mergevid.AudioFileClip(converted)
                    videoclip = mergevid.VideoFileClip(f2)

                    convideo = videoclip.set_audio(audioclip)
                    convideo.write_videofile(output, fps=60)
                    progress.config(text=f"Download Completed{output}")
                except Exception as e:
                    tkinter.messagebox.showerror("Error", e)

            elif(quality == options[3]):
                file = yt.streams.filter(only_audio=True).get_by_itag(140)
                self.filesize(file)
                file.download(Folder_Name)
                progress.config(text=f"Download Completed{file}")
            else:
                tkinter.messagebox.showerror("Not a valid URL", url)

        else:
            tkinter.messagebox.showerror(
                "Error", "Something went worng! \n Please Restart the application")


url = link_var.get()


def DownloadNow():
    t2 = threading.Thread(target=D.Download)
    t2.start()


# Download Button
D = DownloadFile(Folder_Name)
DownloadButton = Button(root, text="Download Now",
                        bg="red", fg="black", borderwidth=2, command=DownloadNow)
DownloadButton.place(x=202, y=450, width=366, height=30)

# Download Progress
progress = Label(root, fg="red", bg="pink", font=("josh", 10), padx=10, pady=5)
progress.place(x=32, y=500, width=535, height=30)

# progressBar = ttk.Progressbar(
#     root, orient=HORIZONTAL, length=500, mode="determinate")
# progressBar.place(x=32, y=560, width=530, height=30)

root.mainloop()
