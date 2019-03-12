from flask import Flask
from flask_bootstrap import Bootstrap

from frontend import frontend
from nav import nav

application = app = Flask('__name__')

Bootstrap(app)

app.register_blueprint(frontend)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = 'devkey'

nav.init_app(app)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)