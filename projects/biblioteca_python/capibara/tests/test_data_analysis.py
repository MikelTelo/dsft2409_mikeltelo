import pytest
import pandas as pd
import numpy as np
from capibara.data_analysis import (
    filter_rows,
    remove_outliers,
    basic_data_analysis,
    outlier_meanSd,
    data_report,
    missing_values_summary
)

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'A': [1, 2, 3, 100, 4, 5],
        'B': ['x', 'y', 'z', 'x', 'y', 'z'],
        'C': [10, 20, np.nan, 40, 50, np.nan]
    })

def test_filter_rows(sample_df):
    result = filter_rows(sample_df, {'B': 'x'})
    assert len(result) == 2
    assert all(result['B'] == 'x')

def test_remove_outliers(sample_df):
    result = remove_outliers(sample_df, ['A'])
    assert len(result) == 5  # Should remove the value 100
    assert 100 not in result['A'].values

def test_basic_data_analysis(sample_df):
    result = basic_data_analysis(sample_df)
    assert isinstance(result, dict)
    assert 'shape' in result
    assert 'dtypes' in result
    assert 'missing_values' in result

def test_outlier_meanSd(sample_df):
    result = outlier_meanSd(sample_df, 'A')
    assert isinstance(result, pd.Series)
    assert result.dtype == bool

def test_data_report(sample_df):
    result = data_report(sample_df)
    assert isinstance(result, dict)
    assert 'basic_info' in result
    assert 'column_info' in result

def test_missing_values_summary(sample_df):
    result = missing_values_summary(sample_df)
    assert isinstance(result, list)
    assert len(result) == 3  # Number of columns 