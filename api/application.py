from . import helper
from flask import Flask, request, Response
from flask_restx import Api, Resource

import json

flask_app = Flask(__name__)
app = Api(flask_app)

item_name_space = app.namespace('items', description='Route endpoints for items')


@item_name_space.route('/new', methods=['POST'])
class New_Item(Resource):
    def post(self):
        # Get item from the POST body
        req_data = request.get_json()
        item = req_data['item']

        # Add item to the list
        res_data = helper.add_to_list(item)

        # Return error if item not added
        if res_data is None:
            response = Response("{'error': 'Item not added - " + item + "'}", status=400 , mimetype='application/json')
            return response

        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')

        return response

@item_name_space.route('/all')
class All_Items(Resource):
    def get(self):

        res_data = helper.get_all_items()

        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')
        return {
            "data":res_data
        },200


@item_name_space.route('/status', methods=['GET'])
class Item_Status(Resource):
    def get(self):

        # Get parameter from the URL ie ?name=
        item_name = request.args.get('name')

        # Get items from the helper
        status = helper.get_item(item_name)

        # Return 404 if item not found
        if status is None:
            response = Response("{'error': 'Item Not Found - %s'}"  % item_name, status=404 , mimetype='application/json')
            return response

        # Return status
        res_data = {
            'status': status
        }

        response = Response(json.dumps(res_data), status=200, mimetype='application/json')
        return response

@item_name_space.route('/update', methods=['PUT'])
class Update_Item(Resource):
    def update_status(self):
        # Get item from the POST body
        req_data = request.get_json()
        item = req_data['item']
        status = req_data['status']

        # Update item in the list
        res_data = helper.update_status(item, status)

        # Return error if the status could not be updated
        if res_data is None:
            response = Response("{'error': 'Error updating item - '" + item + ", " + status   +  "}", status=400 , mimetype='application/json')
            return response

        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')

        return response


@item_name_space.route('/remove', methods=['DELETE'])
class Remove_Item(Resource):
    def delete(self):
        # Get item from the POST body
        req_data = request.get_json()
        item = req_data['item']

        # Delete item from the list
        res_data = helper.delete_item(item)

        # Return error if the item could not be deleted
        if res_data is None:
            response = Response("{'error': 'Error deleting item - '" + item +  "}", status=400 , mimetype='application/json')
            return response

        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')

        return response