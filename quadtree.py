import numpy as np
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distancetocenter(self, center):
        return math.sqrt((center.x-self.x)**2 + (center.y-self.y)**2)

class Rectangle:
    def __init__(self, center, width, height):
        self.center= center
        self.width = width
        self.height = height
        self.west = center.x - width
        self.east = center.x + width
        self.north = center.y - height
        self.south = center.y + height

    def containspoint(self, point):
        return (self.west <= point.x < self.east and
               self.north <= point.y <self.south)
    
    def intersects(self, range):
        return not (range.west > self.east or
                    range.east < self.west or
                    range.north > self.south or
                    range.south < self.north)

    def draw(self, ax, c='k', lw=1, **kwargs):
        x1, y1 =self.west, self.north
        x2, y2 =self.east, self.south
        ax.plot([x1,x2,x2,x1,x1], [y1,y1,y2,y2,y1], c=c, lw=lw, **kwargs)


class Quadtree:
    def __init__(self, boundary, capacity =1):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        # caso o ponto esteja no alcance da quadtree atual
        if not self.boundary.containspoint(point):
            return False
    
        #se não tiver alcançado a capacidade
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.divide()
        
        if self.nw.insert(point):
            return True
        elif self.ne.insert(point):
            return True
        elif self.sw.insert(point):
            return True
        elif self.se.insert(point):
            return True

        return False

    def queryrange(self, range):
        found_points = []

        if not self.boundary.intersects(range):
            return []

        for point in self.points:
            if range.containspoint(point):
                found_points.append(point)

        if self.divided:
            found_points.extend(self.nw.queryrange(range))
            found_points.extend(self.ne.queryrange(range))
            found_points.extend(self.sw.queryrange(range))
            found_points.extend(self.se.queryrange(range))

        return found_points

    def queryradius(self, range, center):
        found_points = []

        if not self.boundary.intersects(range):
            return []

        for point in self.points:
            if range.containspoint(point) and point.distancetocenter(center) <= range.width:
                found_points.append(point)

        if self.divided:
            found_points.extend(self.nw.queryradius(range, center))
            found_points.extend(self.ne.queryradius(range, center))
            found_points.extend(self.sw.queryradius(range, center))
            found_points.extend(self.se.queryradius(range, center))

            return found_points

    def divide(self):
        center_x = self.boundary.center.x
        center_y = self.boundary.center.y
        new_width = self.boundary.width / 2
        new_height = self.boundary.height / 2

        nw = Rectangle(Point(center_x - new_width, center_y - new_height), new_width, new_height)
        self.nw = Quadtree (nw)
        for p in self.points:
                if self.nw.boundary.containspoint(p):
                    self.nw.points.append(p)

        ne = Rectangle(Point(center_x + new_width, center_y - new_height), new_width, new_height)
        self.ne = Quadtree (ne)
        for p in self.points:
            if self.ne.boundary.containspoint(p):
                self.ne.points.append(p)

        sw = Rectangle(Point(center_x - new_width, center_y + new_height), new_width, new_height)
        self.sw = Quadtree (sw)
        for p in self.points:
            if self.sw.boundary.containspoint(p):
                self.sw.points.append(p)

        se = Rectangle(Point(center_x + new_width, center_y + new_height), new_width, new_height)
        self.se = Quadtree (se)
        for p in self.points:
            if self.se.boundary.containspoint(p):
                self.se.points.append(p)

        self.divided = True

    def __len__(self):
        count = len(self.points)
        if self.divided:
            count += len(self.nw) + len(self.ne) + len(self.sw) + len(self.se)

        return count

    def draw (self, ax):
        self.boundary.draw(ax)

        if self.divided:
            self.nw.draw(ax)
            self.ne.draw(ax)
            self.se.draw(ax)
            self.sw.draw(ax)