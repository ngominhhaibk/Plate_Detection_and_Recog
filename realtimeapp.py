from tkinter import *
from tkinter import messagebox as tkMessageBox
import tkinter as tk

#import tkinter as tk, tạo app
root = tk.Tk()  #tạo cửa sổ window
root.title('HUST_Parking')
root.geometry("+30+30")  #khởi tạo vị trí mở cửa sổ app ban đầu trên màn hình chính

canvas = tk.Canvas(root, height=700, width=1350)  #tạo vùng chữ nhật để bố trí bố cục (700 *300)
canvas.pack() #tạo bố cục

###################################################################################

#2)GUI-IPCAM
vung_CAM = tk.Frame(root, bg = 'yellow')
vung_CAM.place(relwidth=0.55, relheight=1, relx = 0.01)

#3)Image process
vung_anh_daluu = tk.Frame(root, bg = 'gray')
vung_anh_daluu.place(relwidth=0.42, relheight=1, relx = 0.58)



# ###################################################################################
# CAM frame 
lb_CAM_IP = tk.Label(vung_CAM)#, bg = 'purple')
lb_CAM_IP.place( relwidth = 1, relheight=1)

# # ###################################################################################
# #vùng ảnh biển số (kèm kí tự đã lưu) đã lưu trước đó
lb_bienso_tim_dc = tk.Label(vung_anh_daluu, bg = 'gray')
lb_bienso_tim_dc.place(relx=0, rely = 0.09, relwidth = 1, relheight=0.7)

lb_kitu_tim_dc = tk.Label(vung_anh_daluu, font=("Courier", 27), fg = 'black')#, bg= '#57f542')
lb_kitu_tim_dc.place(relx=0, rely = 0.8, relheight=0.18, relwidth=1)
# ###################################################################################

root.mainloop()