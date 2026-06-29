import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import calendar
from api import api
import numpy as np

col1_1, col1_2 , col1_3 = st.columns(3)
col2_1, col2_2 , col2_3 = st.columns(3)

 
df_year  = pd.DataFrame(api.get_income_by_year())
total_sum = df_year["total_income"].sum()
dashboard = pd.DataFrame(api.get_dashboard_main())
total_spends = dashboard["total_extra_pay"].sum() + dashboard["project_budjet"].sum()
saldo = total_spends - total_sum
year_range=df_year.iloc[:,0]


def plate_color(bg_gradient,text_color,formatted_sum, Header_name):
    st.markdown(f"""
    <div style="
        background: {bg_gradient};
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    ">
        <div style="
            color: {text_color};
            font-size: 14px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            opacity: 0.9;
            margin-bottom: 10px;
        ">
             {Header_name}
        </div>
        <div style="
            color: {text_color};
            font-size: 48px;
            font-weight: 700;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            letter-spacing: 2px;
        ">
            {formatted_sum.replace(',', ' ')}
        </div>
    </div>
""", unsafe_allow_html=True)
    
def generate_palette(n_colors, palette_type='pastel'):
    """Генерация палитры из n цветов"""
    
    if palette_type == 'pastel':
        # Пастельные тона
        base_colors = px.colors.qualitative.Pastel
        if len(base_colors) >= n_colors:
            return base_colors[:n_colors]
        else:
            # Если нужно больше цветов, повторяем с небольшим сдвигом
            return [base_colors[i % len(base_colors)] for i in range(n_colors)]
    
    elif palette_type == 'bright':
        # Яркие, но приятные цвета
        base_colors = px.colors.qualitative.Bold
        return [base_colors[i % len(base_colors)] for i in range(n_colors)]
    
    elif palette_type == 'sequential':
        # Градиент от одного цвета к другому
        colors = px.colors.sequential.Viridis
        # Берем равномерно распределенные цвета из палитры
        indices = np.linspace(0, len(colors)-1, n_colors).astype(int)
        return [colors[i] for i in indices]
    
    elif palette_type == 'custom_pleasant':
        # Моя любимая комбинация приятных цветов
        pleasant_colors = [
            '#FF6B6B', '#FF9F43', '#FECA57', '#48DBFB', 
            '#0ABDE3', '#10AC84', '#EE5A24', '#5F27CD',
            '#341F97', '#01CBC6', '#FF6FB5', '#8395A7'
        ]
        return pleasant_colors[:n_colors]
    
    return px.colors.qualitative.Plotly[:n_colors]    
    
with col1_1:
    bg_gradient = "linear-gradient(135deg, #2d8f5e 0%, #3aaf7a 100%)"  # приятный зеленый
    text_color = "#ffffff"
    Header_name = "Total income"
    # Форматирование с разделением на разряды
    formatted_sum = f"{total_sum:,.2f}"  # для целых чисел
    # или для чисел с копейками: formatted_sum = f"{total_sum:,.2f}"

    # HTML с CSS стилями
    plate_color(bg_gradient,text_color,formatted_sum,Header_name)
 
with col1_2:
    bg_gradient = "linear-gradient(135deg, #b8860b 0%, #daa520 100%)"  # золотой
    text_color = "#ffffff"
    Header_name = "Total costs"
    # Форматирование с разделением на разряды
    formatted_sum = f"{total_spends:,.2f}"  # для целых чисел
    # или для чисел с копейками: formatted_sum = f"{total_sum:,.2f}"

    # HTML с CSS стилями
    plate_color(bg_gradient,text_color,formatted_sum, Header_name)
    
with col1_3:
    bg_gradient = "linear-gradient(135deg, #8b3a3a 0%, #c0392b 100%)"  # приглушенный красный
    text_color = "#ffffff"
    Header_name = "Saldo"
    # Форматирование с разделением на разряды
    formatted_sum = f"{saldo:,.2f}"  # для целых чисел
    # или для чисел с копейками: formatted_sum = f"{total_sum:,.2f}"

    # HTML с CSS стилями
    plate_color(bg_gradient,text_color,formatted_sum, Header_name)
    

    
with col2_1:
    colors = generate_palette(12, 'pastel')
    
    fig = px.bar(
    df_year,
    x="year",
    y="total_income",
    text="total_income",
    color= 'total_income'
    )

    fig.update_layout(
    xaxis_title=None,
    yaxis_title=None
    )

    fig.update_xaxes(
    type="category"
    )

    fig.update_traces(
        texttemplate="%{y:,.0f}",
        textposition="outside"
    )
    st.header("Annual income", text_alignment="center")
    st.plotly_chart(fig, width="stretch")




with col2_2:
    colors = generate_palette(12, 'pastel')
    st.header("Monthly income by year", text_alignment="center")
    current_year = datetime.now().year
    year = st.selectbox(
        "Select year",
        options=list(year_range)
    ) 
    
    df_monthly = pd.DataFrame(api.get_income_by_month(year))
    df_monthly['month_name']=df_monthly.iloc[:,0].apply(lambda x: calendar.month_name[int(x)])
    fig = px.pie(
            df_monthly,
            names=df_monthly.iloc[:,2],
            values=df_monthly.iloc[:,1],
            color= 'total_income',  # если нужно раскрасить по месяцам
            color_discrete_sequence=colors
            )
    
    df_monthly_new=df_monthly.iloc[:,[2,1]]
    st.dataframe(df_monthly_new, hide_index=True, width="stretch")
    
with col2_3:
    colors = px.colors.diverging.Spectral
    st.plotly_chart(fig, width="stretch")

