class Center:
  def __init__(self, x, y, z):

    self.x = x
    self.y = y
    self.z = z

class Rotation:
  def __init__(self, x, y, z):

    self.x = x
    self.y = y
    self.z = z

class Dimension:
  def __init__(self, length, width, height):

    self.length = length
    self.width = width
    self.height = height

class Prim_Object:
  def __init__(self, name, center_x, center_y, center_z, rot_x, rot_y, rot_z, width, height, depth):

    self.name = name

    self.centroid = Center(center_x, center_y, center_z)

    self.dimensions = Dimension(width, height, depth)

    self.rotations = Rotation(rot_x, rot_y, rot_z)
