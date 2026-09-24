from manim import *
import math

class Clock():
    one = math.pi/6
    two = one*2
    three = one*3
    four = one*4
    five = one*5
    seven = one*7
    nine = one*9
    eleven = one*11

class IntroIntro(Scene):
    def construct(self):
        return super().construct()

class HexBg(Scene):
    global dotsGrid, patternList

    def construct(self):
        HexBg.dotsGrid = HexBg.makeBoard()
        HexBg.patternList = VGroup()
        self.play(FadeIn(HexBg.dotsGrid))
        #for some reason it's coming out as each individual line being a ease-in-out. idk why.
        pattern1 = self.drawPattern(3, 1, Clock.one, "qaq")
        pattern2 = self.drawPattern(3, 2, Clock.three, "aa")
        pattern3 = self.drawPattern(3, 4, Clock.one, "qaq")
        pattern4 = self.drawPattern(3, 5, Clock.one, "wa")
        pattern5 = self.drawPattern(4, 7, Clock.three, "wqaawdd")
        pattern6 = self.drawPattern(4, 10, Clock.three, "qaqqqqq")
        self.wait(1)
        self.clearBoard()
        self.play(FadeOut(HexBg.dotsGrid))

    def drawPattern(self, row, column, clockDirection, path, col=PURPLE_B):
        #from bottom left
        #take in a position, a direction, and an aqwed map, add a vgroup to list and return a vgroup
        #implied w in front of the aqwed map, that being the direction
        #direction like from a clock: 1, 3, 5, 7, 9, 11, where 3 is right and 9 is left
        #swap cos and sin

        #!!!!!!!IMPORTANT!!!!!!!
        #the construction of the pattern is like its declaration in the actual hexmod mod:
        #initial direction and then only store the angles of each 'joint'
        #meaning, if the initial direction changes, it's still the same pattern.
        #e.g. pattern4 is always going to be alidade's even if it's the book rotation

        #default color is purple B
        #yellow for inside intro/retro
        #red for error
        #blue for second tier of intro/retro

        #create the first line
        pattern = VGroup()
        lineOut = Line(
            HexBg.dotsGrid[row][column].get_center(), HexBg.dotsGrid[row][column].get_center() + UP*math.cos(clockDirection) + RIGHT*math.sin(clockDirection),
            0, 0, stroke_width=6, color=col
        )
        loc = HexBg.dotsGrid[row][column].get_center() + UP*math.cos(clockDirection) + RIGHT*math.sin(clockDirection)
        pattern.add(lineOut)
        dir = clockDirection
        for c in path:
            #change the direction based on c
            match c:
                case "a": dir = dir - Clock.four
                case "q": dir = dir - Clock.two
                case "w": dir = dir
                case "e": dir = dir + Clock.two
                case "d": dir = dir + Clock.four
            #make a line in that direction
            line = Line(loc, loc + UP*math.cos(dir) + RIGHT*math.sin(dir), 0, 0, stroke_width=6, color=col)
            pattern.add(line)
            #update loc accordingly
            loc = loc + UP*math.cos(dir) + RIGHT*math.sin(dir)
            #add line to pattern
        self.play(AnimationGroup(Create(pattern), rate_func=rate_functions.linear, run_time=len(pattern)*.15))
        HexBg.patternList.add(pattern)
        return pattern

    def clearPattern(self, pattern):
        HexBg.patternList.remove(pattern)
        self.play(FadeOut(pattern))

    def clearBoard(self):
        self.play(FadeOut(HexBg.patternList))
        HexBg.patternList = VGroup()

    def makeBoard():
        #makes the board and makes it easily accessible through double indices, logically
        length = 7
        height = 5
        spacing = 1
        dotsGrid = VGroup.add(
            *[VGroup().add(
                *[Dot().set_color(PURPLE_A).shift(RIGHT*spacing*shift) for shift in range(-length,length)]
            ).shift((UP*math.sqrt(3)/2)*spacing*shift) for shift in range(-height,height)]
        )
        #indices 0-2l are the bottom row, while 2l+1, 2l+2...2l+2h are each row in rising order, then another index for a specific dot in there
        dotsGrid.set_opacity(.4)
        for i in range((2*length) + 1, ((2*length) + 1)+2*height-2, 2):
            dotsGrid[i].shift(RIGHT*spacing*.5)
        returnDots = VGroup()
        bottomRow = VGroup()
        for i in range(2*length):
            bottomRow.add(dotsGrid[i])
        returnDots.add(bottomRow)
        for i in range((2*length) + 1, ((2*length) + 1)+2*height-2):
            returnDots.add(dotsGrid[i])
        bottomRow.move_to(returnDots[2])
        bottomRow.shift(DOWN*math.sqrt(3))
        return returnDots