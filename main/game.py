import time
import random


def text_animation(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def loading_animation():
    for i in range(5):
        print("Загрузка" + "." * (i + 1))
        time.sleep(0.5)
        print("\033[F\033[K", end="")


user_name = "Тестируемый"
user_password = ""

class unit:
    def __init__(self, name, health, attack, ap, max_ap, speed, attack_cost=2, flee_chance=50, xp_reward=0, dodge=0):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.ap = ap
        self.max_ap = max_ap
        self.speed = speed
        self.attack_cost = attack_cost
        self.flee_chance = flee_chance
        self.xp_reward = xp_reward
        self.dodge = dodge
        self.level = 1
        self.xp = 0


subject_025 = unit("Тестируемый", 24, 4, 6, 8, speed=5)

def make_enemy(kind):
    if kind == "зомби":
        return unit("Зомби", 12, 3, 4, 6, speed=2, attack_cost=2, flee_chance=70, xp_reward=10)
    if kind == "бегун":
        return unit("Бегун", 10, 4, 6, 8, speed=7, attack_cost=2, flee_chance=50, xp_reward=15)
    if kind == "бот":
        return unit("Охранный бот", 22, 5, 6, 9, speed=6, attack_cost=3, flee_chance=40, xp_reward=20)
    if kind == "мутант":
        return unit("Мутант", 30, 8, 8, 10, speed=4, attack_cost=4, flee_chance=30, xp_reward=30)
    return unit("Глич", 40, 8, 10, 14, speed=9, attack_cost=3, flee_chance=0, dodge=15)


weapons = {
    "кулаки": {"bonus": 0, "cost": 2, "stun": 0},
    "арматура": {"bonus": 3, "cost": 2, "stun": 0},
    "электрошокер": {"bonus": 2, "cost": 2, "stun": 35},
    "пожарный топор": {"bonus": 6, "cost": 3, "stun": 0},
    "миниган": {"bonus": 1000000, "cost": 0, "stun": 0},
}
owned_weapons = ["кулаки"]
gear = {"weapon": "кулаки"}

inventory = ["аптечка"]
key_items = ("ключ от двери", "карта доступа", "энергоядро")


meta = {"lives": 3, "memories": 0}
stats = {"kills": 0, "deaths": 0, "restarts": 0, "secrets": 0}


def new_state():
    return {
        "visited": [], "bed": False, "closet": False,
        "storage": False, "boxes": False, "shelf": False,
        "server": False, "math": False, "vent": False,
        "lab": False, "riddle": False, "cabinet": False,
        "safe_wall": False, "rests": 0,
        "powered": False, "portal": False, "password": "",
    }


state = new_state()



def comment(text):
    text_animation(f"{user_name}: {text}")


def thought(*lines):
    stage = min(meta["memories"] // 4, len(lines) - 1)
    comment(lines[stage])


def first_visit(room):
    if room in state["visited"]:
        return False
    state["visited"].append(room)
    meta["memories"] += 1
    return True


def found_secret():
    stats["secrets"] += 1
    meta["memories"] += 1


def give_weapon(name):
    if name in owned_weapons:
        return
    owned_weapons.append(name)
    text_animation(f"Новое оружие: {name}!")
    if gear["weapon"] == "кулаки":
        gear["weapon"] = name
        text_animation(f"Вы берете {name} в руки.")
    else:
        text_animation("Сменить оружие можно командой 'оружие'.")


def show_inventory():
    medkits = inventory.count("аптечка")
    items = [item for item in inventory if item != "аптечка"]
    print("\n--- ИНВЕНТАРЬ ---")
    print("Предметы:", ", ".join(items) if items else "нет")
    print(f"Аптечки: {medkits}")
    print(f"Оружие в руках: {gear['weapon']}")
    p = subject_025
    print(f"Уровень {p.level}  HP {p.health}/{p.max_health}  Жизни: {meta['lives']}")


def show_help():
    print("\n--- ПОМОЩЬ ---")
    print("Цифры - выбор действия в меню.")
    print("инвентарь - показать предметы и состояние")
    print("оружие - сменить оружие (не в бою)")
    print("аптечка - использовать аптечку (не в бою)")
    print("помощь - эта подсказка")
    print("выход - выйти из игры")


def show_stats():
    print("\n=== СТАТИСТИКА ===")
    print(f"Уровень: {subject_025.level}")
    print(f"Побеждено врагов: {stats['kills']}")
    print(f"Смертей: {stats['deaths']}")
    print(f"Перезапусков (ошибка 407): {stats['restarts']}")
    print(f"Найдено секретов: {stats['secrets']}")
    print(f"Осталось жизней: {meta['lives']}")


def quit_game():
    text_animation("Вы вышли из игры.")
    show_stats()
    raise SystemExit


def use_medkit():
    p = subject_025
    if "аптечка" not in inventory:
        text_animation("Аптечек нет.")
    elif p.health >= p.max_health:
        text_animation("Вы и так в порядке.")
    else:
        inventory.remove("аптечка")
        heal = min(12, p.max_health - p.health)
        p.health += heal
        text_animation(f"Вы используете аптечку: +{heal} HP.")


def change_weapon():
    print("\nОружие:")
    for i, name in enumerate(owned_weapons, 1):
        w = weapons[name]
        extra = f", оглушение {w['stun']}%" if w["stun"] else ""
        mark = " (в руках)" if name == gear["weapon"] else ""
        print(f"{i}. {name}: урон +{w['bonus']}, {w['cost']} AP{extra}{mark}")
    choice = input("Номер оружия (Enter - отмена): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(owned_weapons):
        gear["weapon"] = owned_weapons[int(choice) - 1]
        text_animation(f"В руках: {gear['weapon']}.")


def ask(prompt="Выберите действие: ", in_battle=False):
    # команды, которые работают в любой момент
    while True:
        choice = input(prompt).strip().lower()
        if choice == "инвентарь":
            show_inventory()
        elif choice == "помощь":
            show_help()
        elif choice == "выход":
            quit_game()
        elif choice in ("оружие", "аптечка") and in_battle:
            print("В бою используйте меню боя.")
        elif choice == "оружие":
            change_weapon()
        elif choice == "аптечка":
            use_medkit()
        else:
            return choice


# ---------- БОЙ ----------

def hit_damage(player, weapon):
    dmg = player.attack + weapon["bonus"] + random.randint(-1, 1)
    return max(1, dmg)


def gain_xp(amount):
    p = subject_025
    p.xp += amount
    while p.xp >= 20 * p.level:
        p.xp -= 20 * p.level
        p.level += 1
        p.max_health += 4
        p.attack += 1
        p.max_ap += 1
        p.health = min(p.max_health, p.health + p.max_health // 2)
        text_animation(f"Уровень повышен! Теперь у вас {p.level} уровень: больше HP, урона и AP.")
        thought("тело само вспоминает, как драться. приятно.",
                "становлюсь сильнее. быстрее, чем они успевают меня стирать.",
                "ладно, теперь меня так просто не остановить.")


def battle(player, enemy):
    weapon = weapons[gear["weapon"]]
    player.ap = player.max_ap
    text_animation(f"Битва между {player.name} и {enemy.name}")
    is_defending_player = False
    enemy_stunned = False

    while player.health > 0 and enemy.health > 0:
        order = ("player", "enemy") if player.speed >= enemy.speed else ("enemy", "player")

        for turn in order:
            if player.health <= 0 or enemy.health <= 0:
                break

            if turn == "player":
                is_defending_player = False
                print(f"\n{player.name}: {max(0, player.health)}/{player.max_health} HP  AP {player.ap}/{player.max_ap}"
                      f"   |   {enemy.name}: {max(0, enemy.health)}/{enemy.max_health} HP")
                print(f"1. Атака: {gear['weapon']} ({weapon['cost']} AP)")
                print("2. Защита (+2 AP, урон вдвое меньше)")
                print("3. Мощный удар (4 AP, двойной урон, не промахивается)")
                print(f"4. Аптечка (осталось: {inventory.count('аптечка')})")
                print("5. Побег")

                choice = ask(in_battle=True)

                if choice == "1":
                    if player.ap >= weapon["cost"]:
                        player.ap -= weapon["cost"]
                        if random.randint(1, 100) <= enemy.dodge:
                            text_animation(f"{enemy.name} мерцает, удар проходит сквозь него!")
                        else:
                            dmg = hit_damage(player, weapon)
                            enemy.health -= dmg
                            text_animation(f"Вы бьете: {gear['weapon']}, {dmg} урона!")
                            if weapon["stun"] and enemy.health > 0 and random.randint(1, 100) <= weapon["stun"]:
                                enemy_stunned = True
                                text_animation(f"{enemy.name} дергается от разряда и теряет ход!")
                    else:
                        text_animation("Недостаточно AP для атаки!")

                elif choice == "2":
                    is_defending_player = True
                    player.ap = min(player.ap + 2, player.max_ap)
                    text_animation("Вы встали в защитную стойку.")

                elif choice == "3":
                    if player.ap >= 4:
                        player.ap -= 4
                        dmg = hit_damage(player, weapon) * 2
                        enemy.health -= dmg
                        text_animation(f"Вы используете мощный удар! {dmg} урона!")
                    else:
                        text_animation("Недостаточно AP для мощного удара!")

                elif choice == "4":
                    if "аптечка" in inventory:
                        inventory.remove("аптечка")
                        heal = min(12, player.max_health - player.health)
                        player.health += heal
                        text_animation(f"Вы используете аптечку: +{heal} HP.")
                    else:
                        text_animation("Аптечек нет!")

                elif choice == "5":
                    if random.randint(1, 100) <= enemy.flee_chance:
                        text_animation("Вам удалось сбежать!")
                        return "fled"
                    else:
                        text_animation("Побег не удался!")

                else:
                    text_animation("Некорректный ввод, ход пропущен.")

            else:
                if enemy_stunned:
                    enemy_stunned = False
                    text_animation(f"{enemy.name} приходит в себя.")
                elif enemy.ap >= enemy.attack_cost:
                    enemy.ap -= enemy.attack_cost
                    dmg = enemy.attack + random.randint(-1, 1)
                    if is_defending_player:
                        dmg = dmg // 2
                    dmg = max(1, dmg)
                    player.health -= dmg
                    text_animation(f"{enemy.name} атакует вас на {dmg} урона!")
                else:
                    enemy.ap = min(enemy.ap + 2, enemy.max_ap)
                    text_animation(f"{enemy.name} копит силы...")

        player.ap = min(player.ap + 1 + player.speed // 3, player.max_ap)
        enemy.ap = min(enemy.ap + 1 + enemy.speed // 3, enemy.max_ap)

    if player.health <= 0:
        text_animation(f"{player.name} повержен!")
        return "dead"
    text_animation(f"{enemy.name} побежден!")
    return "won"


def fight(kind):
    enemy = make_enemy(kind)
    result = battle(subject_025, enemy)
    if result == "won":
        stats["kills"] += 1
        # небольшая передышка после боя, чтобы развитие было плавным
        subject_025.health = min(subject_025.max_health, subject_025.health + subject_025.max_health // 4)
        if enemy.xp_reward:
            text_animation(f"Опыт: +{enemy.xp_reward}")
            gain_xp(enemy.xp_reward)
    elif result == "dead":
        stats["deaths"] += 1
    return result


# комнаты

def starting_room():
    if first_visit("start"):
        text_animation("Вы просыпаетесь в уютной комнате, в которой есть кровать, огромный шкаф, компьютер и дверь.")
        thought("так, спокойно. имя помню, остальное как отрезало.",
                "опять эта комната. я тут уже был, точно был.",
                "знакомая комната. значит цикл все-таки есть.")
    else:
        text_animation("Вы в своей комнате.")

    while True:
        print("\n1. Осмотреть кровать")
        print("2. Осмотреть шкаф")
        print("3. Осмотреть компьютер")
        print("4. Попробовать открыть дверь")

        choice = ask()

        if choice == "1":
            if not state["bed"]:
                state["bed"] = True
                found_secret()
                text_animation("Вы заглядываете под кровать. Там лежит кусок арматуры.")
                give_weapon("арматура")
                thought("кулаки это конечно хорошо, но арматура лучше.",
                        "под кроватью арматура. кто-то тут явно готовился.",
                        "арматура на месте. значит я не первый, кто тут прятал оружие.")
            else:
                text_animation("Обычная кровать, больше ничего интересного.")

        elif choice == "2":
            if state["closet"]:
                text_animation("В шкафу больше ничего нет.")
            else:
                text_animation("Вы открываете шкаф. Внутри прячется зомби!")
                result = fight("зомби")
                if result == "dead":
                    text_animation("Вы погибли в схватке с зомби...")
                    return "dead"
                elif result == "fled":
                    text_animation("Вы захлопнули шкаф и отступили.")
                else:
                    state["closet"] = True
                    inventory.append("ключ от двери")
                    text_animation("Зомби повержен. В глубине шкафа вы находите ключ от двери.")
                    thought("зомби в шкафу. классика. зато ключ достался.",
                            "опять зомби в шкафу. я уже начинаю привыкать.",
                            "зомби в шкафу, ключ внутри. сценарий я уже выучил.")

        elif choice == "3":
            text_animation("Маленький компьютер не включается. Экран мертвый.")
            thought("старый комп, не включается. ладно, потом разберусь.",
                    "почему-то именно к этому компьютеру меня тянет.",
                    "этот комп важнее, чем кажется. я чувствую.")

        elif choice == "4":
            if "ключ от двери" in inventory:
                text_animation("Вы отпираете дверь ключом и выходите из комнаты.")
                return "hub"
            else:
                text_animation("Дверь заперта, нужно найти ключ.")

        else:
            text_animation("Некорректный ввод.")


def main_room():
    falsePassword = "aristotle"
    truePassword = user_password

    if first_visit("hub"):
        text_animation("Вы вошли в главную комнату. Здесь есть несколько дверей, ведущих в разные части здания.")
        text_animation("по середине комнаты стоит портал и огромный компьютер, который светится странным светом. Похоже, что он управляет порталом.")
        thought("ничего себе. портал. и что-то мне подсказывает, что просто так он не включится.",
                "главная комната. портал, компьютер. все как я и думал.",
                "ну здравствуй, портал. посмотрим, что ты на этот раз выкинешь.")

    while True:
        print("\n1. Осмотреть портал")
        print("2. Осмотреть компьютер")
        print("3. Дверь в лабораторию")
        print("4. Дверь на склад")
        print("5. Дверь в серверную")
        print("6. Безопасная комната")
        print("7. Вернуться в свою комнату")

        choice = ask()

        if choice == "1":
            if not state["portal"]:
                text_animation("Портал не активен. Похоже, его включает компьютер.")
            elif state["password"] == falsePassword:
                text_animation("Портал активен, вы входите в него...")
                text_animation("total error, 407 proxy server not found")
                text_animation("Все вокруг рассыпается на пиксели...")
                return "407"
            else:
                text_animation("Портал активен. Вы входите в него...")
                text_animation("Вы попадаете в странное измерение, где все выглядит искаженно")
                text_animation("глич: это изначально была смертью, никто не должен был согласиться на это.")
                text_animation(f"{user_name}: о чем ты говоришь? кто ты?")
                text_animation("глич: мы тестировщики этой программы, ученые разработали ее, чтобы увеличить стрессоустойчивость солдат.")
                text_animation("глич: но что-то пошло не так, после того как мы вводили пароль чтобы выйти из портала, программа глючила и мы перезапускались в этом цифровом мире.")
                text_animation("глич: перезапускался и наш мозг, мы теряли память каждый раз и все начиналось заново, мы пытались найти способ выйти из портала, но все было тщетно.")
                text_animation("глич: я тестируемый номер 014, я смог как-то найти способ выйти из портала, но мое тело уже давно гниет, а я застрял в этом цифровом мире.")
                text_animation(f"{user_name}: что мне делать?")
                text_animation("глич: никто не должен отсюда выйти, люди должны знать что такая программа опасна и никого больше не стоит сюда запихивать.")
                text_animation(f"{user_name}: тупо, люди и так будут запихивать, прогресс не остановить.")
                text_animation(f"{user_name}: лучше исправлять ошибки и идти дальше.")
                result = fight("глич")
                if result == "dead":
                    text_animation("Вы погибли в схватке с гличем...")
                    return "dead"
                elif result == "won":
                    text_animation("Вы победили глича и нашли способ выйти из портала.")
                    text_animation("Вы выходите из портала и возвращаетесь в реальный мир.")
                    return "win"

        elif choice == "2":
            if state["portal"]:
                text_animation("Компьютер уже работает. Портал активен.")
            elif not state["powered"] and "энергоядро" not in inventory:
                text_animation("Компьютер не работает. Похоже, ему нужен энергетический источник.")
            else:
                if not state["powered"]:
                    inventory.remove("энергоядро")
                    state["powered"] = True
                    text_animation("Вы вставляете исправное энергоядро в компьютер.")
                text_animation("Компьютер включился, спрашивает пароль.")
                password = ask("Введите пароль: ")
                if password in (falsePassword, truePassword):
                    state["portal"] = True
                    state["password"] = password
                    text_animation("Пароль верный, можете активировать портал.")
                else:
                    text_animation("Пароль неверный.")

        elif choice == "3":
            return "lab"
        elif choice == "4":
            return "storage"
        elif choice == "5":
            if "карта доступа" in inventory:
                return "server"
            text_animation("Дверь в серверную заперта. Нужна карта доступа.")
            thought("замок с картой. значит карта где-то лежит.",
                    "карта доступа. надо поискать на складе.",
                    "без карты сюда не попасть. склад, наверное.")
        elif choice == "6":
            return "safe"
        elif choice == "7":
            return "start"
        else:
            text_animation("Некорректный ввод.")


def storage_room():
    if first_visit("storage"):
        text_animation("На складе темно. Между стеллажами кто-то быстро двигается...")

    if not state["storage"]:
        text_animation("Из темноты вылетает бегун!")
        thought("быстрый, зараза. ну, держись.",
                "бегун. быстрый, но хрупкий. знаю.",
                "бегун, ага. подпускаем и бьем.")
        result = fight("бегун")
        if result == "dead":
            text_animation("Вы погибли на складе...")
            return "dead"
        elif result == "fled":
            text_animation("Вы выскакиваете обратно в коридор.")
            return "hub"
        state["storage"] = True

    while True:
        print("\n1. Осмотреть ящики")
        print("2. Осмотреть запертый стеллаж")
        print("3. Вернуться в главную комнату")

        choice = ask()

        if choice == "1":
            if not state["boxes"]:
                state["boxes"] = True
                inventory.append("карта доступа")
                inventory.append("аптечка")
                text_animation("В ящиках вы находите карту доступа и аптечку.")
                thought("вот и карта. и аптечка, как мило.",
                        "карта доступа. сразу в серверную.",
                        "карта, аптечка. все как и в прошлый раз.")
            else:
                text_animation("Ящики пусты.")

        elif choice == "2":
            if state["shelf"]:
                text_animation("Стеллаж уже вскрыт, внутри пусто.")
            elif "арматура" in owned_weapons:
                state["shelf"] = True
                found_secret()
                inventory.append("аптечка")
                text_animation("Вы поддеваете замок арматурой. Внутри электрошокер и аптечка.")
                give_weapon("электрошокер")
                thought("арматура и тут пригодилась. шокер вообще мечта.",
                        "замок поддался. шокер, пригодится.",
                        "знал, что замок слабый. шокер забираю.")
            else:
                text_animation("Стеллаж закрыт на крепкий замок. Нужен рычаг.")
                thought("замок. рычаг бы какой-нибудь.",
                        "замок крепкий. нужно что-то твердое.",
                        "рычаг бы, и вскроем.")

        elif choice == "3":
            return "hub"
        else:
            text_animation("Некорректный ввод.")


def server_room():
    if first_visit("server"):
        text_animation("Серверная гудит от работающего оборудования. В проходе мигает красный огонек.")

    if not state["server"]:
        text_animation("Охранный бот сходит с подставки!")
        thought("охранный бот. логично, куда ж без него.",
                "бот. опять. ладно, разберемся.",
                "бот-охранник. знаю его слабые места.")
        result = fight("бот")
        if result == "dead":
            text_animation("Вы погибли в серверной...")
            return "dead"
        elif result == "fled":
            text_animation("Вы выбегаете обратно в главную комнату.")
            return "hub"
        state["server"] = True

    while True:
        print("\n1. Осмотреть главный сервер")
        print("2. Осмотреть вентиляцию")
        print("3. Вернуться в главную комнату")

        choice = ask()

        if choice == "1":
            if state["math"]:
                text_animation("Сервер уже открыт.")
            else:
                text_animation("На экране сервера загадка: чему равно (7 * 6) - 12 + 3 ?")
                for attempt in range(3):
                    answer = ask("Ответ: ")
                    if answer == "33":
                        state["math"] = True
                        inventory.append("энергоядро")
                        text_animation("Сервер открывается. Внутри лежит энергоядро.")
                        thought("математика, надо же. зато ядро получили.",
                                "ядро у меня. теперь к главному компьютеру.",
                                "ядро в кармане. идем включать портал.")
                        break
                    subject_025.health -= 3
                    text_animation(f"Сервер бьет током! -3 HP. Осталось попыток: {2 - attempt}")
                    if subject_025.health <= 0:
                        stats["deaths"] += 1
                        text_animation("Вы погибли от удара током...")
                        return "dead"

        elif choice == "2":
            if state["vent"]:
                text_animation("В вентиляции больше ничего нет.")
            else:
                state["vent"] = True
                found_secret()
                inventory.append("аптечка")
                text_animation("В вентиляции лежит аптечка и обрывок лога: 'Тестируемый 014 нашел выход, но не смог им воспользоваться.'")
                thought("014. значит до меня тут кто-то был.",
                        "тестируемый 014. я его еще встречу, чувствую.",
                        "014. я знаю, кто это. значит, надо спешить.")

        elif choice == "3":
            return "hub"
        else:
            text_animation("Некорректный ввод.")


def lab_room():
    if first_visit("lab"):
        text_animation("В лаборатории пахнет озоном. Между рядами оборудования что-то огромное шевелится в темноте.")

    if not state["lab"]:
        text_animation("Из темноты выходит мутант!")
        thought("вот это громила. надо бы осторожнее.",
                "мутант. бьет редко, но больно. запомнил.",
                "мутант, ага. терпим, ждем окно и бьем.")
        result = fight("мутант")
        if result == "dead":
            text_animation("Вы погибли в лаборатории...")
            return "dead"
        elif result == "fled":
            text_animation("Вы выбегаете обратно в главную комнату.")
            return "hub"
        state["lab"] = True

    while True:
        print("\n1. Осмотреть терминал")
        print("2. Осмотреть шкафчик с кодовым замком")
        print("3. Вернуться в главную комнату")

        choice = ask()

        if choice == "1":
            if state["riddle"]:
                text_animation("Терминал: временный пароль администратора - aristotle.")
            else:
                text_animation("На экране: 'Введите слово ПОРТАЛ задом наперед, чтобы продолжить'.")
                for attempt in range(3):
                    answer = ask("Ответ: ")
                    if answer == "латроп":
                        state["riddle"] = True
                        text_animation("Терминал: доступ получен. Временный пароль администратора - aristotle.")
                        thought("слишком просто. подозрительно просто.",
                                "пароль дали слишком легко. не верю.",
                                "система сама подсунула пароль. значит ловушка.")
                        break
                    text_animation(f"Неверно. Осталось попыток: {2 - attempt}")
                else:
                    text_animation("Терминал блокируется. Попробуйте позже.")

        elif choice == "2":
            if state["cabinet"]:
                text_animation("Шкафчик уже пуст.")
            elif "карта доступа" in inventory:
                state["cabinet"] = True
                found_secret()
                text_animation("Вы прикладываете карту доступа. Замок щелкает, внутри пожарный топор.")
                give_weapon("пожарный топор")
                thought("топор. вот это уже серьезный аргумент.",
                        "топор. тяжелый, но им можно разговаривать.",
                        "топор. теперь поговорим по-другому.")
            else:
                text_animation("Шкафчик закрыт. Нужна карта доступа.")

        elif choice == "3":
            return "hub"
        else:
            text_animation("Некорректный ввод.")


def safe_room():
    if first_visit("safe"):
        text_animation("Тихая комната без монстров. Пахнет пылью и старыми одеялами.")
        thought("тихо. непривычно тихо.",
                "безопасная комната. как же тут спокойно.",
                "моя маленькая база. то, что надо.")

    while True:
        print("\n1. Отдохнуть")
        print("2. Осмотреть стену")
        print("3. Вернуться в главную комнату")

        choice = ask()

        if choice == "1":
            if state["rests"] >= 2:
                text_animation("Вы уже отдыхали здесь дважды, больше не заснуть.")
            else:
                state["rests"] += 1
                subject_025.health = subject_025.max_health
                text_animation("Вы отдыхаете и полностью восстанавливаете силы.")

        elif choice == "2":
            if state["safe_wall"]:
                text_animation("На стене все те же царапины.")
            else:
                state["safe_wall"] = True
                found_secret()
                text_animation("На стене нацарапано: 'Правильный выход, это тот который ты сам изначально выберал'")
                thought("какой имбецил придумывает такие фразы?.")

        elif choice == "3":
            return "hub"
        else:
            text_animation("Некорректный ввод.")



def reset_run():
    state.clear()
    state.update(new_state())
    for item in key_items:
        while item in inventory:
            inventory.remove(item)
    stats["restarts"] += 1


def play():
    rooms = {
        "start": starting_room,
        "hub": main_room,
        "storage": storage_room,
        "server": server_room,
        "lab": lab_room,
        "safe": safe_room,
    }
    location = "start"
    first = True

    while True:
        if not first:
            loading_animation()
        first = False

        result = rooms[location]()

        if result == "win":
            return "win"

        elif result in ("dead", "407"):
            meta["lives"] -= 1
            if result == "407":
                reset_run()
            subject_025.health = subject_025.max_health

            if meta["lives"] <= 0:
                text_animation("Система окончательно рухнула. Жизни закончились.")
                return "lose"

            if result == "407":
                text_animation("Вы просыпаетесь снова. Память стерта, но тело почему-то помнит.")
            else:
                text_animation("Система перезагружает вас...")
            text_animation(f"Осталось жизней: {meta['lives']}")
            location = "start"

        else:
            location = result


def main():
    global user_name, user_password

    text_animation("Ошибка! невозможно получить доступ к данным. Пожалуйста, введите новое имя пользователя: ")
    user_name = input().strip() or "Тестируемый"
    user_password = input("Введите пароль: ")
    subject_025.name = user_name

    text_animation("введите 1 для начала игры")
    text_animation("введите 2 для выхода из игры (при выходе данные не сохраняются)")

    while True:
        try:
            menu_choice = int(input())
            if menu_choice in (1, 2):
                break
            text_animation("Введите 1 или 2")
        except ValueError:
            text_animation("Введите число: 1 или 2")

    if menu_choice == 1:
        text_animation("Начало игры")
        loading_animation()
        result = play()

        if result == "win":
            text_animation("Поздравляем, вы выбрались!")
        else:
            text_animation("Игра окончена")
        show_stats()

    elif menu_choice == 2:
        text_animation("Выход из игры")


if __name__ == "__main__":
    main()