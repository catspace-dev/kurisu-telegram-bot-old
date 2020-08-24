from tortoise import fields, Model


class ActionCommand(Model):
    chat_id = fields.relational.ForeignKeyField("model.Chats",
                                                related_name="commands")
    command = fields.CharField(max_length=15)
    templates: fields.ReverseRelation["ActionTemplate"]
    attachs: fields.ReverseRelation["ActionAttachs"]


class ActionTemplate(Model):
    command = fields.relational.ForeignKeyField("model.ActionCommand",
                                                related_name="templates",
                                                )
    text = fields.TextField()


class ActionAttachs(Model):
    command = fields.relational.ForeignKeyField("model.ActionCommand",
                                                related_name="attachs")
    file_id = fields.TextField()
