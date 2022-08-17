from .models import Dish, WeekMenu, MyUser
from .utils import ingredientsToDict
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = '__all__'

    def to_representation(self, instance):
        data = super(DishSerializer, self).to_representation(instance)
        context_user = self.context.get("user")
        data['is_owner'] = data['owner'] == context_user

        return ingredientsToDict(data)

class MenuDetailSerializer(serializers.ModelSerializer):
    mon_lun = DishSerializer()
    wed_lun = DishSerializer()
    tue_lun = DishSerializer()
    thu_lun = DishSerializer()
    fri_lun = DishSerializer()
    sat_lun = DishSerializer()
    sun_lun = DishSerializer()

    mon_din = DishSerializer()
    tue_din = DishSerializer()
    wed_din = DishSerializer()
    thu_din = DishSerializer()
    fri_din = DishSerializer()
    sat_din = DishSerializer()
    sun_din = DishSerializer()

    class Meta:
        model = WeekMenu
        exclude = ['shopping_list', ]

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekMenu
        exclude = ['shopping_list', ]


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['password', 'email']

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = MyUser(password=make_password(validated_data.pop('password')), **validated_data)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['password', 'email']

    def login(self, validated_data):
        try:
            user = MyUser.objects.get(email=validated_data['email'])
        except MyUser.DoesNotExist:
            return {'status': 'error', 'message': 'email is not correct'}

        if user.check_password(validated_data['password']):
            print("password is ok")
            token = Token.objects.create(user=user)
            print(token.key)
        else:
            print("password is not ok")
