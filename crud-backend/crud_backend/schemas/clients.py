from pydantic import BaseModel, ConfigDict, EmailStr


class ClientSchema(BaseModel):
    company: str
    email: EmailStr
    phone: str


class ClientDB(ClientSchema):
    id: int


class ClientPublic(BaseModel):
    id: int
    company: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class ClientList(BaseModel):
    clients: list[ClientPublic]
