from django.http import Http404

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

    def get(self, request, format=None):
        data_serializer = GetDataByNameRequest(data=request.data)
        if data_serializer.is_valid():
            brand = self.get_object_or_404(
                'Указанный брэнд не найден',
                name__iexact=request.data.get('brand'),
                _type=Vehicle.Type.BRAND.value
            )
            model = self.get_object_or_404(
                'Указанная модель не найдена',
                parent=brand,
                name__iexact=request.data.get('model'),
                _type=Vehicle.Type.MODEL.value
            )
            generation = self.get_object_or_404(
                'Указанное поколение не найдено',
                parent=model,
                name__iexact=request.data.get('generation'),
                _type=Vehicle.Type.GENERATION.value
            )
            serializer = VehicleSerializer(generation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_object_or_404(error_text: str = None, **kwargs) -> Vehicle:
        try:
            return Vehicle.objects.get(**kwargs)
        except Vehicle.DoesNotExist:
            raise Http404(error_text)
