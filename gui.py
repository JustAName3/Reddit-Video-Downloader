import tkinter as tk
import functions
import ffmpeg_cmd
import platform
import os


op_sys = platform.system()
win_default_path = os.path.join("C:", r"\Users", os.getlogin(), "Videos")



class App(tk.Tk):
    """
    Simple UI with logic for downloading Reddit videos
    """
    def __init__(self):
        super().__init__()

        self.title("Reddit Video Downloader")
        self.inputs: list = [] # Used for storing all input widgets and clearing them
        self.info: dict = None
        self.response = None #requsests.Response object

        self.url_label = tk.Label(master= self, text= "Reddit URL:")
        self.url_label.grid(row= 0, column= 0, pady= 10, padx= 10)

        self.url_entry = tk.Entry(master= self, width= 80)
        self.url_entry.grid(row= 0, column= 1, pady= 10, padx= (0, 10), columnspan= 2)

        self.check_button = tk.Button(master= self,
                                      text= "Check",
                                      command=lambda : self.check(url= self.url_entry.get()))
        self.check_button.grid(row= 1, column= 0, padx= 10)

        self.title_label = tk.Label(master= self, text= "Title:")
        self.title_label.grid(row= 2, column= 0, pady= (20, 5), padx= 20)

        self.title_entry = tk.Entry(master= self, width= 60)
        self.title_entry.grid(row= 2, column= 1, sticky= "w")

        self.path_label = tk.Label(master= self, text="Save in:")
        self.path_label.grid(row= 3, column= 0, padx= 10, pady= 5)

        self.path_entry = tk.Entry(master= self, width= 60)
        self.path_entry.grid(row= 3, column= 1, sticky="w")


        self.inputs.append(self.url_entry)
        self.inputs.append(self.title_entry)
        self.inputs.append(self.path_entry)


    def clear(self):
        for entry in self.inputs:
            entry.delete("0", "end")

        del self.info
        del self.response


    def check(self, url):
        """
        Gets the HTML and info: dict of url and inserts them into entry widgets
        Stores info and response in self.info and self.response.
        """
        if self.url_entry.get() == "":
            print("No url")
            return

        self.response = functions.get(url)
        self.info = functions.get_info(url)

        self.title_entry.insert(0, self.info["title"])

        if op_sys == "Windows":
            self.path_entry.insert(0, win_default_path)








app = App()

app.mainloop()