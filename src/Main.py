import streamlit as st
from components.database.migration import Migration
from injector import get_config, get_logger
from pages.utils.utils import setup_page

config = get_config()
logger = get_logger()


def main():
    check_db()
    home_page()


def home_page():
    setup_page()
    logo_col, title_col = st.columns([3, 1])

    with logo_col:
        logo_path = getattr(config, "logo_path", None)
        if logo_path:
            st.image(logo_path, width=600)
        else:
            st.write("Logo not available")

    st.subheader("Your Automated Stocks Advisor")
    st.write(
        """
        MoneyMonkey provides automated fundamental analysis to help you make informed stock decisions.
        Get clear buy, hold, or sell advice, and rebalance your portfolio with ease.
        """
    )


def check_db():
    db_manager = Migration(config=config)
    try:
        db_manager.check_and_apply_migrations()
    except Exception as e:
        st.error(f"Database setup failed: {e}")
        st.stop()


if __name__ == "__main__":
    main()
