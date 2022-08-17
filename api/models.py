from django.db import models
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User
from django.utils import timezone
import json

User._meta.get_field('email')._unique = True
class MyUser(User, models.Model):

    is_verified = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

class Dish(models.Model):

    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, default=None)
    ingredients = models.TextField()
    is_veggie = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return self.name


class WeekMenu(models.Model):

    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='menus')
    start_day = models.DateField(default=timezone.now)

    mon_lun = models.ForeignKey(Dish, related_name='menu1', on_delete=SET_NULL, null=True, default=None)
    tue_lun = models.ForeignKey(Dish, related_name='menu2', on_delete=SET_NULL, null=True, default=None)
    wed_lun = models.ForeignKey(Dish, related_name='menu3', on_delete=SET_NULL, null=True, default=None)
    thu_lun = models.ForeignKey(Dish, related_name='menu4', on_delete=SET_NULL, null=True, default=None)
    fri_lun = models.ForeignKey(Dish, related_name='menu5', on_delete=SET_NULL, null=True, default=None)
    sat_lun = models.ForeignKey(Dish, related_name='menu6', on_delete=SET_NULL, null=True, default=None)
    sun_lun = models.ForeignKey(Dish, related_name='menu7', on_delete=SET_NULL, null=True, default=None)

    mon_din = models.ForeignKey(Dish, related_name='menu8', on_delete=SET_NULL, null=True, default=None)
    tue_din = models.ForeignKey(Dish, related_name='menu9', on_delete=SET_NULL, null=True, default=None)
    wed_din = models.ForeignKey(Dish, related_name='menu10', on_delete=SET_NULL, null=True, default=None)
    thu_din = models.ForeignKey(Dish, related_name='menu11', on_delete=SET_NULL, null=True, default=None)
    fri_din = models.ForeignKey(Dish, related_name='menu12', on_delete=SET_NULL, null=True, default=None)
    sat_din = models.ForeignKey(Dish, related_name='menu13', on_delete=SET_NULL, null=True, default=None)
    sun_din = models.ForeignKey(Dish, related_name='menu14', on_delete=SET_NULL, null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    shopping_list = models.TextField(null=True, default=None)

    def __str__(self):
        return self.name

    def dish_list(self):
        dishes = []
        dishes.append(self.mon_lun)
        dishes.append(self.mon_din)
        dishes.append(self.tue_lun)
        dishes.append(self.tue_din)
        dishes.append(self.wed_lun)
        dishes.append(self.wed_din)
        dishes.append(self.thu_lun)
        dishes.append(self.thu_din)
        dishes.append(self.fri_lun)
        dishes.append(self.fri_din)
        dishes.append(self.sat_lun)
        dishes.append(self.sat_din)
        dishes.append(self.sun_lun)
        dishes.append(self.sun_din)
        return dishes

    def create_shoping_list(self):
        d_list = self.dish_list()
        ing_list = []
        for dish in d_list:
            if dish != None:
                ing = json.loads(dish.ingredients)
                ing_list += ing

        for ind1, ing1 in enumerate(ing_list):
            for ind2, ing2 in enumerate(ing_list):
                if ind1 != ind2:
                    if ing1['name'] == ing2['name'] and ing1['unit'] == ing2['unit']:
                        ing1['amount'] = str(float(ing1['amount']) + float(ing2['amount']))
                        ing2['amount'] = "0"

        ing_list = list(filter(lambda ing: ing['amount'] != '0', ing_list))

        #AI clasification
        unclasified_list = json.dumps(ing_list)
        openai.api_key = "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"
        command = f'separar estos productos: {str(unclasified_list)} en 3 listas distintas: supermercado, carniceria, verduleria. el formado debe ser: "lista1":["producto1", "producto2" ], "lista2": ["producto3", "producto4" ]. debe ser formato json y cada elemento debe tener su peso.'
        clasified_list = openai.Completion.create(model="text-davinci-002", prompt=command, temperature=0.1, max_tokens=lenght)["choices"][0]["text"]

        print(clasified_list)

        self.shopping_list = json.dumps(unclasified_list)
        self.save()


    def get_shoping_list(self):

        list = json.loads(self.shopping_list)
        return list
