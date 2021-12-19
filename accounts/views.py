
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from .models import User, City
from .serializers import ( 
                          UpdateUserSerializer,
                          UserSerializer, 
                          LoginSerializer,
                        )
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .permissions import CustomPermission

# Create your views here.

class RegisterUserView(CreateAPIView):
    """This api registers a user by taking the details """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # this is the better way of writing createAPIview
    def create(self, request, *args, **kwargs):
        # the super method will send data to serializer create instance
        user = super().create(request, *args, **kwargs)
        response = dict()
        response["email"] = user.data.get('email')
        response["message"] = "User registered successfully"
        return Response(response)
        
        
class LoginView(CreateAPIView):
    """This api logs a user into the system"""
    
    serializer_class = LoginSerializer
    
    def post(self, request):
        data = request.data
        response = dict()
        try:
            user = User.objects.get(email=data["email"])
            token = Token.objects.get_or_create(user=user, )
            response["user_id"] = user.id
            response["token"] = token[0].key
        except Exception as e:
            response["message"] = str(e)
        return Response(response) 
        
class LogoutView(APIView):
    """This api logs out a user"""
    
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        request.user.auth_token.delete()
        return Response({"message": "successfully logged out"})
    
class UpdateUserData(RetrieveUpdateAPIView):
    """This api lets the currently logged in user to view and update his/her details"""
    
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated, CustomPermission]


    
    
    