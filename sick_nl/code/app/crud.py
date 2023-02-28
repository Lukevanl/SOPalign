from sqlalchemy.orm import Session
from sqlalchemy import delete
import models_sql, schemas

def get_feedback(db: Session, feedback_id: int):
    return db.query(models_sql.Feedback).filter(models_sql.Feedback.id == feedback_id).first()
    
def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models_sql.Feedback(aanbeveling=feedback.aanbeveling, aanbeveling_id=feedback.aanbeveling_id, sop_passage=feedback.sop_passage, nli_label=feedback.nli_label)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def remove_richtlijn_by_name(db: Session, name: str):
    db.query(models_sql.Richtlijn).filter(models_sql.Richtlijn.name == name).delete()
    db.commit()
    results = get_richtlijnen(db)
    return results

def get_richtlijn_by_name(db: Session, name: str):
    return db.query(models_sql.Richtlijn).filter(models_sql.Richtlijn.name == name).first()

def get_richtlijnen(db: Session, skip: int = 0, limit: int = 200):
    return db.query(models_sql.Richtlijn).offset(skip).limit(limit).all()
    
def create_richtlijn(db: Session, richtlijn: schemas.RichtlijnCreate):
    db_richtlijn = models_sql.Richtlijn(name = richtlijn.name, aanbevelingen=richtlijn.aanbevelingen, aanbevelingen_ids=richtlijn.aanbevelingen_ids)
    db.add(db_richtlijn)
    db.commit()
    db.refresh(db_richtlijn)
    return db_richtlijn