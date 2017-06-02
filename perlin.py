import pyglet, tkengine, random, math

class Noise(tkengine.TkScene):

	PERMUTATION = (151,160,137,91,90,15, 
		131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23, 
		190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33, 
		88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,134,139,48,27,166, 
		77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244, 
		102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,196, 
		135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,250,124,123, 
		5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42, 
		223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,172,9, 
		129,22,39,253,9,98,108,110,79,113,224,232,178,185,112,104,218,246,97,228, 
		251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107, 
		49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254, 
		138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180) * 2

	PERIOD = len(PERMUTATION) // 2

	GRAD = ((1,1,0),(-1,1,0),(1,-1,0),(-1,-1,0), 
			(1,0,1),(-1,0,1),(1,0,-1),(-1,0,-1), 
			(0,1,1),(0,-1,1),(0,1,-1),(0,-1,-1),
			(1,1,0),(0,-1,1),(-1,1,0),(0,-1,-1),)

	F = 0.5 * (math.sqrt(3.0) - 1.0)

	G = (3.0 - math.sqrt(3.0)) / 6.0

	def __init__(self, world, size_x, size_y, scale):
		super(Noise, self).__init__(world)
		self.size_x = size_x
		self.size_y = size_y
		self.scale = scale
		self.batch = pyglet.graphics.Batch()
		self.field = [[0.0 for y in range(self.size_y)] for x in range(self.size_x)]
		self.whole = []
		self.tile = pyglet.image.load("assets/tile.png")
		self._setup_field()
		self.key_handlers = {
			pyglet.window.key.RETURN	: lambda: self._step(),
			pyglet.window.key.ESCAPE	: pyglet.app.exit
		}
		pyglet.clock.schedule_interval(self._update, 1/60)


	def on_draw(self):
		self.world.window.clear()
		self.batch.draw()

	def _update(self, _):
		if self.keys[pyglet.window.key.SPACE]:
			self._step(1)
		if self.keys[pyglet.window.key.TAB]:
			self._step(10)

	def _step(self, count=-1):
		if not len(self.whole):
			return
		while len(self.whole) and count != 0:
			self._noise(*self.whole.pop())
			count -= 1

	def _setup_field(self):
		for x in range(self.size_x):
			for y in range(self.size_y):
				self.field[x][y] = pyglet.sprite.Sprite(self.tile, x=x*64*self.scale,
									y=y*64*self.scale, batch=self.batch)
				self.whole.append((x, y))

	def _noise(self, x, y):
		s = (x + y) * Noise.F
		i = math.floor(x + s)
		j = math.floor(y + s)
		t = (i + j) * Noise.G
		x0 = x - (i - t)
		y0 = y - (j - t)

		if x0 > y0:
			i1, j1 = 1, 0
		else:
			i1, j1 = 0, 1

		x1 = x0 - j1 + Noise.G
		y1 = y0 - j1 + Noise.G
		x2 = x0 + Noise.G * 2 - 1
		y2 = y0 + Noise.G * 2 - 1

		ii = int(i) % Noise.PERIOD
		jj = int(j) % Noise.PERIOD
		gi0 = Noise.PERMUTATION[ii + Noise.PERMUTATION[jj]] % 12
		gi1 = Noise.PERMUTATION[ii + i1 + Noise.PERMUTATION[jj + j1]] % 12
		gi2 = Noise.PERMUTATION[ii + 1 + Noise.PERMUTATION[jj + 1]] % 12
		
		tt = 0.5 - x0**2 - y0**2
		if tt > 0:
			g = Noise.GRAD[gi0]
			noise = tt**4 * (g[0] * x0 + g[1] * y0)
		else:
			noise = 0.0

		tt = 0.5 - x1**2 - y1**2
		if tt > 0:
			g = Noise.GRAD[gi1]
			noise += tt**4 * (g[0] * x1 + g[1] * y1)

		tt = 0.5 - x2**2 - y2**2
		if tt > 0:
			g = Noise.GRAD[gi2]
			noise += tt**4 * (g[0] * x2 + g[1] * y2)

		noise = int((70 * noise + 1) * 382)
		gradient = noise
		a = (255 if gradient > 255 else gradient)
		gradient = max	(0, gradient - 255)
		b = (255 if gradient > 255 else gradient)
		gradient = max	(0, gradient - 255)
		c = (255 if gradient > 255 else gradient)
		
		if noise % 3 == 0:
			hue = (a, b, c)
		if noise % 3 == 1:
			hue = (b, c, a)
		if noise % 3 == 2:
			hue = (c, b, a)
		
		self.field[x][y].color = hue

if __name__ == "__main__":
	size_x = 120
	size_y = 80
	scale = 0.25
	window = tkengine.TkWindow(int(64 * size_x * scale), int(64 * size_y * scale))
	world = tkengine.TkWorld(window)
	main = Noise(world, size_x, size_y, scale)
	world.add_scenes({"main": main})
	world.run("main")
