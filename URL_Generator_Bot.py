import io
import telebot
import random
import string
import sqlite3

# Telegram bot API token
API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Telegram user ID for access control
NXR8_ID = YOUR_TELEGRAM_ID

# Initialize the Telegram bot
bot = telebot.TeleBot(API_TOKEN)

# Connect to the SQLite database
conn = sqlite3.connect('url_shortener.db', check_same_thread=False)
cursor = conn.cursor()

# Create a table to store URL mappings if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS url_mapping (
    short_url TEXT PRIMARY KEY,
    original_url TEXT NOT NULL
)
''')
conn.commit()

# Function to generate a random string of given length
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to generate a unique short URL
def generate_unique_short_url():
    while True:
        short_url = generate_random_string()
        cursor.execute('SELECT 1 FROM url_mapping WHERE short_url = ?', (short_url,))
        if cursor.fetchone() is None:
            return short_url

# Function to find a short URL for a given original URL
def find_short_url_for_original(original_url):
    cursor.execute('SELECT short_url FROM url_mapping WHERE original_url = ?', (original_url,))
    row = cursor.fetchone()
    if row:
        return row[0]
    return None

# Handler for the /rurl command to generate a random short URL
@bot.message_handler(commands=['rurl'])
def handle_rurl(message):
    try:
        # Extract the original URL from the message
        original_url = message.text.lower().split(maxsplit=1)[1]

        # Check if the original URL already has a short URL
        existing_short_url = find_short_url_for_original(original_url)
        if existing_short_url:
            bot.reply_to(message, f"Your shortened URL already exists: url.nxr8.me/{existing_short_url}")
            return
        
        # Generate a unique short URL
        short_url = generate_unique_short_url()

        # Store the mapping in the database
        cursor.execute('INSERT INTO url_mapping (short_url, original_url) VALUES (?, ?)', (short_url, original_url))
        conn.commit()

        # Reply to the user with the shortened URL
        bot.reply_to(message, f"Your shortened URL: url.nxr8.me/{short_url}")
    except IndexError:
        bot.reply_to(message, "Please enter the original URL after the command.")

# Handler for the /nurl command to generate a custom short URL
@bot.message_handler(commands=['vurl'])
def handle_nurl(message):
    if (message.chat.id == NXR8_ID):
        try:
            # Extract the original URL and custom text from the message
            parts = message.text.lower().plit(maxsplit=2)
            if len(parts) < 3:
                bot.reply_to(message, "Please enter the URL and custom text correctly.")
                return

            original_url = parts[1]
            custom_text = parts[2]

            # Check if the original URL already has a short URL
            existing_short_url = find_short_url_for_original(original_url)
            if existing_short_url:
                bot.reply_to(message, f"Your shortened URL already exists: url.nxr8.me/{existing_short_url}")
                return

            # Check if the custom text is already in use
            cursor.execute('SELECT 1 FROM url_mapping WHERE short_url = ?', (custom_text,))
            if cursor.fetchone() is not None:
                bot.reply_to(message, "The custom text already exists, please choose another.")
                return

            # Store the mapping in the database
            cursor.execute('INSERT INTO url_mapping (short_url, original_url) VALUES (?, ?)', (custom_text, original_url))
            conn.commit()

            # Reply to the user with the shortened URL
            bot.reply_to(message, f"Your shortened URL: url.nxr8.me/{custom_text}")
        except IndexError:
            bot.reply_to(message, "Please enter the URL and custom text after the command.")

# Handler for the /dbv command to display URL mappings
@bot.message_handler(commands=['dbv'])
def handle_dbv(message):
    if (message.chat.id == NXR8_ID):
        cursor.execute('SELECT * FROM url_mapping')
        rows = cursor.fetchall()

        response = "URL Mappings:\n"
        for row in rows:
            response += f"Short URL: {row[0]} - Original URL: {row[1]}\n"
        
        if len(response) > 4096:  # Telegram message character limit
            with io.StringIO(response) as file:
                file.seek(0)
                bot.send_document(message.chat.id, file, visible_file_name="url_mappings.txt")
        else:
            bot.reply_to(message, response)

# Start polling for Telegram messages
bot.polling()

# Close the database connection when finished
conn.close()
