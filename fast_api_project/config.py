from pydantic import BaseModel


class Config(BaseModel):
    DEFAULT_JOKER_NUM: int = 2
    DEFAULT_PLAYER_NUM: int = 4
    FUNCTION_333SANDSTORM: bool = False
    FUNCTION_44STOP: bool = False
    FUNCTION_5SKIP: bool = False
    FUNCTION_66NECK: bool = False
    FUNCTION_7GIFT: bool = True
    FUNCTION_8CUT: bool = True
    FUNCTION_99RESQUE: bool = False
    FUNCTION_10THROW: bool = True
    FUNCTION_11BACK: bool = False
    FUNCTION_12BOMBER: bool = False
    FUNCTION_13SKIP: bool = False
    FUNCTION_REVOLUTION: bool = True
    FUNCTION_LOW_LIMIT: bool = True
    FUNCTION_HIGH_LIMIT: bool = True
    FUNCTION_EMPEROR: bool = False
