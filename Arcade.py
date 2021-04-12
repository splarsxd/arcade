from os import system
import random
from turtle import *
import curses
import time

def menu():
    system("cls")
    system("title Spelmenyn 1.0")
    system("color c")
    print("Välkommen till spelmenyn!\n")
    print("A) Ping Pong (2 spelare.)")
    print("B) Snake! (1 spelare.)")
    print("C) Hero's Quest (1 spelare.)\n\n")

    menuselect = input(">> ").lower()
    if not menuselect:
        menu()

    if menuselect == "a":
        pingpong()

    elif menuselect == "b":
        snake()

    elif menuselect == "c":
        questgame()

    else:
        print("\nVänligen välj ett av ovanstående alternativ.")
        system("timeout 2 >nul")
        menu()



def pingpong():
    system("cls")
    system("title Spelmenyn: Ping Pong")
    system("color 4")
    global score1, score2

    # Variabler d
    ballspeed = 17
    playerspeed = 50
    cursor_size = 20
    player_height = 75
    player_width = 15

    court_height = 600

    FONT = ("Verdena", 44, "normal")

    # Screen m
    wn = Screen()
    wn.bgcolor("dimgray")
    wn.setup(1.0, 1.0)
    wn.tracer(1)

    # Spelplan m
    sp = Turtle()
    sp.ht()
    sp.speed(0)
    sp.penup()
    sp.goto(-700, -400)
    sp.pendown()
    sp.color("red")

    for i in range(2):
        sp.fd(1390)
        sp.left(90)
        sp.fd(810)
        sp.left(90)

    sp.goto(-700, 300)
    sp.fd(1390)
    sp.penup()
    sp.goto(0, 300)
    sp.pd()
    sp.left(90)
    sp.fd(110)
    sp.left(180)
    sp.fd(110)

    for l in range(17):
        sp.penup()
        sp.fd(20)
        sp.pd()
        sp.fd(20)

    # Spelare 1 rörelse m
    def up1():
        y = player1.ycor()
        y += playerspeed
        if y < court_height / 2 - player_height / 2:
            player1.sety(y)

    def down1():
        y = player1.ycor()
        y -= playerspeed
        if y > -100 - court_height / 2:
            player1.sety(y)

    # Spelare 2 rörelse m
    def up2():
        y = player2.ycor()
        y += playerspeed
        if y < court_height / 2 - player_height / 2:
            player2.sety(y)

    def down2():
        y = player2.ycor()
        y -= playerspeed
        if y > -100 - court_height / 2:
            player2.sety(y)

    # Boll rörelse och distans d
    def reset_ball():
        ball.setposition(0, 0)
        ball.setheading(random.choice([0, 180]) + random.randint(-60, 60))

    def distance(t1, t2):
        my_distance = t1.distance(t2)

        if my_distance < player_height / 2:
            t2.setheading(180 - t2.heading())
            t2.forward(ballspeed)

    # Allmän d
    def move():
        global score1, score2

        ball.forward(ballspeed)

        x, y = ball.position()

        if x > 500 + cursor_size:
            score1 += 1
            s1.undo()
            s1.write(score1, font=FONT)
            reset_ball()

        elif x < cursor_size - 500:
            score2 += 1
            s2.undo()
            s2.write(score2, font=FONT)
            reset_ball()

        elif y > court_height / 2 - cursor_size or y < cursor_size - 400:
            ball.setheading(-ball.heading())

        else:
            distance(player1, ball)
            distance(player2, ball)

        wn.ontimer(move, 20)

    # Boll m
    ball = Turtle("circle")
    ball.color("crimson")
    ball.penup()
    ball.speed(0)

    reset_ball()

    # Spelare 1 m
    player1 = Turtle("square")
    player1.turtlesize(player_height / cursor_size, player_width / cursor_size)
    player1.color("goldenrod")
    player1.penup()
    player1.setx(cursor_size - 500)
    player1.speed(0)

    # Spelare 2 m
    player2 = Turtle("square")
    player2.shapesize(player_height / cursor_size, player_width / cursor_size)
    player2.color("goldenrod")
    player2.penup()
    player2.setx(500 + cursor_size)
    player2.speed(0)

    # Spelare 1 poäng d
    score1 = 0
    s1 = Turtle()
    s1.ht()
    s1.speed(0)
    s1.color("lavender")
    s1.penup()
    s1.setposition(-250, 320)
    s1.write(score1, font=FONT)

    # Spelare 2 poäng d
    score2 = 0
    s2 = Turtle()
    s2.ht()
    s2.speed(0)
    s2.color("lavender")
    s2.penup()
    s2.setposition(250, 320)
    s2.write(score2, font=FONT)

    # Rörelse m
    wn.onkey(up1, "w")
    wn.onkey(down1, "s")
    wn.onkey(up2, "Up")
    wn.onkey(down2, "Down")

    # Restart m
    wn.onkey(reset_ball, "o")

    # Funktioner som körs d
    wn.listen()
    move()
    wn.mainloop()



