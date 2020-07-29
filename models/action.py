from tortoise import fields

from . import AbstractBaseModel


class Action(AbstractBaseModel):
    chat_id = fields.BigIntField()
    command = fields.CharField(max_length=15)
    text = fields.TextField()
