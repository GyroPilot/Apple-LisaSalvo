"""ship_preview.py  18-Oct-2026: LisaSalvo REV D ship pictures, drawn by the same rules as ShipSeg in BSH-MAIN
(PaintRect / EraseRect boxes in 'along' and 'across' coordinates), on the 'Your fleet' grid (16 x 11 squares) and
the target sea (22 x 15).  Writes ship_preview.png (Lisa pixels, 1-bit, shown 3x)."""
from PIL import Image, ImageDraw

LEN = {1: 5, 2: 4, 3: 3, 4: 3, 5: 2}


def ship_seg(px, x, y, w, h, j, k, ln, d):
    if d == 0:
        A, C, x0, y0 = w - 1, h - 1, x + 1, y + 1
    else:
        A, C, x0, y0 = h - 1, h - 1, x + 1 + (w - h) // 2, y + 1

    def box(a0, c0, a1, c1, paint):
        for a in range(a0, a1):
            for c in range(c0, c1):
                X, Y = (x0 + a, y0 + c) if d == 0 else (x0 + c, y0 + a)
                px[X, Y] = 0 if paint else 1

    hT, hB = (C * 3) // 10, C - 1
    if j == 1:
        hT = (C * 2) // 10
    if j == 4:
        hT = (C * 5) // 10
    last = ln - 1
    a0 = -1 if k > 0 else 0                        # across the grid line to the square before
    a1 = A + 1 if k < last else A                  # ... and to the one after
    if k == last and j != 4:                       # the bow
        for i in range(hT, hB):
            dd = abs(2 * i - (hT + hB - 1))
            if A - dd > a0:
                box(a0, i, A - dd, i + 1, True)
    else:
        box(a0, hT, a1, hB, True)
    if k == 0:                                      # the stern, rounded
        box(0, hT, 1, hT + 1, False)
        box(0, hB - 1, 1, hB, False)
    if j == 4 and k == last:
        box(A - 1, hT, A, hT + 1, False)
        box(A - 1, hB - 1, A, hB, False)
    if j == 1:                                      # carrier: a dashed flight deck, the island
        box(2, hT + 2, A - 2, hT + 3, False)
        if k == 3:
            box(A // 2, 0, A - 2, hT, True)
    elif j == 2:                                    # battleship: turrets, a bridge tower
        if k == 2:
            box(A // 2 - 2, 0, A // 2 + 2, hT, True)
        elif k < last:
            box(A // 2 - 4, hT - 2, A // 2 + 4, hT, True)
        else:
            box(1, hT - 2, A // 2 - 1, hT, True)
    elif j == 3:                                    # cruiser
        if k == 1:
            box(A // 2 - 2, 0, A // 2 + 2, hT, True)
        elif k == 0:
            box(A // 2 - 4, hT - 2, A // 2 + 4, hT, True)
        else:
            box(1, hT - 2, A // 2 - 1, hT, True)
    elif j == 4:                                    # submarine: the conning tower
        if k == 1:
            box(A // 2 - 3, hT - 3, A // 2 + 3, hT, True)
    elif j == 5:                                    # destroyer: bridge and funnel
        if k == 0:
            box(A // 2 - 2, hT - 3, A // 2 + 4, hT, True)
        else:
            box(1, hT - 2, 4, hT, True)


def grid(dr, X, Y, w, h):
    for i in range(11):
        dr.line([(X + i * w, Y), (X + i * w, Y + 10 * h)], 0)
        dr.line([(X, Y + i * h), (X + 10 * w, Y + i * h)], 0)


def fleet(px, X, Y, w, h, ships, hits=()):
    for j, (pos, d) in ships.items():
        for k in range(LEN[j]):
            p = pos + k if d == 0 else pos + 10 * k
            ship_seg(px, X + (p % 10) * w, Y + (p // 10) * h, w, h, j, k, LEN[j], d)
    for p in hits:                                  # a hit on your ship: a white hole with an X
        x, y = X + (p % 10) * w, Y + (p // 10) * h
        for a in range(x + 3, x + w - 2):
            for b in range(y + 3, y + h - 2):
                px[a, b] = 1
        dr = ImageDraw.Draw(im)
        dr.line([(x + 3, y + 3), (x + w - 3, y + h - 3)], 0)
        dr.line([(x + w - 3, y + 3), (x + 3, y + h - 3)], 0)


im = Image.new("1", (440, 200), 1)
px = im.load()
dr = ImageDraw.Draw(im)
ships = {1: (11, 0), 2: (52, 0), 3: (7, 1), 4: (75, 0), 5: (93, 1)}
grid(dr, 20, 30, 16, 11)
fleet(px, 20, 30, 16, 11, ships, hits=(13, 54))
dr.text((20, 16), "Your fleet (16 x 11 squares)", fill=0)
grid(dr, 206, 30, 22, 15)
fleet(px, 206, 30, 22, 15, {1: (21, 0), 2: (60, 0), 3: (4, 1), 4: (84, 0), 5: (38, 1)})
dr.text((206, 16), "The winner's fleet on the target sea (22 x 15)", fill=0)
im.resize((im.width * 2, im.height * 3), Image.NEAREST).save("ship_preview.png")   # Lisa pixels are tall
print("ship_preview.png")
