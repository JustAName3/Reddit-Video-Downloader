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
        self.src = None # Tuple, list or str, URL to video source

        self.url_label = tk.Label(master= self, text= "Reddit URL:")
        self.url_label.grid(row= 0, column= 0, pady= 10, padx= 10)

        self.url_entry = tk.Entry(master= self, width= 80)
        self.url_entry.grid(row= 0, column= 1, pady= 10, padx= (0, 10), columnspan= 2)

        self.check_button = tk.Button(master= self,
                                      text= "Check",
                                      command= self.check)
        self.check_button.grid(row= 1, column= 0, padx= 10)

        self.title_label = tk.Label(master= self, text= "Title:")
        self.title_label.grid(row= 2, column= 0, pady= (20, 5), padx= 20)

        self.title_entry = tk.Entry(master= self, width= 60)
        self.title_entry.grid(row= 2, column= 1, sticky= "w")

        self.path_label = tk.Label(master= self, text="Save in:")
        self.path_label.grid(row= 3, column= 0, padx= 10, pady= 5)

        self.path_entry = tk.Entry(master= self, width= 60)
        self.path_entry.grid(row= 3, column= 1, sticky="w")

        self.download_button = tk.Button(master= self,
                                         text= "Download",
                                         command= self.download)
        self.download_button.grid(row= 4, column= 0, padx= 10, pady= 20)


        self.inputs.append(self.url_entry)
        self.inputs.append(self.title_entry)
        self.inputs.append(self.path_entry)


    def clear(self):
        for entry in self.inputs:
            entry.delete("0", "end")

        self.info = None
        self.response = None
        self.src = None


    def make_request(self, url):
        if self.url_entry.get() == "":
            print("No url")
            return

        self.response = functions.get(url)
        self.info = functions.get_info(url)


    def check(self):
        """
        Calls self.make_request and inserts title and path into entries.
        """
        if self.info is None or self.response is None:
            self.make_request(self.url_entry.get())

        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, self.info["title"])

        if op_sys == "Windows":
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, win_default_path)

        print("Check completed")


    def parse(self):
        """
        Calls the functions.py parsing functions
        Returns str -> "v", "i" or "p" depending on video source URL
        """
        if self.info["domain"] == "v.redd.it":
            self.src = functions.parse_packaged_media_redd_it(self.response)

            if self.src is None:
                self.src = functions.parse_v_redd_it(self.info)
                return "v"
            else:
                return "p"

        elif self.info["domain"] == "i.redd.it":
            self.src = functions.parse_i_redd_it(self.response)
            return "i"


    def download(self):

        if self.info is None or self.response is None:
            self.make_request(self.url_entry.get())

        # Checks if either of the entries is empty
        if self.url_entry.get() == "":
            print("No URL given")
            return
        elif self.title_entry.get() == "":
            print("No file name given")
            return
        elif self.path_entry.get() == "":
            print("No path given")
            return

        if self.info["is_reddit_media_domain"] is False:
            print("Media not hosted on Redit")
            return

        title = self.title_entry.get()
        path = self.path_entry.get()

        domain = self.parse()
        print(domain)

        if domain == "i":
            functions.download(url= self.src,
                               path= path,
                               file_name= title,
                               file_type= ".gif")
        elif domain == "p":
            functions.download(url= self.src[-1],
                               path= path,
                               file_name= title)
        elif domain == "v":
            functions.download(url= self.src[0],
                               path= os.getcwd(),
                               file_name= "Vid",
                               file_type= ".ts")
            functions.download(url= self.src[-1],
                               path= os.getcwd(),
                               file_name= "Aud",
                               file_type= ".aac")

            cmd_stdout = ffmpeg_cmd.merge_av(video= "Vid.ts",
                                             audio= "Aud.aac",
                                             output_name= title,
                                             path= path)

            os.remove("Aud.aac")
            os.remove("Vid.ts")

        print("Downloaded video")
        self.clear()





app = App()

app.mainloop()