import cv2
import numpy as np
import sys

# -------------------------------------------------------------
# 1. Block Letter Generator Matrix
# -------------------------------------------------------------
def get_char_matrix(ch):
    star_map = {
        'A': [(1,0),(2,0),(3,0),(4,0), (0,1),(0,2),(0,3), (1,4),(2,4),(3,4),(4,4), (2,1),(2,2),(2,3)],
        'B': [(0,0),(1,0),(2,0),(3,0),(4,0), (0,1),(0,2),(0,3), (2,1),(2,2),(2,3), (4,1),(4,2),(4,3), (1,4),(3,4)],
        'C': [(0,1),(0,2),(0,3),(0,4), (1,0),(2,0),(3,0), (4,1),(4,2),(4,3),(4,4)],
        'D': [(0,0),(1,0),(2,0),(3,0),(4,0), (0,1),(0,2),(0,3), (4,1),(4,2),(4,3), (1,4),(2,4),(3,4)],
        'E': [(0,0),(1,0),(2,0),(3,0),(4,0), (0,1),(0,2),(0,3),(0,4), (2,1),(2,2),(2,3), (4,1),(4,2),(4,3),(4,4)],
        'H': [(0,0),(1,0),(2,0),(3,0),(4,0), (0,4),(1,4),(2,4),(3,4),(4,4), (2,1),(2,2),(2,3)],
        'I': [(0,0),(0,1),(0,2),(0,3),(0,4), (4,0),(4,1),(4,2),(4,3),(4,4), (1,2),(2,2),(3,2)],
        'M': [(0,0),(1,0),(2,0),(3,0),(4,0), (0,4),(1,4),(2,4),(3,4),(4,4), (1,1),(2,2),(1,3)],
        'N': [(0,0),(1,0),(2,0),(3,0),(4,0), (0,4),(1,4),(2,4),(3,4),(4,4), (1,1),(2,2),(3,3)],
        'O': [(0,1),(0,2),(0,3), (4,1),(4,2),(4,3), (1,0),(2,0),(3,0), (1,4),(2,4),(3,4)],
        'R': [(0,0),(1,0),(2,0),(3,0),(4,0), (0,1),(0,2),(0,3), (2,1),(2,2),(2,3), (1,4), (3,2),(4,4)],
        'S': [(0,1),(0,2),(0,3),(0,4), (1,0),(2,0),(2,1),(2,2),(2,3),(2,4), (3,4),(4,0),(4,1),(4,2),(4,3)],
        'T': [(0,0),(0,1),(0,2),(0,3),(0,4), (1,2),(2,2),(3,2),(4,2)],
        'U': [(0,0),(1,0),(2,0),(3,0), (0,4),(1,4),(2,4),(3,4), (4,1),(4,2),(4,3)],
        'V': [(0,0),(1,0),(2,0),(3,0), (0,4),(1,4),(2,4),(3,4), (4,2)],
        'Y': [(0,0),(1,0), (0,4),(1,4), (2,2),(3,2),(4,2), (2,1),(2,3)],
        '1': [(0,2),(1,2),(2,2),(3,2),(4,2), (1,1), (4,0),(4,1),(4,3),(4,4)],
        '2': [(0,0),(0,1),(0,2),(0,3),(0,4), (1,4), (2,0),(2,1),(2,2),(2,3),(2,4), (3,0), (4,0),(4,1),(4,2),(4,3),(4,4)],
        '4': [(0,0),(1,0),(2,0), (2,1),(2,2),(2,3),(2,4), (0,4),(1,4),(3,4),(4,4)],
        '8': [(0,1),(0,2),(0,3), (4,1),(4,2),(4,3), (2,1),(2,2),(2,3), (1,0),(3,0), (1,4),(3,4)],
        '9': [(0,0),(0,1),(0,2),(0,3),(0,4), (1,0),(2,0), (1,4),(2,4),(3,4),(4,4), (2,1),(2,2),(2,3), (4,0),(4,1),(4,2),(4,3)],
        '0': [(0,1),(0,2),(0,3), (4,1),(4,2),(4,3), (1,0),(2,0),(3,0), (1,4),(2,4),(3,4)],
        ' ': []
    }
    return star_map.get(ch, [])

def draw_block_word(img, text, start_x, start_y, font_scale=0.6, color=(0, 255, 255), spacing=9, thickness=2):
    for char_idx, ch in enumerate(text):
        coords = get_char_matrix(ch)
        char_x = start_x + char_idx * (5 * spacing + 10)
        for r in range(5):
            for c in range(5):
                if (r, c) in coords:
                    px = char_x + c * spacing
                    py = start_y + r * spacing
                    cv2.putText(img, "*", (px, py), cv2.FONT_HERSHEY_PLAIN, font_scale, color, thickness, cv2.LINE_AA)

def prepare_text_side(height, width):
    left_panel = np.zeros((height, width, 3), dtype=np.uint8)
    
    cv2.putText(left_panel, "NAME :", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    draw_block_word(left_panel, "MAHATHI", 25, 70, color=(0, 255, 0), spacing=9, font_scale=0.6, thickness=2)
    
    cv2.putText(left_panel, "ROLL NO :", (25, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    draw_block_word(left_panel, "24B11DS084", 25, 190, color=(0, 215, 255), spacing=8, font_scale=0.55, thickness=2)
    
    cv2.putText(left_panel, "BRANCH :", (25, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    draw_block_word(left_panel, "DATA", 25, 310, color=(255, 100, 255), spacing=9, font_scale=0.6, thickness=2)
    draw_block_word(left_panel, "SCIENCE", 25, 380, color=(255, 100, 255), spacing=8, font_scale=0.55, thickness=2)
    
    cv2.putText(left_panel, "COLLEGE :", (25, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    draw_block_word(left_panel, "ADITYA", 25, 500, color=(0, 165, 255), spacing=9, font_scale=0.6, thickness=2)
    draw_block_word(left_panel, "UNIVERSITY", 25, 570, color=(0, 165, 255), spacing=7, font_scale=0.5, thickness=2)
    
    return left_panel

# -------------------------------------------------------------
# 2. Main Execution Loop
# -------------------------------------------------------------
video_path = "background.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"\n[Error] '{video_path}' file missing in folder!")
    sys.exit()

fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps) if fps > 0 else 30

# Window layout sizing: slightly expanded right logo panel
window_h = 650
left_w = 600         # Large area for text
right_panel_w = 450  # Increased slightly for better logo visibility

left_side = prepare_text_side(window_h, left_w)

window_name = "Mahathi Details & Aditya Logo Animation"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Resize video into the right panel space
    video_resized = cv2.resize(frame, (right_panel_w, window_h))

    # Combine Left Text + Right Video
    combined_window = np.hstack((left_side, video_resized))

    cv2.imshow(window_name, combined_window)

    key = cv2.waitKey(delay) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()