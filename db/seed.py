import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "blog.db")

connection = sqlite3.connect(db_path)


cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL ) 
              ''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS blogPosts (
               id INTEGER PRIMARY KEY,
               title TEXT NOT NULL,
               body TEXT NOT NULL,
               creatorId INTEGER NOT NULL,
               FOREIGN KEY (creatorId) REFERENCES users (id))
              ''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS comments (
               id INTEGER PRIMARY KEY,
               text TEXT NOT NULL,
               postId INTEGER NOT NULL,
               FOREIGN KEY (postId) REFERENCES blogPosts (id))
              ''')

cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("Mislav", "Valsim"))

cursor.execute("INSERT INTO blogPosts (title, body, creatorId) VALUES (?, ?, ?)", ("My 1st Title", "fun content", 1))

cursor.execute("INSERT INTO comments (text, postId) VALUES (?, ?)", ("This is great", "1"))

cursor.execute("SELECT * FROM USERS")
print('Users table')
print(cursor.fetchall())

cursor.execute("SELECT * FROM blogPosts")
print('Posts table')
print(cursor.fetchall())

cursor.execute("SELECT * FROM comments")
print('Comments table')
print(cursor.fetchall())




connection.commit()
connection.close()