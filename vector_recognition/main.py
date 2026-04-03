import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.io import imread
from pathlib import Path

save_path = Path(__file__).parent



def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] + 2, shape[1] + 2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return max(0, np.max(labeled) - 1)


def extractor(region):
    cy, cx = region.centroid_local
    cy/= region.image.shape[0]
    cx/= region.image.shape[1]
    holes = count_holes(region)
    vlines = (np.sum(region.image, 0) == region.image.shape[0]).sum()
    hlines = (np.sum(region.image, 1) == region.image.shape[1]).sum()
    eccentricity = region.eccentricity
    aspect = region.image.shape[0] / region.image.shape[1]
    bays = 0
    for r in regionprops(labeled):
        if r.area > 3:
            bays += 1
    angle_rad = region.orientation
    angle_deg = np.degrees(angle_rad) % 180
    compactness = (4 * np.pi * region.area) / (region.perimeter ** 2)
    return np.array([cy, cx, holes,
                    vlines / max(1, region.image.shape[1]),
                    hlines / max(1, region.image.shape[0]),
                    eccentricity, aspect, bays, angle_deg/180, compactness])

def classificator(region,templates):
    features = extractor(region)
    result = ""
    min_d = 10**16
    for symbol, t in templates.items():
        d = ((t - features)** 2).sum() ** 0.5
        if d < min_d:
            result = symbol
            min_d = d
    return result


template = imread("alphabet-small.png")[:,:, :-1]
print(template.shape)
template = template.sum(2)
binary = template != 765.

labeled = label(binary)
props = regionprops(labeled)

templates = {}

for region, symbol in zip(props, ["8", "O",
                                   "A", "B", "1", "W",
                                     "X", "*", "/", "-"]):
    templates[symbol] = extractor(region)

print(templates)

print(classificator(props[0], templates))

image = imread("alphabet.png")[:, :, :-1]
abinary = image.mean(2) > 0

alabeled = label(abinary)
print(np.max(alabeled))
aprops = regionprops(alabeled)
result = {}

image_path = save_path / "out"
image_path.mkdir(exist_ok = True)

# plt.ion()
plt.figure(figsize = (5,7))
for region in aprops:
    symbol = classificator(region, templates)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
    plt.cla()
    plt.title(f"Class - '{symbol}'")
    plt.imshow(region.image)
    plt.savefig(image_path/ f"image_{region.label}.png")
print(result)

plt.imshow(abinary)
plt.show()
