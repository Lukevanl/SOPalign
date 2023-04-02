from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, PickleType
from sqlalchemy.orm import relationship

from database import Base


class Feedback(Base):
    __tablename__ = "user_feedback"
    id = Column(Integer, primary_key=True, index=True)
    aanbeveling = Column(String, unique=False, index=True)
    aanbeveling_id = Column(String, unique=False, index=True)
    sop_passage = Column(String, unique=False, index=True)
    nli_label = Column(String, unique=False, index=True)

class Richtlijn(Base):
    __tablename__ = "saved_richtlijnen"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=False)
    aanbeveling = Column(String, unique=False, index=False)
    aanbeveling_id = Column(String, unique=False, index=False)


