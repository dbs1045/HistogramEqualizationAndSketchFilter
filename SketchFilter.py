import numpy as np
import tkinter
from tkinter.filedialog import askopenfilename
import cv2

DELTA = 0
KSIZE = 5

tkinter.Tk().withdraw()
filename = askopenfilename(title = 'Select input a Image')
im = cv2.imread(filename)
width = im.shape[1]
height = im.shape[0]

hueIm = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
h1, s1, v = cv2.split(hueIm)

r = im[:, :, 2].copy()
g = im[:, :, 1].copy()
b = im[:, :, 0].copy()

me = np.finfo(float).eps

v1 = v.copy()

def sketchFilter(value):
    for a in range(KSIZE // 2, height - KSIZE // 2):
        for b in range(KSIZE // 2, width - KSIZE // 2):
            d = []
            for c in range(-KSIZE // 2 + 1, KSIZE // 2 + 1):
                for f in range(-KSIZE // 2 + 1, KSIZE // 2 + 1):
                    d.append(v[a + c, b + f])
            value[a, b] = value[a, b] / (max(d) + me + DELTA)*255


sketchFilter(v1)
sketchFilter(r)
sketchFilter(g)
sketchFilter(b)

v1 = np.clip(v1, 0, 255)
r = np.clip(r, 0, 255)
g = np.clip(g, 0, 255)
b = np.clip(b, 0, 255)
print("그림을 준비 중입니다")

result1 = cv2.merge([h1, s1, v1])
result2 = cv2.merge([b, g, r])
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

result2 = cv2. resize(result2, (nw, nh))

cv2.imshow("Original", im)
cv2.imshow("HSV My Hist", result1)
cv2.imwrite('result1.png', result1)
cv2.imshow("RGB My Hist", result2)
cv2.imwrite('result2.png', result2)
cv2.waitKey()
cv2.destroyAllWindows()