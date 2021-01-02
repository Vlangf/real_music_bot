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
    result: bool = None
    error_code: int = None
    description: str


class From(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str = None


class Chat(BaseModel):
    id: int
    first_name: str
    username: str
    type: str


class InlineButton(BaseModel):
    text: str
    callback_data: str = None


class ReplyMarkup(BaseModel):
    inline_keyboard: List[List[InlineButton]]


class Entities(BaseModel):
    offset: int
    length: int
    type: str


class Message(BaseModel):
    message_id: int
    from_: From
    chat: Chat
    date: int
    edit_date: int = None
    text: str = None
    caption: str = None
    reply_markup: ReplyMarkup = None
    entities: List[Entities] = None

    class Config:
        fields = {'from_': 'from'}


class CallbackQuery(BaseModel):
    id: str
    from_: From
    message: Message
    chat_instance: str
    data: str

    class Config:
        fields = {'from_': 'from'}


class UpdateResult(BaseModel):
    update_id: int
    message: Message = None
    edited_message: Message = None
    callback_query: CallbackQuery = None


class Update(BaseModel):
    ok: bool
    result: List[UpdateResult]


class Error(BaseModel):
    ok: bool
    error_code: int
    description: str


class Song(BaseModel):
    id_: int
    name: str
    band_name: str
    link: str
    like: int
    date_add_to_site: str
    genre: str

    class Config:
        fields = {'id_': 'id'}
