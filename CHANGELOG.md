#### 0.1.5
* FIX: Made the D3DShot class a singleton to avoid crashes when subsequent calls are made to `create()`
* FIX: Actually honor `DXGI_MAPPED_RECT.Pitch` when building the capture output. This resolves issues with garbled output at some resolutions.

#### 0.1.4

* FIX: If no display is identified as the primary display, default to the first one (@Ricky54326)
* FIX: When stopping a capture, give the capture thread a budget of up to 1 second to join. Should provide a better guarantee the frame buffer won't be written to after stop() returns
* FIX: When saving the frame buffer to disk, iterate over a tuple-cast frame buffer copy. Prevents iteration errors if the frame buffer gets written to during iteration
* INTERNAL: Manage dependencies + builds with Poetry
* INTERNAL: Code auto-formatting with Black



