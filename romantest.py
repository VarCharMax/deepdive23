"""_summary_"""

import unittest
import roman


class KnownValues(unittest.TestCase):
    """_summary_

    Args:
        pytest (_type_): _description_
    """

    knownValues = (
        (1, "I"),
        (2, "II"),
        (3, "III"),
        (4, "IV"),
        (5, "V"),
        (6, "VI"),
        (7, "VII"),
        (8, "VIII"),
        (9, "IX"),
        (10, "X"),
        (50, "L"),
        (100, "C"),
        (500, "D"),
        (1000, "M"),
        (31, "XXXI"),
        (148, "CXLVIII"),
        (294, "CCXCIV"),
        (312, "CCCXII"),
        (421, "CDXXI"),
        (528, "DXXVIII"),
        (621, "DCXXI"),
        (782, "DCCLXXXII"),
        (870, "DCCCLXX"),
        (941, "CMXLI"),
        (1043, "MXLIII"),
        (1110, "MCX"),
        (1226, "MCCXXVI"),
        (1301, "MCCCI"),
        (1485, "MCDLXXXV"),
        (1509, "MDIX"),
        (1607, "MDCVII"),
        (1754, "MDCCLIV"),
        (1832, "MDCCCXXXII"),
        (1993, "MCMXCIII"),
        (2074, "MMLXXIV"),
        (2152, "MMCLII"),
        (2212, "MMCCXII"),
        (2343, "MMCCCXLIII"),
        (2499, "MMCDXCIX"),
        (2574, "MMDLXXIV"),
        (2646, "MMDCXLVI"),
        (2723, "MMDCCXXIII"),
        (2892, "MMDCCCXCII"),
        (2975, "MMCMLXXV"),
        (3051, "MMMLI"),
        (3185, "MMMCLXXXV"),
        (3250, "MMMCCL"),
        (3313, "MMMCCCXIII"),
        (3408, "MMMCDVIII"),
        (3501, "MMMDI"),
        (3610, "MMMDCX"),
        (3743, "MMMDCCXLIII"),
        (3844, "MMMDCCCXLIV"),
        (3888, "MMMDCCCLXXXVIII"),
        (3940, "MMMCMXL"),
        (3999, "MMMCMXCIX"),
    )

    def testtoromanknownvalues(self) -> None:
        """toroman should give known result with known input"""
        for integer, numeral in self.knownValues:
            result = roman.toroman(integer)
            self.assertEqual(numeral, result)

    def testfromromanknownvalues(self):
        """fromroman should give known result with known input"""
        for integer, numeral in self.knownValues:
            result = roman.fromroman(numeral)
            self.assertEqual(integer, result)


class ToRomanBadInput(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    def testtoolarge(self):
        """toRoman should fail with large input"""
        self.assertRaises(roman.OutOfRangeError, roman.toroman, 5000)

    def testzero(self):
        """toRoman should fail with 0 input"""
        self.assertRaises(roman.OutOfRangeError, roman.toroman, 0)

    def testnegative(self):
        """toRoman should fail with negative input"""
        self.assertRaises(roman.OutOfRangeError, roman.toroman, -1)

    def testdecimal(self):
        """toRoman should fail with non-integer input"""
        self.assertRaises(roman.NotIntegerError, roman.toroman, 0.5)


class FromRomanBadInput(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    def testtoomanyrepeatednumerals(self):
        """fromRoman should fail with too many repeated numerals"""
        for s in ("MMMMM", "DD", "CCCC", "LL", "XXXX", "VV", "IIII"):
            self.assertRaises(roman.InvalidRomanNumeralError, roman.fromroman, s)

    def testrepeatedpairs(self):
        """fromRoman should fail with repeated pairs of numerals"""
        for s in ("CMCM", "CDCD", "XCXC", "XLXL", "IXIX", "IVIV"):
            self.assertRaises(roman.InvalidRomanNumeralError, roman.fromroman, s)

    def testmalformedantecedent(self):
        """fromRoman should fail with malformed antecedents"""
        for s in (
            "IIMXCC",
            "VX",
            "DCM",
            "CMM",
            "IXIV",
            "MCMC",
            "XCX",
            "IVI",
            "LM",
            "LD",
            "LC",
        ):
            self.assertRaises(roman.InvalidRomanNumeralError, roman.fromroman, s)

    def testblank(self):
        """fromRoman should fail with blank string"""
        self.assertRaises(roman.InvalidRomanNumeralError, roman.fromroman, "")


class SanityCheck(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    def testsanity(self):
        """fromRoman(toRoman(n))==n for all n"""
        for integer in range(1, 5000):
            numeral = roman.toroman(integer)
            result = roman.fromroman(numeral)
            self.assertEqual(integer, result)


class CaseCheck(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    def testtoromancase(self):
        """toRoman should always return uppercase"""
        for integer in range(1, 5000):
            numeral = roman.toroman(integer)
            self.assertEqual(numeral, numeral.upper())

    def testfromromancase(self):
        """fromRoman should only accept uppercase input"""
        for integer in range(1, 5000):
            numeral = roman.toroman(integer)
            roman.fromroman(numeral.upper())
            self.assertRaises(
                roman.InvalidRomanNumeralError, roman.fromroman, numeral.lower()
            )


if __name__ == "__main__":
    unittest.main()
