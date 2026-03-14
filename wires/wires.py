import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import opening

for j in range(1, 7):
    image = np.load(f"images/wires{j}.npy")


    struct = np.ones((3, 1))

    process = opening(image, struct)

    labeled_image = label(image)
    print(f"Original {np.max(labeled_image)} wires")

    for i in range(1, np.max(labeled_image) +1):
        labeled_wire = (labeled_image == i)
        processed_wire = opening(labeled_wire, struct)
        lab_proc_wire = label(processed_wire)
        if np.max(lab_proc_wire) == 1:
            print(f"Wire{i} is not processed")
        elif np.max(lab_proc_wire) == 0:
            print(f"Wire{i} is fully cut down")
        else:
            print(f"Wire{i} processed on {np.max(lab_proc_wire)} parts")
        


    plt.subplot(121+j*10)
    plt.imshow(labeled_image)
    plt.subplot(122+j*10)
    plt.imshow(label(process))
    plt.show()