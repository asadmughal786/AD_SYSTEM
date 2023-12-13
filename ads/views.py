from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Advertisement, Location, DailyVisitorCount
from .serializers import AdvertisementSerializer, LocationSerializer, DailyVisitorCountSerializer
from .helpers import check_visitor_count, create_daily_visitor_counts


class AdvertisementView(APIView):
    '''
    GET:{pk}
    POST : {
    "ad_name": "New Advertisement",
    "end_date": "2023-12-31",
    "location_ids": [1, 2, 3],
    "ad_blocked": false
    }
    PUT: QUERY PARAMS {PK}
    {
    "ad_name": "New Advertisement",
    "end_date": "2023-12-31",
    "location_ids": [1, 2, 3],
    "ad_blocked": false
    }
    PATCH: QUERY PARAMS {PK}
    {
    "ad_name": "New Advertisement",
    "end_date": "2023-12-31",
    "location_ids": [1, 2, 3],
    "ad_blocked": false
    }
    DELETE: QUERY PARAMS {PK}
    '''
    def get(self, request, pk=None, format=None):
        try:
            if pk is not None:
                check_visitor_count(pk)
                create_daily_visitor_counts(pk)
                advertisements = Advertisement.objects.filter(locations__id=pk, ad_blocked=False)
                serializer = AdvertisementSerializer(advertisements, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            advertisements = Advertisement.objects.all().order_by('-created_at')
            serializer = AdvertisementSerializer(advertisements, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    '''
    JSON Format to create post
    {
    "ad_name": "New Advertisement",
    "end_date": "2023-12-31",
    "location_ids": [1, 2, 3],
    "ad_blocked": false
    }
    '''

    def post(self, request, format=None):
        try:
            serializer = AdvertisementSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'msg': 'Validation error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'msg': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    '''
    JSON Format to complete update post
    {
    "ad_name": "New Advertisement",
    "end_date": "2023-12-31",
    "location_ids": [1, 2, 3],
    "ad_blocked": false
    }
    '''
    def put(self, request, pk=None, format=None):
        try:
            advertisement = get_object_or_404(Advertisement, id=pk)
            serializer = AdvertisementSerializer(advertisement, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg': 'Validation error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'msg': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    '''
    JSON Format to patch/partial update post
    {
    "ad_name": "New Advertisement",
    "end_date": "2023-12-31",
    "location_ids": [1, 2, 3],
    "ad_blocked": false
    }
    '''
    def patch(self, request, pk=None, format=None):
        try:
            advertisement = get_object_or_404(Advertisement, id=pk)
            serializer = AdvertisementSerializer(advertisement, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg': 'Validation error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'msg': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    '''
    Delete {pk}
    '''
    def delete(self, request, pk=None, format=None):
        try:
            advertisement = get_object_or_404(Advertisement, id=pk)
            advertisement.delete()
            return Response({'msg': 'Advertisement deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'msg': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LocationView(APIView):
    '''
    GET: {pk}
    
    POST: {
    "location_name": "New Location",
    "max_daily_visitors": 100
    }
    
    PUT: QUERY PARAMS {PK}
    {
    "location_name": "New Location",
    "max_daily_visitors": 100
    }
    
    PATCH: QUERY PARAMS {PK}
    {
    "location_name": "New Location",
    }
    
    DELETE: QUERY PARAMS {pk}
    
    '''
    
    
    def get(self, request, pk=None, format=None):
        try:
            if pk is not None:
                location = get_object_or_404(Location, id=pk)
                serializer = LocationSerializer(location)
            else:
                locations = Location.objects.all().order_by("-created_at")
                serializer = LocationSerializer(locations, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    '''
    JSON Formate to create locations
    {
    "location_name": "New Location",
    "max_daily_visitors": 100
    }
    '''
    
    def post(self, request, format=None):
        try:
            serializer = LocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'msg': 'Validation error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'msg': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk=None, format=None):
        try:
            location = get_object_or_404(Location, id=pk)
            serializer = LocationSerializer(location, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg': 'Validation error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'msg': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None, format=None):
        try:
            location = get_object_or_404(Location, id=pk)
            location.delete()
            return Response({'msg': 'Location deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'msg': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DailyVisitorCountView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = DailyVisitorCount.objects.all()
        serializer = DailyVisitorCountSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
