from flask import Flask, render_template, request, redirect, url_for
import csv
import sqlite3

app = Flask(__name__)

try:
    conn = sqlite3.connect('login.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE Student(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """)
    conn.commit()  # make changes to db
    conn.close()  # closes the connection
except sqlite3.IntegrityError:
    pieces = []

@app.route('/')
def index():
    pieces = []
    # file closes after with block
    with open('files.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            pieces.append(row)
    return render_template('home.html', pieces=pieces)

@app.route('/login', methods=['POST', 'GET'])
def login():
    pieces = []
    # file closes after with block
    with open('files.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            pieces.append(row)
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('login.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM Login WHERE username=? AND password=?',
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        if user is None:
            error = 'Invalid username or password'
            return render_template('login.html', error=error, pieces=pieces)

        return redirect('/home')
    return redirect('/home')

@app.route('/register_now', methods=['POST', 'GET'])
def register_now():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        confirm_password = request.form['conpass']
        if password != confirm_password:
            return 'Passwords do not match'
        conn = sqlite3.connect('login.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Login(username, password)
                VALUES(?, ?);
                """, (user, password))
            conn.commit() # make changes to db
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
        return redirect('/login')
    return redirect('/login')

@app.route('/register')
def register():

    return render_template('register.html')

@app.route('/home')
def home():
    pieces = []
    # file closes after with block
    try:
        with open('files.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                pieces.append(row)
    except FileNotFoundError:
        return "There are no pieces yet~"
    return render_template('index.html', pieces=pieces)

@app.route('/add_file', methods=['POST'])
def add():
    piece = request.form['piece']
    file = request.form['file']

    dropbox = 'https://www.dropbox.com'

    if file == '' or piece == '':
        return "Please enter a file/piece name"

    if file[:23] != dropbox:
        return "Please enter a valid file link"

    new_piece = [piece, file]
    # file closes after with block
    with open('files.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(new_piece)

    return redirect('/home')

@app.route('/file')
def file():
    return render_template('file.html')

@app.route('/add_item', methods=['POST'])
def item():
    section = request.form['section']
    item = request.form['item']
    size = request.form['size']
    quantity = request.form['quantity']
    if section == '' or item == '' or size == '' or quantity == '':
        return 'Please Fill out the Fields'
    if section.lower() == 'percussion':
        size = ''
    if item.lower() == 'reed' and not(size == 3 or size == 3.5):
        return 'Please enter a valid size'
    try:
        if item.lower() == 'swab' and size.lower() not in ['m', 'l', 'xl']:
            return 'Please enter a valid size'
    except AttributeError:
        return 'Please enter a valid size'

    new_item = [section, item, size, quantity]
    # file closes after with block
    with open('items.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(new_item)

    return redirect('/item')

@app.route('/item')
def item_page():
    items = []
    # file closes after with block
    # try:
    with open('items.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            items.append(row)
    # except FileNotFoundError:
    #     return "There are no items needed yet"
    return render_template('item.html', items=items)


if __name__ == '__main__':
  app.run(debug=True)
