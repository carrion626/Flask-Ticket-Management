from app import create_app
from data.config import config

app = create_app()


if __name__ == '__main__':
    # print(app.url_map)
    print(f'link for localhost: http://localhost:{config.FLASK_PORT}/index')
    app.run(debug=True, port=config.FLASK_PORT)
