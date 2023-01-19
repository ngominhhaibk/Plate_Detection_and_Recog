import cv2
from local_utils import detect_lp
from keras.models import model_from_json
from os.path import splitext
import numpy as np

def load_model(path):
    try:
        path = splitext(path)[0]
        with open('%s.json' % path, 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('%s.h5' % path)          #load weights
        return model
    except Exception as e:
        print(e)

# Hàm normalize ảnh
def preprocess_image(image): # chuyển ảnh về đoạn 0-1 để đưa vào model
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = img / 255
    return img

# Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh Dmax = 608 Dmin = 288
def get_plate(image, wpod_net, Dmax=608, Dmin=256): #quan trọng
    phuong_tien = preprocess_image(image)  #chuyển dải màu từ (0,255) sang (0,1)
    ratio = float(max(phuong_tien.shape[:2])) / min(phuong_tien.shape[:2]) #tỉ lệ chiều dài nhất / chiều ngắn nhất
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    # xác định được chiều dài , rộng hợp lý cho ảnh biển số
    _ , LpImg, _, cor = detect_lp(wpod_net, phuong_tien, bound_dim, lp_threshold=0.5)
    return LpImg, cor

# chuyển về ảnh thực (chuyển thành ảnh 8bit (đang ở (0,1)))
def plate_image(image, wpod_net):
    LpImg,cor = get_plate(image, wpod_net)
    plate_img = cv2.convertScaleAbs(LpImg[0], alpha=(255.0)) # chuyển thành ảnh 8bit (đang ở (0,1))
    return plate_img,cor    

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

if __name__ =="__main__":
    image = cv2.imread("./images/car.jpg")
    print("kích thước ảnh:",image.shape)
    wpod_net_model = load_model("./model/wpod-net.json")
    plate_image,cor = plate_image(image, wpod_net_model)
    cv2.imshow('plate_image', draw_box(image,cor))
    cv2.waitKey()