from pydantic import BaseModel, ValidationError, HttpUrl
from typing import Optional, Literal

class CreateMonitor(BaseModel):
    name : str
    url : HttpUrl
    selector_id : int
    monitor_type : str
    threshold : int
    check_intervall : int
    is_active : Literal[0, 1]
    notification_id : int

class CreateSelector(BaseModel):
    selector_name : str

def check_user_input(model : type[BaseModel], user_input : dict):
    fields = model.model_fields.keys()
    user_input = user_input
    
    while True:
        try:
            data = model(**user_input)
            return data
        except ValidationError as e:
            for error in e.errors():
                field = error['loc'][0]
                user_input.pop(field, None)

        for field in fields:
            if field not in user_input:
                print(f"{field} should be {model.model_fields[field].annotation.__name__}")
                user_input[field] = input(f"{field.capitalize()}: ")
        
if __name__ == "__main__":
    vals = {
        "name" : "Fredrik",
        "url" : "asdasd",
        "selector_id": 1,
        "monitor_type" : "price",
        "threshold" : "1",
        "check_intervall" : 123,
        "is_active" : 1,
        "notification_id" : 1
    }
    check_user_input(CreateMonitor, vals)