from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import (
NumericProperty, ReferenceListProperty,ObjectProperty)
from kivy.vector import Vector
from random import randint

""" Pong game made with python kivy which
can be played on desktop and mobile """

class PongPaddle(Widget):
    score  = NumericProperty(0)
    
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            sx,sy = ball.speed
            offset  = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * sx,sy)
            spel = bounced * 1.1
            ball.speed = spel.x, spel.y + offset
            speedup = 1.1
            # offset = 0.02 * Vector(0, ball.center_y - self.center_y)
            # ball.speed = speedup * (offset - ball.speed)

class PongBall(Widget):
    
    # speed of the ball on x and y
    speed_x = NumericProperty(0)
    speed_y = NumericProperty(0)
    
    # using reference list property to use ball.speed as shorthand, 
    # just like using w.pos for w.x and w.y
    speed = ReferenceListProperty(speed_x,speed_y)
    
    # move function to move a step. It would be called in equal
    # intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.speed) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    
    def serve_ball(self, spel=(4,0)):
        self.ball.center = self.center
        self.ball.speed = spel
    
    def update(self, dt):
        # calling the ball and making updates
        self.ball.move()
        
        # paddle bounce
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
        # bounce the ball off the top and bottom
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.speed_y *= -1
            
            # point scored?
            if self.ball.x < self.x:
                self.player2.score += 1
                self.serve_ball(spel=(4,0))
            if self.ball.right > self.width:
                self.player1.score += 1
                self.serve_ball(spel=(-4, 0))
    
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