def snake():
    system("cls")
    system("title Spelmenyn: Snake!")
    system("color c")

    s = curses.initscr()
    curses.curs_set(0)
    sh, sw = s.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    snk_x = sw / 4
    snk_y = sh / 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    food = [sh / 2, sw / 2]
    w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

    key = curses.KEY_RIGHT

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
            curses.endwin()
            print("\n\n\n\n\n\n\n\n\n\n\n\n                                                 Du har förlorat.")
            system("timeout 3 >nul")
            menu()

        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        if snake[0] == food:
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 1),
                    random.randint(1, sw - 1)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(int(tail[0]), int(tail[1]), ' ')

        w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)



def questgame():
    system("cls")
    system("title Spelmenyn: Hero's Quest")
    system("color b")

    '''Importerar system bibloteket, randint modulen samt uniform modulen och tid modulen.'''

    def start():
        global name, lvl, mhp, hp, dmg, defense, xd, classes, chants
        system("cls")

        name = input("\nUsername: ")
        if not name:
            start()
            '''Låter användaren skriva in ett eget användarnamn.'''

        system("cls")
        print("Classes:\n")
        print("A) Warrior")
        print("B) Sorcerer")
        classes = input("\n\n>> ").lower()
        if not classes:
            start()

        if classes == "a":
            hp = 100
            mhp = 100
            dmg = 8
            defense = 16

        elif classes == "b":
            hp = 100
            mhp = 100
            dmg = 3
            defense = 0
            chants = 0

        else:
            print("\nYou did not make a valid selection.")
            system("timeout 2 >nul")
            start()

        xd = 0
        lvl = 1
        prep()

    def gameover():
        print("\nYou have died . . .")
        time.sleep(5)
        start()
        '''En funktion som används när spelaren dör.'''

    def victory():
        system("cls")
        print(f"{name}, you are victorious!")
        print("\nPlayer stats:\n")
        print(f"Name: {name}")
        if classes == "a":
            print("Class: Warrior")
        elif classes == "b":
            print("Class: Sorcerer")
        else:
            print("Class: Unknown to mankind")
        print(f"Level: {lvl}")
        print(f"HP: {hp}/{mhp}")
        print(f"Strength: {round(dmg)}")
        print(f"Defense: {defense}")
        if classes == "b":
            print(f"Chants used: {chants}\n")
        time.sleep(2)
        system("timeout -1")
        menu()
        '''En funktion som används när spelaren vinner.'''

    def prep():
        global ename, elvl, emhp, ehp, edmg, eboost, xd
        system("cls")

        list = ["Werewolf", "Golem", "Slime King"]
        list2 = ["Vampire", "Reaper", "Demon"]
        list3 = ["Wraith", "Red Crimson Demon", "Wyvern"]
        list4 = ["Titan", "Celestial Entity", "Seraphim"]
        '''Detta hanterar monsterns namn.'''

        if xd == 0:
            ename = list[random.randint(0, 2)]
            elvl = random.randint(1, 6)
            edmg = random.uniform(6, 11)
            emhp = random.randint(12, 23)
            ehp = emhp
            eboost = random.randint(21, 31), random.uniform(9, 12), random.randint(8, 11), random.randint(7, 11)  # hp, dmg, lvl, def
            battle()

        elif xd == 1:
            ename = list2[random.randint(0, 2)]
            elvl = random.randint(10, 30)
            edmg = random.uniform(14, 27)
            emhp = random.randint(28, 53)
            ehp = emhp
            eboost = random.randint(46, 73), random.uniform(12, 14), random.randint(18, 24), random.randint(11, 18)  # hp, dmg, lvl, def
            battle()

        elif xd == 2:
            ename = list3[random.randint(0, 2)]
            elvl = random.randint(40, 60)
            edmg = random.uniform(34, 61)
            emhp = random.randint(66, 112)
            ehp = emhp
            eboost = random.randint(132, 184), random.uniform(33, 38), random.randint(26, 37), random.randint(18, 37)  # hp, dmg, lvl, def
            battle()

        elif xd == 3:
            ename = list4[random.randint(0, 2)]
            elvl = random.randint(70, 100)
            edmg = random.uniform(83, 129)
            emhp = random.randint(168, 220)
            ehp = emhp
            eboost = random.randint(96, 106), random.uniform(47, 51), random.randint(58, 63), random.randint(37, 105)  # hp, dmg, lvl, def
            battle()
            '''En funktion som hanterar monsterns liv, skada, prestationsnivå samt rustningskydd.'''

    def battle():
        global lvl, hp, mhp, dmg, ehp, xd, defense, chants
        system("cls")

        print(f"\n\nName: {name}")
        if classes == "a":
            print("Class: Warrior")
        elif classes == "b":
            print("Class: Sorcerer")
        else:
            print("Class: Unknown to mankind")
        print(f"Level: {lvl}")

        print(f"\nHealth: {hp} / {mhp}")
        print(f"Strength: {round(dmg)}")
        print(f"Defense: {defense}")
        print("====================    ooooooooooooooooo")
        print("                        o A) Attack     o")
        print("                        o B) Run        o")
        if classes == "b":
            print("                        o C) Heal       o")
        print("====================    ooooooooooooooooo")
        print(f"Name: {ename}")
        print(f"Level: {elvl}")

        print(f"\nHealth: {round(ehp)} / {emhp}")
        print(f"Strength: {round(edmg)}")
        '''Detta är den visuella delen av striden med massvis summa av detaljerade information för spelaren.'''

        battlechoice = input("\n\n>> ").lower()
        if not battlechoice:
            battle()

        if battlechoice == "a":
            ehp -= dmg
            print(f"\n\nYou have hit the {ename} for {round(dmg)} ({round(ehp)}/{emhp})")
            system("timeout 3 >nul")
            '''Detta gör så att du slår fienden.'''

            if ehp <= 0:
                hp += eboost[0]
                mhp += eboost[0]
                dmg += eboost[1]
                lvl += eboost[2]
                defense += eboost[3]
                xd += 1
                if xd < 4:
                    print(f"\n\nYou have killed the {ename}, so you continue to fight other creatures.")
                    print(f"\nReward:")
                    print(f"{eboost[2]} +LVL")
                    print(f"{eboost[0]} +HP")
                    print(f"{eboost[2]} +DMG")
                    print(f"{eboost[3]} +DEF")
                    system("timeout 10 >nul")
                    prep()
                    '''Detta kollar om du har dödat fienden, och ifall du gjort det belönas du med statistik.'''
                elif xd == 4:
                    hp += eboost[0]
                    mhp += eboost[0]
                    dmg += eboost[1]
                    lvl += eboost[2]
                    defense += eboost[3]
                    print(f"\n\nYou have killed the {ename}, but there are no other creatures to fight.")
                    print(f"\nReward:")
                    print(f"{eboost[2]} +LVL")
                    print(f"{eboost[0]} +HP")
                    print(f"{eboost[2]} +DMG")
                    print(f"{eboost[3]} +DEF")
                    system("timeout 10 >nul")
                    victory()
                    '''Detta kollar ifall du har dödat den sista fienden, ifall du har gjort det vinner du över spelet.'''

            ACF = round(int(edmg * 100 / (100 + defense)))
            hp -= ACF
            print(f"The {ename} have hit you for {ACF} ({hp}/{mhp})")
            system("timeout 3 >nul")

            if hp <= 0:
                gameover()
            else:
                battle()
                '''Detta kontrollerar hur mycket skada fienden gör mot dig.'''


        elif battlechoice == "b":
            print(
                "\nYou have chosen to flee the battle.\nYou retreat to your castle and recover from the damage taken.")
            system("timeout 5 >nul")
            start()
            '''Denna funktion används när du flyr ifrån en strid mot ett monster.'''

        elif battlechoice == "c":
            if classes == "b":
                if chants < 3:

                    if lvl >= 60:
                        chants += 1
                        print("\nChanting yourself for health points.. (30 sec.)")
                        time.sleep(30)
                        chant = random.randint(22, 46)
                        mhp += chant
                        hp += chant
                        print(f"\n{chant} +HP")
                        system("timeout 3 >nul")

                    elif lvl >= 30:
                        chants += 1
                        print("\nChanting yourself for health points.. (20 sec.)")
                        time.sleep(20)
                        chant = random.randint(16, 38)
                        mhp += chant
                        hp += chant
                        print(f"\n{chant} +HP")
                        system("timeout 3 >nul")

                    elif lvl >= 10:
                        chants += 1
                        print("\nChanting yourself for health points.. (10 sec.)")
                        time.sleep(10)
                        chant = random.randint(8, 22)
                        mhp += chant
                        hp += chant
                        print(f"\n{chant} +HP")
                        system("timeout 3 >nul")

                    else:
                        print("\nYour level is too low to start chanting. (Level 10 Required.)")
                        system("timeout 2 >nul")
                    battle()
                    '''Denna flödestyrelsen kontrollerar hur mycket du kan läka dig själv samt när du kan börja läka dig.'''

                else:
                    print("\nYou can only chant yourself 3 times in one run.")
                    system("timeout 2 >nul")
                    battle()

            else:
                print("\nYou did not make a valid selection.")
                system("timeout 2 >nul")
                battle()

        else:
            print("\nYou did not make a valid selection.")
            system("timeout 2 >nul")
            battle()
            '''Detta kollar om användaren inte har skrivit in rätt alternativ.'''

    start()
    '''Detta startar den första funktionen som sedan hoppar vidare tills nästa och nästa och tillbaka osv.'''

menu()