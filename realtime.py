from part04_predict_character import *
import time
from sklearn import preprocessing
import numpy as np
import tkinter as tk  #modul tạo giao diện đồ họa
import cv2
from PIL import ImageTk
import PIL
from threading import Thread


previour_time = time.time()
frame_image = 1
# url = "http://192.168.92.238:4747/video"

# load model
wpod_net = load_model("model/wpod-net.json")

json_file = open('model/MobileNets_character_recognition.json', 'r')
loaded_model_json = json_file.read()
model = model_from_json(loaded_model_json)
model.load_weights("model/License_character_recognition_weight.h5")
labels = preprocessing.LabelEncoder()
labels.classes_ = np.load('model/license_character_classes.npy')
json_file.close()
###################################################################################
root = tk.Tk()  #tạo cửa sổ window
root.title('HUST_Parking')
root.geometry("+30+30")  #khởi tạo vị trí mở cửa sổ app ban đầu trên màn hình chính

canvas = tk.Canvas(root, height=700, width=1350)  #tạo vùng chữ nhật để bố trí bố cục (700 *300)
canvas.pack() #tạo bố cục
###################################################################################
#GUI-IPCAM
vung_CAM = tk.Frame(root, bg = 'yellow')
vung_CAM.place(relwidth=0.55, relheight=1, relx = 0.01)

#Image process
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
def cv2_to_image_tkinter(image):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)  #BGR ->RGBA
	imagePIL = PIL.Image.fromarray(image)  #Tạo bộ nhớ hình ảnh từ một đối tượng xuất giao diện mảng
	imgtk = ImageTk.PhotoImage(image = imagePIL) #hình ảnh tương thích với Tkinter
	return imgtk
# ###################################################################################
def CAM_IP():
	# cap = cv2.VideoCapture(url)
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	######lặp
	def showCam_IP():
		global previour_time
		global frame_image
		_, frame_image = cap.read()
		threadReadBarcode = Thread(target = delay())
		threadReadBarcode.start()
		imgtk = cv2_to_image_tkinter(frame_image) # chuyển ảnh đọc từ cv2 sang hình ảnh riêng của tkinter
		lb_CAM_IP.imgtk = imgtk  #đặt ảnh đọc được từ cam sang ô lb_webcam, quan trọng
		lb_CAM_IP.configure(image=imgtk) #cấu hình ảnh cho widget
		lb_CAM_IP.after(10, showCam_IP) #sau 10ms sẽ gọi lại hàm showCam_QR (khung web_cam)
	######lặp
	threadShowCam_QR=Thread(target=showCam_IP)  #thực thi chính của CAM() -> chạy hàm showCam()
	threadShowCam_QR.start()
# ###################################################################################
def delay():
	global previour_time
	if(time.time() - previour_time > 2):  #check sau 2s
		check_plate()
		previour_time = time.time()
# ###################################################################################
def check_plate():
	try:
		text_plate,img_plate = get_plate()   #lấy biển số
		clear_data() #xóa ô dữ liệu cũ
		lb_kitu_tim_dc['text'] = text_plate  #đặt biển số vào ô lbPlate_ipcam
		imgtk = cv2_to_image_tkinter(img_plate)
		lb_bienso_tim_dc.imgtk = imgtk
		lb_bienso_tim_dc.configure(image = imgtk)
	except: #do không có biển số hoặc không có COr -> lỗi -> dùng try,except
		print("No License plate is founded!")
# ###################################################################################
def clear_data():
	lb_kitu_tim_dc['bg'] = '#F0F0F0'	 #cài đặt màu nền màu #F0F0F0(màu trắng)  (xóa sạch) 
	lb_kitu_tim_dc['text'] = ''	#xóa text
# ###################################################################################
def get_plate():
	global frame_image
	image,_ = plate_image(frame_image, wpod_net)  #part1
	image_binary = binary_image(image)				#part2
	list_ki_tu_tren, list_ki_tu_duoi = get_characters(image_binary) #part3	
	# ###################################################################################
	flag_top = False
	for j in range(5): #(từ 0 đến 4)
		string_ki_tu_tren = string_LP(list_ki_tu_tren, model, labels) #predict_character.py
		if(len(string_ki_tu_tren)!=4): #nếu số kí tự >=4 thì thực hiện bước sau
			continue
		if(string_ki_tu_tren[0].isdigit() and string_ki_tu_tren[1].isdigit() and string_ki_tu_tren[-1].isdigit() and not string_ki_tu_tren[2].isdigit()):
			#nếu kí tự thứ 0,1,3 là số và kí tự 2 không là số
			flag_top = True
			break
	# ví dụ : 59M2 ứng ới 0,1,2,3
	if not(flag_top):   # nếu mà kí tự thứ 0,1,3 là số và kí tự 2 không là số
		if not(string_ki_tu_tren[0].isdigit()): #nếu kí thứ thứ 0 không là số 
			string_ki_tu_tren = string_ki_tu_tren.replace(string_ki_tu_tren[0], '') #loại bỏ 
		if not(string_ki_tu_tren[-1].isdigit()): #nếu kí thứ thứ 3 không là số 
			string_ki_tu_tren = string_ki_tu_tren.replace(string_ki_tu_tren[-1], '') #loại bỏ 
		if not(string_ki_tu_tren[1].isdigit()): #nếu kí thứ thứ 1 không là số 
			string_ki_tu_tren = string_ki_tu_tren.replace(string_ki_tu_tren[1], '') #loại bỏ 
		if (string_ki_tu_tren[2].isdigit()): #nếu kí thứ thứ 2 là số 
			string_ki_tu_tren = string_ki_tu_tren.replace(string_ki_tu_tren[2], '') #loại bỏ 
	# ###################################################################################
	flag_bot = False
	string_ki_tu_duoi = string_LP(list_ki_tu_duoi, model, labels)
	'''check chuỗi kí tự dưới của biển số, xem có phải là số hay không và có đủ 5 kí tự hay không '''
	if(string_ki_tu_duoi.isdigit() and len(string_ki_tu_duoi) ==5):
		flag_bot = True
	# print(string_ki_tu_duoi)
	#vd: 19999 # 5 kí tự
	if not (flag_bot):
		for i in string_ki_tu_duoi:
			if not (i.isdigit()):  # nếu kí tự nào không phải là số 
				string_ki_tu_duoi = string_ki_tu_duoi.replace(i, '') # loại bỏ

	string_ki_tu_tren = string_ki_tu_tren[0:2] + "-" + string_ki_tu_tren[2:]
	if len(string_ki_tu_duoi) == 5:
		string_ki_tu_duoi = string_ki_tu_duoi[0:3] + "." + string_ki_tu_duoi[3:]

	text_plate = string_ki_tu_tren + '\n' + string_ki_tu_duoi
	return text_plate,image
# ###################################################################################

CAM_IP()
#lặp cuối
root.mainloop()


