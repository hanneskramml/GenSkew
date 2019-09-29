import unittest
from genskew.lib import GenSkew


class LibraryCase(unittest.TestCase):
    def test_plot_1seq(self):
        GenSkew.plot("volvox.fasta")
        self.assertTrue(True)

    def test_plot_multseq(self):
        GenSkew.plot("Efaecalis-49.fasta")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
