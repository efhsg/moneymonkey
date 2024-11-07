import streamlit as st
from injector import get_config


def main():
    home_page()


config = get_config()


def home_page():
    st.title("MoneyMonkey")
    col1, col2 = st.columns([2, 1])

    with col1:

        st.subheader("Your Automated Stocks Advisor")
        st.write(
            """
            MoneyMonkey will help you to automate fundamental analysis of your stocks.
            On an individual level a buy, hold or sell advice, based on a fundamental analysis.
            It will also help you to rebalance your current portfolio.
            """
        )

    with col2:
        st.image(config.logo_small_path, width=200)


if __name__ == "__main__":
    main()
