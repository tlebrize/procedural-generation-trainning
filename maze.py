import pyglet, tkengine, random, math

class Main(tkengine.TkScene):

	"""
		? unexposed and undetermined
		, exposed but undetermined
		. empty space
		# wall
	"""

	def __init__(self, world, size):
		self.world = world
		self.size = size
		self.batch = pyglet.graphics.Batch()
		self.wall = pyglet.image.load('assets/wall.png')
		self.field = [['?' for _ in range(self.size)] for _ in range(self.size)]
		self.sprites = []
		self.frontier = []
		self._carve(random.randint(0, self.size-1), random.randint(0, self.size-1))
		self.branchrate = 5
		self.key_handlers = {
			pyglet.window.key.ESCAPE	: pyglet.app.exit,
			pyglet.window.key.SPACE		: self._step,
			pyglet.window.key.RETURN		: self._whole,
		}
		pyglet.gl.glClearColor(0.1, 0.1, 0.1, 0.0)

	def on_draw(self):
		self.world.window.clear()
		self.batch.draw()

	def _carve(self, y, x):
		extra = []
		self.field[y][x] = '.'
		if x > 0:
			if self.field[y][x-1] == '?':
				self.field[y][x-1] = ','
				extra.append((y,x-1))
		if x < self.size-1:
			if self.field[y][x+1] == '?':
				self.field[y][x+1] = ','
				extra.append((y,x+1))
		if y > 0:
			if self.field[y-1][x] == '?':
				self.field[y-1][x] = ','
				extra.append((y-1,x))
		if y < self.size-1:
			if self.field[y+1][x] == '?':
				self.field[y+1][x] = ','
				extra.append((y+1,x))
		random.shuffle(extra)
		self.frontier.extend(extra)

	def _make_wall(self, y, x):
		self.field[y][x] = '#'
		self.sprites.append(pyglet.sprite.Sprite(self.wall,
			y*32, x*32, batch=self.batch))

	def _check(self, y, x):
		edgestate = 0
		if x > 0:
			if self.field[y][x-1] == '.':
				edgestate += 1
		if x < self.size-1:
			if self.field[y][x+1] == '.':
				edgestate += 2
		if y > 0:
			if self.field[y-1][x] == '.':
				edgestate += 4
		if y < self.size-1:
			if self.field[y+1][x] == '.':
				edgestate += 8

		if edgestate == 1:
			if x < self.size-1:
				if y > 0:
					if self.field[y-1][x+1] == '.':
						return False
				if y < self.size-1:
					if self.field[y+1][x+1] == '.':
						return False
			return True
		elif edgestate == 2:
			if x > 0:
				if y > 0:
					if self.field[y-1][x-1] == '.':
						return False
				if y < self.size-1:
					if self.field[y+1][x-1] == '.':
						return False
			return True
		elif edgestate == 4:
			if y < self.size-1:
				if x > 0:
					if self.field[y+1][x-1] == '.':
						return False
				if x < self.size-1:
					if self.field[y+1][x+1] == '.':
						return False
			return True
		elif edgestate == 8:
			if x > 0:
				if x > 0:
					if self.field[y-1][x-1] == '.':
						return False
				if x < self.size-1:
					if self.field[y-1][x+1] == '.':
						return False
			return True
		return False

	def _step(self):
		if len(self.frontier):
			i = 20
			while len(self.frontier) and i:
				pos = random.random()
				pos = pos ** (math.e ** -self.branchrate)
				choice = self.frontier[int(pos*len(self.frontier))]
				if self._check(*choice):
					self._carve(*choice)
				else:
					self._make_wall(*choice)
				self.frontier.remove(choice)
				i -= 1
			return True
		else:
			for x in range(self.size):
				for y in range(self.size):
					if self.field[y][x] == '?':
						self._make_wall(y, x)
			return False

	def _whole(self):
		while self._step():
			pass


if __name__ == '__main__':
	size = 40
	window = tkengine.TkWindow(32 * size, 32 * size)
	world = tkengine.TkWorld(window)
	main = Main(world, size)
	world.add_scenes({'main': main})
	world.run('main')


