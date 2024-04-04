import os
from gunicorn.app.base import BaseApplication
from StartUp import app

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application

if __name__ == "__main__":
    # Use environment variables or default values
    bind_ip = os.environ.get("WSGI_IP_DEFAULT", "0.0.0.0")
    bind_port = os.environ.get("WSGI_PORT_DEFAULT", "5000")

    options = {
        'bind': f'{bind_ip}:{bind_port}',  # Set the desired host and port
        'workers': 4, # Adjust the number of workers as needed
    }

    StandaloneApplication(app, options).run()