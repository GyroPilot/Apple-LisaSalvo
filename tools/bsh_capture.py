"""bsh_capture.py -- save real binary replies from each phase of a game on the hidden 'test' table
(lobby, place ships, playing, game over) for the Pascal reader test.  18-Oct-2026."""
import random, time, urllib.request, sys
sys.path.insert(0, ".")
from bsh_probe import get, parse, placement, NAMES   # noqa  (runs nothing: bsh_probe guards below)

def save(name, b):
    open("cap_%s.bin" % name, "wb").write(b)
    s = parse(b)
    print("%-8s %4d bytes status %d pstat %d active %d players %d" % (name, len(b), s["status"], s["pstatus"], s["active"], s["n"]))

a, b = NAMES
save("lobby", get("/state", a))
get("/state", b)
get("/ready/1", a)
save("ready", get("/ready/1", b))
t0 = time.time()
placedA = placedB = False
shots = list(range(100)); random.shuffle(shots)
shots2 = list(range(100)); random.shuffle(shots2)
saved_play = saved_place = False
while time.time() - t0 < 900:
    ra = get("/state", a); sa = parse(ra)
    if sa["status"] == 1 and not saved_place:
        save("place", ra); saved_place = True
    if sa["status"] == 1 and sa["pstatus"] == 10 and not placedA:
        save("placed", get("/place/" + ",".join(map(str, placement())), a)); placedA = True
    rb = get("/state", b); sb = parse(rb)
    if sb["status"] == 1 and sb["pstatus"] == 10 and not placedB:
        get("/place/" + ",".join(map(str, placement())), b); placedB = True
    for nm, st, sh in ((a, sa, shots), (b, sb, shots2)):
        if st["status"] in (10, 11, 12, 13) and st["active"] == 0:
            r = get("/attack/%d" % sh.pop(), nm)
            if not saved_play and len(sh) < 80:
                save("play", r); saved_play = True
        if st["status"] == 99:
            save("over", get("/state", nm))
            for n2 in NAMES: get("/leave", n2)
            sys.exit(0)
    time.sleep(0.3)
