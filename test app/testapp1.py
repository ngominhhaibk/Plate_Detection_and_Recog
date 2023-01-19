from tkinter import *
from tkinter import messagebox as tkMessageBox
import tkinter

top = tkinter.Tk()

def helloCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

B = tkinter.Button(top, text ="Hello", command = helloCallBack)

#relheight, relwidth - tỉ lệ Chiều cao và chiều rộng giữa 0.0 và 1.0,  (kích thước của place)
# theo tỉ lệ của cửa sổ tiện ích
#relx, rely - tỉ lệ Phần bù ngang và dọc giữa 0,0 và 1,0, # theo tỉ lệ của cửa sổ tiện ích (vị trí của place)
B.pack()
# B.place(bordermode=OUTSIDE, height=100, width=100)
B.place(bordermode=INSIDE , relwidth=0.5, relheight=0.5, relx=0.5, rely = 0.5)

top.mainloop()