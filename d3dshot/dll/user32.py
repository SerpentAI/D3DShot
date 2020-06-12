import ctypes
import ctypes.wintypes as wintypes


class DISPLAY_DEVICE(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("DeviceName", wintypes.WCHAR * 32),
        ("DeviceString", wintypes.WCHAR * 128),
        ("StateFlags", wintypes.DWORD),
        ("DeviceID", wintypes.WCHAR * 128),
        ("DeviceKey", wintypes.WCHAR * 128),
    ]


def get_display_device_name_mapping():
    display_names = list()

    i = 0
    while True:
        display_device = DISPLAY_DEVICE()
        display_device.cb = ctypes.sizeof(display_device)

        if not ctypes.windll.user32.EnumDisplayDevicesW(None, i, ctypes.byref(display_device), 0):
            break

        if display_device.StateFlags > 0:
            is_primary_display_device = bool(display_device.StateFlags & 4)
            display_names.append((display_device.DeviceName, is_primary_display_device))

        i += 1

    display_device_name_mapping = dict()

    for display_name, is_primary in display_names:
        display_device = DISPLAY_DEVICE()
        display_device.cb = ctypes.sizeof(display_device)

        if ctypes.windll.user32.EnumDisplayDevicesW(
            display_name, 0, ctypes.byref(display_device), 0
        ):
            display_device_name_mapping[display_name.split("\\")[-1]] = (
                display_device.DeviceString,
                is_primary,
            )

    return display_device_name_mapping


def get_hmonitor_by_point(x, y):
    point = wintypes.POINT()

    point.x = x
    point.y = y

    return ctypes.windll.user32.MonitorFromPoint(point, 0)
