from pydantic import BaseModel

class FeedbackBase(BaseModel):
    aanbeveling : str
    aanbeveling_id : str
    sop_passage : str
    nli_label : str


class FeedbackCreate(FeedbackBase):
    pass


class Feedback(FeedbackBase):
    id: int

    class Config:
        orm_mode = True


class RichtlijnBase(BaseModel):
    aanbeveling : str
    aanbeveling_id : str
    name: str

class RichtlijnCreate(RichtlijnBase):
    pass


class Richtlijn(RichtlijnBase):
    id: int
    class Config:
        orm_mode = True