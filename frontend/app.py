import streamlit as st
#streamlit run app.py


st.set_page_config(
    layout="wide"  # Включает полноэкранный режим
)

pg = st.navigation([st.Page("pages/Finance.py"), st.Page("pages/Projects.py"), st.Page("pages/Project_types.py")])
pg.run()

