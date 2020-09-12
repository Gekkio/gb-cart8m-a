import unittest

def assemble():
    from gb_cart8m_a.platform import GbCartPlatform
    from gb_cart8m_a.top import Top

    GbCartPlatform().build(Top())

def test():
    import gb_cart8m_a.mbc5_test
    unittest.main(gb_cart8m_a.mbc5_test)
