from pydantic import BaseModel, ValidationError, HttpUrl

class CreateMonitor(BaseModel):
    name : str
    url : HttpUrl
    selector_id : int
    monitor_type : str
    threshold : int
    check_intervall : int
    is_active : int
    notification_id : int
    

def get_user_input(model : type[BaseModel]):
    data = {}
    fields = model.model_fields.keys()
    
    while True:
        for field in fields:
            if field not in data:
                data[field] = input(f"{field.capitalize()}: ")