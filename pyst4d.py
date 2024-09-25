import streamlit as st
import requests
import pandas as pd

st.title('Last Day Total Volume from CoinGecko')

def get_top_500_pairs_by_volume():
    all_data = []
    for page in range(1, 6):  # Loop through 5 pages to get 500 coins
        try:
            url = 'https://api.coingecko.com/api/v3/coins/markets'
            params = {
                'vs_currency': 'usd',
                'order': 'volume_desc',
                'per_page': 100,  # 100 coins per page
                'page': page
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                coins = response.json()
                all_data.extend(coins)  # Append data from all pages
            else:
                st.error('Failed to fetch data from CoinGecko API')
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching pairs from CoinGecko: {e}")
            return pd.DataFrame()

    # Create DataFrame from all collected data (500 coins)
    df = pd.DataFrame(all_data)
    df.loc[:, 'symbol'] = df['symbol'].str.upper()  # Convert symbols to uppercase
    df.rename(columns={'total_volume': 'Total Volume in USD'}, inplace=True)  # Rename the column
    return df[['symbol', 'Total Volume in USD']]

# Get the top 500 pairs by volume
pairs_df = get_top_500_pairs_by_volume()

# Style the DataFrame with pandas to center the text and format the numbers
styled_df = pairs_df.style.format({'Total Volume in USD': '{:,.2f}'}).set_properties(**{
    'text-align': 'center'
}).set_table_styles([{
    'selector': 'th',
    'props': [('text-align', 'center')]
}])

# Display styled DataFrame using st.dataframe() for interactivity
st.dataframe(styled_df)
