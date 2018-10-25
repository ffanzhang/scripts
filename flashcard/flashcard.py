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
         keys = list(d.keys())
         n = len(keys)
         while True:
             os.system('clear')
             print("Starting a new round")
             print("Press enter to proceed")
             input()
             for i in range(n):
                 target = random.randrange(i, n)
                 keys[i], keys[target] = keys[target], keys[i]
                 koi = keys[i]
                 os.system('clear')
                 print(koi)
                 input()
                 print(d[koi])
                 input()
                 
if __name__ == "__main__":
     main()
