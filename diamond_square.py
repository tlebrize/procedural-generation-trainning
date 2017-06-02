import pyglet, tkengine, random

SIZE = 800

class Main(tkengine.TkScene):
	def __init__(self, world, size, roughness, scale):
		self.world = world
		self.key_handlers = {
			pyglet.window.key.ESCAPE	: pyglet.app.exit,
			pyglet.window.key.SPACE		: self._step
		}
		self.size = size
		self.roughness = roughness
		self.scale = scale
		self.max = self.size -1
		self.current = self.size -1
		self.array = [[0 for _ in range(self.size)] for _ in range(self.size)]
		self.array[0][0] = 1
		self.array[self.max][0] = 1
		self.array[0][self.max] = 1
		self.array[self.max][self.max] = 1

	def on_draw(self):
		self.world.window.clear()
		s = self.scale
		a = self.array
		for x in range(self.size):
			for y in range(self.size):
				origin = self._translate(x*s, y*s, a[x][y]*s)
				if x > 0:
					pyglet.graphics.draw(2, pyglet.gl.GL_LINES, 
						("v2i", (*origin, *self._translate((x-1)*s, y*s, a[x-1][y]*s))))
				if y > 0:
					pyglet.graphics.draw(2, pyglet.gl.GL_LINES, 
						("v2i", (*origin, *self._translate(x*s, (y-1)*s, a[x][y-1]*s))))

	def _translate(self, x, y, z):
		xt = x - self.size
		yt = y - self.size
		x = 0.4 * (xt - yt)
		y = 0.2 * (xt + yt)
		y -= 0.1 * z
		return (int(x) + SIZE//2, int(y) + SIZE//3)

	def _step(self):
		size = self.current
		x = size // 2
		y = size // 2
		half = size // 2
		scale = self.roughness * size
		if (half < 1):
			return
		for y in range(half, self.max, size):
			for x in range(half, self.max, size):
				s_scale = random.uniform(0, 1) * scale * 2 - scale
				self._square(x, y, half, s_scale)
		for y in range(0, self.max + 1, half):
			for x in range((y + half) % size, self.max + 1, size):
				d_scale = random.uniform(0, 1) * scale * 2 - scale
				self._diamond(x, y, half, d_scale)
		self.current = self.current // 2


	def _square(self, x, y, size, scale):
		top_left = self.array[x-size][y-size]
		top_right = self.array[x+size][y-size]
		bottom_left = self.array[x+size][y+size]
		bottom_right = self.array[x-size][y+size]
		average = ((top_left + top_right + bottom_right + bottom_left) // 4)
		self.array[x][y] = average + scale

	def _diamond(self, x, y, size, scale):
		def get(x, y):
			if (x < 0 or x > self.max or y < 0 or y > self.max):
				return 0
			return self.array[x][y]
		top = get(x-size, y-size)
		right = get(x+size, y-size)
		bottom = get(x+size, y+size)
		left = get(x-size, y+size)
		average = ((top + right + bottom + left) // 4)
		self.array[x][y] = average + scale


if __name__ == "__main__":
	window = tkengine.TkWindow(SIZE, SIZE)
	world = tkengine.TkWorld(window)
	main = Main(world, 17, 0.5, 50)
	world.add_scenes({"main": main})
	world.run("main")


