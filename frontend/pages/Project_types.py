import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from api import api

# Выбор типа диаграммы
chart_type = st.selectbox(
    "Выберите тип диаграммы",
    [
        "🌞 Солнечная диаграмма",
        "🌳 Древовидная карта",
        "🌊 Диаграмма Санкея",
        "📊 Параллельные координаты",
        "🎯 Матрица рассеяния",
        "🕸️ Лепестковая диаграмма",
        "🎲 3D анализ"
    ]
)

df = pd.DataFrame(api.get_dashboard_main()).copy()

if chart_type == "🌞 Солнечная диаграмма":
    fig = px.sunburst(
        df,
        path=['company_name', 'project_type', 'unique_project_key'],
        values='project_budjet',
        color='percent_paid',
        color_continuous_scale='Viridis',
        title='Иерархия проектов'
    )
    
elif chart_type == "🌳 Древовидная карта":
    fig = px.treemap(
        df,
        path=['company_name', 'project_type'],
        values='project_budjet',
        color='fact_payment',
        color_continuous_scale='RdBu',
        title='Структура проектов'
    )
    
elif chart_type == "🌊 Диаграмма Санкея":
    
    # Подготовка данных для Sankey
    companies = df['company_name'].unique().tolist()
    project_types = df['project_type'].unique().tolist()

    # Создаем узлы (все компании + все типы проектов)
    all_nodes = companies + project_types + ['Проекты']

    # Индексы для узлов
    company_indices = {comp: i for i, comp in enumerate(companies)}
    type_indices = {ptype: i + len(companies) for i, ptype in enumerate(project_types)}
    project_index = len(companies) + len(project_types)

    # Создаем связи
    links = []
    for company in companies:
        company_df = df[df['company_name'] == company]
        company_sum = company_df['project_budjet'].sum()
        links.append({
            'source': company_indices[company],
            'target': project_index,
            'value': company_sum,
            'label': f'{company} → Все проекты'
        })

    # Добавляем связи от типов проектов
    for ptype in project_types:
        type_df = df[df['project_type'] == ptype]
        type_sum = type_df['project_budjet'].sum()
        links.append({
            'source': type_indices[ptype],
            'target': project_index,
            'value': type_sum,
            'label': f'{ptype} → Все проекты'
        })

    # Создаем диаграмму
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color="blue"
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
            label=[link['label'] for link in links]
        )
    )])

    fig.update_layout(
        title="💰 Потоки бюджета по компаниям и типам проектов",
        font=dict(color='white', size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        height=600
    )

    #st.plotly_chart(fig, width='stretch')
    
elif chart_type == "📊 Параллельные координаты":
    fig = px.parallel_coordinates(
        df,
        dimensions=['project_budjet', 'fact_payment', 'extra_work_price', 'percent_paid'],
        color='project_budjet',
        color_continuous_scale=px.colors.diverging.RdBu
    )
    
elif chart_type == "🎯 Матрица рассеяния":
    fig = px.scatter_matrix(
        df,
        dimensions=['project_budjet', 'fact_payment', 'extra_work_price', 'total_extra_pay', 'percent_paid'],
        color='company_name'
    )
    
elif chart_type == "🕸️ Лепестковая диаграмма":
    # Выбираем топ-5 проектов по бюджету
    top_projects = df.nlargest(5, 'project_budjet')

    categories = ['Бюджет', 'Оплачено', '% оплаты', 'Доп. работы', 'Доп. оплата']

    fig = go.Figure()

    for _, project in top_projects.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[
                project['project_budjet'] / 1000,  # в тысячах
                project['fact_payment'] / 1000,
                project['percent_paid'] * 100,
                project['extra_work_price'] / 1000,
                project['total_extra_pay'] / 1000
            ],
            theta=categories,
            fill='toself',
            name=project['unique_project_key'][:8],  # первые 8 символов ID
            hovertemplate='<b>%{theta}</b>: %{r:,.0f}<extra></extra>'
        ))
    
else:  # 3D анализ
    fig = px.scatter_3d(
        df,
        x='project_budjet',
        y='fact_payment',
        z='extra_work_price',
        color='company_name',
        size='percent_paid'
    )

# Общий стиль для всех диаграмм
fig.update_layout(
    template='plotly_dark',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', size=12),
    height=700
)

# Отображение в стилизованном контейнере
total_sum = df['project_budjet'].sum()
bg_gradient = "linear-gradient(135deg, #2d8653 0%, #4CAF50 100%)"

st.markdown(f"""
    <div style="
        background: {bg_gradient};
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        ">
            <div style="color: white; font-size: 18px; font-weight: 600;">
                {chart_type}
            </div>
            <div style="
                color: white;
                font-size: 20px;
                font-weight: 700;
                background: rgba(255,255,255,0.15);
                padding: 5px 20px;
                border-radius: 10px;
            ">
                Всего: {total_sum:,.0f} ₽
            </div>
        </div>
""", unsafe_allow_html=True)

st.plotly_chart(fig, width='stretch')

st.markdown("</div>", unsafe_allow_html=True)