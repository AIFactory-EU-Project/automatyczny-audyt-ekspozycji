from ai_service.api.common.helpers import create_app
from ai_service.api.common.logger import configure_logging

configure_logging()

app = create_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7552, debug=True)

