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

    name = Column(String, primary_key=True, index=True)
    aanbevelingen = Column(PickleType, unique=False, index=True)
    aanbevelingen_ids = Column(PickleType, unique=False, index=True)


