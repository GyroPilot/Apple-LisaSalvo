"""bsh_opponent.py -- a patient scripted admiral for testing LisaSalvo: sits at a table (default the hidden
'test' table) as 'banana', readies, places at random, fires at random squares on its turn, and plays games until
told to stop (Ctrl-C) or MAX_GAMES are over.  Prints what happens.  18-Oct-2026.
   python bsh_opponent.py [table] [name] [games]"""
import random, sys, time
from bsh_probe import parse, placement
import urllib.request

BASE = "https://battleship.carr-designs.com"
TABLE = sys.argv[1] if len(sys.argv) > 1 else "test"
NAME = sys.argv[2] if len(sys.argv) > 2 else "banana"
GAMES = int(sys.argv[3]) if len(sys.argv) > 3 else 1


def get(path):
    sep = "&" if "?" in path else "?"
    with urllib.request.urlopen("%s%s%stable=%s&player=%s&bin=1&v=2" % (BASE, path, sep, TABLE, NAME), timeout=20) as r:
        return r.read()


def say(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


games, placed, last, shots = 0, False, None, []
try:
    while games < GAMES:
        s = parse(get("/state"))
        key = (s["status"], s["pstatus"], s["active"], s["n"], s["prompt"])
        if key != last:
            say("status", s["status"], "me", s["pstatus"], "turn", s["active"], "players",
                [p["name"] + ":" + str(p["status"]) for p in s["players"]], "|", s["prompt"])
            last = key
        if s["status"] == 0:
            placed = False
            if s["pstatus"] != 3 and s["n"] > 1:
                get("/ready/1")
        elif s["status"] == 1 and s["pstatus"] == 10 and not placed:
            get("/place/" + ",".join(map(str, placement())))
            placed = True
            shots = list(range(100))
            random.shuffle(shots)
        elif s["status"] in (10, 11, 12, 13) and s["active"] == 0 and shots:
            pos = shots.pop()
            r = parse(get("/attack/%d" % pos))
            say("fired at", chr(65 + pos % 10) + str(pos // 10 + 1), "->", {11: "miss", 12: "HIT", 13: "SUNK"}.get(r["status"], r["status"]))
        elif s["status"] == 99:
            say("GAME OVER:", s["prompt"])
            games += 1
            time.sleep(12)
        time.sleep(1.5)
finally:
    get("/leave")
    say("left the table")
