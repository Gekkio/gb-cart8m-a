from enum import Enum
from nmigen import Elaboratable, Module, Signal, Mux
from nmigen.build import Platform
from nmigen.cli import main

from gb_cart8m_a.mbc5 import Mbc5


class DataDirection(Enum):
    INPUT = 0
    OUTPUT = 1


class GbCart(Elaboratable):
    def __init__(self):
        self.cart_rst = Signal()
        self.cart_addr = Signal(16)
        self.cart_data = Signal(8)
        self.cart_rd = Signal()
        self.cart_wr = Signal()
        self.cart_cs = Signal()
        self.rom_wr = Signal()

        self.data_dir = Signal()
        self.cart_oe = Signal()
        self.ram_cs = Signal()
        self.ram_bank = Signal(4)
        self.rom_bank = Signal(9)

        self.mbc = Mbc5()

    def elaborate(self, platform: Platform) -> Module:
        m = Module()
        m.submodules.mbc = self.mbc

        any_cs = Signal()
        rom_cs = Signal()

        m.d.comb += [
            self.mbc.cart_rst.eq(self.cart_rst),
            self.mbc.cart_addr.eq(self.cart_addr),
            self.mbc.cart_data.eq(self.cart_data),
            self.mbc.cart_wr.eq(self.cart_wr),
        ]
        m.d.comb += [
            self.ram_bank.eq(self.mbc.ram_bank),
            self.rom_bank.eq(self.mbc.rom_bank),
        ]

        m.d.comb += [rom_cs.eq(~self.cart_addr[15]), any_cs.eq(self.ram_cs ^ rom_cs)]

        m.d.comb += self.data_dir.eq(
            Mux(self.cart_rd & any_cs, DataDirection.OUTPUT, DataDirection.INPUT)
        )
        m.d.comb += self.cart_oe.eq(
            (self.cart_rd | self.cart_wr | self.rom_wr) & any_cs
        )
        m.d.comb += self.ram_cs.eq(
            m.submodules.mbc.ram_en & self.cart_cs & (self.cart_addr[13:] == 0b101)
        )

        return m

    def ports(self):
        return [
            self.cart_rst,
            self.cart_addr,
            self.cart_data,
            self.cart_rd,
            self.cart_wr,
            self.cart_cs,
            self.rom_wr,
            self.data_dir,
            self.cart_oe,
            self.ram_cs,
            self.ram_bank,
            self.rom_bank,
        ]


if __name__ == "__main__":
    gb_cart = GbCart()
    main(gb_cart, ports=gb_cart.ports)
