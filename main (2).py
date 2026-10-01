import os
import sys
import pygame
import cv2

VIDEO_PATH = "background.mp4"    # <-- your video file, same folder as this script
WINDOW_SIZE = (1000, 650)        # window width, height
TEXT_VISIBLE_MS = 1500           # how long the text stays visible in each color (increase = longer)
COLOR_CHANGE_MS = 100            # quick flicker gap before switching to the next color (decrease = faster)
OVERLAY_ALPHA = 150              # 0 = video fully visible, 255 = video fully hidden
                                  # (try values between 100-180 for a good balance)

HEIGHT = 7
LETTER_WIDTH = 5

COLORS = [
    (255, 80, 80),    # red
    (80, 255, 120),   # green
    (255, 230, 80),   # yellow
    (100, 160, 255),  # blue
    (255, 100, 230),  # magenta
    (100, 230, 255),  # cyan
]

# ---------------------------------------------------------------------------
# Letter definitions: each letter has its own function that builds its
# HEIGHT x LETTER_WIDTH grid of '@'/' ' rows using nested for loops (over
# row r, then column c) and a boolean formula per pixel -- no letter-shaped
# text is written directly in the source.
# ---------------------------------------------------------------------------
def draw_A():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c in (0, 4) and r > 0) or (r == 0 and 0 < c < 4) or (r == 3)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_B():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c == 0) or (r in (0, 3, 6) and c < 4) or (c == 4 and r not in (0, 3, 6))
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_C():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c == 0) or (r in (0, 6))
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_D():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c == 0) or (r in (0, 6) and c < 4) or (c == 4 and 0 < r < 6)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_E():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c == 0) or (r in (0, 3, 6))
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_H():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c in (0, 4)) or (r == 3)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_I():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (r in (0, 6)) or (c == 2)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_J():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (r == 0) or (c == 3 and r < 5) or (r == 5 and c in (0, 3)) or (r == 6 and c in (1, 2))
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_K():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c == 0) or (r <= 3 and c == 4 - r) or (r >= 3 and c == r - 3)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_L():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c == 0) or (r == 6)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_M():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c in (0, 4)) or (r == c and c <= 2) or (r + c == 4 and c >= 2)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_N():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c in (0, 4)) or (r == c)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_O():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (r in (0, 6) and 0 < c < 4) or (c in (0, 4) and 0 < r < 6)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_P():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c == 0) or (r in (0, 3) and c < 4) or (c == 4 and 0 < r < 3)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_R():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (
                c == 0 or
                r == 0 or
                r == 3 or
                (c == LETTER_WIDTH - 1 and r < 3) or
                (r - 3 == c and r > 3)
            )
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_S():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (r in (0, 3, 6)) or (c == 0 and r < 3) or (c == 4 and r > 3)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_T():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (r == 0) or (c == 2)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_U():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = ((c in (0, 4)) and r < 6) or (r == 6 and 0 < c < 4)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_V():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = ((c == 0 and r < 5) or (c == 4 and r < 5)
                  or (r == 5 and c in (1, 3)) or (r == 6 and c == 2))
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_Y():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (r == c and r < 3) or (r + c == 4 and r < 3) or (c == 2 and r >= 3)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_0():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (r in (0, 6) and 0 < c < 4) or (c in (0, 4) and 0 < r < 6)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_1():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c == 2) or (r == 6) or (r == 1 and c == 1)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_2():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (r in (0, 3, 6)) or (c == 4 and r < 3) or (c == 0 and r > 3)
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_4():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (c == 4) or (c == 0 and r < 4) or (r == 3)
            row += "@" if on else " "
        rows.append(row)
    return rows
def draw_9():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (
                (r == 0 and 0 < c < 4) or      # Top
                (r == 3 and 0 < c < 4) or      # Middle
                (r == HEIGHT - 1 and 0 < c < 4) or  # Bottom
                (c == 0 and 0 < r < 3) or      # Left upper
                (c == 4 and r < HEIGHT - 1)    # Right side
            )
            row += "@" if on else " "
        rows.append(row)
    return rows
def draw_6():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (
                r in (0, 3, 6) or
                c == 0 or
                (c == 4 and r > 3)
            )
            row += "@" if on else " "
        rows.append(row)
    return rows
def draw_7():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            on = (
                r == 0 or
                c == LETTER_WIDTH - 1 - (r if r < LETTER_WIDTH else LETTER_WIDTH - 1)
            )
            row += "@" if on else " "
        rows.append(row)
    return rows


def draw_space():
    rows = []
    for r in range(HEIGHT):
        row = ""
        for c in range(LETTER_WIDTH):
            row += " "
        rows.append(row)
    return rows


LETTER_FUNCS = {
    'A': draw_A, 'B': draw_B, 'C': draw_C, 'D': draw_D, 'E': draw_E,
    'H': draw_H, 'I': draw_I, 'J': draw_J, 'K': draw_K, 'L': draw_L,
    'M': draw_M, 'N': draw_N, 'O': draw_O, 'P': draw_P, 'R': draw_R,
    'S': draw_S, 'T': draw_T, 'U': draw_U, 'V': draw_V, 'Y': draw_Y,
    '0': draw_0, '1': draw_1, '2': draw_2, '4': draw_4, '6': draw_6, '7': draw_7, '9': draw_9, ' ': draw_space,
}

