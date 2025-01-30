from tortoise import fields, models

class TaskExecutionLog(models.Model):
    id = fields.IntField(pk=True)
    task = fields.ForeignKeyField("models.Task", related_name="execution_logs", on_delete="CASCADE")
    step_name = fields.CharField(max_length=100, null=True)
    step_status = fields.IntField(default=0, choices=[0, 1, 2, 3])
    old_state = fields.IntField(null=True, choices=[0, 1, 2, 3])
    new_state = fields.IntField(null=True, choices=[0, 1, 2, 3])
    error_message = fields.TextField(null=True)
    machine = fields.ForeignKeyField("models.Machine", null=True, related_name="logs", on_delete="SET NULL")
    timestamp = fields.DatetimeField(auto_now_add=True)
