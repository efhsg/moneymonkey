import streamlit as st
from injector import get_config

# Load configuration
config = get_config()


def main():
    """Main entry point for the Streamlit app."""
    home_page()


def home_page():
    """Displays the main content of the home page with title and logo alignment."""
    # Create a two-column layout for the title and logo
    title_col, logo_col = st.columns([3, 1])

    # Place title in the left column
    with title_col:
        st.title("MoneyMonkey")

    # Place logo in the right column
    with logo_col:
        logo_path = getattr(config, "logo_small_path", None)
        if logo_path:
            st.image(logo_path, width=120)
        else:
            st.write("Logo not available")

    # Main content section
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


if __name__ == "__main__":
    main()
