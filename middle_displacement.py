import pyglet, tkengine, random

class Main(tkengine.TkScene):
	def __init__(self, world):
		self.world = world
		self.key_handlers = {
			pyglet.window.key.ESCAPE	: pyglet.app.exit,
			pyglet.window.key.SPACE		: self._step
		}
		self.range = 50
		self.lines = [[0, 200, 400, 200]]

	def on_draw(self):
		self.world.window.clear()
		for line in self.lines:
			pyglet.graphics.draw(2, pyglet.gl.GL_LINES, 
				("v2i", line))

	def _step(self):
		new_lines = []
		for line in self.lines:
			print(line)
			start = line[0:2]
			end = line[2:4]
			middle = [(start[0] + end[0]) // 2, 200 + random.randint(-self.range, self.range)]
			new_lines.append([*start, *middle])
			new_lines.append([*middle, *end])
			print([*start, *middle])
			print([*middle, *end])
			print("")
		self.lines = new_lines
		self.range = int(0.7*self.range)

if __name__ == "__main__":
	window = tkengine.TkWindow(400, 400)
	world = tkengine.TkWorld(window)
	main = Main(world)
	world.add_scenes({"main": main})
	world.run("main")
