import unittest
from modules.evaluation import _is_num


# TODO: Add more test of other things. I know, I know.
class MyTestCase(unittest.TestCase):
    def test_is_num1(self):
        self.assertEqual(_is_num(1), True)

    def test_is_num2(self):
        self.assertEqual(_is_num("A"), False)

    def test_is_num3(self):
        self.assertEqual(_is_num("1"), True)


if __name__ == '__main__':
    unittest.main()
