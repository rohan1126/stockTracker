# app.py
from flask import Flask, render_template, request, redirect, url_for
from utils import create_table, get_live_info, get_news, add_stock_to_db, clear_stocks_in_db

import sqlite3
import finnhub
app = Flask(__name__)

DATABASE = "stocks.db"

create_table()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stocks')
    stocks = cursor.fetchall()

    live_stock_prices = []
    for stock in stocks:
        symbol = stock[1]
        close_price, current_price, logo, color, buy_values, sell_values, stock_link = get_live_info(symbol)
        live_stock_prices.append({'symbol': symbol, 'close_price': close_price, 'current_price': current_price, 'color': color,
                                  'logo':logo, 'buy_values': buy_values, 'sell_values':sell_values,'stock_link':stock_link })

    news_headlines = get_news()
    conn.close()

    return render_template('index.html', live_stock_prices=live_stock_prices, news_headlines=news_headlines)



@app.route('/add_stock', methods=['POST'])
def add_stock():
    if request.method == 'POST':
        symbol = request.form['symbol']
        add_stock_to_db(symbol)
        return redirect(url_for('index'))

@app.route('/clear_stocks', methods=['GET', 'POST'])
def clear_stocks():
    if request.method == 'POST':
        clear_stocks_in_db()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/remove_stock/<symbol>', methods=['GET', 'POST'])
def remove_stock(symbol):
    print('Removing stock:', symbol)
    if request.method == 'POST':
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM stocks WHERE symbol = ?', (symbol,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

