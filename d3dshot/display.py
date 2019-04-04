import d3dshot.dll.dxgi
import d3dshot.dll.d3d
import d3dshot.dll.user32
import d3dshot.dll.shcore


class Display:

    def __init__(
        self,
        name=None,
        adapter_name=None,
        resolution=None,
        position=None,
        rotation=None,
        scale_factor=None,
        is_primary=False,
        hmonitor=None,
        dxgi_output=None,
        dxgi_adapter=None
    ):
        self.name = name or "Unknown" 
        self.adapter_name = adapter_name or "Unknown Adapter" 
        
        self.resolution = resolution or (0, 0)
        
        self.position = position or { "left": 0, "top": 0, "right": 0, "bottom": 0 }
        self.rotation = rotation or 0
        self.scale_factor = scale_factor or 1.0

        self.is_primary = is_primary
        self.hmonitor = hmonitor or 0

        self.dxgi_output = dxgi_output
        self.dxgi_adapter = dxgi_adapter

        self.d3d_device = None
        self.d3d_device_context = None

        self.dxgi_output_duplication = self._initialize_dxgi_output_duplication()

    def __repr__(self):
        return f"<Display name={self.name} adapter={self.adapter_name} resolution={self.resolution[0]}x{self.resolution[1]} rotation={self.rotation} scale_factor={self.scale_factor} primary={self.is_primary}>"

    def capture(self, process_func, region=None):
        region = self._get_clean_region(region)
        frame = None

        try:
            frame = d3dshot.dll.dxgi.get_dxgi_output_duplication_frame(
                self.dxgi_output_duplication,
                self.d3d_device,
                process_func=process_func,
                width=self.resolution[0],
                height=self.resolution[1],
                region = region,
                rotation=self.rotation
            )
        except:
            pass

        return frame

    def _initialize_dxgi_output_duplication(self):
        self.d3d_device, self.d3d_device_context = d3dshot.dll.d3d.initialize_d3d_device(self.dxgi_adapter)
        return d3dshot.dll.dxgi.initialize_dxgi_output_duplication(self.dxgi_output, self.d3d_device)

    def _get_clean_region(self, region):
        if region is None:
            return (0, 0, self.resolution[0], self.resolution[1])

        clean_region = list()

        clean_region.append(0 if region[0] < 0 or region[0] > self.resolution[0] else region[0])
        clean_region.append(0 if region[1] < 0 or region[1] > self.resolution[1] else region[1])
        clean_region.append(self.resolution[0] if region[2] < 0 or region[2] > self.resolution[0] else region[2])
        clean_region.append(self.resolution[1] if region[3] < 0 or region[3] > self.resolution[1] else region[3])

        return tuple(clean_region)

    @classmethod
    def discover_displays(cls):
        display_device_name_mapping = d3dshot.dll.user32.get_display_device_name_mapping()

        dxgi_factory = d3dshot.dll.dxgi.initialize_dxgi_factory()
        dxgi_adapters = d3dshot.dll.dxgi.discover_dxgi_adapters(dxgi_factory)
  
        displays = list()

        for dxgi_adapter in dxgi_adapters:
            dxgi_adapter_description = d3dshot.dll.dxgi.describe_dxgi_adapter(dxgi_adapter)

            for dxgi_output in d3dshot.dll.dxgi.discover_dxgi_outputs(dxgi_adapter):
                dxgi_output_description = d3dshot.dll.dxgi.describe_dxgi_output(dxgi_output)

                if dxgi_output_description["is_attached_to_desktop"]:
                    display_device = display_device_name_mapping.get(dxgi_output_description["name"])

                    if display_device is None:
                        display_device = ("Unknown", False)

                    hmonitor = d3dshot.dll.user32.get_hmonitor_by_point(
                        dxgi_output_description["position"]["left"],
                        dxgi_output_description["position"]["top"]
                    )

                    scale_factor = d3dshot.dll.shcore.get_scale_factor_for_monitor(hmonitor)

                    display = cls(
                        name=display_device[0],
                        adapter_name=dxgi_adapter_description,
                        resolution=dxgi_output_description["resolution"],
                        position=dxgi_output_description["position"],
                        rotation=dxgi_output_description["rotation"],
                        scale_factor=scale_factor,
                        is_primary=display_device[1],
                        hmonitor=hmonitor,
                        dxgi_output=dxgi_output,
                        dxgi_adapter=dxgi_adapter
                    )

                    displays.append(display)

        return displays
