import streamlit as st
from injector import get_config
from pages.utils.utils import setup_page

# Load configuration
config = get_config()


def main():
    home_page()


def home_page():
    setup_page()
    logo_col, title_col = st.columns([3, 1])

    with logo_col:
        logo_path = getattr(config, "logo_path", None)
        if logo_path:
            st.image(logo_path, width=240)
        else:
            st.write("Logo not available")

    st.subheader("Your Automated Stocks Advisor")
    st.write(
        """
        MoneyMonkey provides automated fundamental analysis to help you make informed stock decisions.
        Get clear buy, hold, or sell advice, and rebalance your portfolio with ease.
        """
    )


if __name__ == "__main__":
    main()
