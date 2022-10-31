from email.policy import HTTP
import imp
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from business.models import Customer
from api.serializers import CustomerSerializer
from rest_framework import status
from functools import wraps

# Create your views here.
class CustomerView(APIView):
    def get(self, request, format=None):
        customers = Customer.published.all()    # select all customer whose status = published instead of saying
                                                # Customer.object.filter(status='published')
        serializer = CustomerSerializer(customers, many=True) #since we need to return more than one items
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def resource_checker(model):
        def check_entity(fun):
            @wraps(fun)
            def inner_fun(*args, **kwargs):
                try:
                    x = fun(*args, **kwargs)
                    return x
                except model.DoesNotExist:
                    return Response({'messg':'Not Found'}, status=status.HTTP_204_NO_CONTENT)
            return inner_fun
        return check_entity

class CustomerDetailView(APIView):

    @resource_checker(Customer)
    def get(self, request, pk, format=None):
        customer = Customer.published.get(pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @resource_checker(Customer)   
    def put(self, request, pk, format=None):
        customer = Customer.published.get(pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @resource_checker(Customer)
    def delete(self, request, pk, format=None):
        customer = Customer.published.get(pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
