import customtkinter
from tkinter import *

app = customtkinter.CTk()

tabview = customtkinter.CTkTabview(app)
tabview.pack(padx=20, pady=20)

tabview.add("tab 1")  # add tab at the end
tabview.add("tab 2")  # add tab at the end
tabview.set("tab 2")  # set currently visible tab

button = customtkinter.CTkButton(master=tabview.tab("tab 1"))
button.pack(padx=20, pady=20)

# tab_1 = tabview.add("tab 1")
# tab_2 = tabview.add("tab 2")

button1 = customtkinter.CTkButton(tabview.tab("tab 2"))
button1.pack(padx=20, pady=20)

app.mainloop()