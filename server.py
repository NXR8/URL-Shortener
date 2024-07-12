from flask import Flask, render_template, request, redirect, abort, jsonify
from flask_socketio import SocketIO, send
import random
import string
import sqlite3
import requests

app = Flask(__name__)
socketio = SocketIO(app)

# Database setup function
def get_db_connection():
    conn = sqlite3.connect('url_shortener.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page route
@app.route('/')
def index():
    return render_template('shorten_url.html')

# URL shortening route
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['original_url'].lower()
    if not original_url.startswith("http://") and not original_url.startswith("https://"):
        original_url = "http://" + original_url

    # Verify the original URL is valid
    # if not is_valid_url(original_url):
    #     return jsonify({'error': "Invalid URL format. Please enter a valid URL."})

    # Check if the original URL is already in the database
    fsufo = find_short_url_for_original(original_url)
    if fsufo != None:
        short_url = f'http://yourdomain/{fsufo}'
    else:
        short_url = generate_unique_short_url()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO url_mapping (short_url, original_url) VALUES (?, ?)', (short_url, original_url))
        conn.commit()
        conn.close()

        short_url = f'http://yourdomain/{short_url}'  # Replace with your actual domain

    return jsonify({'short_url': short_url})

# Function to check if the original URL is already in the database
def find_short_url_for_original(original_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT short_url FROM url_mapping WHERE original_url = ?', (original_url,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

# Route to redirect to the original URL
@app.route('/<short_url>')
def redirect_to_original(short_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT original_url FROM url_mapping WHERE short_url = ?', (short_url,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        original_url = row['original_url']
        print(f"Redirecting to original URL: {original_url}")
        
        # Add "http://" if necessary
        if not original_url.startswith("http://") and not original_url.startswith("https://"):
            original_url = "http://" + original_url
        
        # Redirect to the original URL
        return redirect(original_url)
    else:
        print("URL not found")
        return abort(404)

# 404 error handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

# Function to generate a random string for the short URL
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to generate a unique short URL
def generate_unique_short_url():
    while True:
        short_url = generate_random_string()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM url_mapping WHERE short_url = ?', (short_url,))
        if cursor.fetchone() is None:
            conn.close()
            return short_url
        conn.close()

# WebSocket message handler
@socketio.on('send_message')
def handle_message(data):
    print('Received message: ' + data)
    sendTelegramMessage(data)

# Function to send a message to a Telegram bot
def sendTelegramMessage(message):
    chat_id = 'YOUR_TELEGRAM_ID'  # Replace with your chat ID
    bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace with your bot token
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    requests.get(url)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
