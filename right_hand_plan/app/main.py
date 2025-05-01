from app import create_app
from .api.routes import api_blueprint

app = create_app()
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.run(debug=True)