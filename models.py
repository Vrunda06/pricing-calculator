 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    tools = db.relationship('Tool', backref='company', lazy=True)

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    sections = db.relationship('Section', backref='tool', lazy=True)
    state = db.Column(db.String(20), default='draft')  # draft or live

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'), nullable=False)
    components = db.relationship('Component', backref='section', lazy=True)

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    variant = db.Column(db.String(50), nullable=False)
    pricing = db.Column(db.Float, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
