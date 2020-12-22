from typing import List
from pydantic import BaseModel


class WebhookInfoResult(BaseModel):
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: str
    last_error_date: int
    last_error_message: str
    max_connections: int
    allowed_updates: List[str]


class WebhookInfo(BaseModel):
    ok: bool
    result: WebhookInfoResult


class WebhookSetOrDelete(BaseModel):
    ok: bool
    result: bool
    error_code: int = None
    description: str


class From(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str


class Chat(BaseModel):
    id: int
    first_name: str
    username: str
    type: str


class Message(BaseModel):
    message_id: int
    chat: Chat
    date: int
    text: str


class UpdateResult(BaseModel):
    update_id: int
    message: Message


class Update(BaseModel):
    ok: bool
    result: List[UpdateResult]
