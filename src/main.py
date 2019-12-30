__author__ = 'Dror Paz, ClimaCell inc.'
__createdOn__ = '2019/12/30'

import logging
import pandas as pd
from exceedance_calculator import multiple_values_to_level, read_exceedance_mapping
from typing import Dict, Any


def exceedance_calculator(exceedances_filename: str, discharges: pd.Series) -> Dict[Any, int]:
    '''
    Calculate warning levels for stations
    :param exceedances_filename:filename containing exceedance probabilities for discharge values.
    :param discharges: A series of discharge values for stations.
    :return: A dictionary with stations ids for keys and warning levels for values.
    '''
    logging.info(f'Staring exceedance calculator with for {len(discharges)} stations')
    exceedance_mapping = read_exceedance_mapping(exceedances_filename)
    warning_levels = multiple_values_to_level(discharges=discharges, exceedance_values=exceedance_mapping)
    logging.info(f'Finished exceedance calculator for {len(warning_levels)} stations')
    return warning_levels
