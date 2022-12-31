from sqlalchemy.orm import Session
import models_sql, schemas

def get_feedback(db: Session, feedback_id: int):
    return db.query(models_sql.Feedback).filter(models_sql.Feedback.id == feedback_id).first()
    
def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models_sql.Feedback(aanbeveling=feedback.aanbeveling, aanbeveling_id=feedback.aanbeveling_id, sop_passage=feedback.sop_passage, nli_label=feedback.nli_label)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback