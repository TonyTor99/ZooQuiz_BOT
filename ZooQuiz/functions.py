from config import questions
import random


def get_totem_animal(user_answers):
    totem_count = {
        "Тигр": 0,
        "Слон": 0,
        "Енот": 0,
        "Попугай": 0,
        "Аист": 0,
        "Фламинго": 0,
        "Черепаха": 0,
        "Питон": 0,
        "Жаба": 0,
        "Саламандра": 0,
    }
    for answer in user_answers:
        for question in questions:
            if answer in question['answer']:
                for animal in question['answer'][answer]:
                    totem_count[animal] += 1

    max_count = max(totem_count.values())
    totem_animals = [animal for animal, count in totem_count.items() if count == max_count]

    if len(totem_animals) == 1:
        return totem_animals[0]
    else:
        return random.choice(totem_animals)

def get_animal_photo(totem_animal):
    paths = {
        'Тигр': '.\\Photos\\tiger.jpeg',
        'Слон': '.\\Photos\\elefant.jpeg',
        'Енот': '.\\Photos\\enot.jpg',
        'Попугай': '.\\Photos\\popug.jpeg',
        'Аист': '.\\Photos\\aist.jpeg',
        'Фламинго': '.\\Photos\\flamingo.jpeg',
        'Черепаха': '.\\Photos\\turtle.jpeg',
        'Питон': '.\\Photos\\python_.jpeg',
        'Жаба': '.\\Photos\\jaba.jpeg',
        'Саламандра': '.\\Photos\\salamandra.jpeg',
    }
    return paths.get(totem_animal)








