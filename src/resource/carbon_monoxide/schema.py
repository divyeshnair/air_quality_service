import datetime
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, validator


class GetH3IndexRequest(BaseModel):
    start_date: str
    end_date: str

    @validator('start_date','end_date')
    def name_must_contain_space(cls, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return date_text
        except Exception as e:
            raise HTTPException(detail="Incorrect data format, "
                                         "should be YYYY-MM-DD", status_code=400)


class GetCarbonMonoxideRequest(BaseModel):
    h3_index: str
    rolling: int

