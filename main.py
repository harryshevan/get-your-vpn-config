import configparser
import logging

from flask import Flask

from admin_manager import AdminManager
from admin_route import AdminController
from openvpn_api import OpenvpnApi
from persistant import Persistent

config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(level=config.get('logging', 'level', fallback='INFO'),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    persist = Persistent(config['sqlite']['FilePath'])
    admin_manager = AdminManager(persist)
    openvpn_api = OpenvpnApi(config['openvpn-http-api']['Uri'], config['openvpn-http-api']['RootPassword'])
    app = Flask(__name__)

    admin_controller = AdminController(admin_manager)

    app.register_blueprint(admin_controller.blueprint())
    app.run(port=8080)
