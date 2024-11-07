# MoneyMonkey


<p align="center">
  <img width="200" height="200" src="https://github.com/efhsg/moneymonkey/blob/master/src/img/logo_3.png">
</p>

MoneyMonkey will help you to automate fundamental analysis of your stocks.
            On an individual level a buy, hold or sell advice, based on a fundamental analysis.
            It will also help you to rebalance your current portfolio.

## Quick start

- **Check out the repository**
  ```
  git clone <repository-url>
  ```
- **Navigate to your local project directory**
  ```
  cd <local project directory>
  ```  
- **Copy the environment variables example file**
  ```
  cp .env.example .env
  ```
- **Set your API keys in the `.env` file**


### Setup using Docker (recommended for ease of use):
  ```
  docker-compose up -d
  ```

### Setup using a virtual environment (for more control):
- Install Python 3.12.1 (we recommend using pyenv)
- Navigate to your local project directory
- Create a virtual environment and activate it
  ```
  python -m venv .venv
  source .venv/bin/activate
  ```
- Upgrade pip and install dependencies
  ```
  pip install --upgrade pip && pip install -r requirements.txt
  ```
- Set environment variables to avoid bytecode generation and to run unbuffered
  ```
  export PYTHONDONTWRITEBYTECODE=1 && export PYTHONUNBUFFERED=1
  ```
- Run the application
  ```
  cd src && streamlit run Main.py
  ```

### To view the app:
- Open your web browser and navigate to `http://localhost:8501/`

Enjoy!
