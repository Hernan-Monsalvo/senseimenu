from .models import Dish, WeekMenu
from .utils import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser
from rest_framework import status
import json
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from datetime import datetime
from django.shortcuts import get_object_or_404


def get_data(request):
    try:
        data = JSONParser().parse(request)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return data

class PingView(APIView):

    def get(self, request):

        time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return Response({"response": "pong", "time": time_now, "version": "0.0.1"})

class DishView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        dishes = Dish.objects.all()
        type = request.query_params.get('type')
        if type is not None:
            dishes = filterDishes(type, dishes)
        serializer = DishSerializer(dishes, many=True, context={"user":user.pk})
        return Response(serializer.data)

    def post(self, request):

        user = request.user
        if user.email == "guest@senseimenu.com":
            return Response({"status":"error", "message": "guest cant create dishes"}, status=status.HTTP_400_BAD_REQUEST)
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
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            dish = Dish.objects.get(Q(pk=pk, owner=request.user) | Q(pk=pk, owner_id=2)) #.filter(Q(owner=user) | Q(owner_id=6))
        except Dish.DoesNotExist:
            return Response(status=404)
        serializer = DishSerializer(dish, context={"user":request.user.pk})
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            dish = Dish.objects.get(pk=pk, owner=request.user)
        except Dish.DoesNotExist:
            return Response(status=404)
        data = get_data(request)
        if "ingredients" in data:
            data = ingredientsToString(data)
        serializer = DishSerializer(dish, data=data, partial=True, context={"user":request.user.pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            dish = Dish.objects.get(pk=pk, owner=request.user)
        except Dish.DoesNotExist:
            return Response(status=404)
        serializer = DishSerializer(dish)
        dish.delete()
        return Response(serializer.data)

class DishCloneView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        user = get_object_or_404(MyUser, pk=request.user.pk)
        if request.user.email == "guest@senseimenu.com":
            return Response({"status":"error", "message": "guest cant clone dishes"}, status=status.HTTP_400_BAD_REQUEST)

        dish = get_object_or_404(Dish, pk=pk)

        dish.pk = None
        dish.owner = user
        dish.save()

        serializer = DishSerializer(dish, context={"user":user.pk})

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        menus = WeekMenu.objects.filter(owner=user).order_by('-id')[:4]

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
        serializer = MenuDetailSerializer(menu)
        return Response(serializer.data)

class MenuPDF(APIView):

    def get(self, request, pk):
        user = request.user
        try:
            menu = WeekMenu.objects.get(pk=pk, owner=user)
        except WeekMenu.DoesNotExist:
            return Response(status=404)

        html = render_to_string("pdf_menu_template.html", {
            "menu": menu
        })

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; report.pdf"

        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

        return response

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

class ShopListPDF(APIView):

    def get(self, request, pk):
        user = request.user
        try:
            menu = WeekMenu.objects.get(pk=pk, owner=user)
        except WeekMenu.DoesNotExist:
            return Response(status=404)

        if not menu.shopping_list:
            menu.create_shoping_list()

        html = render_to_string("pdf_shoplist_template.html", {
            "shopList": menu.get_shoping_list()
        })

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; report.pdf"

        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

        return response

class LoginView(APIView):

    def get(self, request):
        user = request.user

        return Response(200)

    def post(self, request):

        data = get_data(request)
        try:
            user = MyUser.objects.get(email=data['email'])
        except MyUser.DoesNotExist:
            return Response(status=404)
        if user.check_password(data['password']):
            token = Token.objects.get_or_create(user=user)[0]

        else:
            return Response({"Error": "Wrong password"}, 401)

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

