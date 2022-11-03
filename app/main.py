from flask import Flask, render_template, request, jsonify
from handler import configure_routes

apps = Flask(__name__)
configure_routes(apps)

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    apps.run(host="0.0.0.0")