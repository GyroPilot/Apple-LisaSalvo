"""bsh_probe.py -- play one whole FujiNet Battleship game between two scripted players on the server's
hidden 'test' table, through the same binary replies (bin=1&v=2) the Lisa client will read.
Proves the protocol before any Lisa code.  17-Oct-2026."""
import random, sys, time, urllib.request

BASE = "https://battleship.carr-designs.com"
TABLE = sys.argv[1] if len(sys.argv) > 1 else "test"
NAMES = ["lisaprobe1", "lisaprobe2"]
SIZES = [5, 4, 3, 3, 2]


def get(path, player, raw=True):
    sep = "&" if "?" in path else "?"
    url = "%s%s%stable=%s&player=%s%s" % (BASE, path, sep, TABLE, player, "&bin=1&v=2" if raw else "")
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read()


def cstr(b):
    return b.split(b"\0")[0].decode("latin-1")


def parse(b):
    """The v2 binary state (fujinet-game-system battleship util.go)."""
    s = {"n": b[0], "prompt": cstr(b[1:34]), "status": b[34], "pstatus": b[35],
         "active": b[36] if b[36] != 255 else -1, "movetime": b[37], "len": len(b)}
    if s["status"] == 0:
        s["server"] = cstr(b[38:59])
        off = 59
        withField = False
    else:
        s["last"] = b[38]
        s["ships"] = list(b[39:44])
        s["winner_ships"] = list(b[44:49])
        off = 49
        withField = True
    pl = []
    for i in range(s["n"]):
        p = {"name": cstr(b[off:off + 9]), "status": b[off + 9]}
        off += 10
        if withField and off + 105 <= len(b):
            p["field"] = list(b[off:off + 100])
            p["left"] = list(b[off + 100:off + 105])
            off += 105
        pl.append(p)
    s["players"] = pl
    return s


def placement():
    """Five ships, no overlap, in bounds: dir*100 + top-left."""
    while True:
        used, out = set(), []
        for size in SIZES:
            d = random.randint(0, 1)
            x = random.randint(0, 9 - (size - 1) * (1 - d))
            y = random.randint(0, 9 - (size - 1) * d)
            cells = {(y + k * d) * 10 + x + k * (1 - d) for k in range(size)}
            if cells & used:
                break
            used |= cells
            out.append(d * 100 + y * 10 + x)
        if len(out) == 5:
            return out


def main():
    global log
    log = []
    for nm in NAMES:
        s = parse(get("/state", nm))
        print(nm, "joined:", s["prompt"], "players", s["n"], "bytes", s["len"])
    for nm in NAMES:
        get("/ready/1", nm)
    t0 = time.time()
    placed = set()
    shots = {nm: [p for p in range(100)] for nm in NAMES}
    for nm in NAMES:
        random.shuffle(shots[nm])
    while time.time() - t0 < 900:
        for nm in NAMES:
            s = parse(get("/state", nm))
            if s["status"] == 1 and s["pstatus"] == 10 and nm not in placed:
                pl = placement()
                get("/place/" + ",".join(map(str, pl)), nm)
                placed.add(nm)
                print(nm, "placed", pl)
            elif s["status"] in (10, 11, 12, 13) and s["active"] == 0:
                pos = shots[nm].pop()
                get("/attack/%d" % pos, nm)
                s2 = parse(get("/state", nm))
                log.append((nm, pos, s2["status"], s2["len"]))
            elif s["status"] == 99:
                print("GAME OVER:", s["prompt"], "| bytes in a playing state:", max(l[3] for l in log) if log else "?")
                print("shots:", len(log), " hits:", sum(1 for l in log if l[2] in (12, 13)), " sinks:", sum(1 for l in log if l[2] == 13))
                print("example playing state:", parse(get("/state", nm))["players"][0].get("left"))
                for n2 in NAMES:
                    get("/leave", n2)
                sys.exit(0)
        time.sleep(0.5)
    print("timed out; last state", s)
    for n2 in NAMES:
        get("/leave", n2)


if __name__ == '__main__':
    main()
