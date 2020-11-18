import os
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
import json
from datetime import datetime

database_name = "qa4anything"
database_path = "postgres://{}/{}".format(
    'postgres:password321@localhost:5432', database_name)

db = SQLAlchemy()


# migrate = Migrate(app, db)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    moment = Moment(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    # user1 = User("PakVu", "123456")
    # user1.insert()

    # question1 = Question(title = "first question", body = "How much do you weight", created=datetime.utcnow(), modified=datetime.utcnow(), hidden=False)
    # question1.insert()

    
    # answer1 = Answer(text="5ft7", question_id=4, user_id=4,created=datetime.utcnow(), modified=datetime.utcnow(), hidden=False)
    # answer1.insert()

    # db.session.add_all([user1, question1, answer1])
    # db.session.commit()

    return db


# Prepare relationship table for many to many relationship
users_upvote_questions = db.Table("users_upvote_questions", 
        db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True), 
        db.Column("question_id", db.Integer, db.ForeignKey("questions.id"), primary_key=True))

users_downvote_questions = db.Table("users_downvote_questions", 
        db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
        db.Column("question_id", db.Integer, db.ForeignKey("questions.id"), primary_key=True))

users_upvote_answers = db.Table("users_upvote_answers", 
        db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
        db.Column("answers_id", db.Integer, db.ForeignKey("answers.id"), primary_key=True))

users_downvote_answers = db.Table("users_downvote_answers", 
        db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
        db.Column("answer_id", db.Integer, db.ForeignKey("answers.id"), primary_key=True))




class User(db.Model):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True) 
    user_name = db.Column(String)
    password = db.Column(String)

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password


    # The many2many relationship can be defined in either one of the two classes
    # Here I defined the relationship in User class
    upvote_questions = db.relationship(
        "Question", secondary="users_upvote_questions", backref=db.backref("upvote_users"))

    downvote_questions = db.relationship(
        "Question", secondary="users_downvote_questions", backref=db.backref("downvote_users"))

    upvote_answers = db.relationship(
        "Answer", secondary="users_upvote_answers", backref=db.backref("upvote_users"))

    downvote_answers = db.relationship(
        "Answer", secondary="users_downvote_answers", backref=db.backref("downvote_users"))

    # secondary = specify the name of the association table used in many2many relationship

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(Integer, primary_key=True)
    title = db.Column(String)
    body = db.Column(Text)
    created = db.Column(DateTime, nullable = False, default = datetime.utcnow)
    modified = db.Column(DateTime, nullable = False, default = datetime.utcnow)
    answers_count = db.Column(Integer, default = 0 ) 
    points = db.Column(Integer, default = 0) 
    hidden = db.Column(Boolean, default=False)

    # declare one to many relationship
    answers = db.relationship('Answer', backref = 'question', lazy = True)

    def __init__(self, title, body, created, modified, hidden, answers_count=0, points=0):
        
        self.title = title
        self.body = body
        self.created = created
        self.modified = modified
        self.hidden = hidden
        self.answers_count = answers_count
        self.points = points

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }

    def num_answers(self):
        answers = Answer.query.filter_by(question_id=self.id).all()
        return len(answers)

    def x_ago(self):
        diff = datetime.utcnow() - self.created
        return x_ago_helper(diff)

    def show_points(self):
        if self.points < 0:
            return 0
        else:
            return self.points

    def update_points(self):
        update_points_helper(self)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.utcnow()
        self.modified = datetime.utcnow()
        return super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Answer(db.Model):

    __tablename__ = 'answers'
    id = db.Column(Integer, primary_key = True)
    question_id = db.Column(Integer, db.ForeignKey("questions.id"), nullable = False)
    user_id = db.Column(Integer, db.ForeignKey("users.id"), nullable = False)
 
    text = db.Column(Text)
    created = db.Column(DateTime, nullable = False, default = datetime.utcnow)
    modified = db.Column(DateTime, nullable = False, default = datetime.utcnow)
    points = db.Column(Integer, default = 0) 
    hidden = db.Column(Boolean, default=False)

    def __init__(self, text, created, modified, hidden, question_id, user_id):
  
        self.text = text
        self.created = created
        self.modified = modified
        self.hidden = hidden
        self.question_id = question_id
        self.user_id = user_id



    def insert(self):
        db.session.add(self)
        db.session.commit()



    def x_ago(self):
        diff = datetime.utcnow() - self.created
        return x_ago_helper(diff)

    def update_points(self):
        update_points_helper(self)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.utcnow()
        self.modified = datetime.utcnow()
        return super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return self.text

# QA web app database

def x_ago_helper(diff):
    if diff.days > 0:
        return f'{diff.days} days ago'
    if diff.seconds < 60:
        return f'{diff.seconds} seconds ago'
    if diff.seconds < 3600:
        return f'{diff.seconds // 60} minutes ago'
    return f'{diff.seconds // 3600} hours ago'


def update_points_helper(obj):
    upvotes = obj.upvoted_users.filter(
        is_shadow_banned=False).distinct().count()
    downvotes = obj.downvoted_users.filter(
        is_shadow_banned=False).distinct().count()
    downvotes += obj.downvoted_users.filter(is_staff=True).count()
    obj.points = upvotes - downvotes
    obj.save()

# class QuestionForm(forms.Form):
#     title = forms.CharField(max_length=200)
#     body = forms.CharField(
#         max_length=5000, widget=forms.Textarea, required=False)


# class AnswerForm(forms.Form):
#     text = forms.CharField(max_length=5000, widget=forms.Textarea)


# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ('user', 'title', 'body', 'created',
#                   'answers_count', 'points')


# class CreatedField(serializers.RelatedField):
#     def to_representation(self, value):
#         diff = timezone.now() - value
#         return x_ago_helper(diff)


# class UserField(serializers.Field):
#     def to_representation(self, value):
#         return value.username


# class AnswerSerializer(serializers.ModelSerializer):
#     user = UserField()
#     x_ago = serializers.SerializerMethodField()
#     text_html = serializers.SerializerMethodField()

#     class Meta:
#         model = Answer
#         fields = ('text_html', 'x_ago', 'user', 'id', 'points', 'hidden')

#     def get_text_html(self, obj):
#         return urlize(escape(obj.text))

#     def get_x_ago(self, obj):
#         return x_ago_helper(timezone.now() - obj.created)






