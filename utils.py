# utils.py
import sqlite3
import finnhub

finnhub_client = finnhub.Client(api_key="cm6dbehr01qg94pu0f7gcm6dbehr01qg94pu0f80")

DATABASE = "stocks.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_live_info(symbol):
    try:
        quote_info = finnhub_client.quote(symbol)
        logoconn = finnhub_client.company_profile2(symbol=symbol)
        recommendcon = finnhub_client.recommendation_trends(symbol)
        close_price = quote_info['pc']
        current_price = quote_info['c']
        logo = logoconn['logo']
        buy_values = recommendcon[0]['buy']
        sell_values = recommendcon[0]['sell']
        stock_link = f"https://www.nasdaq.com/market-activity/stocks/{symbol}"

        color = "#90EE90" if close_price < current_price else "#ffcccb"
        return close_price, current_price, logo, color, buy_values, sell_values, stock_link
    except Exception as e:
        print(f"Error fetching live information for {symbol}: {e}")
        return None, None, None, None, None, None, None
def get_news():
    headlines = []
    conn = finnhub_client.general_news('general', min_id=0)
    if conn:
        for i in range(0, 9):
            headline = conn[i]['headline']
            url = conn[i]['url']
            image = conn[i]['image']
            summary = conn[i]['summary']
            headline_with_link = f'<a href="{url}" target="_blank">{headline}</a>'
            headlines.append({"headline": headline_with_link, "image": image, "summary": summary})
    return headlines

def add_stock_to_db(symbol):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the stock already exists in the database
    cursor.execute('SELECT * FROM stocks WHERE symbol = ?', (symbol,))
    existing_stock = cursor.fetchone()

    if existing_stock:
        # Update the existing stock
        cursor.execute('UPDATE stocks SET symbol = ? WHERE id = ?', (symbol, existing_stock[0]))
    else:
        # Add a new stock if it doesn't exist
        cursor.execute('INSERT INTO stocks (symbol) VALUES (?)', (symbol,))

    conn.commit()
    conn.close()

def clear_stocks_in_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM stocks')
    conn.commit()
    conn.close()
