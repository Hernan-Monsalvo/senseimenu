from .models import Dish, WeekMenu
from .utils import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser
from rest_framework import status
import json


def get_data(request):
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return data


class DishView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        dishes = Dish.objects.filter(owner=user)
        type = request.query_params.get('type')
        if type is not None:
            dishes = filterDishes(type, dishes)
        serializer = DishSerializer(dishes, many=True)
        return Response(serializer.data)

    def post(self, request):

        user = request.user
        data = get_data(request)
        data['owner'] = user
        newData = ingredientsToString(data)
        serializer = DishSerializer(data=newData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DishDetailView(APIView):

    def get(self, request, pk):
        try:
            dish = Dish.objects.get(pk=pk, user=request.user)
        except Dish.DoesNotExist:
            return Response(status=404)
        serializer = DishSerializer(dish)
        return Response(serializer.data)


class MenuRandomView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        try:
            config = get_data(request)['config']
        except KeyError as e:
            print(e)
            return Response({"Error": "no config"}, status=400)

        if len(config) == 14:
            print(config)
        else:
            return Response({"Error": "config needs to have 14 elements"}, status=400)

        menu = randomMenu(config, user)
        return Response({"data": menu}, status=200)


class MenuView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        menus = WeekMenu.objects.filter(owner=user)

        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        try:
            data = get_data(request)
        except KeyError as e:
            print(e)
            return Response({"Error": "no data"}, status=400)

        data['owner'] = user
        serializer = MenuSerializer(data=dishListToDict(data))
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetailView(APIView):

    def get(self, request, pk):
        user = request.user
        try:
            menu = WeekMenu.objects.get(pk=pk, owner=user)
        except WeekMenu.DoesNotExist:
            return Response(status=404)
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

class ShopListView(APIView):

    def get(self, request, pk):
        user = request.user
        try:
            menu = WeekMenu.objects.get(pk=pk, owner=user)
        except WeekMenu.DoesNotExist:
            return Response(status=404)

        if not menu.shopping_list:
            menu.create_shoping_list()

        list = menu.get_shoping_list()

        return Response(list)

class LoginView(APIView):

    def get(self, request):
        user = request.user
        print(user)

        return Response(200)

    def post(self, request):

        data = get_data(request)
        try:
            user = MyUser.objects.get(email=data['email'])
        except MyUser.DoesNotExist:
            return Response(status=404)
        if user.check_password(data['password']):
            token = Token.objects.get_or_create(user=user)[0]
            print(token)
        else:
            return Response(400)

        return Response({"token": token.key}, 200)

class RegisterView(APIView):

    def post(self, request):

        data = get_data(request)
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

