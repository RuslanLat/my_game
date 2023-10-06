from dataclasses import dataclass


# Базовые структуры, для выполнения задания их достаточно,
# поэтому постарайтесь не менять их пожалуйста из-за возможных проблем с тестами
@dataclass
class Message:
    peer_id: int
    text: str


# @dataclass
# class UpdateMessage:
#     from_id: int
#     text: str
#     id: int


@dataclass
class UpdateObject:
    message: dict


@dataclass
class Update:
    type: str
    group_id: int
    object: UpdateObject


@dataclass
class Members:
    vk_id: int
    first_name: str
    last_name: str