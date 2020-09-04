from . import db
from . import user

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), nullable=False)
    course_section = db.Column(db.String(40), nullable=True)
    professor_id = db.Column(db.Integer, db.ForeignKey("professors.id"), nullable=False)
    join_code = db.Column('join_code', db.Integer, unique=True, autoincrement=True, nullable=False)    
    
    def __repr__(self):
        return '<Student_Course \'%s\'>' % self.id