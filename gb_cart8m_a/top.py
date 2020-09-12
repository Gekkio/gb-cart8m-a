from nmigen import Elaboratable, Module
from nmigen.build import Platform

from gb_cart8m_a.gb_cart import GbCart


class Top(Elaboratable):
    def __init__(self):
        self.gb_cart = GbCart()

    def elaborate(self, platform: Platform) -> Module:
        m = Module()
        m.submodules.gb_cart = self.gb_cart

        cart_rst = platform.request("cart_rst")
        cart_addr = platform.request("cart_addr")
        cart_data = platform.request("cart_data")
        cart_rd = platform.request("cart_rd")
        cart_wr = platform.request("cart_wr")
        cart_cs = platform.request("cart_cs")
        rom_wr = platform.request("rom_wr")
        data_dir = platform.request("data_dir")
        cart_oe = platform.request("cart_oe")
        ram_cs = platform.request("ram_cs")
        ram_bank = platform.request("ram_bank")
        rom_bank = platform.request("rom_bank")

        platform.request("cart_phi")

        m.d.comb += [
            self.gb_cart.cart_rst.eq(cart_rst),
            self.gb_cart.cart_addr.eq(cart_addr),
            self.gb_cart.cart_data.eq(cart_data),
            self.gb_cart.cart_rd.eq(cart_rd),
            self.gb_cart.cart_wr.eq(cart_wr),
            self.gb_cart.cart_cs.eq(cart_cs),
            self.gb_cart.rom_wr.eq(rom_wr),
            data_dir.eq(self.gb_cart.data_dir),
            cart_oe.eq(self.gb_cart.cart_oe),
            ram_cs.eq(self.gb_cart.ram_cs),
            ram_bank.eq(self.gb_cart.ram_bank),
            rom_bank.eq(self.gb_cart.rom_bank),
        ]

        return m


if __name__ == "__main__":
    from gb_cart_platform import GbCartPlatform

    GbCartPlatform().build(Top())
