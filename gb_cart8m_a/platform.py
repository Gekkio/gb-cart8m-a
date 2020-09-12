from nmigen.vendor.intel import IntelPlatform
from nmigen.hdl import Module, Instance
from nmigen.build import Attrs, Resource, Pins


class GbCartPlatform(IntelPlatform):
    device = "5M40Z"
    package = "E64"
    speed = "C5"
    resources = [
        Resource(
            "cart_rst",
            0,
            Pins("29", dir="i", invert=True),
            Attrs(io_standard="3.3V SCHMITT TRIGGER INPUT"),
        ),
        Resource(
            "cart_addr",
            0,
            Pins("55 54 24 25 26 27 28 30 31 32 21 20 49 53 52 56", dir="i"),
            Attrs(
                io_standard="3.3V SCHMITT TRIGGER INPUT", enable_bus_hold_circuitry="ON"
            ),
        ),
        Resource(
            "cart_data",
            0,
            Pins("58 59 60 61 62 63 64 1", dir="i"),
            Attrs(
                io_standard="3.3V SCHMITT TRIGGER INPUT", enable_bus_hold_circuitry="ON"
            ),
        ),
        Resource(
            "cart_rd",
            0,
            Pins("33", dir="i", invert=True),
            Attrs(io_standard="3.3V SCHMITT TRIGGER INPUT"),
        ),
        Resource(
            "cart_wr",
            0,
            Pins("44", dir="i", invert=True),
            Attrs(io_standard="3.3V SCHMITT TRIGGER INPUT"),
        ),
        Resource(
            "cart_cs",
            0,
            Pins("47", dir="i", invert=True),
            Attrs(io_standard="3.3V SCHMITT TRIGGER INPUT"),
        ),
        Resource(
            "cart_phi",
            0,
            Pins("48", dir="i"),
            Attrs(
                io_standard="3.3V SCHMITT TRIGGER INPUT", enable_bus_hold_circuitry="ON"
            ),
        ),
        Resource(
            "rom_wr",
            0,
            Pins("10", dir="i", invert=True),
            Attrs(io_standard="3.3V SCHMITT TRIGGER INPUT"),
        ),
        Resource("data_dir", 0, Pins("51", dir="o"), Attrs(io_standard="3.3-V LVCMOS")),
        Resource(
            "cart_oe",
            0,
            Pins("46", dir="o", invert=True),
            Attrs(io_standard="3.3-V LVCMOS"),
        ),
        Resource(
            "ram_cs",
            0,
            Pins("35", dir="o", invert=True),
            Attrs(io_standard="3.3-V LVCMOS"),
        ),
        Resource(
            "ram_bank",
            0,
            Pins("36 37 38 34", dir="o"),
            Attrs(io_standard="3.3-V LVCMOS"),
        ),
        Resource(
            "rom_bank",
            0,
            Pins("5 4 3 2 13 11 7 9 12", dir="o"),
            Attrs(io_standard="3.3-V LVCMOS"),
        ),
    ]
    connectors = []
    file_templates = {
        **IntelPlatform.file_templates,
        "{{name}}.qsf": IntelPlatform.file_templates["{{name}}.qsf"]
        + r"""
            set_global_assignment -name ISP_CLAMP_STATE_DEFAULT HIGH

            set_global_assignment -name IOBANK_VCCIO 3.3V -section_id 1
            set_global_assignment -name IOBANK_VCCIO 3.3V -section_id 2
            set_global_assignment -name RESERVE_ALL_UNUSED_PINS "AS INPUT TRI-STATED WITH BUS-HOLD"

            set_global_assignment -name POWER_PRESET_COOLING_SOLUTION "NO HEAT SINK WITH STILL AIR"
            set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE POWER"
            set_global_assignment -name AUTO_RESOURCE_SHARING ON
            set_global_assignment -name ROUTER_TIMING_OPTIMIZATION_LEVEL MAXIMUM
            set_global_assignment -name FITTER_EFFORT "STANDARD FIT"
            set_global_assignment -name PHYSICAL_SYNTHESIS_EFFORT EXTRA
        """,
        "{{name}}.sdc": IntelPlatform.file_templates["{{name}}.sdc"]
        + r"""
            create_clock -name gb_clk -period 120 -waveform {10 110}
            create_clock -name ramg_clk -period 120 -waveform {10 110} [get_nets {gb_cart|mbc|ramg_clk}]
            create_clock -name romb0_clk -period 120 -waveform {10 110} [get_nets {gb_cart|mbc|romb0_clk}]
            create_clock -name romb1_clk -period 120 -waveform {10 110} [get_nets {gb_cart|mbc|romb1_clk}]
            create_clock -name ramb_clk -period 120 -waveform {10 110} [get_nets {gb_cart|mbc|ramb_clk}]
            set_input_delay -clock { gb_clk } 20 [get_ports {cart_rd_* cart_wr_* cart_cs_* cart_addr_* cart_data_* rom_wr_*}]
            set_output_delay -clock { gb_clk } 20 [get_ports {ram_bank_* rom_bank_* data_dir_* ram_cs_* cart_oe_*}]
            set_false_path -from [get_ports {cart_rst_*}] -to *
        """
    }

    def get_input(self, pin, port, attrs, invert):
        self._check_feature(
            "single-ended input", pin, attrs, valid_xdrs=(0, 1), valid_attrs=True
        )

        m = Module()
        i = self._get_ireg(m, pin, invert)
        for bit in range(pin.width):
            m.submodules["{}_{}".format(pin.name, bit)] = Instance(
                "alt_inbuf", i_i=port.io[bit], o_o=i[bit]
            )
        return m

    def get_output(self, pin, port, attrs, invert):
        self._check_feature(
            "single-ended output", pin, attrs, valid_xdrs=(0, 1), valid_attrs=True
        )

        m = Module()
        o = self._get_oreg(m, pin, invert)
        for bit in range(pin.width):
            m.submodules["{}_{}".format(pin.name, bit)] = Instance(
                "alt_outbuf", i_i=o[bit], o_o=port.io[bit]
            )
        return m
