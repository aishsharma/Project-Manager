import models
from router import tracker

if __name__ == '__main__':
	# Create tables if they don't exist
	models.init_db()

	# Starting the app
	tracker.run(debug=True, reloader=True)
