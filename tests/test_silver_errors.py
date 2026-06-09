import pytest
import pandas as pd
from transform.silver_transformation import basic_cleaning, apply_business_rules, create_perfumes_enriched, create_sales_enriched

def test_basic_cleaning_empty_df():
    """Verifies that basic_cleaning correctly handles an empty DataFrame."""
    df = pd.DataFrame()
    result = basic_cleaning(df, "test_table")
    assert result.empty
    assert isinstance(result, pd.DataFrame)

def test_apply_business_rules_perfumes_negative_price():
    """Verifies that perfumes with prices <= 0 are removed."""
    df = pd.DataFrame({
        'id': [1, 2],
        'name': ['Perfume A', 'Perfume B'],
        'price': [100.0, -50.0]
    })
    result = apply_business_rules(df, "perfumes")
    assert len(result) == 1
    assert result.iloc[0]['name'] == 'Perfume A'

def test_apply_business_rules_customers_invalid_email():
    """Verifies that customers with emails that do not meet the format are filtered."""
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'first_name': ['Juan', 'Pedro', 'Maria'],
        'email': ['juan@gmail.com', 'pedro-malo', 'maria@empresa.com.ar']
    })
    result = apply_business_rules(df, "customers")
    assert len(result) == 2
    assert 'pedro-malo' not in result['email'].values

def test_apply_business_rules_sales_null_ids():
    """Verifies that sales without critical IDs are discarded."""
    df = pd.DataFrame({
        'customer_id': [1, None, 3],
        'perfume_id': [1, 2, None],
        'location_id': [1, 1, 1],
        'quantity': [1, 1, 1]
    })
    result = apply_business_rules(df, "sales")
    assert len(result) == 1

def test_create_perfumes_enriched_empty_df():
    """Verifies it doesn't crash if passed empty DataFrames with correct columns."""
    perfumes_df = pd.DataFrame(columns=['id', 'brand_id', 'name', 'perfume_type', 'size_ml', 'price'])
    brands_df = pd.DataFrame(columns=['id', 'name', 'country'])
    
    result = create_perfumes_enriched(perfumes_df, brands_df)
    assert result.empty
    assert list(result.columns) == ['brand_name', 'name', 'perfume_type', 'size_ml', 'price', 'country']

def test_create_sales_enriched_missing_columns():
    """Verifies it fails if critical columns are missing when enriching sales."""
    sales_df = pd.DataFrame(columns=['id', 'customer_id']) # Almost all missing
    perfumes_df = pd.DataFrame(columns=['id', 'name', 'brand_id', 'price'])
    locations_df = pd.DataFrame(columns=['id', 'name', 'state'])
    customers_df = pd.DataFrame(columns=['id', 'first_name', 'last_name'])
    brands_df = pd.DataFrame(columns=['id', 'name'])
    
    with pytest.raises(KeyError):
        create_sales_enriched(sales_df, perfumes_df, locations_df, customers_df, brands_df)
