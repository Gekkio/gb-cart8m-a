import os

root_dir = os.path.dirname(os.path.realpath(__file__))


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


def check():
    import black

    black.main(["--check", root_dir])


def fmt():
    import black

    black.main([root_dir])


def test():
    import gb_cart8m_a.mbc5_test
    import unittest

    unittest.main(gb_cart8m_a.mbc5_test)
