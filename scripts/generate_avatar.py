from svg import BLUE, WHITE, reveal, save

GRID = [
    '     BB           BB     ',
    '    BBBB         BBBB    ',
    '    BBWBB       BBWBB    ',
    '   BBBWBBB     BBBWBBB   ',
    '   BBBBBBBBBBBBBBBBBBB   ',
    '  BBBBBBBBBBBBBBBBBBBBB  ',
    '  BBBBBBBBBWWWBBBBBBBBB  ',
    ' BBBBBBBBBWWWWWBBBBBBBBB ',
    ' BBBBBBBBWWWWWWWBBBBBBBB ',
    ' WWWWWWWWWWWWWWWWWWWWWWW ',
    ' WWWWWWWWWWWWWWWWWWWWWWW ',
    ' WWWWWWDDWWWWWWWDDWWWWWW ',
    ' WWWWWWDDWWWWWWWDDWWWWWW ',
    ' WWWWWWWWWWWWWWWWWWWWWWW ',
    '  WWWWWWWWWWDWWWWWWWWWW  ',
    '  WWWWWWWWWDWDWWWWWWWWW  ',
    '   WWWWWWWDWWWDWWWWWWW   ',
    '    WWWWWWWWWWWWWWWWW    ',
    '      WWWWWWWWWWWWW      ',
]
COLORS = {"B": BLUE, "W": WHITE, "D": "#263241"}
parts = ""
for y, row in enumerate(GRID):
    pixels = "".join(f'<rect x="{43+x*9}" y="{65+y*9}" width="8" height="8" fill="{COLORS[c]}"/>' for x,c in enumerate(row) if c != " ")
    parts += reveal(pixels, round(y * .045, 3))
save("avatar.svg", 330, 310, "Original blue and white pixel cat, with a quiet, slightly blank expression", parts)
save("avatar-mobile.svg", 440, 310, "Original blue and white pixel cat", '<g transform="translate(55 0)">' + parts + '</g>')
