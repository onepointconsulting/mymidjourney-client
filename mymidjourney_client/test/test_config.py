import unittest

from mymidjourney_client.config import midjourney_cfg


class TestImagineResult(unittest.TestCase):
    def test_convert_from_str(self):
        assert midjourney_cfg is not None
        assert midjourney_cfg.temp_dir.exists()


if __name__ == "__main__":
    unittest.main()
