# Importing Required Modules & libraries
from tkinter import *
import pygame
import os
from os import path
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

# Defining MusicPlayer Class
class MusicPlayer:

  # Defining Constructor

  def __init__(self,root):
    self.root = root
    # Title of the window
    self.root.title("Music Player")
    # Window Geometry
    self.root.geometry("1000x200+200+200")
    # Initiating Pygame
    pygame.init()
    # Initiating Pygame Mixer
    pygame.mixer.init()
    # Declaring track Variable
    self.track = StringVar()
    # Declaring Status Variable
    self.status = StringVar()

    # adding the menu bar
    menubar = Menu(self.root)
    files = Menu(menubar,tearoff = 0)
    files.add_command(label="Conversion",command=self.conversion)
    files.add_command(label="Open",command=self.open)
    files.add_command(label="SaveAs",command=self.save)
    files.add_separator()
    files.add_command(label="Exit",command=root.destroy)
    menubar.add_cascade(label="Collection",menu=files)
   
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Set Volume",command=self.volume)
    editmenu.add_separator()
    editmenu.add_command(label="Exit",command=root.destroy)
    menubar.add_cascade(label="Edit", menu=editmenu)
    
    self.root.config(menu=menubar)
    # Creating Track Frame for Song label & status label
    trackframe = LabelFrame(self.root,text="Song Track",font=("times new roman",15,"bold"),bg="grey",fg="gold",bd=5,relief=GROOVE)
    trackframe.place(x=0,y=0,width=600,height=100)
    # Inserting Song Track Label
    songtrack = Label(trackframe,textvariable=self.track,width=20,font=("times new roman",24,"bold"),bg="grey",fg="gold").grid(row=0,column=0,padx=10,pady=5)
    # Inserting Status Label
    trackstatus = Label(trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="grey",fg="gold").grid(row=0,column=1,padx=10,pady=5)

    # Creating Button Frame
    buttonframe = LabelFrame(self.root,text="Control Panel",font=("times new roman",15,"bold"),bg="grey",fg="gold",bd=5,relief=GROOVE)
    buttonframe.place(x=0,y=100,width=600,height=100)
    # Inserting Play Button
    playbtn = Button(buttonframe,text="PLAY",command=self.playsong,width=6,height=2,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=0,padx=10,pady=5)
    # Inserting Pause Button
    playbtn = Button(buttonframe,text="PAUSE",command=self.pausesong,width=6,height=2,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=1,padx=10,pady=5)
    # Inserting Unpause Button
    playbtn = Button(buttonframe,text="UNPAUSE",command=self.unpausesong,width=10,height=2,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=2,padx=10,pady=5)
    # Inserting Stop Button
    playbtn = Button(buttonframe,text="STOP",command=self.stopsong,width=6,height=2,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=3,padx=10,pady=5)
    # Inserting the exit button
    exitbtn = Button(buttonframe,text="EXIT",command=root.destroy,width=4,height=2,font=('times new roman',16,'bold'),fg='navyblue',bg='gold').grid(row=0,column=4,padx=10,pady=5)

    # Creating Playlist Frame
    songsframe = LabelFrame(self.root,text="Song Playlist",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
    songsframe.place(x=600,y=0,width=400,height=200)
    # Inserting scrollbar
    scrol_y = Scrollbar(songsframe,orient=VERTICAL)
    # Inserting Playlist listbox
    self.playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="gold",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="silver",fg="navyblue",bd=5,relief=GROOVE)
    # Applying Scrollbar to listbox
    scrol_y.pack(side=RIGHT,fill=Y)
    scrol_y.config(command=self.playlist.yview)
    self.playlist.pack(fill=BOTH)
    # Changing Directory for fetching Songs
    os.chdir("/home/kali/Desktop/git/my personal projects/music_player/music_files/")
    # Fetching Songs
    songtracks = os.listdir()
    # Inserting Songs into Playlist
    for track in songtracks:
      self.playlist.insert(END,track)

  def conversion(self):
      try:
        files = simpledialog.askstring("File","Enter the name of the file")
        save = simpledialog.askstring("File","Enter the name by which you want to save the File")
        sound = AudioSegment.from_mp3(files)
        sound.export(save,format = 'wav')
        messagebox.showinfo("Converted",str(sound)+".wav")
        os.chdir('/home/kali/Desktop/git/my personal projects/music_player/music_files/')
        songstracks = os.listdir()
        for track in songstracks:
            self.playlist.insert(END,track)
      except:
          messagebox.showerror("Error","Cannot Convert the file")

  def volume(self):
      a = pygame.mixer.music.get_volume()
      messagebox.showinfo("Volume","Your current Volume is"+str(int(pygame.mixer.music.get_volume()*100)))
      pygame.mixer.music.set_volume(a)
  
  def open(self):
      try:
        root.filename = filedialog.askopenfilename(initialdir = "/home/kali",title = "Selct your track/album in .wav EXTENSION",filetypes=(("Mp 3 Music Files","*.mp3"),("wav Music Files","*.wav")))
        print("Added"+" " +root.filename)
        messagebox.showinfo("Added","Ahoy! Press the Play Button")
        os.chdir('/home/kali/Desktop/music_playeri/music_files')
        tracks = os.listdir()
        for track in tracks:
            self.playlist.insert(END,track)
      except:
          messagebox.showerror("Error","Cannot Open the File")
    
  def save(self):
      try:
          files = filedialog.asksaveasfilename(title="Enter the name of your file",filetypes=(("python files",".py"),("Text files",".txt"),("mp3 Music Files","*.mp3"),("wav Music Files","*.wav"),("mp4 Music Files","*.mp4")),initialdir="/home/kali")
      except:
          print("Cannot save the file")
          messagebox.showerror("Error","Cannot Save the File")

  # Defining Play Song Function
  def playsong(self):
    # Displaying Selected Song title
    self.track.set(self.playlist.get(ACTIVE))
    # Displaying Status
    self.status.set("-Playing")
    # Loading Selected Song
    pygame.mixer.music.load(self.playlist.get(ACTIVE))
    # Playing Selected Song
    pygame.mixer.music.play()

  def stopsong(self):
    # Displaying Status
    self.status.set("-Stopped")
    # Stopped Song
    pygame.mixer.music.stop()

  def pausesong(self):
    # Displaying Status
    self.status.set("-Paused")
    # Paused Song
    pygame.mixer.music.pause()

  def unpausesong(self):
    # Displaying Status
    self.status.set("-Playing")
    # Playing back Song
    pygame.mixer.music.unpause()

  def exitsong(self):
    # Display Status
    self.statu.set("-Exit")
    # Exit the song
    pygame.mixer.music.exit()

# Creating TK Container
root = Tk()

# Passing Root to MusicPlayer Class
MusicPlayer(root)
# Root Window Looping
root.mainloop()
