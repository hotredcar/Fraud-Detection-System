# import modules
import sys
import streamlit as st
import time
import numpy as np
from pathlib import Path
import pandas as pd


# import modules
sys.path.append(Path.cwd().parent)
from proj_modules import *

# ----------------------------------------------------------------------------------------------------------------
# session state variables
# ----------------------------------------------------------------------------------------------------------------

if 'users_csv_loaded' not in st.session_state:
    st.session_state.users_csv_loaded = False

if 'cards_csv_loaded' not in st.session_state:
    st.session_state.cards_csv_loaded = False

if 'transactions_csv_loaded' not in st.session_state:
    st.session_state.transactions_csv_loaded = False

if 'users_df' not in st.session_state:
    st.session_state.users_df = pd.DataFrame()

if 'cards_df' not in st.session_state:
    st.session_state.cards_df = pd.DataFrame()

if 'transactions_df' not in st.session_state:
    st.session_state.transactions_df = pd.DataFrame()


# ****************************************************************************************************************
# ----------------------------------------------------------------------------------------------------------------
# setup page
# ----------------------------------------------------------------------------------------------------------------


st.set_page_config(page_title="Raw Data from Kaggle", 
                   page_icon="ℹ️")

# ----------------------------------------------------------------------------------------------------------------
# page content
# ----------------------------------------------------------------------------------------------------------------

st.markdown("# Data Load")
st.sidebar.header("Data Load")

# ----------------------------------------------------------------------------------------------------------------
# Section Introduction
# ----------------------------------------------------------------------------------------------------------------

st.markdown(
    """ 
    
    Here we walk through the various steps used to load and clean the data. Kaggle provides 3 major synthetic tables:
    - `sd254_users.csv`: Credit card holders
    - `sd254_cards.csv`: Credit cards
    - `credit_card_transactions-ibm_v2.csv`: Transactions


    ## Credit Card holders

    """
)


# ----------------------------------------------------------------------------------------------------------------
# Sidebar 
# ----------------------------------------------------------------------------------------------------------------


users_file = st.sidebar.file_uploader("Load Credit Card Users CSV",
                                      type="csv")
if users_file:
    st.session_state.users_csv_loaded = True

cards_file = st.sidebar.file_uploader("Load Credit Card Details CSV",
                                      type="csv")
if cards_file:
    st.session_state.cards_csv_loaded = True

transactions_file = st.sidebar.file_uploader("Load Transactions CSV",
                                      type="csv")
if transactions_file:
    st.session_state.transactions_csv_loaded = True


# ----------------------------------------------------------------------------------------------------------------
# Tabs
# ----------------------------------------------------------------------------------------------------------------

# set the tabs
tab_users, tab_cards, tab_transactions = st.tabs(["Credit Card Users", "Credit Card Details", "Credit Card Transactions"])

# ----------------------------------------------------------------------------------------------------------------

with tab_users:
    # Before
    # load the sample users csv
    st.markdown("""
    ### The raw csv contents 
                
    The uploaded credit card user file should look like:
    """
    )
    sample_users_path = Path.cwd() / 'data/sample_users.csv'

    sample_users_df = pd.read_csv(sample_users_path)

    st.dataframe(sample_users_df.head())

    st.markdown("""
    On the import, there is an opportunity to choose specific columns to load. 
    The columns we have decided to keep in this dataframe are:
    - 'Birth Year', 
    - 'Zipcode', 
    - 'Per Capita Income - Zipcode',
    - 'Yearly Income - Person', 
    - 'Total Debt',
    - 'FICO Score',
    - 'Num Credit Cards'
    
    On the import, we have preprocessed some of the columns and removed the '$' from appropriate columns and converted them into integers.
    """
    )

    load_users_button = st.button("Click to transform credit card users",
                                  disabled = not st.session_state.users_csv_loaded 
                                  )
    if load_users_button:
        users_columns_import = ['Birth Year', 
                            'Zipcode', 
                            'Per Capita Income - Zipcode',
                            'Yearly Income - Person', 
                            'Total Debt',
                            'FICO Score',
                            'Num Credit Cards']

        user_converters = {'Zipcode': add_leading_zero_to_zipcode,
                        'Per Capita Income - Zipcode': remove_dollar_and_convert,
                        'Yearly Income - Person': remove_dollar_and_convert,
                        'Total Debt': remove_dollar_and_convert}

        users_dtypes = {'Birth Year': np.uint16,
                        'FICO Score': np.uint16,
                        'Num Credit Cards': np.uint8}
        
        # load data
        users_df = load_csv_data(users_file,
                                 users_columns_import,
                                 user_converters,
                                 users_dtypes)
        
        st.session_state.users_df = users_df

        st.markdown("### Loaded and Cleansed Users Dataframe")    
        st.dataframe(st.session_state.head())



