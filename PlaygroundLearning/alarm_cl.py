# A version of the alarm clock with a working GUI. 
import time

from Tkinter import *


print(time.strftime("%H:%M:%S"))

running = True # Global flag

class Application(Frame): 
    def __init__(self, master):
        # super(Application, self).__init__(master)
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()


    def create_widgets(self):
        #Explain the program
        Label(self, text = "This is a basic alarm clock program").grid(row = 0, column = 0, columnspan = 2, sticky = W)

        #Set the alarm time
        Label(self, text = "Enter what time you want the alarm to go off at").grid(row = 1, column = 0, sticky = W)
        self.alarmtime = Entry(self)
        self.alarmtime.grid(row = 1, column = 3, sticky = W)

        #Set the URL for the Youtube video
        Label(self, text = "Enter the URL of the Youtube video you want to be woken up by").grid(row = 2, column = 0, sticky = W)
        self.video_url = Entry(self)
        self.video_url.grid(row = 2, column = 3, sticky = W)
        self.bttn1 = Button(self, text = "Submit", command = self.alarm).grid(row = 5, column = 0)
        self.bttn2 = Button(self, text = "Quit", command = self.quit).grid(row = 5, column = 2)
        self.bttn3 = Button(self, text = "Stop", command = self.stop).grid(row = 5, column = 1)

    def alarm(self):
        #Get the time and URL from the user
        sound = self.alarmtime.get()
        video = self.video_url.get()
        #Show both inputs in terminal
        print(sound)
        print(video)
        #Print starting time
        print "start time:",(time.strftime("%H:%M:%S"))
        the_time = (time.strftime("%H:%M:%S"))
        self.refresher(sound, the_time)
        # while running  == True and sound != the_time:
        #     print("clock:",time.strftime("%H:%M:%S"))
        #     root.after(1000)
        # if sound == the_time:
        #     print(video)
        #     quit()

    def quit(self):
        quit()

    def stop(self):
        running = False

    def refresher(self, sound, the_time):

        while running  == True and sound != the_time:
            print("clock:",time.strftime("%H:%M:%S"))
            root.after(2000, self.refresher)
        # if sound == the_time:
        #     print(video)
        #     quit()


		

#Main

root = Tk() 
root.title("Alarm Clock")
root.geometry()
app = Application(root) 
root.mainloop()