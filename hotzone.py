class HotZone:
    def __init__(self, top, left, bottom, right, priority):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.priority = priority

    def get_coordinates(self):
        return self.top, self.left, self.bottom, self.right

    def is_inside(self, center_x, center_y):
        if self.left <= center_x <= self.right and self.top <= center_y <= self.bottom:
            return True
        return False
