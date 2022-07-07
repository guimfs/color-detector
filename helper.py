import tkinter as tk
from tkinter import ttk


class Loader(tk.Frame):

    selected_image = ''

    def __init__(self, root, list):
        super().__init__(root)

        self.frame = tk.Frame(width=250, height=100, bg="#CDAA7D")
        self.frame.pack(expand=True, padx=20, pady=20)

        self.label = tk.Label(
            self.frame, 
            text='Select your image',
            bg="#CDAA7D",
            justify='center'
            )
        self.label.grid(row=0, column=0, padx=0, pady=0)

        self.var = tk.StringVar()

        self.combo = ttk.Combobox(
            self.frame, 
            width=30, 
            state="readonly", 
            values=list,
            textvariable=self.var,
            justify='center'
            )
        self.combo.grid(row=1, column=0, sticky='nwes', padx=0, pady=7)

        self.button = tk.Button(
            self.frame, 
            text="Load", 
            command=self.select_image)
        self.button.grid(row=2, column=0)

    def select_image(self):
        global selected_image
        selected_image = self.var.get()
        self.master.destroy()
    

def run_loader(list):
    root = tk.Tk()
    root.title('Select your image')
    root.geometry("300x130")
    root.eval('tk::PlaceWindow . center')
    root.config(bg="#CDAA7D")
    my_app = Loader(root, list)
    my_app.mainloop()
    return selected_image