# Import Python Packages.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from django.conf import settings
from django.contrib.auth import login
from random import randint
from django.template.loader import render_to_string
import email.message
import smtplib
# Import user define packages.
from .serializer import UserRegistrationSerializers, UserLoginSerializers, UserActivateSerializers
from custom_user.models import User
from BestofProject.tokens import CsrfExemptSessionAuthentication


# Create class for user registration.
class UserRegistrationView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)

    # Create function for post method.
    def post(self,request):
        if request.method == "POST":  # Check method is post or not.
            serializer = UserRegistrationSerializers(data=request.data)  # Call serializer function created by user.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                data['detail'] = "Account create successfully"  # Response as a successful message.
                data['status'] = 1
                data['user_id'] = serializer.validated_data.id  # Get user id from serializer response.
                # ====================================== SEND MAIL ===============
                logo_image = settings.BASE_URL + 'static/images/logo.png'
                yourname = serializer.validated_data.full_name
                user_email = serializer.validated_data.email
                otp = randint(1000, 9999)
                data_content = {"BASE_URL": settings.BASE_URL, "yourname": yourname, "user_email": user_email, "otp":otp, "logo_image": logo_image}
                # email_content = render_to_string('email_template/bestof-activation-otp.html', data_content)
                # msg = email.message.Message()
                # msg['Subject'] = 'Account verification link.'
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
                User.objects.filter(email=user_email).update(otp=otp)  # Add otp in table for registration.
                data['otp'] = str(otp) # Get user id from serializer response.

            return Response(data)  # Send response as a API result.
# ======================================================================================================================


# Create class for user login.
class UserLoginView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)

    # Create function for post method.
    def post(self,request):
        if request.method == "POST":  # Check method is post or not.
            serializer = UserLoginSerializers(request, data=request.data)  # Call serializer function for user login.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                login(request, serializer.validated_data)   # Login function.
                data['detail'] = "Logged in successfully"  # Response as a successful message.
                data['status'] = 1
                data['user_id'] = serializer.validated_data.id  # Get user id from serializer response.
            return Response(data)  # Send response as a API result.
# ======================================================================================================================


# Create class for user activate.
class UserActivateView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)

    # Create function for post method.
    def post(self,request):
        if request.method == "POST":  # Check method is post or not.
            serializer = UserActivateSerializers(request, data=request.data)   # Serializer function for activation.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                data['detail'] = "Account activate successfully"  # Response as a successful message.
                data['status'] = 1
                data['user_id'] = serializer.validated_data.id  # Get user id from serializer response.
            return Response(data)  # Send response as a API result.
# ======================================================================================================================
