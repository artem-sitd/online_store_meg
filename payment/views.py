from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class PaymentApiView(APIView):
    def post(self, request: Request, **kwargs) -> Response:
        number = request.data["number"]
        name = request.data["name"]
        month = request.data["month"]
        year = request.data["year"]
        code = request.data["code"]
        return Response({number, name, month, year, code}, status=200)
