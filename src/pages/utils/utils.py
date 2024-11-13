import streamlit as st
from PIL import Image
from injector import get_config, get_logger

config = get_config()
logger = get_logger()

image = Image.open(config.icon_path)


def setup_page(page_title="MoneyMonkey"):
    st.set_page_config(
        page_title=page_title,
        page_icon=image,
        layout="wide",
        initial_sidebar_state="auto",
    )


def show_messages():
    message, message_type = st.session_state["message"]
    if message:
        if message_type == "success":
            st.success(message)
        elif message_type == "error":
            st.error(message)
        st.session_state["message"] = (None, None)
