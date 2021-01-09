# Import Python Packages.
import requests
import json
import math
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404
# Import user define packages.Business_Details
from .serializer import BusinessInfoSerializers, GetBusinessInfoSerializer, BusinessVoteSerializers, BusinessLikeSerializers, BusinessSearchSerializers, SearchKeywordSerializers
from audits.models import Search_Keyword
from BestofProject.tokens import CsrfExemptSessionAuthentication
from .models import Business_categories, Business_Details, Business_Photos, Business_Time, Business_Posts


# Create class for Get Business information.
class YelpAPIView(APIView):
    # Create function for get method.
    def get(self, request):
        data = {}
        req = requests.get(settings.YELP_URL, params={"location":"Sanfransisco"}, headers=settings.YELP_HEADERS )
        data = json.loads(req.text)
        return Response(data)  # Send response as a API result.


# Create class for Get Business information using Business ID.
class BusinessInfoView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            serializer = BusinessInfoSerializers(data=request.data)  # Call serializer function created by user.
            if serializer.is_valid():  # Get data if serializer is valid.
                business_id = serializer.validated_data  # Get business id from serializer.
                if Business_Details.objects.filter(business_id=business_id).exists():  # Check business exist or not.
                    pass
                else:  # add business info from yelp.
                    req = requests.get(settings.YELP_ID_URL + business_id, headers=settings.YELP_HEADERS)  # Call yelp.
                    data = json.loads(req.text)  # get data from yelp
                    # ------------------------------------------------------------------------------------------------------
                    display_address = ""
                    for display_address_value in data['location']['display_address']:
                        if display_address:
                            display_address = display_address + " " + display_address_value
                        else:
                            display_address = display_address_value
                    # --------------------------------------------------------------------------------------------------
                    transactions_pickup = False
                    transactions_delivery = False
                    for transactions_value in data['transactions']:
                        if transactions_value == "delivery":
                            transactions_delivery = True
                        if transactions_value == "pickup":
                            transactions_pickup = True

                    # ---------------------------- Add business information --------------------------------------------
                    business_info = Business_Details(name=data['name'], business_id=data['id'],
                                                     image_url=data['image_url'],
                                                     business_display_address=display_address,
                                                     latitude=data['coordinates']['latitude'],
                                                     longitude=data['coordinates']['longitude'],
                                                     address1=data['location']['address1'],
                                                     address2=data['location']['address2'],
                                                     address3=data['location']['address3'],
                                                     city=data['location']['city'], country=data['location']['country'],
                                                     state=data['location']['state'],
                                                     zip_code=data['location']['zip_code'],
                                                     cross_streets=data['location']['cross_streets'],
                                                     phone=data['phone'], display_phone=data['display_phone'],
                                                     is_claimed=data['is_claimed'], is_closed=data['is_closed'],
                                                     transactions_pickup=transactions_pickup,
                                                     transactions_delivery=transactions_delivery
                                                     )
                    business_info.save()
                    # ---------------------------- Add category information --------------------------------------------
                    for category_value in data['categories']:
                        alias = category_value['alias']
                        title = category_value['title']
                        category_info = Business_categories(title=title, alias=alias, Business_id=business_info
                                                            )
                        category_info.save()
                    # ---------------------------- Add photos information ----------------------------------------------
                    for photo_value in data['photos']:
                        photos_info = Business_Photos(url=photo_value, Business_id=business_info
                                                      )
                        photos_info.save()
                    # ---------------------------- Add hours information -----------------------------------------------
                    for hours_value in data['hours']:
                        for open_value in hours_value['open']:
                            photos_info = Business_Time(is_overnight=open_value['is_overnight'],
                                                        start=open_value['start'], end=open_value['end'],
                                                        day=open_value['day'], Business_id=business_info
                                                        )
                            photos_info.save()
                # ---------------------------- Send business information -----------------------------------------------
                business_detail = Business_Details.objects.filter(business_id=business_id).order_by("-id")
                get_data = GetBusinessInfoSerializer(business_detail, many=True)
                data = get_data.data
                total_category = 0
                total_category_data = []
                business_instance = get_object_or_404(Business_Details, business_id=business_id)
                business_data = Business_Posts.objects.filter(Business_id=business_instance)
                for data_val in business_data:
                    if data_val.Category_id not in total_category_data:
                        total_category_data.append(data_val.Category_id)
                        for data_cat_val in data_val.post_activity_for.all():
                            if data_cat_val.Vote == True:
                                total_category = total_category + 1
                data_response = {'detail': "Get Business Information.", 'status': 1, 'data': data, 'total_category':total_category}

                return Response(data_response)


