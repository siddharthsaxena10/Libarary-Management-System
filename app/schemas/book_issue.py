from datetime import date
from pydantic import BaseModel, ConfigDict, model_validator


# Book issue karte waqt aane wala data
class BookIssueCreate(BaseModel):
    student_id: int
    copy_id: int
    admin_id: int
    issue_date: date
    due_date: date

    # Due date, issue date se pehle nahi honi chahiye
    @model_validator(mode="after")
    def validate_dates(self):
        if self.due_date < self.issue_date:
            raise ValueError("Due date cannot be before issue date")
        return self


# Book issue ki response
class BookIssueResponse(BaseModel):
    issue_id: int
    student_id: int
    copy_id: int
    admin_id: int
    issue_date: date
    due_date: date
    return_date: date | None = None

    # SQLAlchemy model ko Pydantic response mein convert karne ke liye
    model_config = ConfigDict(from_attributes=True)