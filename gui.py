import tkinter as tk
import exceptions
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

        self.status_label = tk.Label(master= self, text= "Status code: ")
        self.status_label.grid(row= 1, column= 1, sticky= "w")

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
        """
        Gets the HTML and info of url, saves them into self.response and self.info
        """
        self.response = functions.get(url)
        self.info = functions.get_info(url)


    def insert_path_title(self):
        """
        Inserts default path and title of Reddit post into entries if empty.
        Gets title from self.info.
        """
        if self.title_entry.get() == "":
            self.title_entry.insert(0, self.info["title"])

        if self.path_entry.get() == "":
            if op_sys == "Windows":
                self.path_entry.insert(0, win_default_path)


    def validate_url(self, url: str):
        """
        Checks if "reddit.com" is in URL.
        Returns True if URL is valid, False if not.
        """
        if "reddit.com" in url:
            return True
        else:
            return False


    def preload(self):
        """
        Preloads response and info from URL.
        Calls self.validate_url, self.make_request and self.insert_path_title, configures self.status_label.
        Can raise exceptions.Error and exceptions.ServerError
        """
        url = self.url_entry.get()
        if self.validate_url(url) is False:
            raise exceptions.Error(description= "No Reddit URL", caller= "App.preload()")

        self.make_request(url)
        self.status_label.configure(text= f"Status code: {self.response.status_code}")

        self.insert_path_title()

        print("Finished preload")


    def check(self):
        """
        Calls self.preload and handles the error. Used on self.check_button.
        """
        try:
            self.preload()
        except exceptions.Error as err:
            print(err)
            return
        except exceptions.ServerError as serr:
            self.status_label.configure(text=f"Status code: {serr.code}")
            print(serr)
            return


    def check_path(self, path):
        return os.path.exists(path)


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


    def del_temp(self):
        """
        Deletes the audio and video files in temp folder if the files exist.
        """
        temp_vid = os.path.join(os.getcwd(), "temp", "Vid.ts")
        temp_aud = os.path.join(os.getcwd(), "temp", "Aud.aac")

        if os.path.exists(temp_vid):
            os.remove(temp_vid)

        if os.path.exists(temp_aud):
            os.remove(temp_aud)


    def download(self):
        """
        Main function to download videos. Calls preload it not called prior. Handles errors.
        """
        if self.response is None or self.info is None:
            try:
                self.preload()
            except exceptions.Error as err:
                print(err)
                return
            except exceptions.ServerError as serr:
                self.status_label.configure(text= f"Status code: {serr.code}")
                print(serr)
                return

        title = self.title_entry.get()
        path = self.path_entry.get()

        # Checks for empty entries and path validity
        if title == "":
            print("No title given")
            return
        if self.check_path(path) is False:
            print("Invalid path")
            return

        if self.info["is_reddit_media_domain"] is False:
            print("Media not hosted on Reddit")
            return

        domain = self.parse()
        print(domain)

        if domain == "i":
            try:
                functions.download(url= self.src,
                                   path= path,
                                   file_name= title,
                                   file_type= ".gif")
            except exceptions.ServerError as serr:
                print(serr)
                return
        elif domain == "p":
            try:
                functions.download(url= self.src[-1],
                                   path= path,
                                   file_name= title)
            except exceptions.ServerError as serr:
                print(serr)
                return
        elif domain == "v":
            try:
                functions.download(url= self.src[0],
                                   path= os.path.join(os.getcwd(), "temp"),
                                   file_name= "Vid",
                                   file_type= ".ts")
                functions.download(url= self.src[-1],
                                   path= os.path.join(os.getcwd(), "temp"),
                                   file_name= "Aud",
                                   file_type= ".aac")
            except exceptions.ServerError as serr:
                print(serr)
                return

            try:
                cmd_stdout = ffmpeg_cmd.merge_av(video= "Vid.ts",
                                                 audio= "Aud.aac",
                                                 output_name= title,
                                                 path= path)
            except exceptions.FFmpegError as ferr:
                print(ferr)
                return

            self.del_temp()

        print("Downloaded video")
        self.clear()





app = App()

app.mainloop()