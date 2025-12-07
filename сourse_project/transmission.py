import re
import numpy as np
import pandas as pd


def classify_transmission_simple(transmission):
    if pd.isna(transmission):
        return 'Unknown'

    transmission = str(transmission).upper()

    # Паттерны для автоматической трансмиссии
    auto_patterns = [
        r'.*АКП.*', r'.*АТ.*', r'.*A[ТT].*', r'.*CVT.*', r'.*DCT.*',
        r'.*DSG.*', r'.*TIPTRONIC.*', r'.*STEPTRONIC.*', r'.*PDK.*',
        r'.*AUTOMATIC.*', r'.*A/T.*', r'.*ВАРИАТОР.*', r'.*AMT.*',
        r'^\d+[АТA]$', r'^\d+[АТA].*', r'.*TRONIC.*'
    ]

    # Паттерны для механической трансмиссии
    manual_patterns = [
        r'.*МКП.*', r'.*МТ.*', r'.*M[ТT].*', r'.*M/T.*', r'.*МЕХ.*',
        r'.*MANUAL.*', r'^\d+[МMТT]$', r'^\d+[МMТT].*'
    ]

    # Проверяем паттерны
    for pattern in auto_patterns:
        if re.match(pattern, transmission, re.IGNORECASE):
            return 'Автомат'

    for pattern in manual_patterns:
        if re.match(pattern, transmission, re.IGNORECASE):
            return 'Механика'

    return 'Unknown'