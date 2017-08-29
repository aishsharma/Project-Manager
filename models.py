import peewee
from datetime import datetime

db = peewee.SqliteDatabase('projects.sqlite')


class BaseModel(peewee.Model):
	class Meta:
		database = db


class Project(BaseModel):
	name = peewee.CharField(unique=True)
	description = peewee.CharField()

	def dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"description": self.description,
			"tasks": [task.dict() for task in self.tasks]
		}


class Task(BaseModel):
	project = peewee.ForeignKeyField(Project, related_name='tasks')
	name = peewee.CharField(null=False)
	details = peewee.TextField()
	progress = peewee.IntegerField(default=0,
	                               constraints=[peewee.Check('progress >= 0'), peewee.Check('progress <= 100')])
	start_date = peewee.DateField(default=datetime.today())
	end_date = peewee.DateField()

	def dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"details": self.details,
			"progress": self.progress,
			"start_date": self.start_date.strftime('%m/%d/%Y'),
			"end_date": self.end_date.strftime('%m/%d/%Y')
		}


def init_db():
	try:
		db.connect()
		db.create_tables([Project, Task])
	except peewee.OperationalError:
		print("Database is already initialized")
	finally:
		db.close()
