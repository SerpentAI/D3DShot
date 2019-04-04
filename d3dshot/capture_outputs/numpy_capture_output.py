import ctypes

import numpy as np

from PIL import Image

from d3dshot.capture_output import CaptureOutput


class NumpyCaptureOutput(CaptureOutput):

    def __init__(self):
        pass

    def process(self, pointer, size, width, height, region, rotation):
        image = np.empty((size,), dtype=np.uint8)
        ctypes.memmove(image.ctypes.data, pointer, size)

        if rotation == 0:
            image = np.reshape(image, (height, width, 4))[..., [2, 1, 0]]
        elif rotation == 90:
            image = np.reshape(image, (width, height, 4))[..., [2, 1, 0]]
            image = np.rot90(image, axes=(1, 0))
        elif rotation == 180:
            image = np.reshape(image, (height, width, 4))[..., [2, 1, 0]]
            image = np.rot90(image, k=2, axes=(0, 1))
        elif rotation == 270:
            image = np.reshape(image, (width, height, 4))[..., [2, 1, 0]]
            image = np.rot90(image, axes=(0, 1))

        if region[2] - region[0] != width or region[3] - region[1] != height:
            image = image[region[1]:region[3], region[0]:region[2], :]

        return image

    def to_pil(self, frame):
        return Image.fromarray(frame)

    def stack(self, frames, stack_dimension):
        if stack_dimension == "first":
            dimension = 0
        elif stack_dimension == "last":
            dimension = -1

        return np.stack(frames, axis=dimension)
