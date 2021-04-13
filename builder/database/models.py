from tortoise import fields, Model

class Guild(Model):
    guild_id = fields.BigIntField(pk=True, unique=True)
    prefix = fields.TextField(default="b!")
    case_sensitive_prefix = fields.BooleanField(default=True)
    lang = fields.TextField(default="en")