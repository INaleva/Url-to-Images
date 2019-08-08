from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import logic


class WindowsGui(Frame):
    def __init__(self,parent):
        start = 10
        end = 0

        Frame.__init__(self,parent)
        self.url_label = Label(self, text="Enter URL:", fg="blue")
        self.url_label.grid(row=0, column=0, sticky=W, padx=(start, end), pady=(start, end))

        self.url_address = Entry(self, text="google.com", width=40)
        self.url_address.grid(row=0, column=1, sticky=W, pady=(start, end))

        self.browse_label = Message(self, fg="blue", width=200)
        self.browse_label.grid(row=1, column=1, sticky=W, padx=(start, end))

        self.browse_button = Button(self, text="path to save", command=self.select_folder)
        self.browse_button.grid(row=1, column=0, sticky=W, padx=(start, end), pady=(start, end))

        global download_type
        download_type = StringVar()
        download_type.set("image")

        self.radio1 = Radiobutton(self, text="Save as images", variable=download_type, value="image")
        self.radio1.select()
        self.radio1.grid(row=3, column=0, sticky=W, padx=(start, end), pady=(start, end))

        self.radio2 = Radiobutton(self, text="Save as Urls", variable=download_type, value="url")
        self.radio2.deselect()
        self.radio2.grid(row=3, column=1, stick=W, pady=(start, end))

        self.sep = ttk.Separator(self, orient=HORIZONTAL,)
        self.sep.grid(row=4, columnspan=5, sticky=EW)

        self.download_button = Button(self, text="Fetch images", command=self.start_downloading)
        self.download_button.grid(row=5, column=0, sticky=W, padx=(10, 10), pady=(10, 10))

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        self.browse_label.config(text=folder_path)

    def start_downloading(self):
        logic.fetch_images(self.url_address.get(), self.browse_label.cget("text"), download_type.get())


root = Tk()
root.title("Website Stripper")
root.geometry("400x200")
root.resizable(False, False)
win_gui = WindowsGui(root)
win_gui.pack()
root.mainloop()










