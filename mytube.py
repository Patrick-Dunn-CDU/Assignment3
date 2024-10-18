from tkinter import *
from tkVideoPlayer import TkinterVideo

root = Tk()

class Video():
    def __init__(self,video_name,root):
        self.video=TkinterVideo(root,scaled=True,keep_aspect=True)
        self.video.pack(expand=True, fill="both")
        self.video.load(video_name)
        self.play_button=PlayButton(self,root) #this, and the line below, are examples of nested classes as external classes are instantiated withing this class
        self.bar=ProgressBar(self,root)
        self.video.bind("<<Duration>>", self.update_duration)
        self.video.bind("<<SecondChanged>>", self.update_scale)
    
    def set_grid(self,row,col): #this is an example of polymorphism. The function 'set_grid' is in all three classes but their grids are set slightly differently to fit togather nicely 
        self.video.grid(row=row,column=col,rowspan=2,columnspan=2)
        self.play_button.set_grid(row+1,col-1)
        self.bar.set_grid(row+1,col)
    
    def play(self):
        self.video.play()
    
    def pause(self):
        self.video.pause()
    
    def is_paused(self): #this function, and 'get_duration', are examples of encapsulation. These methods are used to return variables held only within this class to restrict how the private variables are used
        return self.video.is_paused()
    
    def get_duration(self):
        return self.video.video_info()['duration']
    
    def update_duration(self,event):
        """ updates the duration after finding the duration """
        duration = self.video.video_info()["duration"]
        self.bar.bar["to"] = duration
    
    def update_scale(self,event):
        """ updates the scale value """
        self.bar.prog.set(self.video.current_duration())
    
    def seek(self,i):
        self.video.seek(int(i))

class PlayButton():
    def __init__(self,video,root):
        self.video=video
        self.button=Button(root,text="Play",command=self.play_pause)
        self.button.pack()
    
    def play_pause(self):
        if self.video.is_paused():
            self.video.play()
            self.button['text']='Pause'
        else:
            self.video.pause()
            self.button['text']='Play'
    
    def set_grid(self,row,col):
        self.button.grid(row=row,column=col)

class ProgressBar():
    def __init__(self,video,root):
        self.video=video
        self.prog=IntVar(root)
        self.bar=Scale(root,from_=0,to=0,orient=HORIZONTAL,command=self.seek,variable=self.prog)
        self.bar.pack(side="left", fill="x", expand=True)
    
    def seek(self,i):
        self.video.seek(i)
    
    def set_grid(self,row,col):
        self.bar.grid(row=row,column=col)

def video_update(video):
    video.bar.bar.set(int(video.video.current_duration()))

def start_vid():
    main=Toplevel(root)
    main.title("Video 1")
    video1 = Video('example_1.mp4',main)
    main.state('zoomed')

def start_vid2():
    main=Toplevel(root)
    main.title("Video 2")
    video1 = Video('example_2.mp4',main)
    main.state('zoomed')


#video2 = Video('example_2.mp4',root)
#video2.set_grid(1,3)

b1=Button(root,text='Play Video 1',command=start_vid,padx=20,pady=20)
b1.grid(row=0,column=0)
b2=Button(root,text='Play Video 2',command=start_vid2,padx=20,pady=20)
b2.grid(row=0,column=1)

root.mainloop()
