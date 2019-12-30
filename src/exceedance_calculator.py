__author__ = 'Dror Paz, ClimaCell inc.'
__createdOn__ = '2019/12/26'

import logging
import pandas as pd
from typing import Dict

warning_levels_mapping = pd.Series({1:50, 2:20, 3:10, 4:5, 5:2})


def calc_exceedance(value: float, exceedance_mapping: pd.Series) -> int:
    '''
    Find exceedance probability of discharge value
    :param value: discharge value
    :param exceedance_mapping: probability-discharge series
    :return: exceedance percent (0-100)
    '''
    min_exceedance = 0  # minimum possible exceedance probability
    max_exceedance = 100  # maximum supported exceedance probability
    # very small rain events.
    exactmatch = exceedance_mapping[exceedance_mapping == value]
    if not exactmatch.empty:
        exceedance = exactmatch.index[0]
    elif value > exceedance_mapping.max():
        logging.debug(
            f'Discharge of ({value:0.0f} m^3/s) exceeds expected values ({exceedance_mapping.max():0.0f} m^3/s). '
            f'setting probability of exceedance to {min_exceedance}')
        exceedance = min_exceedance
    elif value < exceedance_mapping.min():
        logging.debug(f'Discharge ({value} m^3/s) is below min expected value ({exceedance_mapping.min()} m^3/s). '
                      f'setting probability of exceedance to {max_exceedance}')
        exceedance = max_exceedance
    else:
        lowerneighbour_ind = (exceedance_mapping[exceedance_mapping < value]).idxmax()
        upperneighbour_ind = exceedance_mapping[exceedance_mapping > value].idxmin()
        exceedance_m = (upperneighbour_ind - lowerneighbour_ind) / \
                       (exceedance_mapping[upperneighbour_ind] - exceedance_mapping[lowerneighbour_ind])
        exceedance_n = upperneighbour_ind - (exceedance_mapping[upperneighbour_ind] * exceedance_m)
        exceedance = value * exceedance_m + exceedance_n
        logging.debug('Probability of exceedance is %d' % exceedance)
    return exceedance


def get_warning_level(series: pd.Series, value: float) -> int:
    '''
    This function is meant for use with exceedance<->warning_level series.
    Example:
    >>> pd.Series([100,50,20,4,1], index=[1,2,3,4,5])
    :param series: pd.Series(data=[exceedance_probabilities], index=[warning_values])
    :param value: exceedance value
    :return: warning level
    '''
    if value == 100:
        level = 0
    elif value in series.values:
        level = int(series[series == value].index[0])
    elif series.min() > value:
        level = int(series.idxmin()) + 1
    else:
        ind = series[series < value].index.min()
        level = int(ind)
    return level

def multiple_values_to_level(discharges: pd.Series, exceedance_values: pd.DataFrame,
                             warning_levels_mapping: pd.Series = warning_levels_mapping) -> Dict:
    '''
    Calculate warning levels for a series of discharge values at stations
    :param discharges: A series with dischatges for values and station_ids for index
    :param exceedance_values: A frame with 
    :param stations_warning_levels:
    :return:
    '''
    stations_warning_levels = {}
    for stn_id, discharge in discharges.items():
        if stn_id not in exceedance_values.columns:
            logging.error(f'Could not find exceedance values for station <{stn_id}>')
            continue
        station_exceedance_values = exceedance_values[stn_id]
        exceedanxce = calc_exceedance(discharge, station_exceedance_values)
        warning_level = get_warning_level(warning_levels_mapping, exceedanxce)
        stations_warning_levels[stn_id] = warning_level
    return stations_warning_levels

def read_exceedance_mapping(filename: str) -> pd.DataFrame:
    '''read exceedance mapping from CSV
    staions id column must be named "stn_id"
    exceedance columns must follow the rule "[0-9]_percent"
    other columns will be ignored'''
    logging.debug(f'Loading {filename}')
    index_col_name = 'stn_id'
    exceedance_suffix = '_percent'
    df = pd.read_csv(filename, index_col=index_col_name).T
    exceedance_rows = [x.rstrip(exceedance_suffix).isnumeric() for x in df.index]
    df = df.loc[exceedance_rows, :]
    df.index = [int(x.rstrip(exceedance_suffix)) for x in df.index]
    try:
        df = df.astype(float)
    except ValueError:
        raise ValueError(f'Non numeric value found in exceedance mapping file <{filename}>')
    return df
