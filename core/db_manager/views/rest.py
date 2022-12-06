from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from db_manager.models import Vehicle
from db_manager.rest.api import VehicleSerializer, GetDataByNameRequest


class VehicleViewREST(APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """

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
