from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if len(name) == 0: 
            raise ValueError("Name cannot be null") 

        names = [author.name for author in Author.query.all() ]
        if name in names: 
            raise ValueError("Name must be unique")
        return name

    @validates('phone_number')
    def validation_phone_number(self, key, number):
        if not number.isdigit():
            raise ValueError("Phone number must include only number")
        if len(number) != 10:
            raise ValueError("Phone number must be 10 digits")
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('title')
    def validate_title(self, key, title):
        if len(title) == 0:
            raise ValueError('Title must be non empty string') 
        phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in phrases):
            raise ValueError('Title must contaion one of the phrases')
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be equal to or longer than 250charactors')
        return content

    @validates('category')
    def validate_category(self, key, category):
        categories = ['Fiction', 'Non-Fiction']
        if category not in categories:
            raise ValueError('Category does not exist')
        return category

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary must be shorter than 250')
        return summary



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
