import ctypes

import numpy as np
import torch

from PIL import Image

from d3dshot.capture_output import CaptureOutput


class PytorchCaptureOutput(CaptureOutput):
    def __init__(self):
        pass

    def process(self, pointer, pitch, size, width, height, region, rotation):
        # We proxy through numpy's ctypes interface because making
        # a PyTorch tensor from a bytearray is HORRIBLY slow...
        image = np.empty((size,), dtype=np.uint8)
        ctypes.memmove(image.ctypes.data, pointer, size)

        pitch_per_channel = pitch // 4

        if rotation == 0:
            image = np.reshape(image, (height, pitch_per_channel, 4))[..., [2, 1, 0]]
        elif rotation == 90:
            image = np.reshape(image, (width, pitch_per_channel, 4))[..., [2, 1, 0]]
            image = np.rot90(image, axes=(1, 0)).copy()
        elif rotation == 180:
            image = np.reshape(image, (height, pitch_per_channel, 4))[..., [2, 1, 0]]
            image = np.rot90(image, k=2, axes=(0, 1)).copy()
        elif rotation == 270:
            image = np.reshape(image, (width, pitch_per_channel, 4))[..., [2, 1, 0]]
            image = np.rot90(image, axes=(0, 1)).copy()

        # Trim pitch padding
        if rotation in (0, 180) and pitch_per_channel != width:
            image = image[:, :width, :]
        elif rotation in (90, 270) and pitch_per_channel != height:
            image = image[:height, :, :]

        # Region slicing
        if region[2] - region[0] != width or region[3] - region[1] != height:
            image = image[region[1] : region[3], region[0] : region[2], :]

        return torch.from_numpy(image)

    def to_pil(self, frame):
        return Image.fromarray(np.array(frame))

    def stack(self, frames, stack_dimension):
        if stack_dimension == "first":
            dimension = 0
        elif stack_dimension == "last":
            dimension = -1

        return torch.stack(frames, dim=dimension)
