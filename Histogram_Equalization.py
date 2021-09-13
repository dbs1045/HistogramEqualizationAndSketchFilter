import numpy as np
import tkinter
from tkinter.filedialog import askopenfilename
import cv2

MIN_THRESHOLD = 0
MAX_THRESHOLD = 255  # 0부터 255 사이의 임계값 설정

tkinter.Tk().withdraw()
filename = askopenfilename(title='Select input Sample Image')
im = cv2.imread(filename)
width = im.shape[1]
height = im.shape[0]


hueIm = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
h1, s1, v = cv2.split(hueIm)

b, g, r = cv2.split(im)
# r = im[:, :, 2].copy()
# g = im[:, :, 1].copy()
# b = im[:, :, 0].copy()



def hist(img):
    His = dict()

    for i in range(256):
        His[i] = 0

    for x in range(height):
        for y in range(width):
            val = img[x, y]
            His[val] = His[val] + 1

    return His


hueH = hist(v)

rH = hist(r)
gH = hist(g)
bH = hist(b)

def Equalization(H, vi):
    sum = 0
    nom = 0

    for a in range(256):
        sum += H[a]
        nom = round(sum / (height * width) * 255)
        H[a] = nom

    for x in range(height):
        for y in range(width):
            if MIN_THRESHOLD <= vi[x, y] <= MAX_THRESHOLD:
                val = vi[x, y]
                vi[x, y] = H[val]

    return vi


v1 = np.clip(Equalization(hueH, v), 0, 255)

print("그림을 준비중입니다")

result1 = cv2.merge([h1, s1, v1])
result2 = cv2.merge([Equalization(bH, b.copy()), Equalization(gH, g.copy()), Equalization(rH, r.copy())])
result1 = cv2.cvtColor(result1, cv2.COLOR_HSV2BGR)

(h, w) = result1.shape[:2]
max_size = 600
if h >= w:
    if h > max_size:
        ns = h / max_size
        nh = int(h / ns)
        nw = int(w / ns)
    else:
        nh = h
        nw = w

else:
    if w > max_size:
        ns = w / max_size
        nh = int(h / ns)
        nw = int(w / ns)
    else:
        nh = h
        nw = w

im = cv2.resize(im, (nw, nh))

result1 = cv2.resize(result1, (nw, nh))

result2 = cv2.resize(result2, (nw, nh))

cv2.imshow("Original", im)
cv2.imshow("HSV My Hist", result1)
cv2.imwrite('result1.png', result1)
cv2.imshow("RGB My Hist", result2)
cv2.imwrite('result2.png', result2)
cv2.waitKey()
cv2.destroyAllWindows()