"""
Fiscal to academic year conversion
"""

from collections import namedtuple

Year = namedtuple('Year', ['fiscal', 'academic'])

YEARS = {
    0: Year('2005', '2004/05'),
    1: Year('2006', '2005/06'),
    2: Year('2007', '2006/07'),
    3: Year('2008', '2007/08'),
    4: Year('2009', '2008/09'),
    5: Year('2010', '2009/10'),
    6: Year('2011', '2010/11'),
    7: Year('2012', '2011/12'),
    8: Year('2013', '2012/13'),
    9: Year('2014', '2013/14'),
    10: Year('2015', '2014/15'),
    11: Year('2016', '2015/16'),
    12: Year('2017', '2016/17'),
    13: Year('2018', '2017/18'),
    14: Year('2019', '2018/19'),
}

# Constants
MAX_YEAR_ID = max(YEARS.keys())
MAX_FISCAL_YEAR = YEARS.get(MAX_YEAR_ID).fiscal
MAX_ACADEMIC_YEAR = YEARS.get(MAX_YEAR_ID).academic


def make_academic_year_range(start, end):
    """
    Args:
        start (int): ID of the start year
        end (int): ID of the end year

    Returns:
        list: Returns a list of academic year (e.g. ['2018/19', '2019/20'])
    """

    out = []
    for i in range(start, end + 1):
        out.append(YEARS.get(i).academic)

    return out


if __name__ == "__main__":
    print(make_academic_year_range(0, 14))
