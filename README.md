# URL Shortener

## Overview

This project is a simple URL shortener service built using Flask, Flask-SocketIO, and SQLite. It allows users to shorten long URLs and redirect to the original URLs using the generated short URLs. Additionally, it integrates with a Telegram bot to send messages.

## Features

- Shorten long URLs to unique short URLs.
- Redirect to the original URL using the short URL.
- Store URL mappings in an SQLite database.
- WebSocket support for real-time message handling.
- Integration with a Telegram bot to send messages.

## Requirements

- Python 3.6+
- Flask
- Flask-SocketIO
- SQLite3
- Requests

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/NXR8/URL-Shortener.git
   cd URL-Shortener
   ```

2. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the SQLite database:**

   The database will be created automatically when the application is run for the first time.

4. **Configure the Telegram bot:**

   - Replace `YOUR_TELEGRAM_ID` with your Telegram chat ID.
   - Replace `YOUR_TELEGRAM_BOT_TOKEN` with your Telegram bot token.

## Usage

1. **Run the application:**

   ```bash
   python server.py
   ```

2. **Access the web interface:**

   Open your web browser and go to `http://localhost:5000`.

3. **Shorten a URL:**

   - Enter a long URL in the input field and click the "Shorten" button.
   - The application will generate a short URL and display it.

4. **Redirect to the original URL:**

   - Use the generated short URL in your browser to be redirected to the original URL.

5. **Send a message via WebSocket:**

   - Connect to the WebSocket server and send a message.
   - The message will be forwarded to the configured Telegram bot.

## API Endpoints

- **Home Page:**

  ```
  GET /
  ```

  Displays the home page with the URL shortening form.

- **Shorten URL:**

  ```
  POST /shorten
  ```

  Shortens the provided URL and returns the short URL.

  **Request Parameters:**
  - `original_url` (string): The original long URL to be shortened.

  **Response:**
  - `short_url` (string): The generated short URL.

- **Redirect to Original URL:**

  ```
  GET /<short_url>
  ```

  Redirects to the original URL corresponding to the provided short URL.

## File Structure

```
url-shortener/
│
├── server.py                  # Main application file
├── requirements.txt        # Required packages
├── templates/
│   ├── error.html          # 404 error page template
│   └── shorten_url.html    # Home page template
└── url_shortener.db        # SQLite database (generated automatically)
```

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- [SQLite](https://www.sqlite.org/index.html)

---

Feel free to modify the sections to better fit your project and its specifics.
