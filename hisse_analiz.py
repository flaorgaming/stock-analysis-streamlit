import streamlit as st
import pandas as pd
from helper_hisse_analiz import listeyi_guncelle, get_stock_data, get_historical_prices

st.title('Hisse Analizi Web Uygulaması')

selected_stocks = st.multiselect('Analiz etmek istediğiniz hisse kodlarını seçiniz'.title(), listeyi_guncelle().index)

if selected_stocks:
    result_df = pd.DataFrame(columns=['Stock', 'Open', 'High', 'Low', 'Close', 'Change'])
    st.toast('Veriler aranıyor!')

    for s in selected_stocks:
        result_df = pd.concat([result_df, get_stock_data(s)], ignore_index=True)
        st.toast('Veri güncel dataları indiriliyor!')
    st.subheader('seçilen hisse fiyatları ve son 1 ay kapanış grafiği'.title())

    st.dataframe(result_df)

    st.subheader('Grafikler')

    historical_prices = {}
    for s in selected_stocks:
        st.toast('Geçmiş fiyatlar çekiliyor!')
        historical_prices[s] = get_historical_prices(s)

    st.toast('Tamamlandı!')
    historical_prices_df = pd.DataFrame(historical_prices)
    st.line_chart(historical_prices_df)
