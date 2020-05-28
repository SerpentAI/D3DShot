import importlib.util

from d3dshot.d3dshot import D3DShot
from d3dshot.capture_output import CaptureOutputs


pil_is_available = importlib.util.find_spec("PIL") is not None
numpy_is_available = importlib.util.find_spec("numpy") is not None

pytorch_is_available = (
    importlib.util.find_spec("torch") is not None and numpy_is_available
)

pytorch_gpu_is_available = False

if pytorch_is_available:
    import torch

    pytorch_gpu_is_available = torch.cuda.is_available()


capture_output_mapping = {
    "pil": CaptureOutputs.PIL,
    "numpy": CaptureOutputs.NUMPY,
    "numpy_float": CaptureOutputs.NUMPY_FLOAT,
    "pytorch": CaptureOutputs.PYTORCH,
    "pytorch_float": CaptureOutputs.PYTORCH_FLOAT,
    "pytorch_gpu": CaptureOutputs.PYTORCH_GPU,
    "pytorch_float_gpu": CaptureOutputs.PYTORCH_FLOAT_GPU,
}

capture_outputs = [
    "pil",
    "numpy",
    "numpy_float",
    "pytorch",
    "pytorch_float",
    "pytorch_gpu",
    "pytorch_float_gpu",
]


def determine_available_capture_outputs():
    available_capture_outputs = list()

    if pil_is_available:
        available_capture_outputs.append(CaptureOutputs.PIL)

    if numpy_is_available:
        available_capture_outputs.append(CaptureOutputs.NUMPY)
        available_capture_outputs.append(CaptureOutputs.NUMPY_FLOAT)

    if pytorch_is_available:
        available_capture_outputs.append(CaptureOutputs.PYTORCH)
        available_capture_outputs.append(CaptureOutputs.PYTORCH_FLOAT)

    if pytorch_gpu_is_available:
        available_capture_outputs.append(CaptureOutputs.PYTORCH_GPU)
        available_capture_outputs.append(CaptureOutputs.PYTORCH_FLOAT_GPU)

    return available_capture_outputs


def create(capture_output="pil", frame_buffer_size=60):
    capture_output = _validate_capture_output(capture_output)
    frame_buffer_size = _validate_frame_buffer_size(frame_buffer_size)

    d3dshot = D3DShot(
        capture_output=capture_output,
        frame_buffer_size=frame_buffer_size,
        pil_is_available=pil_is_available,
        numpy_is_available=numpy_is_available,
        pytorch_is_available=pytorch_is_available,
        pytorch_gpu_is_available=pytorch_gpu_is_available,
    )

    return d3dshot


def _validate_capture_output(capture_output):
    available_capture_outputs = determine_available_capture_outputs()

    capture_output_name = capture_output
    capture_output = capture_output_mapping.get(capture_output)

    if capture_output not in available_capture_outputs:
        available_capture_outputs = [
            capture_outputs[co.value] for co in available_capture_outputs
        ]
        raise AttributeError(
            f"Invalid Capture Output '{capture_output_name}'. Available Options: {', '.join(available_capture_outputs)}"
        )

    return capture_output


def _validate_frame_buffer_size(frame_buffer_size):
    if not isinstance(frame_buffer_size, int) or frame_buffer_size < 1:
        raise AttributeError(f"'frame_buffer_size' should be an int greater than 0")

    return frame_buffer_size
