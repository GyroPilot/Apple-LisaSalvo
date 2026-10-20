# LisaSalvo

Sea battles on the Apple Lisa Office System against other FujiNet machines -- Ataris, Apple IIs, Commodores and the
rest -- or the server's own admirals, through an RS-232 FujiNet. The game is Eric Carr's public FujiNet Battleship
server (battleship.carr-designs.com); LisaSalvo is a Lisa client for it. (Named after "Salvo", the public-domain
ancestor of the pencil game, in David Ahl's BASIC games.)

Tool number **419322** in the GyroPilot series. Lisa Pascal, Workshop 3.0, Lisa Office System 3.1.

## Status

**0.3 (REV H) -- released 20 October 2026.**  Tested on a Lisa 2/10: whole games against the computer on the
public Battleship server, the final board kept until R, the flashing YOUR TURN line (F turns it off), Save & Put
Away.  Release floppy: `releases/LISASALVO_0_3.dc42`.

## Playing

Pick a table (the AI tables put you against the server's admirals); R when ready. Place five ships (5, 4, 3, 3, 2) on
your sea: click a square for each, SPACE turns them, A places all at random, RETURN sends them. Then take turns
firing at the target sea; one shot hits every other fleet at that square. A fleet with nothing afloat is out; the last
afloat wins. 45 seconds a turn.

The binary replies (bin=1, v=2) are about 280 bytes with two players: well under a second at 9600 baud.
`tools/` holds the protocol probe, the capture of real replies, and a scripted opponent.

## Credits

Tim O'Connor (bmwcyclist on LisaList2, GyroPilot on GitHub), with Claude (Anthropic). Lisa Pascal with the Lisa
Workshop 3.0 for Lisa Office System 3.1; built in LisaEm and proven on a Lisa 2/10 and a LisaFPGA with a FutureVision
Research FujiNet for RS-232.
