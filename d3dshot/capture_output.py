import enum


class CaptureOutputs(enum.Enum):
    PIL = 0
    NUMPY = 1
    NUMPY_FLOAT = 2
    PYTORCH = 3
    PYTORCH_FLOAT = 4
    PYTORCH_GPU = 5
    PYTORCH_FLOAT_GPU = 6


class CaptureOutputError(BaseException):
    pass


class CaptureOutput:
    def __init__(self, backend=CaptureOutputs.PIL):
        self.backend = self._initialize_backend(backend)

    def process(self, pointer, pitch, size, width, height, region, rotation):
        return self.backend.process(pointer, pitch, size, width, height, region, rotation)

    def to_pil(self, frame):
        return self.backend.to_pil(frame)

    def stack(self, frames, stack_dimension):
        return self.backend.stack(frames, stack_dimension)

    def _initialize_backend(self, backend):
        if backend == CaptureOutputs.PIL:
            from d3dshot.capture_outputs.pil_capture_output import PILCaptureOutput

            return PILCaptureOutput()
        elif backend == CaptureOutputs.NUMPY:
            from d3dshot.capture_outputs.numpy_capture_output import NumpyCaptureOutput

            return NumpyCaptureOutput()
        elif backend == CaptureOutputs.NUMPY_FLOAT:
            from d3dshot.capture_outputs.numpy_float_capture_output import NumpyFloatCaptureOutput

            return NumpyFloatCaptureOutput()
        elif backend == CaptureOutputs.PYTORCH:
            from d3dshot.capture_outputs.pytorch_capture_output import PytorchCaptureOutput

            return PytorchCaptureOutput()
        elif backend == CaptureOutputs.PYTORCH_FLOAT:
            from d3dshot.capture_outputs.pytorch_float_capture_output import (
                PytorchFloatCaptureOutput,
            )

            return PytorchFloatCaptureOutput()
        elif backend == CaptureOutputs.PYTORCH_GPU:
            from d3dshot.capture_outputs.pytorch_gpu_capture_output import PytorchGPUCaptureOutput

            return PytorchGPUCaptureOutput()
        elif backend == CaptureOutputs.PYTORCH_FLOAT_GPU:
            from d3dshot.capture_outputs.pytorch_float_gpu_capture_output import (
                PytorchFloatGPUCaptureOutput,
            )

            return PytorchFloatGPUCaptureOutput()
        else:
            raise CaptureOutputError("The specified backend is invalid!")
