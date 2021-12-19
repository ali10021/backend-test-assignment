from django.db.models.aggregates import Count
from accounts.permissions import CustomPermissionForSalesData
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from sales.models import SalesData
from accounts.models import Country
from .serializers import ( 
                          SalesDataSerializer,
                          CountrySerializer
                        )
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .utils import calculate_average_sales, calculate_average_sales_for_all_users, customResponse
from django.db.models import Max
from django.db.models import F   
        
# Create your views here.
class Statistics(APIView):
    """"This api returns the stats of sales"""
    
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        custom_response = customResponse()
        sales_data = SalesData.objects.filter(user_id=request.user)
        sales_data_all_user = SalesData.objects.all()
        max_revenue = SalesData.objects.filter(user_id=request.user).values('revenue', sale_id=F('id')).order_by('-revenue').first()
        product_highest_revenue_for_current_user = SalesData.objects.filter(user_id=request.user).values(product_name=F('product'), price=F('sales_number')).order_by('-revenue').first()
        product_highest_sales_number_for_current_user = SalesData.objects.filter(user_id=request.user).values(product_name=F('product'), price=F('sales_number')).order_by('-sales_number').first()
        average_sales = calculate_average_sales(sales_data)
        average_sales_all_user = calculate_average_sales_for_all_users(sales_data_all_user)
        custom_response.addKey("average_sales_for_current_user", average_sales)
        custom_response.addKey("average_sale_all_user", average_sales_all_user)
        custom_response.addKey("highest_revenue_sale_for_current_user", max_revenue)
        custom_response.addKey("product_highest_revenue_for_current_user", product_highest_revenue_for_current_user)
        custom_response.addKey("product_highest_sales_number_for_current_user", product_highest_sales_number_for_current_user)
        return Response(custom_response.getResponse())
    
class SalesView(RetrieveUpdateDestroyAPIView):
    """This api enables a user to view, update or delete a sales' record"""
    
    queryset = SalesData.objects.all()
    serializer_class = SalesDataSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated,CustomPermissionForSalesData]
    

class CreateSalesView(ListCreateAPIView):
    """This api creates and lists sales' data """
    
    queryset = SalesData.objects.all()
    serializer_class = SalesDataSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    
class ListCountries(ListAPIView):
    """This api lists all countries"""
    
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = (TokenAuthentication, )
    permission_classßes = [IsAuthenticated]
