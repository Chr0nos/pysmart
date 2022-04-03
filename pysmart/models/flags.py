from pydantic import BaseModel


class Flags(BaseModel):
    auto_keep: bool
    error_rate: bool
    event_count: bool
    performance: bool
    prefailure: bool
    string: str
    updated_online: bool
    value: int
