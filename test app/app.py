from tkinter import *
from tkinter import messagebox as tkMessageBox
import tkinter as tk

#import tkinter as tk, tạo app
root = tk.Tk()  #tạo cửa sổ window
root.title('HUST_Parking')
root.geometry("+30+30")  #khởi tạo vị trí mở cửa sổ app ban đầu trên màn hình chính

canvas = tk.Canvas(root, height=700, width=1500)  #tạo vùng chữ nhật để bố trí bố cục (700 *300)
canvas.pack() #tạo bố cục

###################################################################################
#1)GUI-WEBCAM_quetQR
vung_webcam = tk.Frame(root, bg='gray') #tạo một khung trên cửa số root #bg(màu nền)
vung_webcam.place(relwidth=0.26, relheight=0.66, relx=0.01, rely = 0.15) #tạo bố cục (vị trí)

#2)GUI-IPCAM
vung_CAM_IP = tk.Frame(root, bg = 'yellow')
vung_CAM_IP.place(relwidth=0.35, relheight=1, relx = 0.28)

#3)Image saved frame
vung_anh_daluu = tk.Frame(root, bg = 'red')
vung_anh_daluu.place(relwidth=0.35, relheight=1, relx = 0.64)

#4)clock frame (trên cùng bên trái)
vung_clock = tk.Frame(root, bg='blue')
vung_clock.place(relwidth=0.26, relheight=0.14, relx=0.01, rely=0.01)

#5)#thời gian đỗ (dưới cùng bên trái)
vung_timeIO = tk.Frame(root, bg = 'yellow')
vung_timeIO.place(relwidth=0.26, relheight=0.17, relx=0.01, rely=0.82)

###################################################################################
# webcam
lb1 = tk.Label(vung_webcam, text= "Quét MSSV", font=("Courier", 27))#, fg='red')#, bg ='black')#text
lb1.place(relx=0, rely=0.01, relheight=0.1,relwidth=1)

lb_webcam = tk.Label(vung_webcam, bg='cyan')
lb_webcam.place(relx=0, rely = 0.12, relwidth = 1, relheight=0.77)

lb2 =tk.Label(vung_webcam, text= "MSSV:", font=("Courier", 24), fg='red')#, bg ='black')  #text
lb2.place(relx =0, rely =0.9)

lb_code = tk.Label(vung_webcam, font=("Courier", 24), fg='red')#, bg ='black')   # giao diện phần đọc mã code
lb_code.place(relx = 0.33 , rely = 0.9)
# ###################################################################################
#clock frame 
lb_clock = tk.Label(vung_clock, font = ("Courier", 30, "bold"))#, fg='red')  #fg:màu chữ của label 
lb_clock.place(relx=0, rely=0, relwidth=1, relheight=1)

# ###################################################################################
# IPCAM frame 
lb_CAM_IP = tk.Label(vung_CAM_IP, bg = 'purple')
lb_CAM_IP.place(relx=0, rely = 0.09, relwidth = 1, relheight=0.7)

lb3 = tk.Label(vung_CAM_IP, text = 'IP CAMERA', font=("Courier", 27), fg = 'black')#, bg= 'magenta')
lb3.place(relx=0, rely = 0.01, relwidth =1, relheight=0.07)

lbPlate_ip = tk.Label(vung_CAM_IP, font=("Courier", 27), fg = 'black')#, bg= 'magenta')
lbPlate_ip.place(relx=0, rely = 0.8, relheight=0.18, relwidth=1)
# ###################################################################################
# #vùng ảnh biển số (kèm kí tự đã lưu) đã lưu trước đó
lb_anh_daluu = tk.Label(vung_anh_daluu, bg = 'green')
lb_anh_daluu.place(relx=0, rely = 0.09, relwidth = 1, relheight=0.7)

lb4 = tk.Label(vung_anh_daluu, text = 'Xe ra', font=("Courier", 27), fg = 'black')#, bg= 'yellow')
lb4.place(relx=0, rely = 0.01, relwidth =1, relheight=0.07)

lb_bso_daluu = tk.Label(vung_anh_daluu, font=("Courier", 27), fg = 'black')#, bg= '#57f542')
lb_bso_daluu.place(relx=0, rely = 0.8, relheight=0.18, relwidth=1)
# ###################################################################################
# # time_frame (thời gian đỗ )
lb_time_park = tk.Label(vung_timeIO, font=("Courier", 16))
lb_time_park.place(relx=0, rely=0, relheight=1, relwidth=1)

root.mainloop()