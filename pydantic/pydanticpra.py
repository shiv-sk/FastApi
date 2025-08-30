# from pydantic import BaseModel , Field
# from typing import Optional
# # class Product(BaseModel):
# #     model:int
# #     name:str
# #     price:int
# #     in_stock:bool
#
# # employee model
# class Employee(BaseModel):
#     id:int
#     name:str = Field(... , min_length=3 , max_length=100)
#     salary:float = Field(... , ge=10000)
#     department:Optional[str] = "General"
#
# emp = Employee(id=1 , name="xyz" , salary=10000 , department="HR")
# print(emp.model_dump())
from symtable import Class

from pydantic import BaseModel


#field_validation , model_validation , computed_validation

# from pydantic import BaseModel , Field , model_validator , computed_field , field_validator
# class Username(BaseModel):
#     name:str
#
#     @field_validator('name')
#     def name_length(cls , v):
#         if len(v) < 4:
#             raise ValueError("name must be least 4 chars long..")
#         return v
# user = Username(name="abcxyz")
# print(user.model_dump())

# from pydantic import BaseModel , Field , model_validator , computed_field , field_validator
# class Signup(BaseModel):
#     password:str
#     confirm_password:str
#
#     @model_validator(mode='after')
#     def check_password(cls , val):
#         if val.password != val.confirm_password:
#             print(f"the password is {val.password} and confirm_password is {val.confirm_password}")
#             raise ValueError("password mismatch...")
#         print(f"the password is {val.password} and {val.confirm_password}")
#         return val
# verify_password = Signup(password="pass1" , confirm_password="pass1")
# print(verify_password.model_dump())

# from pydantic import BaseModel , Field , model_validator , computed_field , field_validator
# class Product(BaseModel):
#     price:int
#     quantity:float
#
#     @computed_field
#     @property
#     def final_price(self) -> float:
#         return self.price * self.quantity
# get_final_price = Product(price=500 , quantity=14.8)
# print(get_final_price.model_dump())

# from pydantic import BaseModel , Field , model_validator , computed_field , field_validator
# class Booking(BaseModel):
#     user_id:int
#     room_id:int
#     nights:int = Field(..., ge=1)
#     rent_per_night:float
#
#     @computed_field
#     @property
#     def final_price(self)->float:
#         return self.rent_per_night * self.nights
# get_final_price = Booking(user_id=1 , room_id=50 , nights=3 , rent_per_night=1500.10)
# print(get_final_price.model_dump())

# nested models -- ref to another model

# from typing import List , Optional
# from pydantic import BaseModel
#
# class Address(BaseModel):
#     line1:str
#     line2:Optional[str]
#     city:str
#     posta_code:str
#
# class User(BaseModel):
#     id:int
#     name:str
#     address:Address
#
# address = Address(line1="line_1" , line2="line_2" , posta_code="010101" , city="something")
# user = User(id=1 , name="xyz" , address=address)
# model_dump gives answer in dict
# model_dump_json gives answer in json
# print(user.model_dump())

# nested models ref to self

# from typing import List , Optional
# from pydantic import BaseModel
# class Comments(BaseModel):
#     id:int
#     content:str
#     replies:Optional[List["Comments"]] = "none"
# Comments.model_rebuild()
# comment = Comments(id=1 , content="something" , replies=[Comments(id=1 , content="reply1")])

# course model
from typing import List , Optional
from pydantic import BaseModel
class Instructor(BaseModel):
    user_id:int
    name:str
    about:str
    year_of_exp:int
    courses:Optional[List['Course']]
class Lesson(BaseModel):
    lesson_id:int
    topic:str

class Module(BaseModel):
    module_id:int
    name:str
    lessons:List[Lesson]
class Course(BaseModel):
    course_id:int
    name:str
    instructor:Instructor
    validity:int
    price:int
    modules:List[Module]