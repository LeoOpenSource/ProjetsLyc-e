# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 19:54:46 2025

@author: LILARI
"""

import pyxel
import math
import random


# UIs


class ScoreUI:
    def __init__(self, score, lvl):
        # Set up player's stats
        self.score = score
        self.lvl = lvl

    def update(self, new_score, lvl):
        self.score = new_score
        self.lvl = lvl

    def draw(self):
        # Draw MainUI's background
        pyxel.rect(0, 0, 128, 20, 4)

        pyxel.rect(80, 5, 40, 10, 15)
        pyxel.text(82, 7, str(self.score), 0)
        pyxel.text(30, 7, "Stage : " + str(self.lvl), 0)


class Article:
    def __init__(self, ball, x, y, size, offset):
        # Set the price of the article
        self.article = ball
        self.id = ball[0]

        self.base_price = ball[1]
        self.price = 0

        # Set object properies
        self.color_bg = 15
        self.article_color = ball[2]
        self.x = x
        self.y = y
        self.size = size
        self.offset = offset
        print(self.x, self.y)

    def afford_ball(self, article_amount):
        if self.id in self.article_classes:
            article_class = self.article_classes[self.id]
            article_amount[self.id].append(article_class())
            msg = Message([30, 112], 7, f"Bought {article_class.__name__}")
            print("User can buy")
        return article_amount, msg

    def upgrade_ball(self, article_amount):
        if self.id in self.article_classes:
            article_class = self.article_classes[self.id]
            for article in article_amount[self.id]:
                article.level += 1
            msg = Message([30, 112], 7, f"Upgraded {article_class.__name__}")
            print("User can buy")
        return article_amount, msg

    def draw(self):
        # Draw the frame
        pyxel.rect(self.x, self.y - 8, self.size - self.offset,
                   self.size - self.offset, self.color_bg)
        # Draw the ball icone
        pyxel.circ(self.x + self.size / 3, self.y, 2, self.article_color)
        # Draw the price
        pyxel.text(self.x + self.size / 7, self.y + 4, str(self.price), 0)


class Ball_Article(Article):
    def __init__(self, ball, x, y, size, offset):
        super().__init__(ball, x, y, size, offset)
        # Set classes dictionnary
        self.article_classes = {
            0: BasicBall,
            1: PlasmaBall,
            2: SniperBall,
            3: CanonBall,
            4: AngelBall,
            5: ScatterBall
        }

    def update(self, score, article_amount):
        self.price = (self.base_price + int(0.25 *
                      len(article_amount[self.id]) * self.base_price))
        # Set message variable
        msg = None

        # Check mouse hover
        if (self.x < pyxel.mouse_x < self.x + self.size - self.offset and
                self.y - 8 < pyxel.mouse_y < self.y - 8 + self.size
                - self.offset):

            self.color_bg = 7

            # Check mouse click
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                if self.price <= score:
                    score -= self.price
                    if self.id in self.article_classes:
                        article_amount, msg = self.afford_ball(article_amount)

        else:
            self.color_bg = 15

        return score, article_amount, msg


class Upgrade_Article(Article):
    def __init__(self, ball, x, y, size, offset):
        super().__init__(ball, x, y, size, offset)
        # Set classes dictionnary
        self.article_classes = {
            0: BasicBall,
            1: PlasmaBall,
            2: SniperBall,
            3: CanonBall,
            4: AngelBall,
            5: ScatterBall
        }

        # Set ball ownership propert
        self.owned = False

        # Get ball level
        self.level = 1

    def update(self, score, article_amount):
        # if the ball is owned by the player, show it
        if len(article_amount[self.id]) != 0:
            # Update the ball level
            self.level = article_amount[self.id][0].level

            if not self.owned:
                self.owned = True

        self.price = (self.base_price + int(0.25 *
                      self.level * self.base_price))

        # Set message variable
        msg = None

        # Check mouse hover
        if (self.x < pyxel.mouse_x < self.x + self.size - self.offset and
                self.y - 8 < pyxel.mouse_y < self.y - 8 + self.size
                - self.offset):

            self.color_bg = 7

            # Check mouse click
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                if self.price <= score:
                    score -= self.price
                    article_amount, msg = self.upgrade_ball(article_amount)

        else:
            self.color_bg = 15

        return score, article_amount, msg

    def draw(self):
        if self.owned:
            super().draw()
            # Draw the level
            pyxel.text(self.x + self.size / 10, self.y + 12,
                       "lvl" + str(self.level), 7)


class BoutiqueUI:
    def __init__(self):
        # Set ShopUI's state
        self.state = False

    def init_articles(self):
        # Set shopUI's properties
        amount = len(self.balls)
        amount_per_line = 5
        offset = 6
        size = (128 - offset) // amount_per_line
        count = 0
        for i in range(amount):
            if amount_per_line * (count + 1) - i <= 0:
                count += 1

            x = (i - count * amount_per_line) * size + offset
            y = 48 + count * (size + offset)
            if self.name == "SHOP":
                self.articles.append(Ball_Article(self.balls[i], x, y,
                                     size, offset))
            elif self.name == "UPGRADE":
                self.articles.append(Upgrade_Article(self.balls[i], x, y,
                                                     size, offset))

    def update(self, score, balls, messageservice):
        if self.state:
            # update prices
            for article in self.articles:
                score, balls, message = article.update(score, balls)

                if message:
                    messageservice.Actual_message = message

        # Return new score and balls to the MainUI
        return score, balls

    def draw_name(self):
        # Draw UI's Name
        pyxel.text(self.title_x, 25, str(self.name), 7)

    def draw(self):
        if self.state:
            self.draw_name()
            # Draw article's Frames
            for article in self.articles:
                article.draw()


class ShopUI(BoutiqueUI):
    def __init__(self):
        super().__init__()
        # Set UI's Name
        self.name = "SHOP"
        self.title_x = 56

        # Set game Balls bank
        self.balls = [
            # [rank, price, color]
            # Basic Ball
            [0, 100, 4],
            # Plasma Ball
            [1, 200, 8],
            # Sniper Ball
            [2, 300, 7],
            # Cannon Ball
            [3, 400, 9],
            # Angel Ball
            [4, 500, 10],
            # Scatter Ball
            [5, 600, 6]
            ]

        self.articles = []
        self.init_articles()


class UpgradeUI(BoutiqueUI):
    def __init__(self):
        super().__init__()

        # Set UI's Name
        self.name = "UPGRADE"
        self.title_x = 50

        # Set game Balls bank
        self.balls = [
            # Basic Ball
            [0, 100, 4],
            # Plasma Ball
            [1, 200, 8],
            # Sniper Ball
            [2, 300, 7],
            # Cannon Ball
            [3, 400, 9],
            # Angel Ball
            [4, 500, 10],
            # Scatter Ball
            [5, 50, 6]
            ]

        self.articles = []
        self.init_articles()


class MainUI:
    def __init__(self):
        # Initialise ShopUI
        self.ShopUI = ShopUI()
        self.UpgradeUI = UpgradeUI()

        # Set Shop's variables
        self.shop_bg = 6
        self.upgrade_bg = 10

        self.state = False

    def update(self, score, balls, messageservice):
        # Check if UI is open
        if self.state:

            # Check mouse hover Shop button
            if 28 < pyxel.mouse_x < 100 and 30 < pyxel.mouse_y < 50:
                self.shop_bg = 7

                # Check mouse click
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    if not self.ShopUI.state:
                        self.ShopUI.state = True
                        self.state = False

            # Check mouse hover Upgrade button
            elif 28 < pyxel.mouse_x < 100 and 55 < pyxel.mouse_y < 75:
                self.upgrade_bg = 7

                # Check mouse click
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    if not self.UpgradeUI.state:
                        self.UpgradeUI.state = True
                        self.state = False

            # Reset background colors
            else:
                self.upgrade_bg = 6
                self.shop_bg = 10

        # Return new score and balls of the user provided by shopUI
        score, balls = self.ShopUI.update(score, balls, messageservice)
        score, balls = self.UpgradeUI.update(score, balls, messageservice)
        return score, balls

    def draw(self):
        if self.state:
            pyxel.rect(28, 30, 72, 20, self.shop_bg)
            pyxel.text(28 + 30, 30 + 10, "SHOP", 0)
            pyxel.rect(28, 55, 72, 20, self.upgrade_bg)
            pyxel.text(28 + 24, 55 + 10, "UPGRADE", 0)

        self.ShopUI.draw()
        self.UpgradeUI.draw()

# Message service


class Message:
    def __init__(self, pos, color, text):
        self.color = color
        self.x = pos[0]
        self.y = pos[1]
        self.text = text
        self.birthdate = pyxel.frame_count
        self.lifetime = 4

        self.state = True

    def update(self):
        if self.state:
            if pyxel.frame_count - self.birthdate > self.lifetime * 60:
                self.state = False

    def draw(self):
        if self.state:
            pyxel.text(self.x, self.y, str(self.text), self.color)


class MessageService:
    def __init__(self):
        self.Actual_message = None

    def update(self):
        if self.Actual_message:
            self.Actual_message.update()

            if not self.Actual_message.state:
                self.Actual_message = None

    def draw(self):
        if self.Actual_message:
            self.Actual_message.draw()

# Buttons bank


class Button:
    def __init__(self, pos, size):
        # Set Icone's properties
        self.color_bg = 15
        self.x = pos[0]
        self.y = pos[1]
        self.size = size

    def update(self):
        # Update the color according to mouse hover
        if (self.x < pyxel.mouse_x < self.x + self.size and
                self.y < pyxel.mouse_y < self.y + self.size):

            self.color_bg = 7
        else:

            self.color_bg = 15

    def draw(self):
        # Draw the frame
        pyxel.rect(self.x, self.y, self.size, self.size, self.color_bg)


class OpenUIButton(Button):
    def __init__(self, pos, size):
        super().__init__(pos, size)

        # Initialise MainUI
        self.MainUI = MainUI()

    def update(self, state, score, balls, messageservice):
        super().update()

        # Check mouse hover
        if (self.x < pyxel.mouse_x < self.x + self.size and
                self.y < pyxel.mouse_y < self.y + self.size):

            # Check mouse click
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                if state:
                    # Close all UIs
                    self.MainUI.state = False
                    self.MainUI.ShopUI.state = False
                    self.MainUI.UpgradeUI.state = False
                else:
                    # Open MainUI
                    self.MainUI.state = True

        # Return the new score and balls provided by MainUI
        return self.MainUI.update(score, balls, messageservice)

    def draw(self):
        self.MainUI.draw()
        super().draw()
        # Draw Menu's Icone
        for i in range(1, 4):
            pyxel.rect(self.x + 2, self.y + i*2, 6, 1, 0)


class GUIService:
    def __init__(self):
        # Initialise Icones
        self.MessageService = MessageService()
        self.MenuIcone = OpenUIButton([10, 5], 10)
        self.state = False

    def update(self, score, balls):
        # Get the state of the UIs
        self.state = (self.MenuIcone.MainUI.state or
                      self.MenuIcone.MainUI.ShopUI.state or
                      self.MenuIcone.MainUI.UpgradeUI.state)

        self.MessageService.update()

        # Return the new score and balls provided by the root button
        return self.MenuIcone.update(self.state, score, balls,
                                     self.MessageService)

    def draw(self):
        self.MenuIcone.draw()

        self.MessageService.draw()

# Workspace

    # Stage generation related


class Brick:
    def __init__(self, pos, hp):
        # Set Brick's position
        self.x = pos[0]
        self.y = pos[1]

        # Set Brick's properties
        self.hp = hp
        self.value = hp

        self.color = 1 + self.hp % 15
        self.size_x = 10
        self.size_y = 4

        # Get the time the Brick was created
        self.last_invoke = pyxel.frame_count

    def update(self):
        if self.hp > 0:
            self.color = 1 + self.hp % 15
            # Check mouse hover
            if (self.x < pyxel.mouse_x < self.x + self.size_x and
                    self.y < pyxel.mouse_y < self.y + self.size_y):
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    self.hp -= 1

        else:
            self.color = 0

    def draw(self):
        pyxel.rect(self.x, self.y, self.size_x, self.size_y, self.color)


class Boss(Brick):
    def __init__(self, pos, hp):
        super().__init__(pos, hp)
        self.size_x = 40
        self.size_y = 16

    def draw(self):
        super().draw()
        pyxel.text(self.x + self.size_x / 3, self.y + self.size_y / 3,
                   str(self.hp), 0)


class Stage:
    def __init__(self, lvl):
        self.Bricks = []
        if lvl % 10 == 0:
            self.Bricks.append(Boss([44, 52], lvl * 100))
        else:
            for i in range(112 // 11):
                for j in range(92 // 5):
                    spawn = random.randint(0, 1)
                    if spawn == 0:
                        x = i * (10 + 1) + 10
                        y = j * (4 + 1) + 28
                        self.Bricks.append(Brick([x, y], lvl))

        self.completion_reward = len(self.Bricks) * lvl // 5

    def update(self, score):
        # Handle Brick's status
        for Brick in self.Bricks:
            Brick.update()
            if Brick.hp <= 0:
                self.Bricks.remove(Brick)
                score += Brick.value

        return score

    def draw(self):
        for Brick in self.Bricks:
            Brick.draw()

    # Balls bank


class Ball:
    def __init__(self):
        # Set ball's starting position
        self.x = random.randint(10, 118)
        self.y = random.randint(30, 118)

        # Set ball's properties
        self.radius = 1
        self.color = 4
        self.level = 1

        self.speed_x = 0.5
        self.speed_y = 1
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

        self.damage = self.level

        # Properties useful for scatterBall and non permanent balls
        self.birthdate = 0
        self.lifetime = 0

    def check_horizontal_collisions(self, Brick):

        # Check if the ball hits the up and bottom parts of the brick
        if (Brick.x - self.radius <= round(self.x)
            <= Brick.x + Brick.size_x + self.radius
            and (round(self.y) == Brick.y - self.radius
                 or round(self.y) == Brick.y + Brick.size_y + self.radius)):
            return True
        return False

    def check_vertical_collisions(self, Brick):

        # Check if the ball hits the side parts of the brick
        if (Brick.y - self.radius <= round(self.y)
            <= Brick.y + Brick.size_y + self.radius
            and (round(self.x) == Brick.x - self.radius
                 or round(self.x) == Brick.x + Brick.size_x + self.radius)):
            return True
        return False

    def update_position(self):
        self.x = round(self.x + self.direction_x * self.speed_x, 1)
        self.y = round(self.y + self.direction_y * self.speed_y, 1)

    def update(self):

        # Check collision on screen's sides
        if self.x + self.radius >= 128 or self.x - self.radius <= 0:
            self.direction_x *= -1

        if self.y + self.radius >= 128 or self.y - self.radius <= 20:
            self.direction_y *= -1

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)


class BasicBall(Ball):
    def update(self, Bricks):
        super().update()

        for Brick in Bricks:
            # Calculate collisions on horizontal sides
            if self.check_horizontal_collisions(Brick):
                self.direction_y *= -1

                Brick.hp -= self.damage
                break

            # Calculate collisions on vertical sides
            elif self.check_vertical_collisions(Brick):
                self.direction_x *= -1

                Brick.hp -= self.damage
                break

        self.update_position()


class PlasmaBall(Ball):
    def __init__(self):
        super().__init__()

        # Set ball's properties
        self.range = 20
        self.radius = 2
        self.damage = self.level * 2

        self.color = 8
        self.speed_x = 0.5
        self.speed_y = 0.25

    def update(self, Bricks):
        super().update()
        for Brick in Bricks:

            # Calculate collisions on horizontal sides
            if self.check_horizontal_collisions(Brick):
                self.direction_y *= -1

                Brick.hp -= self.damage

                # Find if there are other bricks in range
                for arround_Brick in Bricks:
                    if (abs(arround_Brick.x - Brick.x) < self.range and
                            abs(arround_Brick.y - Brick.y) < self.range):

                        arround_Brick.hp -= self.damage
                break

            # Calculate collisions on vertical sides
            elif self.check_vertical_collisions(Brick):
                self.direction_x *= -1

                Brick.hp -= self.damage

                # Check if there are other bricks in range
                for arround_Brick in Bricks:
                    if (abs(arround_Brick.x - Brick.x) < self.range and
                            abs(arround_Brick.y - Brick.y) < self.range):

                        arround_Brick.hp -= self.damage
                break

        self.update_position()


class SniperBall(Ball):
    def __init__(self):
        super().__init__()

        # Set ball's properties
        self.target = None
        self.damage = self.level * 3
        self.color = 7
        self.speed_x = 1
        self.speed_y = 1

    def lock_target(self):
        dx = (self.target.x + self.target.size_x / 2 - self.x)
        dy = (self.target.y + self.target.size_y / 2 - self.y)
        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        if magnitude != 0:
            # Set direction of the ball to the go to the target's position
            self.direction_x = round(dx / magnitude, 1) / self.speed_x
            self.direction_y = round(dy / magnitude, 1) / self.speed_y

    def collide_smartly(self):
        # Check collision on screen's sides
        if (self.x + self.radius >= 128 or self.x - self.radius <= 0 or
                self.y + self.radius >= 128 or self.y - self.radius <= 20):
            self.lock_target()

    def update(self, Bricks):
        self.collide_smartly()

        for Brick in Bricks:
            # Calculate collisions on horizontal sides
            if self.check_horizontal_collisions(Brick):
                self.direction_y *= -1

                Brick.hp -= self.damage
                # Set the ball's target
                self.target = Brick
                break

            # Calculate collisions on vertical sides
            elif self.check_vertical_collisions(Brick):
                self.direction_x *= -1

                # Set the ball's target
                Brick.hp -= self.damage

                self.target = Brick

                break

        # Change target if the last target is dead
        if self.target not in Bricks and self.target is not None:
            print("target died")
            # Choose closest brick
            target_candidate = None
            for Brick in Bricks:
                if not target_candidate:
                    target_candidate = Brick

                dx = self.x - Brick.x
                dxref = self.x - target_candidate.x
                dy = self.y - Brick.y
                dyref = self.y - target_candidate.x

                if math.sqrt(dx**2 + dy**2) < math.sqrt(dxref**2 + dyref**2):
                    target_candidate = Brick
            self.target = target_candidate

        elif self.target is None:
            self.target = Bricks[random.randint(0, len(Bricks) - 1)]

        self.update_position()

    def draw(self):
        super().draw()
        if self.target:
            pyxel.circb(self.target.x + self.target.size_x / 2,
                        self.target.y + self.target.size_y / 2, self.radius, 8)


class CanonBall(Ball):
    def __init__(self):
        super().__init__()

        # Set ball's properties
        self.radius = 3
        self.damage = self.level * 5
        self.color = 9
        self.speed_x = 1
        self.speed_y = 1

    def update(self, Bricks):
        super().update()

        for Brick in Bricks:
            # Calculate collisions on horizontal sides
            if self.check_horizontal_collisions(Brick):
                self.direction_y *= -1

                Brick.hp -= self.damage
                break

            # Calculate collisions on vertical sides
            elif self.check_vertical_collisions(Brick):
                self.direction_x *= -1

                Brick.hp -= self.damage
                break

        self.update_position()


class AngelBall(Ball):
    def __init__(self):
        super().__init__()

        # Set ball's properties
        self.radius = 2
        self.buff = self.level * 5
        self.color = 10
        self.speed_x = 2
        self.speed_y = 2

    def update(self, Bricks):
        super().update()

        for Brick in Bricks:
            # Calculate collisions on horizontal sides
            if self.check_horizontal_collisions(Brick):
                self.direction_y *= -1

                Brick.value += self.buff
                break

            # Calculate collisions on vertical sides
            elif self.check_vertical_collisions(Brick):
                self.direction_x *= -1

                Brick.value += self.buff
                break
        self.update_position()


class ScatterBall(Ball):
    def __init__(self):
        super().__init__()

        # Set ball's properties
        self.radius = 2
        self.damage = self.level * 2
        self.color = 6
        self.speed_x = 1
        self.speed_y = 1

        # Set properties linked to scatter
        self.child_limit = 7
        self.scattered_list = []

    def scatter(self, Brick):
        Scatter = BasicBall()
        Scatter.direction_y = self.direction_y
        Scatter.direction_x = self.direction_x
        Scatter.x = self.x
        Scatter.y = self.y
        Scatter.color = 6
        Scatter.lifetime = 60 * 10
        Scatter.birthdate = pyxel.frame_count
        self.scattered_list.append(Scatter)

    def update(self, Bricks):
        super().update()

        for Brick in Bricks:
            # Calculate collisions on horizontal sides
            if self.check_horizontal_collisions(Brick):
                self.direction_y *= -1
                Brick.hp -= self.damage
                if len(self.scattered_list) < self.child_limit:
                    self.scatter(Brick)
                break

            # Calculate collisions on vertical sides
            elif self.check_vertical_collisions(Brick):
                self.direction_x *= -1
                Brick.hp -= self.damage
                if len(self.scattered_list) < self.child_limit:
                    self.scatter(Brick)
                break
        self.update_position()

        for scatter in self.scattered_list:
            if pyxel.frame_count - scatter.birthdate >= scatter.lifetime:
                self.scattered_list.remove(scatter)
            else:
                scatter.update(Bricks)

    def draw(self):
        super().draw()
        for scatter in self.scattered_list:
            scatter.draw()

    # Main game


class Game:
    def __init__(self):
        # Intialise the Game
        self.pixels = 128

        print("game started")
        pyxel.init(self.pixels, self.pixels, title="Idle Bricks",
                   fps=60, quit_key=pyxel.KEY_ESCAPE)

        pyxel.mouse(visible=True)

        # Set up player's stats
        self.score = 100
        self.lvl = 1

        # Set up UIs
        self.GUIService = GUIService()

        self.ScoreUI = ScoreUI(self.score, self.lvl)

        # Set up game
        self.Stage = Stage(self.lvl)

        self.Balls = [[], [], [], [], [], []]
        self.Skils = []
        """
        self.Balls[0].append(BasicBall())
        self.Balls[1].append(PlasmaBall())
        self.Balls[2].append(SniperBall())
        self.Balls[3].append(CanonBall())
        self.Balls[4].append(AngelBall())
        self.Balls[5].append(ScatterBall())
        """
        # Run the game !!
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.GUIService.state:

            # Handle Stage's status
            self.score = self.Stage.update(self.score)
            if len(self.Stage.Bricks) == 0:
                print("staged finished")
                reward = self.Stage.completion_reward
                self.score += reward
                msg = Message([30, 112], 7, f"Awarded {reward} Credits")
                self.GUIService.MessageService.Actual_message = msg
                self.lvl += 1
                self.Stage = Stage(self.lvl)

            # Handle Ball's status
            for category in self.Balls:
                for Ball in category:
                    Ball.update(self.Stage.Bricks)

        self.score, self.Balls = self.GUIService.update(self.score, self.Balls)

        # Handle Score
        self.ScoreUI.update(self.score, self.lvl)

    def draw(self):
        pyxel.cls(0)
        if not self.GUIService.state:
            # Draw Game
            self.Stage.draw()
            for category in self.Balls:
                for Ball in category:
                    Ball.draw()

        # Draw Score
        self.ScoreUI.draw()

        # Draw UIs
        self.GUIService.draw()


Game()
