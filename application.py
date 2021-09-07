from flask import Flask, request, Response
from flask_restx import Api, Resource, fields
import helper
import json


application = Flask(__name__)
app = Api(app=application, version="1.0", title="Todo API Example")

item_name_space = app.namespace("items", description="Route endpoints for items")

item_model = app.model(
        "Item Model",
        {
            "item": fields.String(
                required=True,
                description="Name of the item/todo task",
                help="Name cannot be blank.",
            )
        },
    )
item_with_status_model = app.model(
        "Item w/ Status Model",
        {
            "item": fields.String(
                required=True,
                description="Name of the item/todo task",
                help="Name cannot be blank.",
            ),
            "status": fields.String(
                required=True,
                description="Status of the item/todo task the only accepted values are: not started, in progress, and completed",
                help="Status cannot be blank.",
            )
        },
    )


@item_name_space.route("/new")
class New_Item(Resource):
    @app.doc(
        responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    )
    @app.expect(item_model, validate=True)
    def post(self):
        # Get item from the POST body
        req_data = request.get_json()
        item = req_data["item"]

        # Add item to the list
        res_data = helper.add_to_list(item)

        # Return error if item not added
        if res_data is None:
            response = Response(
                "{'error': 'Item not added - " + item + "'}",
                status=400,
                mimetype="application/json",
            )
            return response

        # Return response
        response = Response(json.dumps(res_data), mimetype="application/json")

        return response


@item_name_space.route("/all")
class All_Items(Resource):
    def get(self):

        res_data = helper.get_all_items()

        # Return response
        response = Response(json.dumps(res_data), mimetype="application/json")
        return {"data": res_data}, 200


@item_name_space.route("/status/<string:name>")
class Item_Status(Resource):
    @app.doc(
        responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
        params={"name": "Specify the name of the task"},
    )
    def get(self, name):

        # obtain name from url
        item_name = name

        # Get items from the helper
        status = helper.get_item(item_name)

        # Return 404 if item not found
        if status is None:
            response = Response(
                "{'error': 'Item Not Found - %s'}" % item_name,
                status=404,
                mimetype="application/json",
            )
            return response

        # Return status
        res_data = {"status": status}

        response = Response(
            json.dumps(res_data), status=200, mimetype="application/json"
        )
        return response


@item_name_space.route("/update")
class Update_Item(Resource):
    
    @app.expect(item_with_status_model, validate=True)
    def put(self):
        # Get item from the POST body
        req_data = request.get_json()
        item = req_data["item"]
        status = req_data["status"]

        # Update item in the list
        res_data = helper.update_status(item, status)

        # Return error if the status could not be updated
        if res_data is None:
            response = Response(
                "{'error': 'Error updating item - '" + item + ", " + status + "}",
                status=400,
                mimetype="application/json",
            )
            return response

        # Return response
        response = Response(json.dumps(res_data), mimetype="application/json")

        return response


@item_name_space.route("/remove")
class Remove_Item(Resource):

    @app.expect(item_model, validate=True)
    def delete(self):
        # Get item from the POST body
        req_data = request.get_json()
        item = req_data["item"]

        # Delete item from the list
        res_data = helper.delete_item(item)

        # Return error if the item could not be deleted
        if res_data is None:
            response = Response(
                "{'error': 'Error deleting item - '" + item + "}",
                status=400,
                mimetype="application/json",
            )
            return response

        # Return response
        response = Response(json.dumps(res_data), mimetype="application/json")

        return response

if __name__ == '__main__':
    application.run()