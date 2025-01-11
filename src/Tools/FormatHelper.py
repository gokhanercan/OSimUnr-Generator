# coding=utf-8
#https://mkaz.blog/code/python-string-format-cookbook/

# Number	Format	Output	Description
# 3.1415926	{:.2f}	3.14	2 decimal places
# 3.1415926	{:+.2f}	+3.14	2 decimal places with sign
#     -1	{:+.2f}	-1.00	2 decimal places with sign
#     2.71828	{:.0f}	3	No decimal places
# 5	{:0>2d}	05	Pad number with zeros (left padding, width 2)
# 5	{:x<4d}	5xxx	Pad number with x’s (right padding, width 4)
# 10	{:x<4d}	10xx	Pad number with x’s (right padding, width 4)
# 1000000	{:,}	1,000,000	Number format with comma separator
# 0.25	{:.2%}	25.00%	Format percentage
# 1000000000	{:.2e}	1.00e+09	Exponent notation
# 13	{:10d}	        13	Right aligned (default, width 10)
# 13	{:<10d}	13	Left aligned (width 10)
# 13	{:^10d}	    13	Center aligned (width 10)

_TwoDigitFormat:str =".2f"
_ThreeDigitFormat:str =".3f"
_FourDigitFormat:str =".4f"
_NoDecimalFormat:str = ".0f"
_ThousandsSeperatorFormat:str = ","

def TwoDigit(value)->str:
    return ("{:"+_TwoDigitFormat+"}").format(value)

def ThreeDigit(value)->str:
    return ("{:"+_ThreeDigitFormat+"}").format(value)

def NoDecimal(value)->str:
    return ("{:"+_NoDecimalFormat+"}").format(value)

def ThousandSeperator(value)->str:
    return ("{:"+_ThousandsSeperatorFormat+"}").format(value)

def Humanize(num, reportActualNumber:bool = False)->str:
    """
    Converts the given large numeric value to easily readable values like 10K, 1M, 4B.
    ref: https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings-in-python/45846841
    :param num:
    :param reportActualNumber: If True, it also gives the actual number in parentheses in addition to the abbreviation.
    :return:
    """
    orgnum = num
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    hum:str = '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
    if(reportActualNumber==True and orgnum > 999):
        hum = hum + " (" + ThousandSeperator(orgnum) + ")"
    return hum



import unittest
from unittest import TestCase

class FormatHelperTest(TestCase):

    import unittest
    from unittest import TestCase

    def test_Humanize_WithReportActualNumber(self):
        self.assertEqual("6.54B (6,543,165,413)",Humanize(6543165413,True))

    def test_Humanize_SmallNumber_WithReportActualNumber_DoNotReportActual(self):
        self.assertEqual("999",Humanize(999,True))

    def test_Humanize_NotSmallNumber_WithReportActualNumber_DoReportActual(self):
        self.assertEqual("1K (1,000)",Humanize(1000,True))

if __name__ == "__main__":
    unittest.main()

    print(Humanize(999999))
    print(Humanize(999499))
    print(Humanize(9994))
    print(Humanize(9994))
    print(Humanize(9900))
    print(Humanize(6543165413, True))
    print(TwoDigit(3.14545))