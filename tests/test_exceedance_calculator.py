__author__ = 'Dror Paz, ClimaCell inc.'
__createdOn__ = '2019/12/26'

import pandas as pd
from pathlib import Path
import pytest
from src.exceedance_calculator import read_exceedance_mapping, multiple_values_to_level, warning_levels_mapping, \
    get_warning_level, calc_exceedance


@pytest.fixture()
def exceedance_mapping():
    filename = Path(__file__).parent / 'test_exceedances.csv'
    exceedance_mapping = read_exceedance_mapping(filename)
    return exceedance_mapping


def test_read_exceedance_mapping_from_csv(exceedance_mapping):
    assert exceedance_mapping.columns.equals(pd.Index([61000, 60190]))
    assert exceedance_mapping.index.equals(pd.Index([1, 2, 5, 10, 20, 50]))


def test_multiple_values_to_level(exceedance_mapping):
    discharges = pd.Series({61000: 50, 60190: 0})
    expected = {61000: 4, 60190: 0}
    ret = multiple_values_to_level(discharges=discharges, exceedance_values=exceedance_mapping,
                                   warning_levels_mapping=warning_levels_mapping)
    assert expected==ret

def test_calc_exceedance(exceedance_mapping):
    mapping = exceedance_mapping[61000]
    assert pytest.approx(calc_exceedance(220, mapping), 1.5)
    assert pytest.approx(calc_exceedance(0, mapping), 100)

def test_get_warning_level():
    assert get_warning_level(warning_levels_mapping, 100) == 0
    assert get_warning_level(warning_levels_mapping, 60) == 1
    assert get_warning_level(warning_levels_mapping, 30) == 2
    assert get_warning_level(warning_levels_mapping, 1) == 6
