from tortoise import fields
from tortoise.models import Model


class LogForm(Model):
    message_id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    group_id = fields.BigIntField(null=True)
    time = fields.BigIntField()
    message = fields.TextField()
    data = fields.JSONField()

    class Meta:
        table = "LogForm"

    def __str__(self):
        return self.message_id
