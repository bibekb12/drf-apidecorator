from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
# Create your views here.
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items':'/',
        'Search by category' : '/?category = category_name',
        'Search by subcategory' : '/?subcategory = subcategory_name',
        'Add' : '/create',
        'Update' : '/update/pk',
        'Delete' : '/item/pk/delete'
    }
    return Response(api_urls)

@api_view(['post'])
def add_items(request):
    item = ItemSerializer(data = request.data)

    #validate for already existing data
    if Item.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
    
    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_items(request):

    #checking for the parameters in url
    if request.query_params:
        items = Item.objects.filter(**request.query_params.dict())
    else:
        items = Item.objects.all()

    # if there is something in item else raise error
    if items:
        serializer = ItemSerializer(items, many = True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def update_items(request,pk):
    item = Item.objects.get(pk=pk)
    data = ItemSerializer(instance = item, data=request.data)
    
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['delete'])
def delete_item(request,pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)