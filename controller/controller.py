# controller.py
import logging
from flask_restx import Namespace, Resource, fields, reqparse
from flask import jsonify, request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.service import RecommendationService

logger = logging.getLogger(__name__)

recommendation_controller = Namespace('recommendations', description='Recommendation operations')
recommendation_service = RecommendationService()

recommendation_parser = reqparse.RequestParser()
recommendation_parser.add_argument('data_source', type=str, required=True, help='Data source (csv or database)', location='form')
recommendation_parser.add_argument('csv_model', type=str, required=False, help='CSV file path', location='form')
recommendation_parser.add_argument('db_model', type=str, required=False, help='Database table name from which you want to get the recomendation', location='form')
recommendation_parser.add_argument('db_engine', type=str, required=False, help='Database engine details. exp: mysql://bdUser:dbPassw0rd@dbHost.com/dbName', location='form')
recommendation_parser.add_argument('sorting_fields', type=str, required=True, help='list of three field name you want to use for getting recomendation. exp: ["field1", "field2"]', location='form')
recommendation_parser.add_argument('filte_column_name', type=str, required=False, help='Provide column name based on which you want to filter data from table', location='form')
recommendation_parser.add_argument('filte_column_value', type=str, required=False, help='Provide column value based on which you want to filter data from table', location='form')

recommendation_response = recommendation_controller.model('RecommendationResponse', {
    'recommendations': fields.List(fields.Raw, description='Top recommendations')
})

# Define parser for headers
header_parser = reqparse.RequestParser()
header_parser.add_argument('Authorization', type=str, required=False, help='Bearer token', location='headers')
header_parser.add_argument('Content-Type', type=str, required=False, help='Content type', location='headers')


@recommendation_controller.route('/recommendations')
class RecommendationResource(Resource):
    # @jwt_required()
    @recommendation_controller.expect(header_parser, recommendation_parser)
    @recommendation_controller.response(200, 'Success', recommendation_response)
    def post(self):
        # current_user = get_jwt_identity()
        try:
            current_user = "xyz"
            request_data = recommendation_parser.parse_args()
            # Extract headers from the request
            headers = {
                'Authorization': request.headers.get('Authorization'),
                'Content-Type': request.headers.get('Content-Type')
            }
            # request_data = request.json
            logger.info(f"Received recommendation request from user: {current_user}")
            recommendations = recommendation_service.get_recommendations(current_user, request_data)
            logger.info(f"Recommendations successfully generated for user: {current_user}")
            return jsonify(recommendations)
        except Exception as e:
            logger.error(f"An error occurred while generating recommendations for user {current_user}: {str(e)}")
            return {"error": str(e)}, 500
