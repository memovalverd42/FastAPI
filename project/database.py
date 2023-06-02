import peewee
from peewee import Model, SqliteDatabase
from datetime import datetime
import hashlib

database = peewee.SqliteDatabase('data.sqlite')

class User(Model):
    username = peewee.CharField(max_length=50, unique=True)
    password = peewee.CharField(max_length=50)
    created_at = peewee.DateTimeField(default=datetime.now)
    
    def __str__(self) -> str:
        return self.username
    
    class Meta:
        database = database
        table_name = 'users'
        
    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        password = h.update(password.encode('utf-8'))
        
        return h.hexdigest()
        
class Movie(Model):
    title = peewee.CharField(max_length=255)
    year = peewee.IntegerField()
    director = peewee.CharField(max_length=255)
    created_at = peewee.DateTimeField(default=datetime.now)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        database = database
        table_name = 'movies'
        
class UserReview(Model):
    user = peewee.ForeignKeyField(model=User, backref='reviews')
    movie = peewee.ForeignKeyField(model=Movie, backref='reviews')
    reviews = peewee.TextField()
    score = peewee.IntegerField()
    created_at = peewee.DateTimeField(default=datetime.now)
    
    def __str__(self) -> str:
        return f'{self.user.username} - {self.movie.title}'
    
    class Meta:
        database = database
        table_name = 'user_reviews'