import pyglet, tkengine, random, math

class Cell(object):
	def __init__(self, x, y, wall, batch, scale):
		self.y = y
		self.x = x
		self.neighbors = { "W": None, "E": None, "S": None, "N": None,
			"NW": None, "NE": None, "SW": None, "SE": None}
		self.wall = random.randint(0, 100) < 45
		self.sprite = None
		if self.wall:
			self.sprite = pyglet.sprite.Sprite(wall, x=x*32*scale, y=y*32*scale,
						batch=batch)
			self.sprite.scale = scale

	def __str__(self):
		return "({}, {}) : {} {}".format(self.x, self.y,
			"Wall" if self.wall else "Empty", "Sprite" if self.sprite else "None")


class Main(tkengine.TkScene):

	def __init__(self, world, size_x, size_y, scale):
		self.world = world
		self.size_x = size_x
		self.size_y = size_y
		self.scale = scale
		self.batch = pyglet.graphics.Batch()
		self.wall = pyglet.image.load("assets/wall.png")
		self.field = [[
			Cell(x, y, self.wall, self.batch, self.scale) for y in range(self.size_y)]
				for x in range(self.size_x)
		]
		self._init_neighbors()
		self.x = 0
		self.y = 0
		current_image = pyglet.image.load("assets/selected.png")
		self.cursor = pyglet.sprite.Sprite(current_image, 0, 0)
		self.cursor.scale = self.scale
		self.key_handlers = {
			pyglet.window.key.ESCAPE	: pyglet.app.exit,
			pyglet.window.key.RETURN	: self._whole,
			pyglet.window.key.TAB		: self._step,
			pyglet.window.key.SPACE		: self._switch,
			pyglet.window.key.LEFT		: lambda : self._move_cursor(-1, 0),
			pyglet.window.key.UP		: lambda : self._move_cursor(0, 1),
			pyglet.window.key.RIGHT		: lambda : self._move_cursor(1, 0),
			pyglet.window.key.DOWN		: lambda : self._move_cursor(0, -1),
		}
		pyglet.gl.glClearColor(0.1, 0.1, 0.1, 0.0)

	def on_draw(self):
		self.world.window.clear()
		self.batch.draw()
		self.cursor.draw()

	def _switch(self):
		current = self.field[self.x][self.y]
		if current.wall:
			self._remove_wall(self.x, self.y)
		else:
			self._make_wall(self.x, self.y)

	def _move_cursor(self, x, y):
		if self.x + x >= 0 and self.x + x < self.size_x - 1 and \
				self.y + y >= 0 and self.y + y < self.size_y - 1:
			self.cursor.x += 32*self.scale*x 
			self.cursor.y += 32*self.scale*y
			self.x += x
			self.y += y

	def _init_neighbors(self):
		for x in range(self.size_x):
			for y in range(self.size_y):
				if x > 0:
					self.field[x][y].neighbors["W"] = self.field[x - 1][y]
				if x < self.size_x -1:
					self.field[x][y].neighbors["E"] = self.field[x + 1][y]
				if y > 0:
					self.field[x][y].neighbors["S"] = self.field[x][y - 1]
				if y < self.size_y -1:
					self.field[x][y].neighbors["N"] = self.field[x][y + 1]
				if x > 0 and y < self.size_y -1:
					self.field[x][y].neighbors["NW"] = self.field[x - 1][y + 1]
				if x < self.size_y - 1 and y < self.size_y -1:
					self.field[x][y].neighbors["NE"] = self.field[x + 1][y + 1]
				if x > 0 and y > 0:
					self.field[x][y].neighbors["SW"] = self.field[x - 1][y - 1]
				if x < self.size_x - 1 and y > 0:
					self.field[x][y].neighbors["SE"] = self.field[x + 1][y - 1]

	def _make_wall(self, x, y):
		self.field[x][y].wall = True
		self.field[x][y].sprite = pyglet.sprite.Sprite(self.wall, x=x*32*self.scale, y=y*32*self.scale,
			batch=self.batch)
		self.field[x][y].sprite.scale = self.scale

	def _remove_wall(self, x, y):
		self.field[x][y].wall = False
		self.field[x][y].sprite.delete()
		self.field[x][y].sprite = None

	def _check(self, x, y):
		neighbors = list(self.field[x][y].neighbors.values())
		wall_count = len(list(filter(lambda x: x == None or x.wall == True, neighbors)))
		wall_count += 1 if self.field[x][y].wall else 0
		if self.field[x][y].wall:
			if wall_count < 5:
				self._remove_wall(x, y)
				return True
			else:
				return False
		else:
			if wall_count >= 5:
				self._make_wall(x, y)
				return True
			else:
				return False

	def _step(self):
		change = False
		for x in range(0, self.size_x):
			for y in range(0, self.size_y):
				if self._check(x, y):
					change = True
		return change

	def _whole(self):
		while self._step():
			pass


if __name__ == "__main__":
	size_x = 120
	size_y = 80
	scale = 0.5
	window = tkengine.TkWindow(int(32 * size_x * scale), int(32 * size_y * scale))
	world = tkengine.TkWorld(window)
	main = Main(world, size_x, size_y, scale)
	world.add_scenes({"main": main})
	world.run("main")


