from part02_binary_image import *

# https://www.pyimagesearch.com/2015/04/20/sorting-contours-using-python-and-opencv/

#hàm sort_contours () để lấy đường viền của từng chữ số từ trái sang phải
# Do cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# trả ra các mảng có chứa cạnh tìm được , nhưng chúng được sắp xếp một cách lộn xộn, ko đúng thứ tự
# tạo boundingRect quanh các cạnh vừa tìm được
# nhờ tọa độ x của boundingRect ta sắp xếp được các mảng có chứa các cạnh này
def sort_contours(cnts,reverse = False): #reverse = False sắp xếp tăng dần trái sang phải
	i = 0		#sắp xếp theo tọa độ x của hộp giới hạn (boundingRect)
	#boundingRect trả ra #tọa độ góc trái trên cùng, chiều rộng, chiều cao đường bao 
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]  #tạo hộp giới hạn,(x, y, w, h) = cv2.boundingRect(
	#lambda b: b[1][i] trả ra (return) b[1][i] tọa độ x của hộp giới hạn (boundingRect) 
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),key=lambda b: b[1][i], reverse=reverse)) # sắp xếp
	#print("(cnts[1], boundingBoxes[1]):",(cnts[1], boundingBoxes[1]))
	#(cnts[1], boundingBoxes[1]): (array([[[ 31,   0]],
	#[[ 31,   1]],...[[164,   0]]], dtype=int32), (31, 0, 249, 22))
	#zip(cnts, boundingBoxes) -> cnts này ứng với boundingBoxes này
	return cnts

# cắt ảnh thành 2 phần
def cut_image_to_2_images(image):
	h, w = image.shape
	bot = int(h*0.55) #phần phía dưới
	top = int(h*0.45) #phần phía trên
	image_top = image[0:bot, 0:w]
	image_bottom = image[top:h, 0:w]
	return image_top, image_bottom

#lấy kí tự từ hình ảnh cắt
def get_characters_from_image(image):
	#get contour
	cont,_  = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# test_roi = image.copy()
	# Khởi tạo danh sách sẽ được sử dụng để nối các cụm kí tự(mảng)
	crop_characters = []
	# xác định chiều rộng và chiều cao tiêu chuẩn của ký tự
	digit_w, digit_h = 30, 60

	for c in sort_contours(cont):
			(x, y, w, h) = cv2.boundingRect(c) #tọa độ góc trái trên cùng, chiều rộng, chiều cao đường bao
			ratio = h/w
			if 1<=ratio<=5: # chọn những hình bao có tỉ lệ trong khoảng (hình chữ nhật)  					#quan trọng
				if h/image.shape[0]>=0.3: # chọn sao cho đường cao của hình bao lớn hơn 30% ảnh gốc cắt 	#quan trọng
					# cv2.rectangle(test_roi, (x, y), (x + w, y + h), (0, 255,0), 2)
					# Tách số và đưa ra dự đoán
					curr_num = image[y:y+h,x:x+w]
					curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h)) #đưa về kích thước tiêu chuẩn
					_, curr_num = cv2.threshold(curr_num, 220, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #ngưỡng nhị phân
					crop_characters.append(curr_num) # thêm vào mảng
	return crop_characters #đưa ra mảng

#cắt được từng kí tự trong cả 2 phần biển số
def get_characters(image):  											#cần xem lại chỗ này , do hàm cut_image_to_2_images để phát hiện xe máy (biển 2 tầng)
	image_top, image_bottom = cut_image_to_2_images(image)
	charater_top = get_characters_from_image(image_top)
	charater_bot = get_characters_from_image(image_bottom)
	return charater_top, charater_bot

if __name__ == "__main__":
	image = cv2.imread("./images/bs6.jpg")
	wpod_net_model = load_model("./model/wpod-net.json")
	plate_image,_ = plate_image(image, wpod_net_model)
	binary_plate_image = binary_image(plate_image)
	charater_top, charater_bot = get_characters(binary_plate_image)
	cv2.waitKey()
	for character in charater_top:
		cv2.destroyAllWindows()
		cv2.imshow('top', character)
		cv2.waitKey()

	for character in charater_bot:
		cv2.destroyAllWindows()
		cv2.imshow('bottom', character)
		cv2.waitKey()