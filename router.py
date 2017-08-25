import datetime
import json
from typing import List, List

from bottle import Bottle, response, request

from models import db, Project, Task

tracker = Bottle()


@tracker.hook('after_request')
def after_request():
	"""
	You need to add some headers to each request.
	Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
	"""
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
	response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@tracker.post('/api/project')
def new_project():
	data: json = request.json

	try:
		db.connect()
		project: Project = Project(
			name=str(data['name']),
			description=str(data['description']),
			status=str(data['status']),
			start_date=datetime.datetime.strptime(data['start_date'],
			                                      '%m/%d/%Y').date() if data[
				'start_date'] else datetime.datetime.today().date(),
			end_date=datetime.datetime.strptime(data['end_date'], '%m/%d/%Y').date() if data[
				'end_date'] else datetime.datetime.today().date()
		)

		project.save()
	except Exception as e:
		print(e)
		return {"status": False, "error": str(e), "data": {}}
	finally:
		db.close()

	return {"status": True, "error": "", "data": {}}


@tracker.post('/api/task')
def new_task():
	data: json = request.json

	try:
		db.connect()
		task: Task = Task(
			project=int(data['project_id']),
			name=str(data['name']),
			details=str(data['description']),
			progress=int(data['status']),
			start_date=datetime.datetime.strptime(data['start_date'],
			                                      '%m/%d/%Y').date() if data[
				'start_date'] else datetime.datetime.today().date(),
			end_date=datetime.datetime.strptime(data['end_date'], '%m/%d/%Y').date() if data[
				'end_date'] else datetime.datetime.today().date()
		)

		task.save()
	except Exception as e:
		print(e)
		return {"status": False, "error": str(e), "data": {}}
	finally:
		db.close()

	return {"status": True, "error": "", "data": {}}


@tracker.get('/api/project')
def get_projects():
	projects: List[Project] = []
	try:
		db.connect()
		for project in Project.select():
			projects.append(project.dict())
	except Exception as e:
		print(e)
		return {"status": False, "error": str(e), "data": {}}
	finally:
		db.close()

	return {"status": True, "error": "", "data": projects}


@tracker.get('/api/project/<project_id:int>')
def get_project(project_id: int):
	try:
		db.connect()
		project: Project = Project.get(Project.id == int(project_id))
	except Exception as e:
		print(e)
		return {"status": False, "error": str(e), "data": {}}
	finally:
		db.close()

	return {"status": True, "error": "", "data": project.dict()}


@tracker.get('/api/projects/<project_id:int>/tasks')
def get_project_tasks(project_id: int):
	tasks: List[Task] = []
	try:
		db.connect()
		for task in Task.select(Task.project.id == int(project_id)):
			tasks.append(task.dict())
	except Exception as e:
		print(e)
		return {"status": False, "error": str(e), "data": {}}
	finally:
		db.close()

	return {"status": True, "error": "", "data": tasks}
