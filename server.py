# # app.py (أو أي اسم تختاره لملف التطبيق)
# from flask import Flask, redirect, abort, render_template
# import sqlite3

# app = Flask(__name__)

# # إعداد قاعدة البيانات
# def get_db_connection():
#     conn = sqlite3.connect('url_shortener.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# @app.route('/<short_url>')
# def redirect_to_original(short_url):
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     cursor.execute('SELECT original_url FROM url_mapping WHERE short_url = ?', (short_url,))
#     row = cursor.fetchone()
#     conn.close()
    
#     if row:
#         original_url = row['original_url']
#         print(f"Redirecting to original URL: {original_url}")
        
#         # تحقق وإضافة "http://" إذا لزم الأمر
#         if not original_url.startswith("http://") and not original_url.startswith("https://"):
#             original_url = "http://" + original_url
        
#         # إعادة التوجيه إلى الرابط النهائي
#         return redirect(original_url)
#     else:
#         print("URL not found")
#         return abort(404)

# # تكوين صفحة الخطأ 404
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('error.html'), 404

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

################################################

# from flask import Flask, render_template, request, redirect, abort
# import random
# import string
# import sqlite3
# import requests


# app = Flask(__name__)

# # إعداد قاعدة البيانات
# def get_db_connection():
#     conn = sqlite3.connect('url_shortener.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# @app.route('/')
# def index():
#     return render_template('shorten_url.html')

# @app.route('/shorten', methods=['POST'])
# def shorten_url():
#     original_url = request.form['original_url']

#     # التحقق من صحة الرابط الأصلي
#     if not is_valid_url(original_url):
#         return render_template('shorten_url.html', error="Invalid URL format. Please enter a valid URL.")

#     # التحقق من عدم وجود الرابط الأصلي في قاعدة البيانات
#     if find_short_url_for_original(original_url):
#         return render_template('shorten_url.html', error="URL already exists in database. Please enter a different URL.")

#     short_url = generate_unique_short_url()

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO url_mapping (short_url, original_url) VALUES (?, ?)', (short_url, original_url))
#     conn.commit()
#     conn.close()

#     short_url = f'http://yourdomain/{short_url}'  # Replace with your actual domain

#     return render_template('shorten_url.html', short_url=short_url)

# def is_valid_url(url):
#     try:
#         response = requests.head(url)
#         return response.status_code == 200
#     except requests.ConnectionError:
#         return False

# # تحقق من وجود الرابط الأصلي في قاعدة البيانات
# def find_short_url_for_original(original_url):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT short_url FROM url_mapping WHERE original_url = ?', (original_url,))
#     row = cursor.fetchone()
#     conn.close()
#     if row:
#         return row[0]
#     return None

# @app.route('/<short_url>')
# def redirect_to_original(short_url):
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     cursor.execute('SELECT original_url FROM url_mapping WHERE short_url = ?', (short_url,))
#     row = cursor.fetchone()
#     conn.close()
    
#     if row:
#         original_url = row['original_url']
#         print(f"Redirecting to original URL: {original_url}")
        
#         # تحقق وإضافة "http://" إذا لزم الأمر
#         if not original_url.startswith("http://") and not original_url.startswith("https://"):
#             original_url = "http://" + original_url
        
#         # إعادة التوجيه إلى الرابط النهائي
#         return redirect(original_url)
#     else:
#         print("URL not found")
#         return abort(404)

# # تكوين صفحة الخطأ 404
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('error.html'), 404

# def generate_random_string(length=8):
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# def generate_unique_short_url():
#     while True:
#         short_url = generate_random_string()
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('SELECT 1 FROM url_mapping WHERE short_url = ?', (short_url,))
#         if cursor.fetchone() is None:
#             conn.close()
#             return short_url
#         conn.close()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)



################################


from flask import Flask, render_template, request, redirect, abort
import random
import string
import sqlite3
import requests

app = Flask(__name__)

# إعداد قاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect('url_shortener.db')
    conn.row_factory = sqlite3.Row
    return conn

# صفحة الرئيسية
@app.route('/')
def index():
    return render_template('shorten_url.html')

# صفحة اختصار الرابط
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['original_url']
    if not original_url.startswith("http://") and not original_url.startswith("https://"):
        original_url = "http://" + original_url

    # التحقق من صحة الرابط الأصلي
    # if not is_valid_url(original_url):
    #     return render_template('shorten_url.html', error="Invalid URL format. Please enter a valid URL.")

    # التحقق من عدم وجود الرابط الأصلي في قاعدة البيانات
    ff = find_short_url_for_original(original_url)
    if ff != None:
        short_url = f'http://yourdomain/{ff}'
    else:
        short_url = generate_unique_short_url()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO url_mapping (short_url, original_url) VALUES (?, ?)', (short_url, original_url))
        conn.commit()
        conn.close()

        short_url = f'http://yourdomain/{short_url}'  # Replace with your actual domain

    return render_template('shorten_url.html', short_url=short_url)

# تحقق من وجود الرابط الأصلي في قاعدة البيانات
def find_short_url_for_original(original_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT short_url FROM url_mapping WHERE original_url = ?', (original_url,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

# صفحة التوجيه إلى الرابط الأصلي
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
        
        # تحقق وإضافة "http://" إذا لزم الأمر
        if not original_url.startswith("http://") and not original_url.startswith("https://"):
            original_url = "http://" + original_url
        
        # إعادة التوجيه إلى الرابط النهائي
        return redirect(original_url)
    else:
        print("URL not found")
        return abort(404)

# صفحة الخطأ 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

# توليد سلسلة عشوائية للرابط المختصر
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# توليد رابط مختصر فريد
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
