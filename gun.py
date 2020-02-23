from random import randrange as rnd, choice
import tkinter as tk
import math
import time


# print (dir(math))
def main():
    global root, fr, canvas
    root = tk.Tk()
    fr = tk.Frame(root)
    root.geometry('800x600')
    canvas = tk.Canvas(root, bg='white')
    canvas.pack(fill=tk.BOTH, expand=1)


class Ball:
    def __init__(self, x, y, vx, vy):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.x += self.vx
        self.y -= self.vy
        self.set_coords()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        flag_x_condition = (self.x + self.r) >= obj.x and (self.x - self.r) <= obj.x
        flag_y_condition = (self.y + self.r) >= obj.y and (self.y - self.r) <= obj.y
        if flag_x_condition and flag_y_condition:
            return True
        # FIXME
        return False


class Gun:
    def __init__(self, balls, bullet):
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.id = canvas.create_line(20, 450, 50, 420, width=7)  # FIXME: don't know how to set it...
        self.balls = balls
        self.bullet = bullet

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.bullet += 1
        self.angle = math.atan((event.y - self.y) / (event.x - self.x))
        self.dxv = self.f2_power * math.cos(self.angle)
        self.dyv = - self.f2_power * math.sin(self.angle)
        new_ball = Ball(self.x, self.y, self.dxv, self.dyv)
        new_ball.r += 5
        self.balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        self.x = 20 + max(self.f2_power, 20) * math.cos(self.angle)
        self.y = 450 + max(self.f2_power, 20) * math.sin(self.angle)
        canvas.coords(self.id, 20, 450, self.x, self.y)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        # FIXME: don't work!!! How to call this functions when object is created?
        self.id = canvas.create_oval(0, 0, 0, 0)
        self.id_points = canvas.create_text(30, 30, text=self.points, font='28')
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canvas.coords(self.id, x - r, y - r, x + r, y + r)
        canvas.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canvas.itemconfig(self.id_points, text=self.points)



class Game:
    def __init__(self):
        self.target = Target()
        self.screen1 = canvas.create_text(400, 300, text='', font='28')
        self.gun = Gun(balls=[], bullet=0)

    def move_ball(self):
        self.target.new_target()
        canvas.bind('<Button-1>', self.gun.fire2_start)
        canvas.bind('<ButtonRelease-1>', self.gun.fire2_end)
        canvas.bind('<Motion>', self.gun.targetting)
        self.target.live = 1
        while self.target.live:
            print(self.gun.balls)
            for b in self.gun.balls:
                b.move()
                if b.hittest(self.target) and self.target.live:
                    self.target.live = 0
                    self.target.hit()
                    canvas.bind('<Button-1>', '')
                    canvas.bind('<ButtonRelease-1>', '')
                    canvas.itemconfig(self.screen1, text='Вы уничтожили цель за ' + str(self.gun.bullet) + ' выстрелов')
                    canvas.update()
            canvas.update()
        #TODO: will make to pop ball from list and create wall
            time.sleep(0.03)
            self.gun.targetting()
            self.gun.power_up()
        self.gun.balls.pop()
        canvas.itemconfig(self.screen1, text='')
        canvas.delete(self.gun)
        root.after(750, self.move_ball)

main()
game = Game()
game.move_ball()
root.mainloop()
