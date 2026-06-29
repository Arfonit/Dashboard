import streamlit as st
from api import api
        
def create_project_form(project=None, prefix=""):
    
    # Инициализация session_state
    if 'companies_list' not in st.session_state:
        st.session_state.companies_list = [
            row["company_name"] for row in api.get_all_companies()
        ]
        
    if 'project_types' not in st.session_state:
        st.session_state.project_types = [
            row["project_type"] for row in api.get_all_project_types()
        ]      
        

    default_company = project["company_name"]
    default_companies_index = st.session_state.companies_list.index(default_company) if default_company in st.session_state.companies_list else 0

    

    default_project_type = project["project_type"]
    default_project_index = st.session_state.project_types.index(default_project_type) if default_project_type in st.session_state.project_types else 0

        
    project_date = st.date_input(
        "Дата проекта",
        value = project["project_date"],
        key=f"{prefix}_project_date_{project['unique_project_key']}"
        
    )
    
    company = st.selectbox(
        "Компания",
        options=st.session_state.companies_list,
        index=default_companies_index,
        accept_new_options= True,
        #on_change = update_companies(project,prefix),
        key=f"{prefix}_company_{project['unique_project_key']}"
    )

    ptype = st.selectbox(
        "Тип проекта",
        options = st.session_state.project_types,
        index = default_project_index,
        accept_new_options=True,
        key=f"{prefix}_project_type_{project['unique_project_key']}"
    )

    comment = st.text_area(
        "Комментарий",
        value=project["comment"],
        key=f"{prefix}_comment_{project['unique_project_key']}"
    )

    budget = st.number_input(
        "Бюджет",
        value=float(project["project_budjet"]),
        key=f"{prefix}_project_budjet_{project['unique_project_key']}"
    )

    payment = st.number_input(
        "Оплачено",
        value=float(project["fact_payment"]),
        key=f"{prefix}_fact_payment_{project['unique_project_key']}"
    )

    hour_price = st.number_input(
        "Стоимость часа",
        value=float(project["extra_work_price"]),
        key=f"{prefix}_extra_work_price_{project['unique_project_key']}"
    )

    hours = st.number_input(
        "Часы",
        value=float(project["extra_work_hours"]),
        key=f"{prefix}_extra_work_hours_{project['unique_project_key']}"
    )
    
    return {
        "project_date": project_date,
        "company_name": company,
        "project_type": ptype,
        "comment": comment,
        "project_budjet": budget,
        "extra_work_price": hour_price,
        "extra_work_hours": hours,
        "fact_payment": payment
    }
  
def edit_form(project=None, prefix= ""):
    
    return create_project_form(project, prefix)
   
    
def new_project_form(project=None, prefix= ""):
    
   return create_project_form(project, prefix)
    
    
