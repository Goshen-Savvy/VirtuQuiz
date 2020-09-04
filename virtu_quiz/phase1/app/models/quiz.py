from . import db
from datetime import datetime


class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    quiz_number = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False) 

    #relationship
    #questions = db.relationship("Question", secondary=quiz_questions, back_populates="questions")
       
    
    def __repr__(self):
        return '<Quiz \'%s\'>' % self.id

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    timelimit = db.Column(db.DateTime, default=datetime.utcnow)

    #relationship
    #quizzes = db.relationship("Quiz", secondary=quiz_questions, back_populates="quizzes")


    quiz_questions = db.Table(
    "quiz_questions",
    db.Column("quiz_id", db.Integer, db.ForeignKey("quizzes.id")),
    db.Column("question_id", db.Integer, db.ForeignKey("questions.id")),
    )




'''
class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
'''
    

class ShortQuiz(db.Model):
    __tablename__ = 'short_quizzes'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False )
    question_text = db.Column(db.String, nullable=False )

class MCQ(db.Model):
    __tablename__ = 'mcqs'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False )
    text = db.Column(db.String, nullable=False )

class ShortQAnswers(db.Model):
    __tablename__ = 'sqas'

    id = db.Column(db.Integer, primary_key=True)
    shortq_id = db.Column(db.Integer, db.ForeignKey("short_quizzes.id"), nullable=False )
    text = db.Column(db.String, nullable=False)
    #keywords = db.Column(db.String, nullable=False)
    correct_answers = db.Column(db.String, nullable=False)

class MCQAnswers(db.Model):
    __tablename__ = 'mcqas'

    id = db.Column(db.Integer, primary_key=True)
    mcq_id = db.Column(db.Integer, db.ForeignKey("mcqs.id"), nullable=False )
    text = db.Column(db.String, nullable=False)
    #option_number = db.Column(db.String, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    