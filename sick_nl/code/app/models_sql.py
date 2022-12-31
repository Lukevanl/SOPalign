from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Feedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    aanbeveling = Column(String, unique=False, index=True)
    aanbeveling_id = Column(String, unique=False, index=True)
    sop_passage = Column(String, unique=False, index=True)
    nli_label = Column(String, unique=False, index=True)