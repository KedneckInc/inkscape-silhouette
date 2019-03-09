import unittest
import sys
# from silhouette.os_isolation import OSIsolation
from silhouette.OSIsolation import OSIsolation

class TestOSIsolation(unittest.TestCase):

    def setUp(self):
        self.isobar = OSIsolation();

    # def tearDown(self):
    #     self.isobar.dispose()

    def test_os_type(self):
        self.assertEqual('linux',self.isobar.os_type,"OS Type Mismatch")

    def test_usb_context(self):
        self.assertEqual(None,self.isobar.usb_context,"USB context should be 'none'")

    def test_usb_vi(self):
        self.assertFalse(self.isobar.usb_vi < 1)

    def test_usb_vi_str(self):
        self.assertTrue(len(self.isobar.usb_vi_str) > 0)

if __name__ == '__main__':
    unittest.main()
