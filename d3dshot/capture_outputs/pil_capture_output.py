import ctypes

from PIL import Image

from d3dshot.capture_output import CaptureOutput


class PILCaptureOutput(CaptureOutput):
    def __init__(self):
        pass

    def process(self, pointer, size, width, height, region, rotation):
        raw_bytes = ctypes.string_at(pointer, size=size)

        if rotation == 0:
            image = Image.frombytes("RGBA", (width, height), raw_bytes)
        elif rotation == 90:
            image = Image.frombytes("RGBA", (height, width), raw_bytes)
            image = image.transpose(Image.ROTATE_270)
        elif rotation == 180:
            image = Image.frombytes("RGBA", (width, height), raw_bytes)
            image = image.transpose(Image.ROTATE_180)
        elif rotation == 270:
            image = Image.frombytes("RGBA", (height, width), raw_bytes)
            image = image.transpose(Image.ROTATE_90)

        b, g, r, _ = image.split()
        image = Image.merge("RGB", (r, g, b))

        if region[2] - region[0] != width or region[3] - region[1] != height:
            image = image.crop(region)

        return image

    def to_pil(self, frame):
        return frame

    def stack(self, frames, stack_dimension):
        return frames
