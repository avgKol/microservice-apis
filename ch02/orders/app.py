# Import the FastAPI module/library
from fastapi import FastAPI

# Create a new instance of FastAPI and enable debug mode
app = FastAPI(debug=True)

# Import the orders API module into the app (assumed to be in the orders/api folder)
from orders.api import api
