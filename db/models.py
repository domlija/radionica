import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "blog.db")

class User:
    def __init__(self, id, name, password):
        self.id = str(id)
        self.username = name 
        self.password = password

    def fetch_by_id(id):
        '''Returns user object from database by id'''
        global db_path
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (id))
        data = cursor.fetchone()
        connection.close()

        if data:
            return User(data[0], data[1], data[2])
        else:
            raise Exception('Invalid user ID')
        
    def fetch_by_username(username):
        '''Returns user object from database by username'''

        global db_path

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        data = cursor.fetchone()
        connection.close()

        if data:
            return User(data[0], data[1], data[2])
        else:
            raise Exception('Invalid user username')
        
        
    def insert_user(username, password):
        global db_path

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        except:
            raise Exception('Username already exists')
        
        connection.commit()
        connection.close()

    def login_user(username, password):
        try:
            user = User.fetch_by_username(username)
            if user.password == password:
                return user.id
            else:
                return None

        except:
            return None
        
    def __str__(self):
        return "(id: {id}, username: {name})".format(id=self.id, name=self.username)
    
class BlogPost():
    def __init__(self, id, title, body, creator_id):
        self.id = str(id)
        self.title = title
        self.body = body 
        self.cretor_id = str(creator_id)

    def fetch_by_id(id):
        global db_path

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM blogPosts WHERE id = ?", (id,))
        data = cursor.fetchone()
        connection.close()

        if data:
            return BlogPost(data[0], data[1], data[2], data[3])
        else:
            raise Exception('Invalid post ID ' + str(id))
        
    def fetch_by_creator_id(id):
        global db_path

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM blogPosts WHERE creatorId = ?", (id))
        data = cursor.fetchall()
        connection.close()

        if data:
            return list ( map(lambda x: BlogPost(x[0], x[1], x[2], x[3]), data) )
        else:
            return []
        
    def insert_post(title, body, creator_id):
        global db_path

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO blogPosts (title, body, creatorId) VALUES (?, ?, ?)", (title, body, creator_id))
        except:
            raise Exception('Username already exists')
        
        connection.commit()
        connection.close()

    def delete_post(id):
        global db_path

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM blogPosts WHERE id = ?", id)
        except:
            raise Exception('Database error')
        
        connection.commit()
        connection.close()

        
    def __str__(self):
        return "(title: {}, body: {}, creatorId: {})".format(self.title, self.body, self.cretor_id)
    
class Comment():
    def __init__(self, id, text, post_id):
        self.id = str(id)
        self.text = text
        self.post_id = str(post_id) 

    def fetch_by_post_id(post_id):
        global db_path

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM comments WHERE postId = ?", (post_id))
        data = cursor.fetchall()
        connection.close()

        if data:
            return list ( map(lambda x: Comment(x[0], x[1], x[2]), data) )
        else:
            raise Exception('Invalid creator ID')
        
    def insert_comment(text, post_id):
        global db_path

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO comments (text, postId) VALUES (?, ?)", (text, post_id))
        except:
            raise Exception('Username already exists')
        
        connection.commit()
        connection.close()

    def delete_comment(id):
        global db_path

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM comments WHERE id = ?", id)
        except:
            raise Exception('Database error')
        
        connection.commit()
        connection.close()


        
    