# ----------------------------------------------------------------------------------------------------------------
with tab_cards:
    # Before
    # load the sample users csv
    st.markdown("""
    ### The raw csv contents 
                
    The uploaded credit card details file should look like:
    """
    )
    sample_cards_path = Path.cwd() / 'data/sample_cards.csv'

    sample_cards_df = pd.read_csv(sample_cards_path)

    st.dataframe(sample_cards_df.head())


    st.markdown("""
    On the import, there is an opportunity to choose specific columns to load. 
    The columns we have decided to keep in this dataframe are:
    - 'User',	
    - 'CARD INDEX',
    - 'Has Chip',
    - 'Cards Issued',
    - 'Year PIN last Changed',
    - 'Card on Dark Web'
    
    On the import, we have preprocessed some of the columns that contain 'Yes' or 'No' categories into the binary 1 or 0.
    """
    )

    load_cards_button = st.button("Click to transform credit card details",
                                  disabled = not st.session_state.cards_csv_loaded 
                                  )
    
    if load_cards_button:
        cards_columns_import = ['User',	
                                'CARD INDEX',
                                'Has Chip',
                                'Cards Issued',
                                'Year PIN last Changed',
                                'Card on Dark Web'
                                ]

        cards_dtypes = {'CARD INDEX': np.uint8,
                        'Cards Issued': np.uint8,
                        'Year PIN last Changed': np.uint16
                        }

        cards_conversions = {'Card on Dark Web': convert_yes_no_to_binary,
                            'Has Chip': convert_yes_no_to_binary}
        
        # load data
        cards_df = load_csv_data(cards_file,
                                 cards_columns_import,
                                 cards_conversions,
                                 cards_dtypes)
        
        st.session_state.cards_df = cards_df

        
        st.markdown("### Loaded and Cleansed Credit Cards Dataframe")    
        st.dataframe(st.session_state.cards_df.head())



# ----------------------------------------------------------------------------------------------------------------

with tab_transactions:
    # Before
    # load the sample users csv
    st.markdown("""
    ### The raw csv contents 
                
    The uploaded transaction details file should look like:
    """
    )
    sample_transactions_path = Path.cwd() / 'data/sample_transactions.csv'

    sample_transactions_df = pd.read_csv(sample_transactions_path)

    st.dataframe(sample_transactions_df.head())


    st.markdown("""
    On the import, there is an opportunity to choose specific columns to load. 
    The columns we have decided to keep in this dataframe are:
    - 'User',
    - 'Card',
    - 'Year',
    - 'Month',
    - 'Day',
    - 'Time',
    - 'Amount',
    - 'Use Chip',
    - 'Merchant City',
    - 'Merchant State',
    - 'Zip',
    - 'MCC',
    - 'Errors?',
    - 'Is Fraud?':  Target variable
    
    On the import, we have preprocessed some of the columns and removed the '$' from the 'Amount' column and converted it into a float. Additionally
    """
    )

    load_transactions_button = st.button("Click to transform transaction details",
                                  disabled = not st.session_state.transaction_csv_loaded 
                                  )
    
    if load_transactions_button:
        transactions_columns_import = ['User',
                                    'Card',
                                    'Year',
                                    'Month',
                                    'Day',
                                    'Time',
                                    'Amount',
                                    'Use Chip',
                                    'Merchant City',
                                    'Merchant State',
                                    'Zip',
                                    'MCC',
                                    'Errors?',
                                    'Is Fraud?'
                                    ]

        transaction_converters = {'Zip': add_leading_zero_to_zipcode,
                                'Amount': remove_dollar_and_convert_float,
                                'Is Fraud?': convert_yes_no_to_binary
                                }
        
        transaction_dtypes = {'Use Chip': 'category',
                              'Merchant State': 'category',
        }
        
        # load data
        cards_df = load_csv_data(cards_file,
                                 cards_columns_import,
                                 cards_conversions,
                                 cards_dtypes
                                 )
        
        st.session_state.cards_df = cards_df

        
        st.markdown("### Loaded and Cleansed Credit Cards Dataframe")    
        st.dataframe(st.session_state.cards_df.head())



# ----------------------------------------------------------------------------------------------------------------