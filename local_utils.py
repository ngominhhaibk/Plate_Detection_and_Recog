# pylint: disable=invalid-name, redefined-outer-name, missing-docstring, non-parent-init-called, trailing-whitespace, line-too-long
import cv2
import numpy as np

##########################################################################################################
class Label:   
    def __init__(self, cl=-1, tl=np.array([0., 0.]), br=np.array([0., 0.]), prob=None):
        self.__tl = tl
        self.__br = br
        self.__cl = cl
        self.__prob = prob

    def __str__(self):
        return 'Class: %d, top left(x: %f, y: %f), bottom right(x: %f, y: %f)' % (
        self.__cl, self.__tl[0], self.__tl[1], self.__br[0], self.__br[1])

    def copy(self):
        return Label(self.__cl, self.__tl, self.__br)

    def wh(self): return self.__br - self.__tl  #ra mảng gồm chiều rộng w, chiều cao h

    def cc(self): return self.__tl + self.wh() / 2

    def tl(self): return self.__tl

    def br(self): return self.__br

    def tr(self): return np.array([self.__br[0], self.__tl[1]])

    def bl(self): return np.array([self.__tl[0], self.__br[1]])

    def cl(self): return self.__cl

    def area(self): return np.prod(self.wh())

    def prob(self): return self.__prob           # x.prob() -line 185

    def set_class(self, cl):
        self.__cl = cl

    def set_tl(self, tl):
        self.__tl = tl

    def set_br(self, br):
        self.__br = br

    def set_wh(self, wh):
        cc = self.cc()
        self.__tl = cc - .5 * wh
        self.__br = cc + .5 * wh

    def set_prob(self, prob):
        self.__prob = prob
##########################################################################################################
class DLabel(Label): #cl: class, tl:top left , br:bottom right
    def __init__(self, cl, pts, prob):
        self.pts = pts
        tl = np.amin(pts, axis=1) #tìm nhỏ nhất trong tệp x,y
        br = np.amax(pts, axis=1) #tìm lớn nhất trong tệp x,y
        Label.__init__(self, cl, tl, br, prob)      
##########################################################################################################
def getWH(shape):
    return np.array(shape[1::-1]).astype(float)
##########################################################################################################
def find_T_matrix(pts, t_pts):
    A = np.zeros((8, 9))
    for i in range(0, 4):
        xi = pts[:, i]
        xil = t_pts[:, i]
        xi = xi.T
        
        A[i*2, 3:6] = -xil[2]*xi
        A[i*2, 6:] = xil[1]*xi
        A[i*2+1, :3] = xil[2]*xi
        A[i*2+1, 6:] = -xil[0]*xi

    [U, S, V] = np.linalg.svd(A)
    H = V[-1, :].reshape((3, 3))
    return H
##########################################################################################################
def getRectPts(tlx, tly, brx, bry):
    return np.matrix([[tlx, brx, brx, tlx], [tly, tly, bry, bry], [1, 1, 1, 1]], dtype=float)
##########################################################################################################
def normal(pts, anpha, mn, MN):
    pts_MN_center_mn = pts * anpha  # Tmn = Amn
    # print("mn:",mn) 
    pts_MN = pts_MN_center_mn + mn.reshape((2, 1))  #mn tọa độ điểm trung tâm (m,n) -> đảo ngược (mn)->
    # print("mn.reshape((2, 1):",mn.reshape((2, 1))) #->mn.reshape((2, 1): [[9.5] [8.5]]
    pts_prop = pts_MN / MN.reshape((2, 1))  #pts_MN nhân N_s/MH (WH) (kích thước ảnh đầu vào) (mảng 2D)
    # print("MN.reshape((2, 1):",MN.reshape((2, 1))) ->MN.reshape((2, 1): [[16.][16.]]
    return pts_prop
