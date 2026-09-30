import time
import random

print("Ошибка! невозможно получить доступ к данным. Пожалуйста, введите новое имя пользователя: ", end="")
user_name = input()

print("введите 1 для начала игры")
print("введите 2 для выхода из игры (при выходе данные не сохраняются)")

# защита от ввода не-числа
while True:
    try:
        menu_choice = int(input())
        if menu_choice in (1, 2):
            break
        print("Введите 1 или 2")
    except ValueError:
        print("Введите число: 1 или 2")

player_status = "alive"


def loading_animation():
    for i in range(5):
        print("Загрузка" + "." * (i + 1))
        time.sleep(0.5)
        print("\033[F\033[K", end="")

def starting_room():
    has_key = False
    door_opened = False
    inventory = []

    print("Вы просыпаетесь в уютной комнате, в которой есть кровать, огромный шкаф, компьютер и дверь.")

    while not door_opened:
        print("\n1. Осмотреть кровать")
        print("2. Осмотреть шкаф")
        print("3. Осмотреть компьютер")
        print("4. Попробовать открыть дверь")
        print("5. Инвентарь")

        choice = input("Выберите действие: ")

        if choice == "1":
            print("Обычная кровать, ничего интересного.")

        elif choice == "2":
            if not has_key:
                print("Вы открываете шкаф. Внутри прячется зомби!")
                result = battle(subject_025, zombie)

                if result == "dead":
                    print("Вы погибли в схватке с зомби...")
                    return "dead"
                elif result == "fled":
                    print("Вы захлопнули шкаф и отступили.")
                else:
                    print("Зомби повержен. В глубине шкафа вы находите ключ от двери.")
                    has_key = True
                    inventory.append("ключ от двери")
            else:
                print("В шкафу больше ничего нет.")

        elif choice == "3":
            print("Компьютер не включается. Кажется, ему нужно что-то ещё.")

        elif choice == "4":
            if has_key:
                print("Вы отпираете дверь ключом и выходите из комнаты.")
                door_opened = True
            else:
                print("Дверь заперта, нужно найти ключ.")

        elif choice == "5":
            if inventory:
                print("Инвентарь:", ", ".join(inventory))
            else:
                print("Инвентарь пуст.")

        else:
            print("Некорректный ввод.")

    return "alive"


class unit:
    def __init__(self, name, health, attack, ap, max_ap, speed, attack_cost=2, flee_chance=50):
        self.name = name
        self.health = health
        self.attack = attack
        self.ap = ap
        self.max_ap = max_ap
        self.speed = speed
        self.attack_cost = attack_cost
        self.flee_chance = flee_chance


subject_025 = unit(user_name, 20, 5, 5, 10, speed=5)
zombie = unit("Зомби", 13, 3, 2, 8, speed=2, attack_cost=2, flee_chance=70)
mutant = unit("Мутант", 20, 10, 4, 10, speed=4, attack_cost=4, flee_chance=30)
subject_014 = unit("Глич", 15, 9, 6, 15, speed=9, attack_cost=3, flee_chance=0)


def battle(player, enemy):
    print(f"Битва между {player.name} и {enemy.name}")
    is_defending_player = False

    while player.health > 0 and enemy.health > 0:
        order = ("player", "enemy") if player.speed >= enemy.speed else ("enemy", "player")

        for turn in order:
            if player.health <= 0 or enemy.health <= 0:
                break

            if turn == "player":
                is_defending_player = False
                print(f"\nВаше здоровье: {max(0, player.health)}  AP: {player.ap}")
                print(f"Здоровье {enemy.name}: {max(0, enemy.health)}")
                print("1. Атака (2 AP)")
                print("2. Защита")
                print("3. Способность (4 AP)")
                print("4. Побег")

                choice = input("Выберите действие: ")

                if choice == "1":
                    if player.ap >= 2:
                        player.ap -= 2
                        enemy.health -= player.attack
                        print(f"Вы атакуете {enemy.name} на {player.attack} урона!")
                    else:
                        print("Недостаточно AP для атаки!")

                elif choice == "2":
                    is_defending_player = True
                    player.ap = min(player.ap + 2, player.max_ap)
                    print("Вы встали в защитную стойку.")

                elif choice == "3":
                    if player.ap >= 4:
                        player.ap -= 4
                        dmg = player.attack * 2
                        enemy.health -= dmg
                        print(f"Вы используете способность! {dmg} урона!")
                    else:
                        print("Недостаточно AP для способности!")

                elif choice == "4":
                    if random.randint(1, 100) <= enemy.flee_chance:
                        print("Вам удалось сбежать!")
                        return "fled"
                    else:
                        print("Побег не удался!")

                else:
                    print("Некорректный ввод, ход пропущен.")

            else:
                if enemy.ap >= enemy.attack_cost:
                    enemy.ap -= enemy.attack_cost
                    dmg = enemy.attack
                    if is_defending_player:
                        dmg = dmg // 2
                    player.health -= dmg
                    print(f"{enemy.name} атакует вас на {dmg} урона!")
                else:
                    enemy.ap = min(enemy.ap + 2, enemy.max_ap)
                    print(f"{enemy.name} копит силы...")

        player.ap = min(player.ap + 1 + player.speed // 3, player.max_ap)
        enemy.ap = min(enemy.ap + 1 + enemy.speed // 3, enemy.max_ap)

    if player.health <= 0:
        print(f"{player.name} повержен!")
        return "dead"
    else:
        print(f"{enemy.name} побежден!")
        return "alive"


if menu_choice == 1:
    print("Начало игры")
    loading_animation()

    if player_status == "alive":
        starting_room()

    if player_status == "dead":
        print("Игра окончена")
    elif player_status == "fled":
        print("Вы сбежали с поля боя")

elif menu_choice == 2:
    print("Выход из игры")