from tortoise import fields, Model
from .action import ActionCommand


class Chats(Model):
    id = fields.BigIntField(pk=True)
    commands: fields.ReverseRelation["ActionCommands"]
