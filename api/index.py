import os
import psycopg2
from flask import Flask, jsonify, request, url_for, redirect, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='monorail.proxy.rlwy.net',
            database='railway',
            user='postgres',
            password='uCvSdWUYewpxUAqxuQFocMlYkfQWVzJB',
            port=38750
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        books_data = [
            {"id": book[0], "title": book[1], "author": book[2], "pages_num": book[3], "review": book[4]}
            for book in books
        ]
        return jsonify(books_data)
    except psycopg2.Error as e:
        print(f"Error querying the database: {e}")
        return jsonify({"error": "Error fetching data from database"}), 500
    finally:
        cur.close()
        conn.close()

    # return render_template('index.html', books = books)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        pages_num = request.form.get('pages_num', type=int)
        review = request.form.get('review')


        if not title or not author or not pages_num or not review:
            return jsonify({"error": "All fields are required"}), 400

        conn = get_db_connection()

        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cur = conn.cursor()

        try:
            insert_script = '''INSERT INTO books (title, author, pages_num, review) VALUES (%s, %s, %s, %s);'''
            insert_value = (title, author, pages_num, review)
            cur.execute(insert_script, insert_value)
            conn.commit()
            return redirect(url_for('/'))
        except psycopg2.Error as e:
            print(f"Error inserting into database: {e}")
            return jsonify({"error": "Error inserting data into database"}), 500
        finally:
            cur.close()
            conn.close()

    # return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)

