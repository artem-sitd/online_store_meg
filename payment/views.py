from rest_framework.views import APIView
from rest_framework.response import Response


class PaymentApiView(APIView):
    def post(self, request, **kwargs):
        number = request.data['number']
        name = request.data['name']
        month = request.data['month']
        year = request.data['year']
        code = request.data['code']
        return Response({number, name, month, year, code}, status=200)