##########################################################################################################
# Chức năng tái cấu trúc từ giá trị dự đoán thành ảnh biển số cắt từ phương tiện
def reconstruct(phuong_tien, img_resize, Yr_model, lp_threshold):
    #Có 4 lớp max-pooling 2 × 2 và bước 2 làm giảm kích thước đầu vào đi một hệ số 16 (nên nhân bù 2^4)
    N_s = 2**4# (2^4) (do có 4 lần MAX_POOLING)
    anpha = ((208 + 40)/2)/N_s #hệ số anpha = 7,75

    # plate size
    one_line = (470, 110)  #1 dòng cho biển số rộng
    two_lines = (280, 200) #2 dòng cho biển số dài

    #bản đồ những chỗ có nguy cơ phát hiện vật(trên từng pixel ảnh)
    Probs = Yr_model[..., 0] #object probability-xác suất đối tượng???????????
    # print("Probs:",Probs)
    Affines = Yr_model[..., 2:]#????????????????????????????????????????????????????????????????????????????????????
    # print("Affines:",Affines)

    #cho biết nơi nào thỏa mãn điều kiện
    xx, yy = np.where(Probs > lp_threshold) # ngưỡng phát hiện ảnh có biển số , mảng 2D ->where ra 2 mảng con
    # print("np.where(Probs > lp_threshold):",np.where(Probs > lp_threshold))
    # Kích thước hình ảnh đầu vào mạng CNN (WPOD-NET)
    WH = getWH(img_resize.shape)
    #kích thước ảnh đầu ra
    MN = WH/N_s #thu nhỏ 16 lần do qua 4 lớp max-pooling

    #biểu thị các đỉnh tương ứng của một hình vuông đơn vị chính tắc có tâm tại điểm gốc.
    #q1= [−0.5,−0.5]T,q2= [0.5,−0.5]T,q3= [0.5,0.5]T,q4= [−0.5,0.5]T
    base = lambda vx, vy: np.matrix([[-vx, -vy, 1], [vx, -vy, 1], [vx, vy, 1], [-vx, vy, 1]]).T 
    labels = []
    labels_frontal = []

#bước tính toán Tmn, Amn để ra tọa độ 4 đỉnh
    for i in range(len(xx)): #i chạy từ 0 đến len(xx)
        x, y = xx[i], yy[i] #một mảng chứa xi,yi
        # print("i:",i)
        # print("x:",x) #là từng điểm
        # print("i:",i)
        # print("y:",y) #i=26 ?

        affine = Affines[x, y]
        # print("affine:",affine)
        prob = Probs[x, y]
        # print("prob:",prob)
        # affine: [ 0.77101415  0.33945787  0.20654605 -0.77006125  0.6651301   0.02998542] [v3 v4 v7 v5 v6 v8]
        # prob: 0.99806386
        #tọa độ điểm trung tâm (m,n)
        mn = np.array([float(y) + 0.5, float(x) + 0.5]) #???????? sao lại cộng thêm 0,5 
        # mn = np.array([float(y) , float(x) ]) #???????? sao lại cộng thêm 0,5 

        # print("mn:",mn) ->mn: [ 9.5 11.5]
        # ma trận chuyển đổi affine
        A = np.reshape(affine, (2, 3))
        A[0, 0] = max(A[0, 0], 0)
        A[1, 1] = max(A[1, 1], 0)
        # identity transformation
        B = np.zeros((2, 3))
        B[0, 0] = max(A[0, 0], 0)
        B[1, 1] = max(A[1, 1], 0)
        # print("B:",B)
        # A: [[ 0.77771455  0.35008743  0.0858364 ]  [v3 v4 v7]
        # [-0.8923675   0.6371357  -0.34070557]]    [v5 v6 v8]
        # B: [[0.77771455 0.         0.        ]
        # [0.         0.63713568 0.        ]]
        #tính Tmn
        pts = np.array(A*base(0.5, 0.5)) #ma trận Tmn = Amn
        pts_frontal = np.array(B*base(0.5, 0.5)) #không có v7, v8
        ################################
        #tính các điểm p (do Amn = Tmn)
        # print("MNpts_prop:",MN)
        pts_prop = normal(pts, anpha, mn, MN) #tìm ra tọa độ 4 đỉnh 
        frontal = normal(pts_frontal, anpha, mn, MN)#tìm ra tọa độ 4 đỉnh 
        # pts: [[-0.60913413  0.15289999  0.49929855 -0.26273557]
        #     [-0.20034513 -1.1229026  -0.47835472  0.44420275]]
        # pts_frontal: [[-0.38101706  0.38101706  0.38101706 -0.38101706]
        #               [-0.32227394 -0.32227394  0.32227394  0.32227394]]
        ################################
        # pts_prop: [[0.29870066 0.66781093 0.83559774 0.46648746]       [x1 x2 x3 x4]
        #           [0.55920783 0.11234405 0.42454693 0.87141071]]         [y1 y2 y3 y4]
        # frontal: [[0.40919486 0.77830514 0.77830514 0.40919486]
        #           [0.50014856 0.50014856 0.81235144 0.81235144]]

        labels.append(DLabel(0, pts_prop, prob)) #thêm vào seft, sắp xếp từ lớn đến bé
        labels_frontal.append(DLabel(0, frontal, prob))
