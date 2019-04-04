# D3DShot


_D3DShot_ is a pure Python implementation of the [Windows Desktop Duplication API](https://docs.microsoft.com/en-us/windows/desktop/direct3ddxgi/desktop-dup-api). It leverages DXGI and Direct3D system libraries to enable extremely fast and robust screen capture functionality for your Python scripts and applications on Windows. 

**D3DShot:**

* Is by far the fastest way to capture the screen with Python on Windows 8.1+
* Is very easy to use. If you can remember 10-ish methods, you know the entire thing.
* Covers all common scenarios and use cases:
	* Screenshot to memory
	* Screenshot to disk
	* Screenshot to memory buffer every X seconds (threaded; non-blocking)
	* Screenshot to disk every X seconds (threaded; non-blocking)
	* High-speed capture to memory buffer (threaded; non-blocking)
* Captures to PIL Images out of the box. Gracefully adds output options if NumPy or PyTorch can be found.
* Detects displays in just about any configuration: Single monitor, multiple monitors on one adapter, multiple monitors on multiple adapters.
* Handles display rotation and scaling for you
* Supports capturing specific regions of the screen
* Is robust and very stable. You can run it for hours / days without performance degradation
* Is even able to capture DirectX 11 / 12 exclusive fullscreen applications and games!


### TL;DR Quick Code Samples

**Screenshot to Memory**

```python
import d3dshot

d = d3dshot.create()
d.screenshot()
```
```
Out[1]: <PIL.Image.Image image mode=RGB size=2560x1440 at 0x1AA7ECB5C88>
```

**Screenshot to Disk**
```python
import d3dshot

d = d3dshot.create()
d.screenshot_to_disk()
```
```
Out[1]: './1554298682.5632973.png'
```

**Screen Capture for 5 Seconds and Grab the Latest Frame**
```python
import d3dshot
import time

d = d3dshot.create()

d.capture()
time.sleep(5)  # Capture is non-blocking so we wait explicitely
d.stop()

d.get_latest_frame()
```
```
Out[1]: <PIL.Image.Image image mode=RGB size=2560x1440 at 0x1AA044BCF60>
```

**Screen Capture the Second Monitor as NumPy Arrays for 3 Seconds and Grab the 4 Latest Frames as a Stack**
```python
import d3dshot
import time

d = d3dshot.create(capture_output="numpy")

d.display = d.displays[1]

d.capture()
time.sleep(3)  # Capture is non-blocking so we wait explicitely
d.stop()

frame_stack = d.get_frame_stack((0, 1, 2, 3), stack_dimension="last")
frame_stack.shape
```
```
Out[1]: (1080, 1920, 3, 4)
```

This is barely scratching the surface... Keep reading!


## Requirements

* Windows 8.1+
* Python 3.6+

## Installation

```
pip install d3dshot
```

_D3DShot_ leverages DLLs that are already available on your system so the dependencies are very light. Namely:

* [_comtypes_](https://github.com/enthought/comtypes): Internal use. To preserve developer sanity while working with COM interfaces.
* [_Pillow_](https://github.com/python-pillow/Pillow): Default Capture Output. Also used to save to disk as PNG and JPG.

These dependencies will automatically be installed alongside _D3DShot_; No need to worry about them!

## Concepts

### Capture Outputs

The desired _Capture Output_ is defined when creating a _D3DShot_ instance. It defines the type of all captured images. By default, all captures will return PIL.Image objects. This is a good option if you mostly intend to take screenshots.

```python
# Captures will be PIL.Image in RGB mode
d = d3dshot.create()
d = d3dshot.create(capture_output="pil")
```

_D3DShot_ is however quite flexible! As your environment meets certain optional sets of requirements, more options become available.


**If _NumPy_ is available**

```python
# Captures will be np.ndarray of dtype uint8 with values in range (0, 255)
d = d3dshot.create(capture_output="numpy")

# Captures will be np.ndarray of dtype float64 with normalized values in range (0.0, 1.0)
d = d3dshot.create(capture_output="numpy_float")  
```

**If _NumPy_ and _PyTorch_ are available**

```python
# Captures will be torch.Tensor of dtype uint8 with values in range (0, 255)
d = d3dshot.create(capture_output="pytorch")

# Captures will be torch.Tensor of dtype float64 with normalized values in range (0.0, 1.0)
d = d3dshot.create(capture_output="pytorch_float")
```

**If _NumPy_ and _PyTorch_ are available + _CUDA_ is installed and _torch.cuda.is_available()_**

```python
# Captures will be torch.Tensor of dtype uint8 with values in range (0, 255) on device cuda:0
d = d3dshot.create(capture_output="pytorch_gpu")

# Captures will be torch.Tensor of dtype float64 with normalized values in range (0.0, 1.0) on device cuda:0
d = d3dshot.create(capture_output="pytorch_float_gpu")
```

Trying to use a Capture Output for which your environment does not meet the requirements will result in an error.

### Frame Buffer

When you create a _D3DShot_ instance, a frame buffer is also initialized. It is meant as a thread-safe, first-in, first-out way to hold a certain quantity of captures and is implemented as a `collections.deque`.

By default, the size of the frame buffer is set to 60. You can customize it when creating your _D3DShot_ object.

```python
d = d3dshot.create(frame_buffer_size=100)
```

Be mindful of RAM usage with larger values; You will be dealing with uncompressed images which use up to 100 MB each depending on the resolution.

The frame buffer can be accessed directly with `d.frame_buffer` but the usage of the utility methods instead is recommended.

The buffer is used by the following methods:

* `d.capture()`
* `d.screenshot_every()`

It is always automatically cleared before starting one of these operations.

### Displays

When you create a _D3DShot_ instance, your available displays will automatically be detected along with all their relevant properties.

```python
d.displays
```
```
Out[1]: 
[<Display name=BenQ XL2730Z (DisplayPort) adapter=NVIDIA GeForce GTX 1080 Ti resolution=2560x1440 rotation=0 scale_factor=1.0 primary=True>,
 <Display name=BenQ XL2430T (HDMI) adapter=Intel(R) UHD Graphics 630 resolution=1920x1080 rotation=0 scale_factor=1.0 primary=False>]
```

By default, your primary display will be selected. At all times you can verify which display is set to be used for capture.

```python
d.display
```
```
Out[1]: <Display name=BenQ XL2730Z (DisplayPort) adapter=NVIDIA GeForce GTX 1080 Ti resolution=2560x1440 rotation=0 scale_factor=1.0 primary=True>
```

Selecting another display for capture is as simple as setting `d.display` to another value from `d.displays`
```python
d.display = d.displays[1]
d.display
```
```
Out[1]: <Display name=BenQ XL2430T (HDMI) adapter=Intel(R) UHD Graphics 630 resolution=1080x1920 rotation=90 scale_factor=1.0 primary=False>
```

Display rotation and scaling is detected and handled for you by _D3DShot_:

* Captures on rotated displays will always be in the correct orientation (i.e. matching what you see on your physical displays)
* Captures on scaled displays will always be in full, non-scaled resolution (e.g. 1280x720 at 200% scaling will yield 2560x1440 captures)

### Regions

All capture methods (screenshots included) accept an optional `region` kwarg. The expected value is a 4-length tuple of integers that is to be structured like this:

```
(left, top, right, bottom)  # values represent pixels
```

For example, if you want to only capture a 200px by 200px region offset by 100px from both the left and top, you would do:

```python
d.screenshot(region=(100, 100, 300, 300))
```

If you are capturing a scaled display, the region will be computed against the full, non-scaled resolution. 

If you go through the source code, you will notice that the region cropping happens after a full display capture. That might seem sub-optimal but testing has revealed that copying a region of the GPU _D3D11Texture2D_ to the destination CPU _D3D11Texture2D_ using _CopySubresourceRegion_ is only faster when the region is very small. In fact, it doesn't take long for larger regions to actually start becoming slower than the full display capture using this method. To make things worse, it adds a lot of complexity by having the surface pitch not match the buffer size and treating rotated displays differently. It was therefore decided that it made more sense to stick to _CopyResource_ in all cases and crop after the fact.

## Usage

**Create a D3DShot instance**

```python
import d3dshot

d = d3dshot.create()
```

`create` accepts 2 optional kwargs:

* `capture_output`: Which capture output to use. See the _Capture Outputs_ section under _Concepts_
* `frame_buffer_size`: The maximum size the frame buffer can grow to. See the _Frame Buffer_ section under _Concepts_

Do NOT import the _D3DShot_ class directly and attempt to initialize it yourself! The `create` helper function initializes and validates a bunch of things for you behind the scenes.

Once you have a _D3DShot_ instance in scope, we can start doing stuff with it!

**List the detected displays**

```python
d.displays
```

**Select a display for capture**

Your primary display is selected by default but if you have a multi-monitor setup, you can select another entry in `d.displays` 

```python
d.display = d.displays[1]
```

**Take a screenshot**

```python
d.screenshot()
```

`screenshot` accepts 1 optional kwarg:

* `region`: A region tuple. See the _Regions_ section under _Concepts_

_Returns_: A screenshot with a format that matches the capture output you selected when creating your _D3DShot_ object

**Take a screenshot and save it to disk**

```python
d.screenshot_to_disk()
```

`screenshot_to_disk` accepts 3 optional kwargs:

* `directory`: The path / directory where to write the file. If omitted, the working directory of the program will be used
* `file_name`: The file name to use. Permitted extensions are: _.png_, _.jpg_. If omitted, the file name will be `<time.time()>.png` 
* `region`: A region tuple. See the _Regions_ section under _Concepts_

_Returns_: A string representing the full path to the saved image file

**Take a screenshot every X seconds**

```python
d.screenshot_every(X)  # Where X is a number representing seconds
```

This operation is threaded and non-blocking. It will keep running until `d.stop()` is called. Captures are pushed to the frame buffer.

`screenshot_every` accepts 1 optional kwarg:

* `region`: A region tuple. See the _Regions_ section under _Concepts_

_Returns_: A boolean indicating whether or not the capture thread was started

**Take a screenshot every X seconds and save it to disk**

```python
d.screenshot_to_disk_every(X)  # Where X is a number representing seconds
```

This operation is threaded and non-blocking. It will keep running until `d.stop()` is called.

`screenshot_to_disk_every` accepts 2 optional kwargs:

* `directory`: The path / directory where to write the file. If omitted, the working directory of the program will be used
* `region`: A region tuple. See the _Regions_ section under _Concepts_

_Returns_: A boolean indicating whether or not the capture thread was started

**Start a high-speed screen capture**

```python
d.capture()
```

This operation is threaded and non-blocking. It will keep running until `d.stop()` is called. Captures are pushed to the frame buffer.

`capture` accepts 2 optional kwargs:

* `target_fps`: How many captures per second to aim for. The effective capture rate will go under if the system can't keep up but it will never go over this target. It is recommended to set this to a reasonable value for your use case in order not to waste system resources. Default is set to 60.
* `region`: A region tuple. See the _Regions_ section under _Concepts_

_Returns_: A boolean indicating whether or not the capture thread was started

**Grab the latest frame from the buffer**

```python
d.get_latest_frame()
```

_Returns_: A frame with a format that matches the capture output you selected when creating your _D3DShot_ object

**Grab a specific frame from the buffer**

```python
d.get_frame(X)  # Where X is the index of the desired frame. Needs to be < len(d.frame_buffer)
```

_Returns_: A frame with a format that matches the capture output you selected when creating your _D3DShot_ object

**Grab specific frames from the buffer**

```python
d.get_frames([X, Y, Z, ...])  # Where X, Y, Z are valid indices to desired frames
```

_Returns_: A list of frames with a format that matches the capture output you selected when creating your _D3DShot_ object

**Grab specific frames from the buffer as a stack**

```python
d.get_frame_stack([X, Y, Z, ...], stack_dimension="first|last")  # Where X, Y, Z are valid indices to desired frames
```

Only has an effect on NumPy and PyTorch capture outputs.

`get_frame_stack` accepts 1 optional kwarg:

* `stack_dimension`: One of _first_, _last_. Which axis / dimension to perform the stack on

_Returns_: A single array stacked on the specified dimension with a format that matches the capture output you selected when creating your _D3DShot_ object. If the capture output is not stackable, returns a list of frames.

**Dump the frame buffer to disk**

The files will be named according to this convention: `<frame buffer index>.png`

```python
d.frame_buffer_to_disk()
```

`frame_buffer_to_disk` accepts 1 optional kwarg:

* `directory`: The path / directory where to write the files. If omitted, the working directory of the program will be used

_Returns_: None

## Performance

Measuring the exact performance of the Windows Desktop Duplication API proves to be a little complicated because it will only return new texture data if the contents of the screen has changed. This is optimal for performance but it makes it difficult to express in terms of frames per second, the measurement people tend to expect for benchmarks. Ultimately the solution ended up being to run a high FPS video game on the display to capture to make sure the screen contents is different at all times while benchmarking.

As always, remember that benchmarks are inherently flawed and highly depend on your individual hardware configuration and other circumstances. Use the numbers below as a relative indication of what to expect from _D3DShot_, not as some sort of absolute truth.

|                         | 2560x1440 on _NVIDIA GTX 1080 Ti_ | 1920x1080 on _Intel UHD Graphics 630_ | 1080x1920 (vertical) on _Intel UHD Graphics 630_ |
|-------------------------|-----------------------------------|---------------------------------------|--------------------------------------------------|
| **"pil"**               | 29.717 FPS                        | 47.75 FPS                             | 35.95 FPS                                        |
| **"numpy"**             | **57.667 FPS**                    | **58.1 FPS**                          | **58.033 FPS**                                   |
| **"numpy_float"**       | 18.783 FPS                        | 29.05 FPS                             | 27.517 FPS                                       |
| **"pytorch"**           | **57.867 FPS**                    | **58.1 FPS**                          | 34.817 FPS                                       |
| **"pytorch_float"**     | 18.767 FPS                        | 28.367 FPS                            | 27.017 FPS                                       |
| **"pytorch_gpu"**       | 27.333 FPS                        | 35.767 FPS                            | 34.8 FPS                                         |
| **"pytorch_float_gpu"** | 27.267 FPS                        | 37.383 FPS                            | 35.033 FPS                                       |

The absolute fastest capture outputs appear to be _"numpy"_ and unrotated _"pytorch"_; all averaging around 58 FPS. In Python land, this is FAST! 

#### How is the "numpy" capture output performance _that_ good?

NumPy arrays have a ctypes interface that can give you their raw memory address (`X.ctypes.data`). If you have the memory address and size of another byte buffer, which is what we end up with by processing what returns from the Desktop Duplication API, you can use `ctypes.memmove` to copy that byte buffer directly to the NumPy structure, effectively bypassing as much Python as possible.

In practice it ends up looking like this:
```python
ctypes.memmove(np.empty((size,), dtype=np.uint8).ctypes.data, pointer, size)
```

This low-level operation is extremely fast, leaving everything else that would normally compete with NumPy in the dust.

#### Why is the "pytorch" capture output slower on rotated displays?

Don't tell anyone but the reason it can compete with NumPy in the first place is only because... _it is_ generated from a NumPy array built from the method above! If you sniff around the code, you will indeed find `torch.from_numpy()` scattered around. This pretty much matches the speed of the "numpy" capture output 1:1, except when dealing with a rotated display. Display rotation is handled by `np.rot90()` calls which yields negative strides on that array. Negative strides are understood and perform well under NumPy but are still unsupported in PyTorch at the time of writing. To address this, an additional copy operation is needed to bring it back to a contiguous array which imposes a performance penalty.

#### Why is the "pil" capture output, being the default, not the fastest?

PIL has no ctypes interface like NumPy so a bytearray needs to be read into Python first and then fed to `PIL.Image.frombytes()`. This is still fast in Python terms, but it just cannot match the speed of the low-level NumPy method.

It remains the default capture output because:

1) PIL Image objects tend to be familiar to Python users
2) It's a way lighter / simpler dependency for a library compared to NumPy or PyTorch

#### Why are the float versions of capture outputs slower?

The data of the Direct3D textures made accessible by the Desktop Duplication API is formatted as bytes. To represent this data as normalized floats instead, a type cast and element-wise division needs to be performed on the array holding those bytes. This imposes a major performance penalty. Interestingly, you can see this performance penalty mitigated on GPU PyTorch tensors since the element-wise division can be massively parallelized on the device.

#

_Crafted with ❤ by Serpent.AI 🐍_  
[Twitter](https://twitter.com/Serpent_AI) - [Twitch](https://www.twitch.tv/serpent_ai)