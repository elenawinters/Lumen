# Python build script

import subprocess
import threading


class ThreadedSassMessenger(object):
	def __init__(self, daemon=True, timeout=None):
		self.timeout = timeout
		self.daemon = daemon
		self.pool = []

	def percentage_alive(self):
		return str((len([x.is_alive() for x in self.pool]) / len(self.pool)) * 100) + "%"

	def append(self, target, *args, **kwargs):
		self.pool.append(threading.Thread(target=target, daemon=self.daemon, args=args, kwargs=kwargs))

	def start(self):
		for x in self.pool:
			x.start()

	def join(self):
		for x in self.pool:
			x.join(timeout=self.timeout)

def log_child(p):
	for line in p.stdout:
		if line == b'Sass is watching for changes. Press Ctrl-C to stop.\n': continue
		if line == b'\n': continue
		print(line.decode("utf-8"), end='')

sass_files = [

]

if __name__ == '__main__':
	print('Compiling TypeScript project')
	subprocess.run(['tsc', '-p', 'tsconfig.json'], shell=True)

	print('Building Sass files')
	children = []
	for f in sass_files:
		if f[1] != None:
			children.append(subprocess.Popen(['sass', '--watch', f[0], f[1]], shell=True, stdout=subprocess.PIPE))
		else:
			children.append(subprocess.Popen(['sass', '--watch', f[0]], shell=True, stdout=subprocess.PIPE))

	sass_manager = ThreadedSassMessenger(timeout=4)
	for child in children:
		sass_manager.append(log_child, child)
	sass_manager.start()
	print('Starting project')
	subprocess.run(['node', 'server.js'], shell=True)
	sass_manager.join()

