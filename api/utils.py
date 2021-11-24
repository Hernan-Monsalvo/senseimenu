from .models import Dish
import random
import json
import ast


def filterDishes(filter, queryset):
    if filter != 'all':
        if filter == 'veggie':
            queryset = queryset.filter(is_veggie=True)
        if filter == 'vegan':
            queryset = queryset.filter(is_vegan=True)
        if filter == 'meat':
            queryset = queryset.filter(is_veggie=False)
    else:
        pass
    return queryset


def randomMenu(config, user):
    all_dishes = Dish.objects.filter(owner=user)
    random_menu = []
    for choice in config:
        if choice != None:
            filtered_dishes = filterDishes(choice, all_dishes)
            dish = random.choice(filtered_dishes)
            dish_json = {
                "id": dish.id,
                "name": dish.name,
                "is_veggie": dish.is_veggie,
                "is_vegan": dish.is_vegan
            }
            random_menu.append(dish_json)
        else:
            random_menu.append(choice)

    return random_menu


def dishListToDict(data):

    dish_list = data['config']

    new_data = {
        "owner": data['owner'],
        "mon_lun": dish_list[0],
        "tue_lun": dish_list[1],
        "wed_lun": dish_list[2],
        "thu_lun": dish_list[3],
        "fri_lun": dish_list[4],
        "sat_lun": dish_list[5],
        "sun_lun": dish_list[6],
        "mon_din": dish_list[7],
        "tue_din": dish_list[8],
        "wed_din": dish_list[9],
        "thu_din": dish_list[10],
        "fri_din": dish_list[11],
        "sat_din": dish_list[12],
        "sun_din": dish_list[13],
    }

    return new_data

def ingredientsToString(data):
    ing_json = data['ingredients']
    ing_str = json.dumps(ing_json)
    data['ingredients'] = ing_str

    return data

def ingredientsToDict(data):
    ing_str = data['ingredients']
    ing_json = json.loads(ing_str)
    data['ingredients'] = ing_json

    return data
