import pytest
import pandas as pd
import numpy as np
from capibara.data_analysis import (
    filter_rows,
    remove_outliers,
    missing_values_summary
)
from capibara.data_processing import (
    create_dummies,
    fill_zeros_with_mean,
    fill_nans_with_mean
)

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'A': [1, 2, 3, 0, 5],
        'B': [10, 20, np.nan, 40, 50],
        'C': ['x', 'y', 'x', 'z', 'y']
    })

def test_filter_rows(sample_df):
    """Test the filter_rows function."""
    result = filter_rows(sample_df, 'A > 2')
    assert len(result) == 2
    assert all(result['A'] > 2)

def test_remove_outliers(sample_df):
    """Test the remove_outliers function."""
    result = remove_outliers(sample_df, 'A')
    assert len(result) <= len(sample_df)

def test_missing_values_summary(sample_df):
    """Test the missing_values_summary function."""
    result = missing_values_summary(sample_df)
    assert 'Missing Values' in result.columns
    assert 'Percentage' in result.columns
    assert result.loc['B', 'Missing Values'] == 1

def test_create_dummies(sample_df):
    """Test the create_dummies function."""
    result = create_dummies(sample_df)
    assert 'C_x' in result.columns
    assert 'C_y' in result.columns
    assert 'C_z' in result.columns

def test_fill_zeros_with_mean(sample_df):
    """Test the fill_zeros_with_mean function."""
    result = fill_zeros_with_mean(sample_df, 'A')
    assert 0 not in result['A'].values

def test_fill_nans_with_mean(sample_df):
    """Test the fill_nans_with_mean function."""
    result = fill_nans_with_mean(sample_df, 'B')
    assert not result['B'].isnull().any() 