# Importing necessary libraries and modules
from marshmallow import Schema, fields, validate, EXCLUDE

# Defining OrderItemSchema class
class OrderItemSchema(Schema):
    # Class Meta to exclude unknown fields
    class Meta:
        unknown = EXCLUDE

    # Defining fields for OrderItemSchema
    product = fields.String(required=True)
    size = fields.String(
        required=True, validate=validate.OneOf(["small", "medium", "big"])
    )
    quantity = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )

# Defining ScheduleOrderSchema class
class ScheduleOrderSchema(Schema):
    # Class Meta to exclude unknown fields
    class Meta:
        unknown = EXCLUDE

    # Defining fields for ScheduleOrderSchema which includes OrderItemSchema as nested object
    order = fields.List(fields.Nested(OrderItemSchema), required=True)

# Defining GetScheduledOrderSchema class which inherits from ScheduleOrderSchema class
class GetScheduledOrderSchema(ScheduleOrderSchema):
    # Defining additional fields for GetScheduledOrderSchema
    id = fields.UUID(required=True)
    scheduled = fields.DateTime(required=True)
    status = fields.String(
        required=True,
        validate=validate.OneOf(["pending", "progress", "cancelled", "finished"]),
    )

# Defining GetScheduledOrdersSchema class
class GetScheduledOrdersSchema(Schema):
    # Class Meta to exclude unknown fields
    class Meta:
        unknown = EXCLUDE

    # Defining fields for GetScheduledOrdersSchema which includes GetScheduledOrderSchema as nested object
    schedules = fields.List(fields.Nested(GetScheduledOrderSchema), required=True)

# Defining ScheduleStatusSchema class
class ScheduleStatusSchema(Schema):
    # Class Meta to exclude unknown fields
    class Meta:
        unknown = EXCLUDE

    # Defining fields for ScheduleStatusSchema
    status = fields.String(
        required=True,
        validate=validate.OneOf(["pending", "progress", "cancelled", "finished"]),
    )

# Defining GetKitchenScheduleParameters class
class GetKitchenScheduleParameters(Schema):
    # Class Meta to exclude unknown fields
    class Meta:
        unknown = EXCLUDE

    # Defining fields for GetKitchenScheduleParameters
    progress = fields.Boolean()
    limit = fields.Integer()
    since = fields.DateTime()
