from recipe_commands import list_ingredients

#TODO: make this a session dependent variable
current_list = {}

def add_to_list(id):
    to_add = list_ingredients(id)
    for ingredient in to_add:
        list_item = f"{ingredient[1]} {ingredient[2]}"
        amount = current_list.get(list_item, 0)
        current_list[list_item] = amount + ingredient[0]
    return True

def get_shopping_list():
    return_list = []
    for item in current_list:
        return_list.append(f"{current_list[item]} {item}")
    return return_list

def remove_from_list(to_remove):
    for item in to_remove:
        key = item[item.find(" ") + 1:]
        current_list.pop(key)

def reset_shopping_list():
    current_list = {}
