#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from forms import AnswerForm, QuestionForm, SearchForm
from flask_migrate import Migrate
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from flask_migrate import Migrate  
from flask_migrate import Migrate
from datetime import datetime
import sys
sys.path.append(
    "c:\\Bach\\ComputerScience\\Fullstack_nanodegree\\QA_4anything\\database")

from models import setup_db, Question, User, Answer



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

QUESTIONS_PER_PAGE = 7

def create_app():

    static_folder='c:\\Bach\\ComputerScience\\Fullstack_nanodegree\\QA_4anything\\static'
    template_folder='c:\\Bach\\ComputerScience\\Fullstack_nanodegree\\QA_4anything\\templates'

    app = Flask(__name__,
        static_url_path= '', 
        static_folder = static_folder,
        template_folder = template_folder)

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    db = setup_db(app)
    migrate = Migrate(app, db)

    @app.route('/', methods = ['GET'])
    def index():

        page = request.args.get("page", 1, type = int)
        questions = Question.query.order_by(Question.created.desc()).paginate(page, QUESTIONS_PER_PAGE, error_out=False)

        return render_template("pages/home.html", page_obj = questions)
      

    @app.route('/questions/<int:question_id>', methods = ['GET', 'POST'])
    def get_question(question_id):
        
        form = AnswerForm()
        question = Question.query.get(question_id)


        if form.validate_on_submit():
            text = form.answer.data


            try: 
                new_answer = Answer(text = text, question_id = question_id, user_id = 4, created=datetime.utcnow(), modified=datetime.utcnow(), hidden=False)
                new_answer.insert()
                # return redirect(url_for('get_question'), question = question, form = form)
                return redirect(url_for("get_question", question_id = question_id))
            except:
                return "Error"

        answers = Answer.query.filter_by(question_id = question.id).all()
            

        return render_template("pages/question.html", question = question, form = form, answers= answers) 


    @app.route('/question/upvote', methods = ['POST'])
    def upvote_question():

      
        form = AnswerForm()
        data_received = json.loads(request.data) 

        # return f"{data_received['questionid']}"
        
        question = Question.query.filter_by(id=data_received['questionid']).first()
        
        if question:
            
            question.points += 1
            question.update()

            # return redirect(url_for("get_question", question_id =data_received['questionid'] ))            
            
            return json.dumps({'status' : 'upvote_success', "new_point": question.points})
        return json.dumps({'status' : 'no post found'})

     


    @app.route('/question/downvote', methods = ['POST'])
    def downvote_question():

        data_received = json.loads(request.data) 

        # return f"{data_received['questionid']}"
        
        question = Question.query.filter_by(id=data_received['questionid']).first()
        
        if question:
            
            question.points -= 1
            question.update()
                 
            return json.dumps({'status' : 'downvote_success', "new_point": question.points})
        return json.dumps({'status' : 'no post found'})
   

    @app.route('/question/new', methods = ["GET", "POST"])
    def create_new_question():

        form = QuestionForm()

        if form.validate_on_submit():
            title = form.title.data
            body = form.body.data

            try: 
                new_question = Question(title = title, body = body, created=datetime.utcnow(),
                modified=datetime.utcnow(), hidden=False)

                new_question.insert()
                # return redirect(url_for('get_question'), question = question, form = form)
                return redirect(url_for("index"))
            except:
                return "Error"
            
        return render_template("pages/new_question.html", form = form) 
                
  
    @app.route('/about', methods = ['GET'])
    def get_about():

        return render_template("pages/about.html")

    @app.route('/search', methods = ['GET', 'POST'])
    def search():
        
        page = request.args.get('page', 1, type = int)
        form = SearchForm()

        if form.validate_on_submit():

            search_term = form.search_body.data

            session["search_term"] = search_term

            searched_title = Question.query.filter(Question.title.ilike("%" + search_term + "%")).paginate(page, QUESTIONS_PER_PAGE, error_out=False)
            # search_body = Question.query.filter(Question.body.ilike("%" + search_term + "%")).paginate(page, QUESTIONS_PER_PAGE, error_out=False)

            # searched_title = Question.query.filter(Question.title.ilike("%" + search_term + "%")).all()
            # search_body = Question.query.filter(Question.body.ilike("%" + search_term + "%")).all()


            # for _ in search_body:
            #     searched_title.append(_)

            return render_template('pages/search.html', form = form, search_result = searched_title)

        if session.get("search_term"):
            
            search_term = session.get("search_term")
            searched_title = Question.query.filter(Question.title.ilike("%" + search_term + "%")).paginate(page, QUESTIONS_PER_PAGE, error_out=False)
            return render_template('pages/search.html', form = form, search_result = searched_title)
        

        return render_template("pages/search.html", form = form)

    return app

    


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
# # Default port:
# if __name__ == '__main__':
#     app.run()