# Build the LETTERS lookup by calling each letter's own function.
LETTERS = {}
for ch, func in LETTER_FUNCS.items():
    LETTERS[ch] = func()





def get_pattern(ch):
    """Return this character's grid pattern, falling back to blank if unknown."""
    return LETTERS.get(ch, LETTERS[' '])


details = [
    "Mahathi",
    "24B11DS084",
    "DATA SCIENCE",
    "ADITYA UNIVERSITY",
]

# ---------------------------------------------------------------------------
# Build plain ASCII art lines (rows of '@' and ' ') using nested for loops
# over the LETTERS grid data.
# ---------------------------------------------------------------------------
plain_output = []

for text_index, text in enumerate(details):
    if text_index > 0:
        plain_output.append("")

    for r in range(HEIGHT):
        line = ""
        for ch in text:
            pattern = get_pattern(ch)
            row = pattern[r]
            for c in range(LETTER_WIDTH):
                line += row[c]
            line += "  "
        plain_output.append(line.rstrip())

# ---------------------------------------------------------------------------
# Wrap the ASCII art in a rectangular border made of '*' characters, sized
# to fit the widest line.
# ---------------------------------------------------------------------------
BORDER_CHAR = "*"
BORDER_PADDING = 1   # spaces between the border and the art on each side

inner_width = max(len(line) for line in plain_output)
border_line = BORDER_CHAR * (inner_width + 2 * (BORDER_PADDING + 1))

bordered_output = [border_line]
for line in plain_output:
    padded = line.ljust(inner_width)
    pad = " " * BORDER_PADDING
    bordered_output.append(f"{BORDER_CHAR}{pad}{padded}{pad}{BORDER_CHAR}")
bordered_output.append(border_line)

plain_output = bordered_output

max_line_len = max(len(line) for line in plain_output)
total_lines = len(plain_output)

# ---------------------------------------------------------------------------
# Pygame setup
# ---------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Name Display")
clock = pygame.time.Clock()

# --- Open the video with OpenCV ---
cap = None
video_fps = 30
if os.path.exists(VIDEO_PATH):
    cap = cv2.VideoCapture(VIDEO_PATH)
    fps_read = cap.get(cv2.CAP_PROP_FPS)
    if fps_read and fps_read > 0:
        video_fps = fps_read
else:
    print(f"[warning] video file '{VIDEO_PATH}' not found. Showing plain background instead.")

frame_interval_ms = 1000 / video_fps
last_frame_time = pygame.time.get_ticks()
current_frame_surface = None


def get_next_video_frame():
    """Read the next frame from the video, looping back to the start when it ends."""
    ok, frame = cap.read()
    if not ok:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # rewind to the beginning
        ok, frame = cap.read()
        if not ok:
            return None
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, WINDOW_SIZE)
    # OpenCV frame is (height, width, 3); pygame surfarray wants (width, height, 3)
    frame = frame.swapaxes(0, 1)
    return pygame.surfarray.make_surface(frame)


# A semi-transparent dark layer drawn over the video so the text stands out
dark_overlay = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
dark_overlay.fill((0, 0, 0, OVERLAY_ALPHA))

# --- Auto-size the font so the whole ASCII block fits neatly inside the window ---
max_text_width = int(WINDOW_SIZE[0] * 0.9)
max_text_height = int(WINDOW_SIZE[1] * 0.75)

font_size = 40
font = pygame.font.SysFont("couriernew", font_size, bold=True)
while font_size > 4:
    font = pygame.font.SysFont("couriernew", font_size, bold=True)
    char_w, char_h = font.size("@")
    total_w = char_w * max_line_len
    total_h = char_h * total_lines
    if total_w <= max_text_width and total_h <= max_text_height:
        break
    font_size -= 1

char_w, char_h = font.size("@")
block_w = char_w * max_line_len
block_h = char_h * total_lines
offset_x = (WINDOW_SIZE[0] - block_w) // 2
offset_y = (WINDOW_SIZE[1] - block_h) // 2

running = True
show_text = True
last_toggle = pygame.time.get_ticks()
color_i = 0

while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    if show_text and (now - last_toggle >= TEXT_VISIBLE_MS):
        last_toggle = now
        show_text = False
    elif (not show_text) and (now - last_toggle >= COLOR_CHANGE_MS):
        last_toggle = now
        color_i = (color_i + 1) % len(COLORS)
        show_text = True

    # --- advance the video frame at its own natural speed ---
    if cap is not None and (now - last_frame_time) >= frame_interval_ms:
        last_frame_time = now
        new_surface = get_next_video_frame()
        if new_surface is not None:
            current_frame_surface = new_surface

    # --- draw background video frame, unchanged ---
    if current_frame_surface is not None:
        screen.blit(current_frame_surface, (0, 0))
    else:
        screen.fill((20, 20, 20))

    # --- dim the video so the text pops out clearly ---
    screen.blit(dark_overlay, (0, 0))

    # --- draw the blinking @ ASCII art text on top ---
    if show_text:
        color = COLORS[color_i]
        for row_idx, line in enumerate(plain_output):
            if not line.strip():
                continue
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (offset_x, offset_y + row_idx * char_h))

    pygame.display.flip()
    clock.tick(60)

if cap is not None:
    cap.release()
pygame.quit()
sys.exit()