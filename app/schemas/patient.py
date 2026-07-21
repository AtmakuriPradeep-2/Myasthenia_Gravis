from pydantic import BaseModel



class PatientCreate(BaseModel):

    patient_code: str
    age: int
    sex: str
    mgfa_class: str


class PatientResponse(PatientCreate):

    id: int

    class Config:
        from_attributes = True