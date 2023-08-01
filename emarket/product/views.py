from django.shortcuts import render,get_object_or_404
from datetime import datetime, timedelta
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .filters import ProductFilter
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product
from rest_framework.pagination import PageNumberPagination
# Create your views here.

@api_view(['GET'])
def get_all_products(request):
    
    filters=ProductFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count = filters.qs.count()
    paginator=PageNumberPagination()
    pageSize=3
    paginator.page_size=pageSize
    queryset=paginator.paginate_queryset(filters.qs,request)
    ser= ProductSerializer( queryset,many=True)
    return Response({'Products':ser.data,'count':count})


@api_view(['GET'])
def get_product_py_id(request,pk):

    products =  get_object_or_404(Product,id=pk)
    ser= ProductSerializer(products,many=False)

    return Response({'msd':ser.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data = data)

    if serializer.is_valid():
        product = Product.objects.create(**data,user=request.user)
        res = ProductSerializer(product,many=False)
 
        return Response({"product":res.data})
    else:
        return Response(serializer.errors)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])

def update_product(request,pk):
    data = request.data
    serializer = ProductSerializer(data = data)
    
    if serializer.is_valid():
        product = get_object_or_404(Product,id=pk)
        if product.user != request.user:
            return Response({"error":"Sorry you can not update this product"}
                            , status=status.HTTP_403_FORBIDDEN),
        else:
            product.name = request.data['name']
            product.description = request.data['description']
            product.price = request.data['price']
            product.brand = request.data['brand']
            product.category = request.data['category']
            product.ratings = request.data['ratings']
            product.stock = request.data['stock']

            product.save()
            serializer = ProductSerializer(product,many=False)
            return Response({"product":serializer.data})

    else:
        return Response(serializer.errors)
        

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request,pk):
    product = get_object_or_404(Product,id=pk)

    if product.user != request.user:
        return Response({"error":"Sorry you can not update this product"}
                        , status=status.HTTP_403_FORBIDDEN)
     

    product.delete() 
    return Response({"details":"Delete action is done"},status=status.HTTP_200_OK)
