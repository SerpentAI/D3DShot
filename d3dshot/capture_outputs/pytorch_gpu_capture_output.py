import numpy as np
import torch

from PIL import Image

from d3dshot.capture_outputs.pytorch_capture_output import PytorchCaptureOutput


class PytorchGPUCaptureOutput(PytorchCaptureOutput):
    def __init__(self):
        self.device = torch.device("cuda")
        torch.tensor([0], device=self.device)  # Warm up CUDA

    def process(self, pointer, pitch, size, width, height, region, rotation):
        image = super().process(pointer, pitch, size, width, height, region, rotation)
        return image.to(self.device)

    def to_pil(self, frame):
        return Image.fromarray(np.array(frame.cpu()))
