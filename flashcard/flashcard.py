import os
import sys
import json
import random
import signal
import time

# interrupt handler for Ctrl + C, for exiting
def exit(signum, frame):
	print("\nExiting")
	sys.exit(0)


def main():
	signal.siginterrupt(signal.SIGINT, True)
	signal.signal(signal.SIGINT, exit)
	args = sys.argv
	if len(args) != 2 or args[1][-4:] == 'help':
		print("usage: python flashcard.py filename.json")
		sys.exit(0)

	with open(args[1], 'r') as f:
		text = f.read()
		d = json.loads(text)
		while True:
			os.system('clear')
			print("Starting a new round")
			print("Press enter to proceed")
			input()
			keys = list(d.keys())
			random.shuffle(keys)
			for key in keys:
				os.system('clear')
				print(key)
				input()
				print(d[key])
				input()
if __name__ == "__main__":
	main()
