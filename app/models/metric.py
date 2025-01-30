from tortoise.models import Model
from tortoise import fields

class Metric(Model):
    id = fields.IntField(pk=True)
    task = fields.ForeignKeyField("models.Task", related_name="metrics", on_delete="CASCADE")
    execution_time = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    machine = fields.ForeignKeyField("models.Machine", null=True, related_name="metrics", on_delete="SET NULL")
    objective_metric = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
