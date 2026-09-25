"""Streamlit entrypoint for Streamlit Community Cloud deployment."""
from medscan_ai import dashboard  # dashboard runs Streamlit UI at import

if __name__ == "__main__":
    # Local launch for convenience
    import streamlit as st
    st.experimental_rerun()
