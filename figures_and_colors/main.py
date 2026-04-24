import numpy as np
from skimage.io import imread
from skimage.color import rgb2hsv
from skimage.measure import label, regionprops

image = imread("balls_and_rects.png")
hsv = rgb2hsv(image)
hue = hsv[:,:, 0]

unique_colors = sorted(np.unique(hue))

groups = []
while unique_colors:
    base = unique_colors.pop(0)
    if base == 0:
        continue
    group = [base]
    to_remove = []
    for c in unique_colors:
        if abs(c - base) <= 0.01:
            group.append(c)
            to_remove.append(c)

    for c in to_remove:
        unique_colors.remove(c)

    groups.append(group)


total_all = 0
total_circles = 0
total_rects = 0

for group in groups:
    mask = np.isin(hue, group)
    labeled = label(mask)

    circles = 0
    rects = 0

    for region in regionprops(labeled):

        minr, minc, maxr, maxc = region.bbox
        height = maxr - minr
        width = maxc - minc

        if height != 0:
            aspect_ratio = width / height
        else:
            aspect_ratio = 0

        if 0.8 < aspect_ratio < 1.2:
            circles += 1
        else:
            rects += 1

    total = circles + rects
    total_all += total
    total_circles += circles
    total_rects += rects

    print(f"Группа {group[0]:.5f}: Всего={total}, Круги={circles}, Прямоугольники={rects}")
print(f"Всего фигур: {total_all}")
print(f"Кругов: {total_circles}")
print(f"Прямоугольников: {total_rects}")