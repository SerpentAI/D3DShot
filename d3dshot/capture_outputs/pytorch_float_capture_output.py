import numpy as np

from PIL import Image

from d3dshot.capture_outputs.pytorch_capture_output import PytorchCaptureOutput


class PytorchFloatCaptureOutput(PytorchCaptureOutput):
    def process(self, pointer, pitch, size, width, height, region, rotation):
        image = super().process(pointer, pitch, size, width, height, region, rotation)
        return image / 255.0

    def to_pil(self, frame):
        return Image.fromarray(np.array(frame * 255.0, dtype=np.uint8))
