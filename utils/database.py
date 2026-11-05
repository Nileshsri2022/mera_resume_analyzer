from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# The canonical persistence implementation lives in config.database.
# The SQL functions below are thin facades routing to it (single source of truth).
from config.database import (
    get_database_connection as _get_database_connection,
    save_resume_data as _save_resume_data,
    save_ai_analysis_data as _save_ai_analysis_data,
    get_all_ai_analyses as _get_all_ai_analyses,
    get_ai_analysis as _get_ai_analysis,
)

# Create the base class for declarative models
Base = declarative_base()

# Define the Resume model
class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))
    job_role = Column(String(100))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Define the Analysis model
class Analysis(Base):
    __tablename__ = 'analyses'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer)
    analysis_data = Column(Text)  # Store JSON data
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AIAnalysis(Base):
    __tablename__ = 'ai_analyses'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer)
    model_used = Column(String(100))
    resume_score = Column(Integer)
    job_role = Column(String(100))
    full_analysis = Column(Text)  # Added to store the full markdown analysis
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DatabaseManager:
    def __init__(self, db_path='resume_data.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def save_resume(self, user_id, job_role, content):
        resume = Resume(
            user_id=user_id,
            job_role=job_role,
            content=content
        )
        self.session.add(resume)
        self.session.commit()
        return resume.id

    def get_resume(self, resume_id):
        return self.session.query(Resume).filter(Resume.id == resume_id).first()

    def get_user_resumes(self, user_id):
        return self.session.query(Resume).filter(Resume.user_id == user_id).all()

    def save_analysis(self, resume_id, analysis_data):
        analysis = Analysis(
            resume_id=resume_id,
            analysis_data=analysis_data
        )
        self.session.add(analysis)
        self.session.commit()
        return analysis.id

    def get_analysis(self, analysis_id):
        return self.session.query(Analysis).filter(Analysis.id == analysis_id).first()

    def get_resume_analyses(self, resume_id):
        return self.session.query(Analysis).filter(Analysis.resume_id == resume_id).all()

    def close(self):
        self.session.close()

def get_database_connection():
    """Get a connection to the database (thin facade over config.database)."""
    return _get_database_connection()

def save_resume_data(resume_data):
    """Save resume data to the database (thin facade over config.database)."""
    return _save_resume_data(resume_data)

def save_ai_analysis_data(resume_id, analysis_data):
    """Save AI analysis data (thin facade over config.database)."""
    return _save_ai_analysis_data(resume_id, analysis_data)

def get_all_ai_analyses():
    """Get all AI analyses (thin facade over config.database)."""
    return _get_all_ai_analyses()

def get_ai_analysis(analysis_id):
    """Get a specific AI analysis (thin facade over config.database)."""
    return _get_ai_analysis(analysis_id)

def get_ai_analysis_statistics():
    """Get statistics about AI analyses (SQLAlchemy legacy capability)."""
    engine = create_engine('sqlite:///resume_data.db')
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        # Get total number of analyses
        total_analyses = session.query(func.count(AIAnalysis.id)).scalar() or 0

        # Get average resume score
        average_score = session.query(func.avg(AIAnalysis.resume_score)).scalar() or 0

        # Get model usage distribution
        model_usage_query = session.query(
            AIAnalysis.model_used,
            func.count(AIAnalysis.id)
        ).group_by(AIAnalysis.model_used).all()

        model_usage = {model: count for model, count in model_usage_query}

        # Get job role distribution
        job_roles_query = session.query(
            AIAnalysis.job_role,
            func.count(AIAnalysis.id)
        ).group_by(AIAnalysis.job_role).all()

        job_roles = {role: count for role, count in job_roles_query}

        return {
            'total_analyses': total_analyses,
            'average_score': float(average_score),
            'model_usage': model_usage,
            'job_roles': job_roles
        }
    except Exception as e:
        print(f"Error getting AI analysis statistics: {e}")
        return None
    finally:
        session.close()
