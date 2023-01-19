from part03_get_characters import *
import numpy as np
from sklearn import preprocessing

# 1)
def predict_from_model(image,model,labels):
	#đưa về kích thước 80*80, vì đây là kích thước ảnh training trc đó
	#muốn đưa ảnh vào predict thì phải có cùng kích thước với ảnh cần train
	image = cv2.resize(image,(80,80))  
	# print("image")
	# print(image)
	# print("image")
	image = np.stack((image,)*3, axis=-1) # do input đầu vào của model là (N,80,80,3)
	#Nối một chuỗi các mảng dọc theo một trục mới.
	# Tham số trục chỉ định chỉ số của trục mới trong các kích thước của kết quả. 
	# Ví dụ: nếu trục = 0 thì nó sẽ là kích thước đầu tiên và nếu trục = -1 thì nó sẽ là kích thước cuối cùng.

	# print(image)
	# print("image")
	# print("model.predict(image[np.newaxis,:]):",model.predict(image[np.newaxis,:])) # trả ra mảng xác suất các kí tự
	# print("np.argmax(model.predict(image[np.newaxis,:]))):",np.argmax(model.predict(image[np.newaxis,:]))) # cho ra stt trong mảng (bắt đầu từ 0)
	
	# model.predict(image[np.newaxis,:]): [[6.8173455e-18 4.6477762e-14 1.0850468e-15 2.7741737e-12 7.7002119e-16
	# 1.0000000e+00 1.4258761e-14 3.7516175e-12 2.6007579e-15 2.0568746e-11
	# 7.1161786e-17 6.6812392e-15 2.7844709e-14 3.1908822e-15 9.0044764e-18
	# 1.8774407e-15 1.0128618e-14 5.3878702e-16 4.9661506e-13 1.2363218e-12
	# 2.4883829e-14 4.2984680e-13 5.5695308e-17 1.1489552e-19 3.8923168e-16
	# 3.8950365e-15 8.7548275e-15 2.0493615e-17 3.0220884e-10 2.1480832e-15
	# 3.3950646e-18 2.5955065e-14 5.0500786e-15 4.7501404e-15 1.1125638e-14
	# 5.7755199e-14]]
	# 1/1 [==============================] - 0s 34ms/step
	# np.argmax(model.predict(image[np.newaxis,:])):]): 5 ( số 5 phát hiện có tỉ lệ gần 1 nhất)1.0000000e+00

	prediction = labels.inverse_transform([np.argmax(model.predict(image[np.newaxis,:]))]) # thêm N để thành (N,80,80,3)
	#argmax tìm ra xác xuất đúng với kí tự cao nhất (36 kí tự) 
	# inverse_transform đẩy cái kí tự đúng đó lên đầu
	# >>> le = preprocessing.LabelEncoder()
	# >>> le.fit(["paris", "paris", "tokyo", "amsterdam"])
	# LabelEncoder()
	# >>> list(le.classes_)
	# ['amsterdam', 'paris', 'tokyo']
	# >>> le.transform(["tokyo", "tokyo", "paris"])
	# array([2, 2, 1]...)
	# >>> list(le.inverse_transform([2, 2, 1]))
	# ['tokyo', 'tokyo', 'paris']
	#print("prediction:",prediction)
	# prediction: ['9']
	return prediction

# 2)###########################################################################################
#hàm xử lí ảnh từ kí tự, đưa ra sâu kí tự từ chuỗi các ảnh vừa xử lí	
########################################################################################################
def string_LP(list_image, model, labels):
	final_string='' #tạo chuỗi trống
	for i in list_image:
		title = np.array2string(predict_from_model(i,model,labels))
		# prediction: ['9']
		final_string+=title.strip("'[]") #Trả lại bản sao của chuỗi đã xóa các ký tự '[]
	return final_string

#vẽ box
def draw_box(image_path, cor, thickness=9): 
    pts=[]  
    x_coordinates=cor[0][0] #mảng(mảng(mảng)) -> hàng chứa tọa độ X (4 tọa độ)
    y_coordinates=cor[0][1]
    # trên cùng bên trái, trên cùng bên phải, dưới cùng bên trái, dưới cùng bên phải
    for i in range(4):
        pts.append([int(x_coordinates[i]),int(y_coordinates[i])]) #thêm theo cụm (x,y) vào mảng
    
    pts = np.array(pts, np.int32) #làm tròn về int32 (vẫn đang dạng tọa độ bình thường)
    pts = pts.reshape((-1,1,2)) #chuyển về mảng các đường cong đa giác 
    # print("pts:",pts)
    cv2.polylines(image_path,[pts],True,(0,255,0),thickness)
    return image_path

if __name__ == "__main__":
	image = cv2.imread("./images/bs6.jpg")
	wpod_net_model = load_model("./model/wpod-net.json")
	plate_image,cor = plate_image(image, wpod_net_model)
	binary_plate_image = binary_image(plate_image)
	charater_top, charater_bot = get_characters(binary_plate_image) #charater_top

	json_file = open('./model/MobileNets_character_recognition.json', 'r')
	loaded_model_json = json_file.read()
	model = model_from_json(loaded_model_json)
	model.load_weights("./model/License_character_recognition_weight.h5")
	vehicle_image = draw_box(image,cor)
	labels = preprocessing.LabelEncoder()  #giải mã nhãn
	labels.classes_ = np.load('./model/license_character_classes.npy') #dòng33
	json_file.close()

	string_ki_tu_tren= string_LP(charater_top, model, labels)
	string_ki_tu_duoi= string_LP(charater_bot, model, labels)


	cv2.putText(vehicle_image, string_ki_tu_tren+" "+string_ki_tu_duoi, (int(cor[0][0][0])-50, int(cor[0][1][0])-300), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255),thickness=3)
	cv2.imshow("a",vehicle_image)
	cv2.imshow("AA",plate_image)

	cv2.waitKey()
	# print(string_LP(charater_top, model, labels))
	# string_ki_tu_tren= string_LP(charater_top, model, labels)
	# print("string_ki_tu_tren:",string_ki_tu_tren)
	# print("string_ki_tu_tren[-1]:",string_ki_tu_tren[-1])

	# print(string_LP(charater_bot, model, labels))