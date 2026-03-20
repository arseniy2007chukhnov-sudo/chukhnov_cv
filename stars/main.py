import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import erosion

image = np.load(f"stars.npy")
labeled_origin_image = label(image)
max_origin = np.max(labeled_origin_image)
struct = np.ones((3, 3))
processed_image = erosion(image, struct)
labeled_image = label(processed_image)
max_processed = np.max(labeled_image)

print(f"{max_origin - max_processed} stars on the image")
plt.imshow(image)
plt.show()