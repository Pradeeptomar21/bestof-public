# Import Python Packages.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from django.conf import settings
from random import randint
from django.template.loader import render_to_string
import email.message
import smtplib
from django.contrib.auth import authenticate, login
# Import user define packages.
from .serializer import UpdatePasswordOtpSerializers, UpdatePasswordSerializers, UpdateProfileSerializers, GetProfileDataSerializers, UserDataSerializer
from custom_user.models import User
from BestofProject.tokens import CsrfExemptSessionAuthentication


# Create class for user registration.
class UpdatePasswordOtpView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)

    # Create function for post method.
    def post(self,request):
        if request.method == "POST":  # Check method is post or not.
            serializer = UpdatePasswordOtpSerializers(data=request.data)  # Call serializer function created by user.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                data['detail'] = "OTP sent to your registered email ID."  # Response as a successful message.
                data['status'] = 1
                data['user_id'] = serializer.validated_data.id  # Get user id from serializer response.
                # ====================================== SEND MAIL ===============
                logo_image = settings.BASE_URL + 'static/images/logo.png'
                yourname = serializer.validated_data.full_name
                user_email = serializer.validated_data.email
                otp = randint(1000, 9999)
                # data_content = {"BASE_URL": settings.BASE_URL, "yourname": yourname, "user_email": user_email, "otp":otp, "logo_image": logo_image}
                # email_content = render_to_string('email_template/bestof-update-password-otp.html', data_content)
                # msg = email.message.Message()
                # msg['Subject'] = 'OTP for update password.'
                # msg['From'] = settings.EMAIL_HOST_USER
                # msg['To'] = user_email
                # password = settings.EMAIL_HOST_PASSWORD
                # msg.add_header('Content-Type', 'text/html')
                # msg.set_payload(email_content)
                # s = smtplib.SMTP(settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT))
                # s.starttls()
                # s.login(msg['From'], password)
                # s.sendmail(msg['From'], [msg['To']], msg.as_string())
                # ====================================== SEND MAIL ===============
                User.objects.filter(email=user_email).update(otp=otp)  # Add otp in table for update password.
                data['otp'] = otp  # Get user id from serializer response.


            return Response(data)  # Send response as a API result.
# ======================================================================================================================


# Create class for user registration.
class UpdatePasswordView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)

    # Create function for post method.
    def post(self,request):
        if request.method == "POST":  # Check method is post or not.
            serializer = UpdatePasswordSerializers(data=request.data)  # Call serializer function created by user.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                data['detail'] = "Password updated."  # Response as a successful message.
                data['status'] = 1
                email = serializer.validated_data['email']  # Get user id from serializer response.
                password = serializer.validated_data['password']  # Get user id from serializer response.
                # data['user_instance'] = serializer.validated_data['user_instance']  # Get user id from serializer response.

                user = authenticate(email=email, password=password)
                login(request, user)
            return Response(data)  # Send response as a API result.
# ======================================================================================================================


# Create class for user registration.
class UpdateProfileView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)

    # Create function for post method.
    def post(self,request):
        if request.method == "POST":  # Check method is post or not.
            serializer = UpdateProfileSerializers(data=request.data)  # Call serializer function created by user.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                data['detail'] = "Profile updated."  # Response as a successful message.
                data['status'] = 1
                data['user_id'] = serializer.validated_data.id  # Get user id from serializer response.
            return Response(data)  # Send response as a API result.
# ======================================================================================================================


# Create class for user registration.
class GetProfileDataView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)

    # Create function for post method.
    def post(self,request):
        if request.method == "POST":  # Check method is post or not.
            serializer = GetProfileDataSerializers(data=request.data)  # Call serializer function created by user.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                user_id = serializer.validated_data.id

                user_detail = User.objects.filter(id=user_id).order_by("-id")
                get_data = UserDataSerializer(user_detail, many=True)
                data = get_data.data
                data_response = {'detail': "Get User Information.", 'status': 1, 'data': data}

                #
                #
                # data['detail'] = "Profile updated."  # Response as a successful message.
                # data['status'] = 1
                # data['user_id'] = serializer.validated_data # Get user id from serializer response.
                return Response(data_response)  # Send response as a API result.
# ======================================================================================================================
