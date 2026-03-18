import pandas as pd
from datetime import datetime
import streamlit as st

def add_log_entry(question: str, model: str, response: str):
    """
    Appends a Q&A entry to the session_state log.
    """
    # Initialize the log in session_state if it doesn't exist
    if 'log' not in st.session_state:
        st.session_state.log = []

    st.session_state.log.append({
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Question": question,
        "Model": model,
        "Response": response,
    })

def get_export_dataframe() -> pd.DataFrame:
    """
    Retrieves the session log as a Pandas DataFrame.
    """
    if 'log' in st.session_state and st.session_state.log:
        return pd.DataFrame(st.session_state.log)
    
    # Return an empty DataFrame with correct columns if the log is empty
    return pd.DataFrame(columns=["Timestamp", "Question", "Model", "Response"])
