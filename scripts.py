def assemble():
    from gb_cart8m_a.platform import GbCartPlatform
    from gb_cart8m_a.top import Top

    GbCartPlatform().build(Top())


def clean():
    from pathlib import Path
    import shutil

    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)


def test():
    import gb_cart8m_a.mbc5_test
    import unittest

    unittest.main(gb_cart8m_a.mbc5_test)
