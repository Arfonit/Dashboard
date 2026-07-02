from api import api
import streamlit as st
from Forms import edit_form, new_project_form
import pandas as pd
import time



st.title("Финансы Хрюндельнессы", text_alignment="center")

df = pd.DataFrame(api.get_dashboard_main())
st.dataframe(df, hide_index=True)


#Неоплаченные проекты
unpaid_projects = api.get_unpaid_projects()
df_unpaid_projects = pd.DataFrame(unpaid_projects)

if len(df_unpaid_projects)>0:
    st.header('Unpaid projects', text_alignment="center")
    st.dataframe(df_unpaid_projects, hide_index=True)
    
# Инициализация
if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False

if 'overlay_message' not in st.session_state:
    st.session_state.overlay_message = ""

# CSS для заглушки
def show_overlay(message, duration=3):
    """Показывает оверлей с сообщением на указанное время"""
    st.markdown(f"""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    ">
        <div style="
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="color: #4CAF50;">{message}</h2>
            <p>Страница обновится через {duration} секунд...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


tab1, tab2 = st.tabs(["Редактирование проекта", "Добавление нового"])

with tab1:
    st.write("Редактирование проекта")


    project_id = st.selectbox(
    "Выберите проект",
    df["unique_project_key"],
    key="edit_project"
    )
    
    project = api.get_project(project_id)
    change_type = "edit"

    form = edit_form(project, prefix=change_type)  # Берем первый элемент из списка

    if st.button("Сохранить", key=change_type):  
        api.update_all_project(project_id, 
                                form,
                                change_type)

        st.session_state.show_overlay = True
        st.session_state.overlay_message = "✅ Проект успешно обновлен!"
        st.query_params.update({"saved": "true"})
        st.rerun()
        
    if st.session_state.show_overlay or st.query_params.get("saved") == "true":
        show_overlay(st.session_state.overlay_message, 3)
        # Сбрасываем флаг после показа
        st.session_state.show_overlay = False
        
            # Автоматический редирект через JavaScript
        st.markdown("""
        <script>
            setTimeout(function() {
                window.location.href = window.location.href.split('?')[0];
            }, 3000);
        </script>
        """, unsafe_allow_html=True)
    
with tab2:
    st.write("Добавление нового")
    
    project = api.get_project(project_id)
    change_type="create"
    
    form = new_project_form(project, prefix="create")  # Берем первый элемент из списка

    
    if st.button("Создать проект", key=change_type):
        try:    
            api.update_all_project(project_id, 
                                form,
                                change_type)

            st.toast("✅ Проект успешно добавлен!", icon="🎉")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Ошибка: {str(e)}")
