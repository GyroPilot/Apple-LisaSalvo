# LisaSalvo changelog

## 1.0 REV I -- 21 Oct 2026 -- RELEASE
- Version 1.0 (About box 21 October 2026); the program is 0.3 REV H.  A whole game in LisaEm; opens from its
  floppy.  Known: the server returns a table to the lobby 10 s after a game ends, so if the other fleet's shot
  ends the game and the Lisa's next look is late, the final board is not kept (a safety net is planned for 1.1).
## 0.3 REV H -- 20 Oct 2026 -- RELEASE 0.3
- The YOUR TURN line flashes white-on-black on your turn (only that line is redrawn); F turns it off and on.
## 0.3 REV G -- 20 Oct 2026
- When a game ends, the final board and both fleets stay on the screen until you press R.
- Tested on a Lisa 2/10 (REV G and REV H): whole games, the flash, Save & Put Away.
## 0.3 REV F -- 20 Oct 2026
- No flashing while you wait: the idle look at the server repaints only what changed; the turn clock
  repaints its own line; the placing cursor is no longer sent back to A1 every 15 s.
  A whole game in LisaEm on the public Battleship server (91 shots).
- The release floppy opens on the Lisa (the previous one was made on the Reversi floppy).
## 0.3 REV E -- 19 Oct 2026
- A failed reply while sending your fleet no longer leaves it marked sent; the next look decides.
  Two whole games played in LisaEm on the public Battleship server (one won by each side).
## 0.3 REV D -- 18 Oct 2026
- Pictures of the ships instead of gray squares: carrier, battleship, cruiser, submarine, destroyer;
  a hit on a ship is a white hole with an X; the winner's fleet at game over drawn the same way.
## 0.2 REV C -- 18 Oct 2026
- Network reads of 128 bytes, not 256 (in LisaEm a 256-byte read took 9-12 s and could time out).
## 0.2 REV B -- 18 Oct 2026
- A turn clock that counts down between looks at the server; your ships afloat on the panel; 'watching'
  when you join a game under way; R for the next game.
## 0.1 REV A -- 18 Oct 2026 -- built, tested in LisaEm
- First build: tables, ready, placing (click, turn, random), firing, the last shot marked on the sea it hit.
