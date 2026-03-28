import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label

def centroid(labeled, label =1):
    y, x = np.where(labeled == label)
    return np.mean(y), np.mean(x)

def distance(px1, px2):
    return (((px1[0] - px2[0]) ** 2 +
             (px1[1] - px2[1]) ** 2)**0.5)

image = np.load("images/h_0.npy")
labeled = label(image)

x1, y1 = [], []
x2, y2 = [], []
x3, y3 = [], []

for i in np.arange(1, 4):
    cy, cx = centroid(labeled, i)

    if i == 1:
        x1.append(cx)
        y1.append(cy)
    elif i == 2:
        x2.append(cx)
        y2.append(cy)
    elif i == 3:
        x3.append(cx)
        y3.append(cy)

for i in np.arange(1, 100):
    image = np.load(f"images/h_{i}.npy")
    labeled = label(image)
    for j in np.arange(1, 4):
        cy, cx = centroid(labeled, j)

        dist = float('inf')
        dist1 = distance((cx, cy), (x1[-1], y1[-1]))
        if dist1 < dist and dist1 <= 20:
            dist = dist1
            index = 1
        
        dist2 = distance((cx, cy), (x2[-1], y2[-1]))
        if dist2 < dist and dist2 <= 20:
            dist = dist2
            index = 2

        dist3 = distance((cx, cy), (x3[-1], y3[-1]))
        if dist3 < dist and dist3 <= 20:
            dist = dist3
            index = 3

        if index == 1:
            x1.append(cx)
            y1.append(cy)
        elif index == 2:
            x2.append(cx)
            y2.append(cy)
        elif index == 3:
            x3.append(cx)
            y3.append(cy)



plt.figure(figsize=(10, 5))
plt.plot(x1, y1, 'pink')
plt.plot(x2, y2, 'green')
plt.plot(x3, y3, 'blue')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid()
plt.show()
