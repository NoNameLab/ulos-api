# C:\Uuu\FastAPIULOS\models.py

from tortoise import fields, models

# Modelo User
class User(models.Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    role = fields.CharField(max_length=50, choices=["student", "admin"])  
    created_at = fields.DatetimeField(auto_now_add=True)

# Modelo TaskType
class TaskType(models.Model):
    task_type_id = fields.IntField(pk=True)
    task_type_name = fields.CharField(max_length=100, unique=True)

# Modelo Task
class Task(models.Model):
    task_id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="tasks", on_delete="CASCADE")
    file_name = fields.CharField(max_length=255, null=True)
    ftp_file_path = fields.CharField(max_length=255, null=True)
    task_type = fields.ForeignKeyField("models.TaskType", related_name="tasks")
    parsed_status = fields.IntField(default=0, choices=[0, 1, 2, 3])
    executed_status = fields.IntField(default=0, choices=[0, 1, 2, 3])
    state = fields.IntField(default=0, choices=[0, 1, 2, 3])
    requeue_count = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    end_time = fields.DatetimeField(null=True)
    last_step_id = fields.IntField(null=True)  # Almacena solo el ID de TaskExecutionLog
    feedback = fields.TextField(null=True)

# Modelo TaskExecutionLog
class TaskExecutionLog(models.Model):
    log_id = fields.IntField(pk=True)
    task = fields.ForeignKeyField("models.Task", related_name="execution_logs", on_delete="CASCADE")
    step_name = fields.CharField(max_length=100, null=True)
    step_status = fields.IntField(default=0, choices=[0, 1, 2, 3])
    old_state = fields.IntField(null=True, choices=[0, 1, 2, 3])
    new_state = fields.IntField(null=True, choices=[0, 1, 2, 3])
    error_message = fields.TextField(null=True)
    machine = fields.ForeignKeyField("models.Machine", null=True, related_name="logs", on_delete="SET NULL")
    timestamp = fields.DatetimeField(auto_now_add=True)

# Modelo Machine
class Machine(models.Model):
    machine_id = fields.IntField(pk=True)
    machine_name = fields.CharField(max_length=100, unique=True)
    machine_ip = fields.CharField(max_length=50, unique=True)
    mac_address = fields.CharField(max_length=17, unique=True, null=True)

# Modelo File
class File(models.Model):
    file_id = fields.IntField(pk=True)
    task = fields.ForeignKeyField("models.Task", related_name="files", on_delete="CASCADE")
    file_name = fields.CharField(max_length=255, null=True)
    file_path = fields.CharField(max_length=255, null=True)
    uploaded_at = fields.DatetimeField(auto_now_add=True)

# Modelo Metric
class Metric(models.Model):
    metric_id = fields.IntField(pk=True)
    task = fields.ForeignKeyField("models.Task", related_name="metrics", on_delete="CASCADE")
    execution_time = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    machine = fields.ForeignKeyField("models.Machine", null=True, related_name="metrics", on_delete="SET NULL")
    objective_metric = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
