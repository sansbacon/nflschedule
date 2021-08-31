# nflschedule/nflschedule/csvreader.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

import csv
from typing import Any, Dict, List


def read_csv(fn: str) -> List[Dict[str, Any]]:
    """Provides a basic replacement for pandas.read_csv

    Args:
        fn (file-like): the csv file

    Returns:
        List[Dict[str, Any]]

    """
    with open(fn) as f:
        return [
            {k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)
        ]
