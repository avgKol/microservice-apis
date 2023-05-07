# Import necessary modules
import copy
import uuid
from datetime import datetime

from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

# Import schema objects used for validation
from api.schemas import (
    GetScheduledOrderSchema,
    ScheduleOrderSchema,
    GetKitchenScheduleParameters,
    GetScheduledOrdersSchema,
    ScheduleStatusSchema,
)

# Create a new Flask Blueprint instance for the Kitchen API
blueprint = Blueprint("kitchen", __name__, description="Kitchen API")

# Initialize an empty list to hold schedules
schedules = []


def validate_schedule(schedule):
    """
    Validates the input schedule data, checking that it adheres to the `GetScheduledOrderSchema`.
    Args:
        schedule (dict): A dictionary containing schedule details.
    Returns:
        None. If the schedule data fails validation, a `ValidationError` is raised.
    """
    # Use deepcopy to ensure original schedule remains unmodified
    schedule = copy.deepcopy(schedule)
    # Convert scheduled time to ISO format before validating
    schedule["scheduled"] = schedule["scheduled"].isoformat()
    errors = GetScheduledOrderSchema().validate(schedule)
    if errors:
        raise ValidationError(errors)


@blueprint.route("/kitchen/schedules")
class KitchenSchedules(MethodView):
    """
    Flask class-based view for retrieving and creating kitchen schedules.
    """
    @blueprint.arguments(GetKitchenScheduleParameters, location="query")
    @blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
    def get(self, parameters):
        """
        Retrieve a list of kitchen schedules based on query parameters.

        Args:
            parameters (dict): Query parameters to filter or limit schedules returned.
        Returns:
            A dictionary containing a list of filtered schedules.
        """
        for schedule in schedules:
            validate_schedule(schedule)

        if not parameters:
            return {"schedules": schedules}

        query_set = [schedule for schedule in schedules]

        cancelled = parameters.get("cancelled")
        if cancelled is not None:
            if cancelled:
                query_set = [
                    schedule
                    for schedule in schedules
                    if schedule["status"] == "cancelled"
                ]
            else:
                query_set = [
                    schedule
                    for schedule in schedules
                    if schedule["status"] != "cancelled"
                ]

        since = parameters.get("since")
        if since is not None:
            query_set = [
                schedule for schedule in schedules if schedule["scheduled"] >= since
            ]

        limit = parameters.get("limit")
        if limit is not None and len(query_set) > limit:
            query_set = query_set[:limit]

        return {"schedules": query_set}

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=201, schema=GetScheduledOrderSchema)
    def post(self, payload):
        """
        Create a new kitchen schedule.

        Args:
            payload (dict): A dictionary containing the new schedule details.
        Returns:
            A dictionary containing the newly created kitchen schedule.
        """
        # Generate a UUIDv4 id and add to the payload
        payload["id"] = str(uuid.uuid4())
        # Set scheduled time to current UTC datetime
        payload["scheduled"] = datetime.utcnow()
        # Set default status to 'pending'
        payload["status"] = "pending"
        # Append the new schedule to the list of existing schedules
        schedules.append(payload)
        validate_schedule(payload)
        return payload


@blueprint.route("/kitchen/schedules/<schedule_id>")
class KitchenSchedule(MethodView):
    """
    Flask class-based view for retrieving, updating, and deleting individual kitchen schedules.
    """
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def get(self, schedule_id):
        """
        Retrieve details for a specific kitchen schedule.

        Args:
            schedule_id (str): The UUIDv4 id of the schedule to retrieve.
        Returns:
            A dictionary containing the details of the specified schedule.
        """
        for schedule in schedules:
            if schedule["id"] == schedule_id:
                validate_schedule(schedule)
                return schedule
        abort(404, description=f"Resource with ID {schedule_id} not found")

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def put(self, payload, schedule_id):
        """
        Update an existing kitchen schedule.

        Args:
            payload (dict): A dictionary containing the updated schedule details.
            schedule_id (str): The UUIDv4 id of the schedule to update.
        Returns:
            A dictionary containing the updated schedule details.
        """
        for schedule in schedules:
            if schedule["id"] == schedule_id:
                # Update the existing schedule with the new payload data
                schedule.update(payload)
                validate_schedule(schedule)
                return schedule
        abort(404, description=f"Resource with ID {schedule_id} not found")

    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        """
        Delete an existing kitchen schedule.

        Args:
            schedule_id (str): The UUIDv4 id of the schedule to delete.
        Returns:
            None.
        """
        for index, schedule in enumerate(schedules):
            if schedule["id"] == schedule_id:
                # Remove the schedule from the list of schedules
                schedules.pop(index)
                return
        abort(404, description=f"Resource with ID {schedule_id} not found")


@blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
@blueprint.route("/kitchen/schedules/<schedule_id>/cancel", methods=["POST"])
def cancel_schedule(schedule_id):
    """
    Cancel a specific kitchen schedule.

    Args:
        schedule_id (str): The UUIDv4 id of the schedule to cancel.
    Returns:
        A dictionary containing the cancelled schedule's details.
    """
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            # Set status of specified schedule to 'cancelled'
            schedule["status"] = "cancelled"
            validate_schedule(schedule)
            return schedule
    abort(404, description=f"Resource with ID {schedule_id} not found")


@blueprint.response(status_code=200, schema=ScheduleStatusSchema)
@blueprint.route("/kitchen/schedules/<schedule_id>/status", methods=["GET"])
def get_schedule_status(schedule_id):
    """
    Retrieve the status of an existing kitchen schedule.

    Args:
        schedule_id (str): The UUIDv4 id of the schedule to retrieve the status of.
    Returns:
        A dictionary containing the status of the specified schedule.
    """
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            validate_schedule(schedule)
            return {"status": schedule["status"]}
    abort(404, description=f"Resource with ID {schedule_id} not found") 
