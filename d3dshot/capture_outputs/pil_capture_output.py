import ctypes

from PIL import Image

from d3dshot.capture_output import CaptureOutput


class PILCaptureOutput(CaptureOutput):
    def __init__(self):
        pass

    def process(self, pointer, pitch, size, width, height, region, rotation):
        raw_bytes = ctypes.string_at(pointer, size=size)

        pitch_per_channel = pitch // 4

        if rotation == 0:
            image = Image.frombytes("RGBA", (pitch_per_channel, height), raw_bytes)
        elif rotation == 90:
            image = Image.frombytes("RGBA", (pitch_per_channel, width), raw_bytes)
            image = image.transpose(Image.ROTATE_270)
        elif rotation == 180:
            image = Image.frombytes("RGBA", (pitch_per_channel, height), raw_bytes)
            image = image.transpose(Image.ROTATE_180)
        elif rotation == 270:
            image = Image.frombytes("RGBA", (pitch_per_channel, width), raw_bytes)
            image = image.transpose(Image.ROTATE_90)

        b, g, r, _ = image.split()
        image = Image.merge("RGB", (r, g, b))

        # Trim pitch padding
        if rotation in (0, 180) and pitch_per_channel != width:
            image = image.crop((0, 0, width, height))
        elif rotation in (90, 270) and pitch_per_channel != height:
            image = image.crop((0, 0, width, height))

        # Region slicing
        if region[2] - region[0] != width or region[3] - region[1] != height:
            image = image.crop(region)

        return image

    def to_pil(self, frame):
        return frame

    def stack(self, frames, stack_dimension):
        return frames
