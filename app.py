import streamlit as st
from query_runner import run_query

st.title("Olist Data Assistant")
st.caption("For now, type SQL by hand. The LLM comes later.")

if "history" not in st.session_state:
    st.session_state.history = []

sql = st.chat_input("Type a SELECT query...")
if sql:
    df, err = run_query(sql)
    st.session_state.history.append((sql, df, err))

for sql, df, err in st.session_state.history:
    with st.chat_message("user"):
        st.code(sql, language="sql")
    with st.chat_message("assistant"):
        if err:
            st.error(err)
        else:
            st.dataframe(df)