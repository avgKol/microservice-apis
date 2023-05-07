# Import necessary modules
from pathlib import Path
import yaml
from apispec import APISpec
from flask import Flask
from flask_smorest import Api

# Import blueprint object and configuration object
from api.api import blueprint
from config import BaseConfig

# Create new Flask application instance
app = Flask(__name__)

# Load configuration values from `BaseConfig`
app.config.from_object(BaseConfig)

# Instantiate a new API instance using the Flask app
kitchen_api = Api(app)

# Register the imported blueprint with the API instance
kitchen_api.register_blueprint(blueprint)

# Load OpenAPI specification file in YAML format
api_spec = yaml.safe_load((Path(__file__).parent / "oas.yaml").read_text())

# Create an instance of an OpenAPI spec using APISpec
spec = APISpec(
    title=api_spec["info"]["title"],
    version=api_spec["info"]["version"],
    openapi_version=api_spec["openapi"],
)

# Define a lambda function to return the original parsed YAML data and assign it to the `to_dict` attribute of `spec`
spec.to_dict = lambda: api_spec

# Assign the `spec` instance to the `spec` attribute of `kitchen_api`
kitchen_api.spec = spec

