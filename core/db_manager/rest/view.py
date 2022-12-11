from db_manager.models import Vehicle
from db_manager.rest.api import GetDataByNameRequest, VehicleSerializer
from db_manager.rest.token import BearerAuthentication
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class VehicleViewREST(APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    authentication_classes = [SessionAuthentication, BearerAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """Пост запрос для получения информации об авто."""
        try:
            serializer = GetDataByNameRequest(data=request.data)
        except ValueError:
            raise ValueError("Input value is bad!")
        if serializer.is_valid():
            # serializer.data['brand']
            # serializer.data['model']
            # serializer.data['generation']
            queryset = Vehicle.objects.filter(name='Toyota')
            serializer = VehicleSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
