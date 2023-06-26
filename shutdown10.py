import customtkinter as ctk
import os
import time
from typing import Callable
import datetime

class Timebox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1,
                 min_value,max_value,
                 command: Callable = None,
                 **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(*args, width=width, height=height, **kwargs)     
        self.step_size = step_size
        self.command = command
        self.configure(fg_color=("gray78", "gray28"))  
        #self.grid_columnconfigure((0, 2), weight=0)  
        #self.grid_columnconfigure(1, weight=1)  
        self.entry = ctk.CTkEntry(self, width=150, height=150,border_width=0,font=("Arial", 106),justify="center",fg_color=('#dbdbdb', '#2b2b2b'), corner_radius=0,insertwidth=0)
        self.entry.grid(row=0,rowspan=1, column=2, columnspan=2, padx=0, pady=0, sticky="nsew")
        # default value
        self.entry.insert(0, "00")
        # All elements on mousewheel event
        self.entry.bind("<MouseWheel>", self.on_mouse_wheel)
        self.entry.bind("<Key>", self.breake)
        self.entry.bind("<Button-1>",self.breake)
        self.entry.bind('<Enter>', self.on_enter)
        self.entry.bind('<Leave>', self.on_leave)
        self.entry.bind("<Button-2>", self.breake)
        
    def breake(self,event):
        return "break" 
        
    def on_enter(self,event):
        event.widget.configure(cursor='hand2')

    def on_leave(self,event):
        event.widget.configure(cursor='xterm')        
        
    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            value1= str(value).zfill(2)
            if value <=self.max_value: 
                self.entry.delete(0, "end")
                self.entry.insert(0, value1)
        except ValueError:
            return
    
    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            value1= str(value).zfill(2)
            if value >=self.min_value: 
                self.entry.delete(0, "end")
                self.entry.insert(0, value1)
        except ValueError:
            return

    def get(self) -> int:
        try:
            return int(self.entry.get())
        except ValueError:
            return 0
            
    def on_mouse_wheel(self, event):
        if not self.timer_running: 
            if event.delta > 0:
                self.add_button_callback()
            else:
                self.subtract_button_callback()
            
    def start_timer(self):
        self.timer_running = True
        self.unbind("<MouseWheel>")

    def stop_timer(self):
        self.timer_running = False
        self.bind("<MouseWheel>", self.on_mouse_wheel)
            
    def set(self, value: int):
        value1= str(value).zfill(2)
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value1))                

        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
        self.title("Shutdowner Windows")
        self.geometry(f"{520}x{235}")
        #Creating Main Frame
        self.main_frame = ctk.CTkFrame(self, width=510,height=290)
        self.main_frame.grid(row=0, column=10,columnspan=10, rowspan=10, ipadx=5, ipady=0, padx=0, pady=0, sticky="nw")
        self.main_frame.grid_rowconfigure(3, weight=1)
        #Option Menu
        self.optionmenu_1 = ctk.CTkOptionMenu(self.main_frame, values=["at", "after"],font=("Arial", 20),fg_color=('#dbdbdb', '#2b2b2b'),text_color=('black','white'),button_color=('#dbdbdb', '#2b2b2b'),button_hover_color=('#dbdbdb', '#2b2b2b'))
        self.optionmenu_1.grid(row=0, column=3, pady=0, padx=5, sticky="ns",columnspan=2,rowspan=1)
        self.optionmenu_1.set("after")
        self.option_menu_2=ctk.CTkOptionMenu(self.main_frame,values=["Shutdown", "Reboot","Sleep","Log Out"], font=("Arial", 20),fg_color=('#dbdbdb', '#2b2b2b'),text_color=('black','white'),button_color=('#dbdbdb', '#2b2b2b'),button_hover_color=('#dbdbdb', '#2b2b2b'))
        self.option_menu_2.grid(row=0, column=0,columnspan=3, pady=0, padx=5, sticky="nsew")
        self.option_menu_2.set("Shutdown")
        #Buttons (start and cancel)
        self.start_button = ctk.CTkButton(self.main_frame, text = "Start", command=self.mod,font=("Arial", 15))
        self.start_button.grid(row=0, column=5,columnspan=3, padx=5, pady=5, rowspan=1)
        self.cancel_button = ctk.CTkButton(self.main_frame, text = "Cancel",font=("Arial", 15), command=self.cancel_shutdown)
        self.cancel_button.grid(row=5, column=5,columnspan=2, padx=5, pady=10, rowspan=1)
        #Ctk Switch for appearance mode 
        self.switch_var = ctk.StringVar()
        self.switch_mode = ctk.CTkSwitch(self.main_frame,text="🌙",font=("Arial", 25), variable=self.switch_var,onvalue="on", offvalue="off",command=self.change_appearance_mode_event)
        self.switch_mode.grid(row=5, column=0, pady=10, padx=20, sticky="n")
        #Timeboxies and labels ":"
        self.timebox_hours = Timebox(self.main_frame, width=105, step_size=1, min_value=0, max_value=23,fg_color= "transparent")
        self.timebox_hours.grid(row=1, column=0,columnspan=1, rowspan=2, ipadx=0, ipady=0, padx=2, pady=0,sticky="n")
        self.label_1 = ctk.CTkLabel(self.main_frame,text=":",font=("Arial", 106),justify="center",fg_color= "transparent")
        self.label_1.grid(row=1, column=2,columnspan=1, rowspan=2, ipadx=0, ipady=0, padx=0, pady=0,sticky="n")
        self.label_2 = ctk.CTkLabel(self.main_frame,text=":",font=("Arial", 106),justify="center",fg_color= "transparent")
        self.label_2.grid(row=1, column=4,columnspan=1, rowspan=2, ipadx=0, ipady=0, padx=0, pady=0,sticky="n")
        self.timebox_minutes = Timebox(self.main_frame, width=105, step_size=1, min_value=0,max_value=59)
        self.timebox_minutes.grid(row=1, column=3,columnspan=1, rowspan=2, ipadx=0, ipady=0, padx=0, pady=0,sticky="n")
        self.timebox_seconds = Timebox(self.main_frame, width=105, step_size=1,min_value=0,max_value=59)
        self.timebox_seconds.grid(row=1, column=5,columnspan=1,rowspan=2, ipadx=0, ipady=0, padx=0, pady=0,sticky="n")
        #Labels Function
        self.label_hours = ctk.CTkLabel(self.main_frame,text="HOURS",font=("Roboto Mono", 20),justify="center",fg_color= "transparent")
        self.label_hours.grid(row=2, column=0,columnspan=1, rowspan=2, ipadx=0, ipady=0, padx=0, pady=0,sticky="s")
        self.label_minutes = ctk.CTkLabel(self.main_frame,text="MINUTES",font=("Roboto Mono", 20),justify="center",fg_color= "transparent")
        self.label_minutes.grid(row=2, column=3,columnspan=1, rowspan=2, ipadx=0, ipady=0, padx=0, pady=0,sticky="s")
        self.label_seconds = ctk.CTkLabel(self.main_frame,text="SECONDS",font=("Roboto Mono", 20),justify="center",fg_color= "transparent")
        self.label_seconds.grid(row=2, column=5,columnspan=1, rowspan=2, ipadx=0, ipady=0, padx=0, pady=0,sticky="s")
        #Flag
        self.active = bool(None)
        self.pause = False
        self.backup = 0
        self.timebox_hours.timer_running = False
        self.timebox_minutes.timer_running = False
        self.timebox_seconds.timer_running = False        

    def update_label_timer(self, shutdown_time_secs):
        if self.active is True:  
            self.timebox_hours.timer_running = True
            self.timebox_minutes.timer_running = True
            self.timebox_seconds.timer_running = True
            if shutdown_time_secs <= 0:
                if self.option_menu_2.get() == "Shutdown":
                    self.shutdown()
                elif self.option_menu_2.get() == "Reboot":     
                    self.suspend()
                elif self.option_menu_2.get() == "Log Out":
                    self.logout()
                    self.destroy() 
                elif self.option_menu_2.get() == "Sleep":
                    self.sleep()
                    self.destroy()
            else:
                hours, remainder = divmod(shutdown_time_secs, 3600)
                minutes, seconds = divmod(remainder, 60)
                hours1 = str(hours).zfill(2) 
                minutes1 = str(minutes).zfill(2) 
                seconds1 = str(seconds).zfill(2) 
                self.timebox_hours.set(hours1) 
                self.timebox_minutes.set(minutes1) 
                self.timebox_seconds.set(seconds1)
            if self.pause is False:
                self.after(1000, self.update_label_timer, shutdown_time_secs - 1)
                self.start_button.configure(text="Pause", command=self.pause_start)
            else:
                self.backup = shutdown_time_secs
                self.start_button.configure(text="Continue", command=self.pause_start) 
                
    def pause_start(self):
        if self.pause:
            self.pause = False
            self.update_label_timer(self.backup)
        else:
            self.pause = True   
            
    def change_appearance_mode_event(self):
        if self.switch_var.get() == "on":
            ctk.set_appearance_mode("light")
            self.switch_mode.configure(text="☀")
        else:
            ctk.set_appearance_mode("dark")
            self.switch_mode.configure(text="🌙")
            
    def mod(self):
        shutdown_time = ((int(self.timebox_hours.get()) * 60) + int(self.timebox_minutes.get())) * 60 + int(self.timebox_seconds.get())
        self.active = True        
        if shutdown_time > 0:
            if self.optionmenu_1.get() == 'after':
                self.shutdown_after()
            elif self.optionmenu_1.get() == 'at':
                self.shutdown_at()

    def shutdown_after(self):
        if self.active is True:
            try:
                hours = int(self.timebox_hours.get())
                minutes = int(self.timebox_minutes.get())
                seconds = int(self.timebox_seconds.get())
            except ValueError:
                hours = 0
                minutes = 0
                seconds = 0
            
            shutdown_time_secs = (hours * 60 + minutes) * 60 + seconds
            if shutdown_time_secs > 0:
                self.update_label_timer(shutdown_time_secs)
        else:
            hours = None
            minutes = None
            seconds = None
    def shutdown_at(self):
        try:
            hours = int(self.timebox_hours.get())
            minutes = int(self.timebox_minutes.get())
            seconds = int(self.timebox_seconds.get())
        except ValueError:
            hours = 0
            minutes = 0
            seconds = 0
        
        now = time.localtime()
        current_time_str = f"{now.tm_year}-{now.tm_mon}-{now.tm_mday} {now.tm_hour}:{now.tm_min}:{now.tm_sec}"
        shutdown_time_str = f"{now.tm_year}-{now.tm_mon}-{now.tm_mday} {hours}:{minutes}:{seconds}"

        shutdown_time = time.strptime(shutdown_time_str, "%Y-%m-%d %H:%M:%S")
        shutdown_time_secs = int(time.mktime(shutdown_time) - time.mktime(now))

        if shutdown_time_secs < 0:
        #The specified time has already passed, we add one day
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%Y-%m-%d")
            shutdown_time_str = f"{tomorrow_str} {hours}:{minutes}:{seconds}"
            shutdown_time = time.strptime(shutdown_time_str, "%Y-%m-%d %H:%M:%S")
            
        shutdown_time_secs = int(time.mktime(shutdown_time) - time.mktime(now))
        if shutdown_time_secs > 0:
            self.update_label_timer(shutdown_time_secs)           
        
    def shutdown(self):
        os.system("shutdown /s /t 0")
        
    def suspend(self):
        os.system("shutdown /r /t 0")
        
    def logout(self):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        
    def sleep(self):
        os.system("rundll32.exe powrprof.dll, SetSuspendState Sleep")
       
    def cancel_shutdown(self): 
        if self.pause is True:
            self.pause_start()           
        self.start_button.configure(text="Start", command=self.mod)
        self.active = False    
        self.timebox_hours.set(0)
        self.timebox_minutes.set(0)
        self.timebox_seconds.set(0) 
        self.timebox_hours.timer_running = False
        self.timebox_minutes.timer_running = False
        self.timebox_seconds.timer_running = False
        
if __name__ == "__main__":
    app = App()
    app.resizable(width=False, height=False)
    app.mainloop()