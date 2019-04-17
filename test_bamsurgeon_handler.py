import unittest
import bamsurgeon_handler as bams

class MyTestCase(unittest.TestCase):
    def test_create_snv(self):
        bams.create_snv()
"""

    def test_something(self):
        self.assertEqual(True, False)



    def test_create_sv(self):
        self.assertEqual(True, False)

    def test_create_indel(self):
        self.assertEqual(True, False)
"""

if __name__ == '__main__':
    unittest.main()
