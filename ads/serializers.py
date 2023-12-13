from rest_framework import serializers
from .models import Advertisement, Location, DailyVisitorCount



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'location_name', 'max_daily_visitors', 'visitor_count', 'created_at']
        read_only_fields = ['id']

class AdvertisementSerializer(serializers.ModelSerializer):
    
    locations = LocationSerializer(many=True, read_only=True)
    location_ids = serializers.ListField(write_only=True, allow_empty=False, source='locations')

    class Meta:
        model = Advertisement
        fields = ['id', 'ad_name', 'end_date','ad_blocked', 'created_at', 'locations', 'location_ids']
        read_only_fields = ['id','ad_blocked']

    def create(self, validated_data):
        location_ids = validated_data.pop('locations')
        print("Location IDs Coming in the request:--------->>>", location_ids) 

        advertisement = Advertisement.objects.create(**validated_data)

        for location_id in location_ids:
            location = Location.objects.get(id=location_id)
            advertisement.locations.add(location)
        return advertisement

    def update(self, instance, validated_data):
        instance.ad_name = validated_data.get('ad_name', instance.ad_name)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.ad_blocked = validated_data.get('ad_blocked', instance.ad_blocked)
        instance.save()
        if 'locations' in validated_data:
            instance.locations.clear()
            for location_id in validated_data['locations']:
                location = Location.objects.get(id=location_id)
                instance.locations.add(location)

        return instance
    


class DailyVisitorCountSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer()

    class Meta:
        model = DailyVisitorCount
        fields = ['today_date', 'advertisement', 'visitor_count']

    def to_representation(self, instance):
        # Custom representation to show only required fields
        return {
            'today_date': instance.today_date,
            'ad_id': instance.advertisement.id,
            'ad_name': instance.advertisement.ad_name,
            'visitor_count': instance.visitor_count,
        }