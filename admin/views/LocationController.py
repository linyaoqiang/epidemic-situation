from django.http import JsonResponse
from django.core import serializers
from admin.models.location import *


class LocationController:
    def get_city(self, request, province_id):
        data = City.objects.filter(province_id=province_id)
        data = serializers.serialize('json', queryset=data)
        return JsonResponse(data, safe=False)

    def get_areas(self, request, province_id, city_id):
        data = Area.objects.filter(city_id=city_id)
        data = serializers.serialize('json', queryset=data)
        return JsonResponse(data, safe=False)

    def fetch_city(self, request, city_id):
        cities = City.objects.filter(id=city_id)
        city_json = serializers.serialize('json', queryset=cities)
        return JsonResponse(city_json, safe=False)

