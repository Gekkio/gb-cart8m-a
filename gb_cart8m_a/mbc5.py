from nmigen import (
    Cat,
    ClockDomain,
    ClockSignal,
    Elaboratable,
    Module,
    ResetSignal,
    Signal,
)
from nmigen.build import Platform
from nmigen.cli import main


class Mbc5(Elaboratable):
    def __init__(self):
        self.cart_rst = Signal(1)
        self.cart_addr = Signal(16)
        self.cart_data = Signal(8)
        self.cart_wr = Signal(1)

        self.ram_en = Signal(1)
        self.ram_bank = Signal(4)
        self.rom_bank = Signal(9)

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        m.domains.ramg = ClockDomain(async_reset=True, local=True)
        m.domains.romb0 = ClockDomain(async_reset=True, local=True)
        m.domains.romb1 = ClockDomain(async_reset=True, local=True)
        m.domains.ramb = ClockDomain(async_reset=True, local=True)

        ramg_clk = ClockSignal("ramg")
        romb0_clk = ClockSignal("romb0")
        romb1_clk = ClockSignal("romb1")
        ramb_clk = ClockSignal("ramb")

        m.d.comb += [
            ResetSignal("ramg").eq(self.cart_rst),
            ResetSignal("romb0").eq(self.cart_rst),
            ResetSignal("romb1").eq(self.cart_rst),
            ResetSignal("ramb").eq(self.cart_rst),
        ]

        ramg = Signal(8)
        romb0 = Signal(8, reset=0x01)
        romb1 = Signal(1)
        ramb = Signal(4)

        m.d.ramg += ramg.eq(self.cart_data)
        m.d.romb0 += romb0.eq(self.cart_data)
        m.d.romb1 += romb1.eq(self.cart_data)
        m.d.ramb += ramb.eq(self.cart_data)

        m.d.comb += [ramg_clk.eq(1), romb0_clk.eq(1), romb1_clk.eq(1), ramb_clk.eq(1)]
        with m.If(self.cart_wr):
            with m.Switch(self.cart_addr[12:]):
                with m.Case(0b0000):
                    m.d.comb += ramg_clk.eq(0)
                with m.Case(0b0001):
                    m.d.comb += ramg_clk.eq(0)
                with m.Case(0b0010):
                    m.d.comb += romb0_clk.eq(0)
                with m.Case(0b0011):
                    m.d.comb += romb1_clk.eq(0)
                with m.Case(0b0100):
                    m.d.comb += ramb_clk.eq(0)
                with m.Case(0b0101):
                    m.d.comb += ramb_clk.eq(0)

        m.d.comb += [
            self.ram_en.eq(ramg == 0x0A),
            self.ram_bank.eq(ramb),
        ]
        with m.If(self.cart_addr[14]):
            m.d.comb += self.rom_bank.eq(Cat(romb0, romb1))
        with m.Else():
            m.d.comb += self.rom_bank.eq(0)

        return m

    def ports(self):
        return [
            self.cart_rst,
            self.cart_addr,
            self.cart_data,
            self.cart_wr,
            self.ram_en,
            self.ram_bank,
            self.rom_bank,
        ]


if __name__ == "__main__":
    mbc = Mbc5()
    main(mbc, ports=mbc.ports)