################################       
    # final_labels = nms(labels, 0.5)  #trong mỗi nhãn chứa tọa độ 4 điểm và tỉ lệ là biển số
    # final_labels_frontal = nms(labels_frontal, 0.5)
    final_labels = labels
    final_labels_frontal = labels_frontal #sắp xếp ở phần labels trên rồi
    #print(final_labels_frontal) 
    assert final_labels_frontal, "không tìm thấy biển số!" #Nếu final_labels_frontal là NULL thì chạy (nếu sai thì chạy) 
    #-> sẽ bị ảnh hưởng ngay từ bước lập ngưỡng -> xx, yy = np.where(Probs > lp_threshold)
    #tìm thấy biển số
    # LP size and type
    # W/ H <1,7 -> 2 line
    out_size, lp_type = (two_lines, 2) if ((final_labels_frontal[0].wh()[0] / final_labels_frontal[0].wh()[1]) < 1.7) else (one_line, 1)
    #lấy theo điểm mà có prob cao nhất đã phát hiện ở hàm DLabel(0, pts_prop, prob) -> final_labels_frontal[0] (do sắp xếp ngược)
    #out_size = two_lines = (280, 200) hoặc one_line = (470, 110)
    TLp = []
    Cor = []
    #chuyển từ cong sang thẳng
    if len(final_labels):
        final_labels.sort(key=lambda x: x.prob(), reverse=True)  #sắp xếp ngược lại từ lớn đến bé (sắp xếp theo prob)
        for _, label in enumerate(final_labels):
            t_ptsh = getRectPts(0, 0, out_size[0], out_size[1])
            #lấy tọa độ 4 đỉnh nhân các chiều của ảnh phương tiện gốc
            ptsh = np.concatenate((label.pts * getWH(phuong_tien.shape).reshape((2, 1)), np.ones((1, 4))))
            H = find_T_matrix(ptsh, t_ptsh)
            #chuyển từ cong sang thẳng
            Ilp = cv2.warpPerspective(phuong_tien, H, out_size, borderValue=0)
            # phuong_tien: input image
            # H: Transformation matrix
            # out_size: size of the output image
            # flags: interpolation method to be used
            TLp.append(Ilp)
            Cor.append(ptsh) 
#tọa độ 4 đỉnh (chuẩn theo ảnh gốc) #nhưng (chứa cả những điểm lân cận (m,n) prob bên cạnh) tập hợp các đỉnh của nhiều nhãn

    return final_labels, TLp, lp_type, Cor
##########################################################################################################
def detect_lp(model, phuong_tien, max_dim, lp_threshold):
    #tính hệ số resize ảnh 
    min_dim_img = min(phuong_tien.shape[:2]) # lấy chiều ngắn nhất 
    factor = float(max_dim) / min_dim_img
    # Tính W và H mới sau khi resize
    w, h = (np.array(phuong_tien.shape[1::-1], dtype=float) * factor).astype(int).tolist()
    # Tiến hành resize ảnh
    Iresized = cv2.resize(phuong_tien, (w, h))
    T = Iresized.copy()
    # Chuyển thành Tensor (#xếp 3 ảnh màu lên nhau)
    T = T.reshape((1, T.shape[0], T.shape[1], T.shape[2]))
    # Tiến hành detect biển số bằng Wpod-net pretrain
    Yr_model = model.predict(T)######################################################### duy nhất dùng model
    # 1/1 [==============================] - 1s 550ms/step
    # Loại bỏ các chiều =1 của Yr
    Yr_model = np.squeeze(Yr_model) #vd [[[0], [1], [2]]] ->[0], [1], [2]
    # print("Yr.shape:",Yr.shape) ->(Yr.shape: (16, 16, 8))
    # Tái tạo và trả về các biến gồm: 1_Nhãn, 2_Ảnh biến số, 3_Loại biển số (1: dài: 2 vuông), 04_tọa độ 4 điểm góc
    L, TLp, lp_type, Cor = reconstruct(phuong_tien, Iresized, Yr_model, lp_threshold)
    return L, TLp, lp_type, Cor