# Create class for business vote.
class BusinessGetInfoView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            business_detail = Business_Details.objects.all().order_by("-id")
            get_data = GetBusinessInfoSerializer(business_detail, many=True)
            data = get_data.data
            data_response = {'detail': "Get Business Information.", 'status': 1, 'data': data}

            return Response(data_response)


# Create class for business Search.
class BusinessSearchView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]
    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            serializer = BusinessSearchSerializers(data=request.data)  # Call serializer function created by user.
            if serializer.is_valid():  # Get data if serializer is valid.
                name = serializer.validated_data["name"]  # Get name from serializer.
                latitude2 = float(serializer.validated_data["latitude"])  # Get latitude from serializer.
                longitude2 = float(serializer.validated_data["longitude"])  # Get longitude from serializer.
                distance = serializer.validated_data["distance"]  # Get distance from serializer.
                # ------------------------------ caluculate distance ----------------------------------------
                R = 6373.0
                lat1 = math.radians(latitude2)
                lon1 = math.radians(longitude2)
                get_business_id = []
                business_detail = Business_Details.objects.all().order_by("-id")
                for data_value in business_detail:
                    latitude2 = float(data_value.latitude)
                    longitude2 = float(data_value.longitude)
                    lat2 = math.radians(latitude2)
                    lon2 = math.radians(longitude2)
                    dlon = lon1 - lon2
                    dlat = lat1 - lat2
                    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                    get_distance = R * c
                    if get_distance <= int(distance) :
                        get_business_id.append(data_value.id)
                business_detail_value = Business_Details.objects.filter(id=get_business_id[0]).filter(name__icontains=name).order_by("-id")
                for data_value in get_business_id:
                    business_detail = Business_Details.objects.filter(id=data_value).filter(name__icontains=name).order_by("-id")
                    if business_detail in business_detail_value:
                        pass
                    else:
                        business_detail_value = business_detail_value | business_detail
                get_data = GetBusinessInfoSerializer(business_detail_value, many=True)
                data = get_data.data
            else:
                data=[]
            data_response = {'detail': "Get Business Information.", 'status': 1, 'data': data}
            return Response(data_response)

# Create class for business vote.
class BusinessVoteView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            serializer = BusinessVoteSerializers(data=request.data)  # Call serializer function business vote.
            if serializer.is_valid():  # Get data if serializer is valid.
                user_id = serializer.validated_data  # Get information after vote from serializer.
                data_response = {'detail': "Vote successfully.", 'status': 1, 'user_id': user_id}

                return Response(data_response)


# Create class for business vote.
class BusinessLikeView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            serializer = BusinessLikeSerializers(data=request.data)  # Call serializer function business vote.
            if serializer.is_valid():  # Get data if serializer is valid.
                display_message = serializer.validated_data  # Get information after vote from serializer.
                data_response = {'detail': display_message, 'status': 1}

                return Response(data_response)



# Create class for business vote.
class SearchKeywordView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            serializer = SearchKeywordSerializers(data=request.data)  # Call serializer function business vote.
            if serializer.is_valid():  # Get data if serializer is valid.
                data_response = {'detail': "Keyword added.", 'status': 1}

                return Response(data_response)
