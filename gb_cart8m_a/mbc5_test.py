from nmigen.sim import Delay, Simulator
import unittest

from gb_cart8m_a.mbc5 import Mbc5

class Mbc5Test(unittest.TestCase):
    def setUp(self):
        self.mbc = Mbc5()

    def write(self, addr, data):
        yield self.mbc.cart_addr.eq(addr | 0x8000)
        yield Delay(1e-6)
        yield self.mbc.cart_addr[15].eq(addr & 0x8000)
        yield Delay(1e-6)
        yield self.mbc.cart_wr.eq(1)
        yield self.mbc.cart_data.eq(data)
        yield Delay(1e-6)
        yield self.mbc.cart_wr.eq(0)
        yield Delay(1e-6)
        yield self.mbc.cart_addr[15].eq(1)
        yield Delay(1e-6)

    def reset(self):
        yield self.mbc.cart_rst.eq(1)
        yield Delay(1e-6)
        yield self.mbc.cart_rst.eq(0)
        yield Delay(1e-6)

    def assert_rom_banks(self, bank0, bank1):
        yield self.mbc.cart_addr.eq(0x0000)
        yield Delay(1e-6)
        assert (yield self.mbc.rom_bank) == bank0
        yield self.mbc.cart_addr.eq(0x4000)
        yield Delay(1e-6)
        assert (yield self.mbc.rom_bank) == bank1

    def test_ram_en(self):
        sim = Simulator(self.mbc)
        def proc():
            yield from self.reset()

            assert (yield self.mbc.ram_en) == 0
            yield from self.write(0x0000, 0x0A)
            assert (yield self.mbc.ram_en) == 1
            yield from self.write(0x0000, 0x1A)
            assert (yield self.mbc.ram_en) == 0

        sim.add_process(proc)
        sim.reset()
        sim.run()

    def test_rom_banks(self):
        sim = Simulator(self.mbc)
        def proc():
            yield from self.reset()

            yield from self.assert_rom_banks(0x000, 0x001)
            yield from self.write(0x2000, 0x42)
            yield from self.assert_rom_banks(0x000, 0x042)
            yield from self.write(0x3000, 0x01)
            yield from self.assert_rom_banks(0x000, 0x142)
            yield from self.write(0x2000, 0x00)
            yield from self.assert_rom_banks(0x000, 0x100)
            yield from self.write(0x3000, 0x00)
            yield from self.assert_rom_banks(0x000, 0x000)

        sim.add_process(proc)
        sim.reset()
        sim.run()

    def test_ram_banks(self):
        sim = Simulator(self.mbc)
        def proc():
            yield from self.reset()

            yield from self.write(0x4000, 0x1F)
            assert (yield self.mbc.ram_bank) == 0xF
            yield from self.write(0x4000, 0x7A)
            assert (yield self.mbc.ram_bank) == 0xA

        sim.add_process(proc)
        sim.reset()
        sim.run()
