import threading
import os
import tkinter
import customtkinter
from pytube import YouTube
from tkinter import ttk
import subprocess

downloadedVideos = []

def playVideo(path):
    try:
        os.startfile(path)
        print(f"Now playing: {path}")
    except subprocess.CalledProcessError as e:
        print(f"Error playing video: {e}")

#region Download Functions
def startDownload():
    try:
        ytLink = link.get() # Sets ytLink = whatever was put in the bar in the GUI
        ytObject = YouTube(ytLink, on_progress_callback=onProgress) # Creates the Youtube object using the link as well as using the callback function
        downloadedVideos.append(ytObject)

        video = ytObject.streams.get_highest_resolution() # Creates the stream

        path = "Downloads/"
        video.download(output_path=path) # Downloads the stream

        finishLabel.configure(text="Download Complete")

        downloadedVideos.append(ytObject.title)
        
    except:
        finishLabel.configure(text="Download Error")

def onProgress(stream, chunk, bytesRemaining):
    # Calculates the percentage
    totalSize = stream.filesize
    bytesDownloaded = totalSize - bytesRemaining
    percentageOfCompletion = bytesDownloaded / totalSize * 100

    percent = int(percentageOfCompletion)
    pPercentage.configure(text=str(percent) + '%')
    pPercentage.update() # Necessary because it forces GUI to update immedietly instead of after the function

    progressBar.set(float(percent) / 100)

def startDownloadThread():
    finishLabel.configure(text="Download Initialized...")
    pPercentage.configure(text="0%")
    pPercentage.update()
    progressBar.set(0)
    threading.Thread(target=startDownload).start()
#endregion

#region Overall Window
# Window
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")


# notebook allows for tabs in the GUI
notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill='both')

# Create a frame for both tabs
downloadTab = customtkinter.CTkFrame(notebook)
libraryTab = customtkinter.CTkFrame(notebook)

# Add the tabs to the notebook
notebook.add(downloadTab, text="Download")
notebook.add(libraryTab, text="Library")
#endregion

#region Download Tab
# Title
title = customtkinter.CTkLabel(downloadTab, text="Insert a youtube link")
title.pack(padx=10, pady=10)

# URL
urlVar = tkinter.StringVar()
link = customtkinter.CTkEntry(downloadTab, width=350, height=40, textvariable=urlVar)
link.pack()

# Finished Label
finishLabel = customtkinter.CTkLabel(downloadTab, text="")
finishLabel.pack()

# Download percentage
pPercentage = customtkinter.CTkLabel(downloadTab, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(downloadTab, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# Download Button
download = customtkinter.CTkButton(downloadTab, text="Download", command=startDownloadThread)
download.pack(padx=10, pady=10)
#endregion

#region Library Tab

# Library Label
libraryLabel = customtkinter.CTkLabel(libraryTab, text="Downloaded Videos")
libraryLabel.pack(padx=10, pady=10)

path = "Downloads"
for file in os.listdir(path):
    path = os.path.join(path, file)
    if os.path.isfile(path):
        downloadedVideos.append(path)
        downloadedVideos.sort()
        tempButton = customtkinter.CTkButton(libraryTab, text=file, command=lambda vid=path: playVideo(vid))
        tempButton.pack(padx=10, pady=10)
    path = "Downloads"



#endregion


# Opens the window and stays till you exit
app.mainloop()