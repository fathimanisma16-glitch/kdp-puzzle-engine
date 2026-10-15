import streamlit as st
import random
from io import BytesIO
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# Page Configuration
st.set_page_config(
    page_title="KDP Activity & Puzzle Studio",
    page_icon="🧩",
    layout="wide"
)

# =========================================================
# HELPER: INSTANT PDF PREVIEW RASTERIZER
# =========================================================
def render_pdf_page_to_image(pdf_bytes, page_index=0, scale=1.3):
    try:
        import pypdfium2 as pdfium
        pdf = pdfium.PdfDocument(pdf_bytes)
        if 0 <= page_index < len(pdf):
            page = pdf[page_index]
            return page.render(scale=scale).to_pil()
    except Exception:
        return None
    return None

# =========================================================
# PROCEDURAL ANIMAL MASCOT & REWARD GRAPHICS (PIL ENGINE)
# =========================================================
def make_bunny(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([55, 15, 85, 100], fill="#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([63, 30, 77, 85], fill="#FBCFE8" if is_color else "#F1F5F9")
    d.ellipse([115, 15, 145, 100], fill="#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([123, 30, 137, 85], fill="#FBCFE8" if is_color else "#F1F5F9")
    d.ellipse([45, 65, 155, 175], fill="#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([70, 105, 82, 120], fill="#1E293B")
    d.ellipse([73, 107, 77, 112], fill="#FFFFFF")
    d.ellipse([118, 105, 130, 120], fill="#1E293B")
    d.ellipse([121, 107, 125, 112], fill="#FFFFFF")
    d.polygon([(94, 125), (106, 125), (100, 133)], fill="#F43F5E" if is_color else "#1E293B")
    d.arc([85, 128, 100, 145], start=0, end=180, fill="#1E293B", width=3)
    d.arc([100, 128, 115, 145], start=0, end=180, fill="#1E293B", width=3)
    if is_color:
        d.ellipse([52, 122, 68, 134], fill="#FDE2E4")
        d.ellipse([132, 122, 148, 134], fill="#FDE2E4")
    d.line([(38, 126), (65, 128)], fill="#94A3B8", width=3)
    d.line([(38, 138), (65, 134)], fill="#94A3B8", width=3)
    d.line([(135, 128), (162, 126)], fill="#94A3B8", width=3)
    d.line([(135, 134), (162, 138)], fill="#94A3B8", width=3)
    return img

def make_carrot(is_color=False):
    # Organic curved cartoon carrot with leafy fronds
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    leaf_col = "#22C55E" if is_color else "#FFFFFF"
    
    # Left, Center, Right leafy fronds
    d.polygon([(90, 80), (65, 30), (95, 75)], fill=leaf_col, outline="#1E293B")
    d.ellipse([56, 22, 85, 52], fill=leaf_col, outline="#1E293B", width=3)
    d.polygon([(105, 75), (135, 30), (110, 80)], fill=leaf_col, outline="#1E293B")
    d.ellipse([115, 22, 144, 52], fill=leaf_col, outline="#1E293B", width=3)
    d.polygon([(95, 80), (100, 18), (105, 80)], fill=leaf_col, outline="#1E293B")
    d.ellipse([91, 12, 109, 42], fill=leaf_col, outline="#1E293B", width=3)

    # Tapered carrot body with rounded crown
    c_fill = "#FB923C" if is_color else "#FFFFFF"
    body_pts = [
        (74, 82), (84, 73), (100, 70), (116, 73), (126, 82),
        (123, 105), (117, 130), (109, 155), (102, 180),
        (100, 184), (98, 180), (91, 155), (83, 130), (77, 105)
    ]
    d.polygon(body_pts, fill=c_fill, outline="#1E293B")
    for i in range(len(body_pts)):
        d.line([body_pts[i], body_pts[(i + 1) % len(body_pts)]], fill="#1E293B", width=4)

    # Horizontal ridges
    grv_col = "#EA580C" if is_color else "#1E293B"
    d.line([(83, 98), (108, 96)], fill=grv_col, width=3)
    d.line([(93, 120), (117, 118)], fill=grv_col, width=3)
    d.line([(87, 142), (107, 140)], fill=grv_col, width=3)
    d.line([(94, 162), (104, 161)], fill=grv_col, width=3)
    return img

def make_puppy(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([30, 60, 75, 130], fill="#FED7AA" if is_color else "#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([125, 60, 170, 130], fill="#FED7AA" if is_color else "#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([50, 50, 150, 150], fill="#FFFFFF", outline="#1E293B", width=4)
    if is_color:
        d.ellipse([55, 75, 95, 115], fill="#FEF08A")
    d.ellipse([70, 85, 84, 100], fill="#1E293B")
    d.ellipse([73, 87, 78, 93], fill="#FFFFFF")
    d.ellipse([116, 85, 130, 100], fill="#1E293B")
    d.ellipse([119, 87, 124, 93], fill="#FFFFFF")
    d.ellipse([80, 102, 120, 135], fill="#FFFFFF", outline="#1E293B", width=3)
    d.ellipse([92, 106, 108, 118], fill="#1E293B")
    d.line([(100, 118), (100, 127)], fill="#1E293B", width=3)
    d.arc([88, 120, 100, 132], start=0, end=180, fill="#1E293B", width=3)
    d.arc([100, 120, 112, 132], start=0, end=180, fill="#1E293B", width=3)
    d.arc([94, 127, 106, 142], start=0, end=180, fill="#F43F5E" if is_color else "#1E293B", width=3)
    return img

def make_bone(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    bone_fill = "#FEF3C7" if is_color else "#FFFFFF"
    d.ellipse([40, 75, 75, 105], fill=bone_fill, outline="#1E293B", width=4)
    d.ellipse([40, 95, 75, 125], fill=bone_fill, outline="#1E293B", width=4)
    d.ellipse([125, 75, 160, 105], fill=bone_fill, outline="#1E293B", width=4)
    d.ellipse([125, 95, 160, 125], fill=bone_fill, outline="#1E293B", width=4)
    d.rectangle([60, 88, 140, 112], fill=bone_fill)
    d.line([(60, 88), (140, 88)], fill="#1E293B", width=4)
    d.line([(60, 112), (140, 112)], fill="#1E293B", width=4)
    return img

def make_kitten(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(50, 40), (85, 75), (40, 85)], fill="#FFFFFF", outline="#1E293B")
    d.polygon([(150, 40), (115, 75), (160, 85)], fill="#FFFFFF", outline="#1E293B")
    d.line([(50, 40), (85, 75)], fill="#1E293B", width=4)
    d.line([(50, 40), (40, 85)], fill="#1E293B", width=4)
    d.line([(150, 40), (115, 75)], fill="#1E293B", width=4)
    d.line([(150, 40), (160, 85)], fill="#1E293B", width=4)
    if is_color:
        d.polygon([(54, 48), (78, 72), (46, 80)], fill="#FBCFE8")
        d.polygon([(146, 48), (122, 72), (154, 80)], fill="#FBCFE8")
    d.ellipse([45, 60, 155, 155], fill="#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([70, 95, 84, 112], fill="#1E293B")
    d.ellipse([73, 97, 78, 103], fill="#FFFFFF")
    d.ellipse([116, 95, 130, 112], fill="#1E293B")
    d.ellipse([119, 97, 124, 103], fill="#FFFFFF")
    d.polygon([(95, 116), (105, 116), (100, 122)], fill="#F43F5E" if is_color else "#1E293B")
    d.arc([88, 118, 100, 130], start=0, end=180, fill="#1E293B", width=3)
    d.arc([100, 118, 112, 130], start=0, end=180, fill="#1E293B", width=3)
    d.line([(38, 116), (68, 118)], fill="#94A3B8", width=3)
    d.line([(38, 128), (68, 124)], fill="#94A3B8", width=3)
    d.line([(132, 118), (162, 116)], fill="#94A3B8", width=3)
    d.line([(132, 124), (162, 128)], fill="#94A3B8", width=3)
    return img

def make_fish(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    fish_col = "#38BDF8" if is_color else "#FFFFFF"
    d.polygon([(140, 100), (175, 75), (175, 125)], fill=fish_col, outline="#1E293B")
    d.line([(140, 100), (175, 75)], fill="#1E293B", width=4)
    d.line([(175, 75), (175, 125)], fill="#1E293B", width=4)
    d.line([(175, 125), (140, 100)], fill="#1E293B", width=4)
    d.ellipse([45, 75, 145, 125], fill=fish_col, outline="#1E293B", width=4)
    d.ellipse([65, 90, 75, 100], fill="#1E293B")
    d.ellipse([67, 92, 70, 95], fill="#FFFFFF")
    d.arc([80, 80, 100, 120], start=270, end=90, fill="#1E293B", width=3)
    return img

def make_bear(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([45, 45, 80, 80], fill="#FED7AA" if is_color else "#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([120, 45, 155, 80], fill="#FED7AA" if is_color else "#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([40, 60, 160, 155], fill="#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([68, 90, 82, 105], fill="#1E293B")
    d.ellipse([70, 92, 75, 98], fill="#FFFFFF")
    d.ellipse([118, 90, 132, 105], fill="#1E293B")
    d.ellipse([120, 92, 125, 98], fill="#FFFFFF")
    d.ellipse([75, 105, 125, 138], fill="#FED7AA" if is_color else "#FFFFFF", outline="#1E293B", width=3)
    d.ellipse([90, 110, 110, 122], fill="#1E293B")
    d.line([(100, 122), (100, 130)], fill="#1E293B", width=3)
    d.arc([90, 122, 100, 133], start=0, end=180, fill="#1E293B", width=3)
    d.arc([100, 122, 110, 133], start=0, end=180, fill="#1E293B", width=3)
    return img

def make_honey(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    pot_fill = "#FDE047" if is_color else "#FFFFFF"
    d.rectangle([70, 50, 130, 70], fill=pot_fill, outline="#1E293B", width=4)
    d.ellipse([50, 65, 150, 155], fill=pot_fill, outline="#1E293B", width=4)
    d.rectangle([72, 95, 128, 122], fill="#FFFFFF", outline="#1E293B", width=2)
    return img

def make_mouse(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([30, 35, 80, 85], fill="#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([120, 35, 170, 85], fill="#FFFFFF", outline="#1E293B", width=4)
    if is_color:
        d.ellipse([42, 45, 68, 75], fill="#FBCFE8")
        d.ellipse([132, 45, 158, 75], fill="#FBCFE8")
    d.ellipse([55, 65, 145, 155], fill="#FFFFFF", outline="#1E293B", width=4)
    d.ellipse([75, 95, 87, 110], fill="#1E293B")
    d.ellipse([113, 95, 125, 110], fill="#1E293B")
    d.ellipse([94, 120, 106, 130], fill="#F43F5E" if is_color else "#1E293B")
    d.line([(42, 122), (72, 124)], fill="#94A3B8", width=3)
    d.line([(128, 124), (158, 122)], fill="#94A3B8", width=3)
    return img

def make_cheese(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    ch_fill = "#FEF08A" if is_color else "#FFFFFF"
    d.polygon([(45, 125), (155, 125), (155, 75), (45, 125)], fill=ch_fill, outline="#1E293B")
    d.line([(45, 125), (155, 125)], fill="#1E293B", width=4)
    d.line([(155, 125), (155, 75)], fill="#1E293B", width=4)
    d.line([(155, 75), (45, 125)], fill="#1E293B", width=4)
    d.ellipse([75, 105, 90, 118], fill="#FFFFFF", outline="#1E293B", width=2)
    d.ellipse([115, 90, 135, 110], fill="#FFFFFF", outline="#1E293B", width=2)
    d.ellipse([135, 112, 145, 122], fill="#FFFFFF", outline="#1E293B", width=2)
    return img

def make_monkey(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    m_fill = "#B45309" if is_color else "#FFFFFF"
    ear_inner = "#FDE68A" if is_color else "#F1F5F9"
    d.ellipse([25, 60, 65, 100], fill=m_fill, outline="#1E293B", width=4)
    d.ellipse([35, 70, 55, 90], fill=ear_inner)
    d.ellipse([135, 60, 175, 100], fill=m_fill, outline="#1E293B", width=4)
    d.ellipse([145, 70, 165, 90], fill=ear_inner)
    d.ellipse([45, 50, 155, 150], fill=m_fill, outline="#1E293B", width=4)
    d.ellipse([55, 75, 145, 145], fill=ear_inner, outline="#1E293B", width=3)
    d.ellipse([70, 90, 84, 104], fill="#1E293B")
    d.ellipse([73, 92, 77, 97], fill="#FFFFFF")
    d.ellipse([116, 90, 130, 104], fill="#1E293B")
    d.ellipse([119, 92, 123, 97], fill="#FFFFFF")
    d.ellipse([92, 114, 98, 120], fill="#1E293B")
    d.ellipse([102, 114, 108, 120], fill="#1E293B")
    d.arc([85, 115, 115, 138], start=0, end=180, fill="#1E293B", width=3)
    return img

def make_banana(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    b_fill = "#FACC15" if is_color else "#FFFFFF"
    pts = [
        (45, 60), (70, 95), (105, 125), (145, 140), (165, 135),
        (155, 148), (120, 150), (80, 132), (50, 100), (35, 65)
    ]
    d.polygon(pts, fill=b_fill, outline="#1E293B")
    for i in range(len(pts)):
        d.line([pts[i], pts[(i + 1) % len(pts)]], fill="#1E293B", width=4)
    stem_col = "#65A30D" if is_color else "#1E293B"
    d.polygon([(35, 65), (25, 52), (32, 48), (45, 60)], fill=stem_col, outline="#1E293B")
    d.polygon([(165, 135), (175, 132), (170, 140), (155, 148)], fill="#78350F" if is_color else "#1E293B")
    return img

def make_squirrel(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    sq_col = "#D97706" if is_color else "#FFFFFF"
    d.ellipse([110, 40, 175, 140], fill=sq_col, outline="#1E293B", width=4)
    d.ellipse([45, 65, 135, 155], fill=sq_col, outline="#1E293B", width=4)
    d.polygon([(65, 45), (85, 75), (55, 80)], fill=sq_col, outline="#1E293B")
    d.line([(65, 45), (85, 75)], fill="#1E293B", width=4)
    d.line([(65, 45), (55, 80)], fill="#1E293B", width=4)
    d.ellipse([70, 90, 86, 110], fill="#1E293B")
    d.ellipse([73, 92, 79, 100], fill="#FFFFFF")
    d.ellipse([50, 115, 60, 125], fill="#1E293B")
    return img

def make_acorn(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    cap_col = "#78350F" if is_color else "#FFFFFF"
    nut_col = "#D97706" if is_color else "#FFFFFF"
    d.polygon([(95, 30), (105, 30), (102, 60), (98, 60)], fill="#78350F" if is_color else "#1E293B", outline="#1E293B")
    d.ellipse([50, 50, 150, 95], fill=cap_col, outline="#1E293B", width=4)
    nut_pts = [(58, 80), (142, 80), (135, 130), (100, 175), (65, 130)]
    d.polygon(nut_pts, fill=nut_col, outline="#1E293B")
    for i in range(len(nut_pts)):
        d.line([nut_pts[i], nut_pts[(i + 1) % len(nut_pts)]], fill="#1E293B", width=4)
    return img

def make_frog(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    f_col = "#22C55E" if is_color else "#FFFFFF"
    d.ellipse([50, 45, 90, 85], fill=f_col, outline="#1E293B", width=4)
    d.ellipse([110, 45, 150, 85], fill=f_col, outline="#1E293B", width=4)
    d.ellipse([40, 60, 160, 145], fill=f_col, outline="#1E293B", width=4)
    d.ellipse([60, 52, 80, 78], fill="#FFFFFF", outline="#1E293B", width=2)
    d.ellipse([67, 58, 77, 72], fill="#1E293B")
    d.ellipse([120, 52, 140, 78], fill="#FFFFFF", outline="#1E293B", width=2)
    d.ellipse([123, 58, 133, 72], fill="#1E293B")
    d.arc([60, 85, 140, 125], start=0, end=180, fill="#1E293B", width=4)
    return img

def make_lilypad(is_color=False):
    img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    pad_col = "#16A34A" if is_color else "#FFFFFF"
    d.ellipse([40, 60, 160, 140], fill=pad_col, outline="#1E293B", width=4)
    d.polygon([(100, 100), (160, 80), (155, 120)], fill="#FFFFFF", outline="#1E293B")
    d.line([(100, 100), (160, 80)], fill="#1E293B", width=4)
    d.line([(100, 100), (155, 120)], fill="#1E293B", width=4)
    return img

ANIMAL_THEMES = [
    {"name": "Bunny & Carrot", "prompt": "Help Barnaby the Bunny find the Sweet Carrot!", "animal": make_bunny, "goal": make_carrot},
    {"name": "Puppy & Bone", "prompt": "Help Pip the Puppy find the Tasty Bone!", "animal": make_puppy, "goal": make_bone},
    {"name": "Kitten & Fish", "prompt": "Help Milo the Kitten catch the Little Fish!", "animal": make_kitten, "goal": make_fish},
    {"name": "Bear & Honey", "prompt": "Help Barnaby the Bear reach the Honey Pot!", "animal": make_bear, "goal": make_honey},
    {"name": "Mouse & Cheese", "prompt": "Help Squeaky the Mouse find the Swiss Cheese!", "animal": make_mouse, "goal": make_cheese},
    {"name": "Monkey & Banana", "prompt": "Help Koko the Monkey grab the Ripe Banana!", "animal": make_monkey, "goal": make_banana},
    {"name": "Squirrel & Acorn", "prompt": "Help Sammy the Squirrel collect the Golden Acorn!", "animal": make_squirrel, "goal": make_acorn},
    {"name": "Frog & Lily Pad", "prompt": "Help Hoppy the Frog leap to the Sunny Lily Pad!", "animal": make_frog, "goal": make_lilypad}
]

# =========================================================
# ENGINE: MAZE GENERATION & RECURSIVE BACKTRACKING
# =========================================================
PAGE_W = 8.5 * inch
PAGE_H = 11.0 * inch
OUTSIDE_MARGIN = 0.5 * inch
GUTTER = 0.625 * inch

def get_margins(page_num):
    is_odd = (page_num % 2 != 0)
    left_m = GUTTER if is_odd else OUTSIDE_MARGIN
    right_m = OUTSIDE_MARGIN if is_odd else GUTTER
    return left_m, right_m

class Maze:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.walls = [[[True, True, True, True] for _ in range(cols)] for _ in range(rows)]
        self.visited = [[False for _ in range(cols)] for _ in range(rows)]
        self.solution_path = []
        self._generate()
        self._solve()

    def _generate(self):
        stack = [(0, 0)]
        self.visited[0][0] = True
        directions = [(-1, 0, 0, 2), (0, 1, 1, 3), (1, 0, 2, 0), (0, -1, 3, 1)]

        while stack:
            r, c = stack[-1]
            neighbors = []
            for dr, dc, wall, opp_wall in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.visited[nr][nc]:
                    neighbors.append((nr, nc, wall, opp_wall))

            if neighbors:
                nr, nc, wall, opp_wall = random.choice(neighbors)
                self.walls[r][c][wall] = False
                self.walls[nr][nc][opp_wall] = False
                self.visited[nr][nc] = True
                stack.append((nr, nc))
            else:
                stack.pop()

    def _solve(self):
        queue = [[(0, 0)]]
        visited = {(0, 0)}
        target = (self.rows - 1, self.cols - 1)

        while queue:
            path = queue.pop(0)
            r, c = path[-1]
            if (r, c) == target:
                self.solution_path = path
                return

            directions = [(-1, 0, 0), (0, 1, 1), (1, 0, 2), (0, -1, 3)]
            for dr, dc, wall in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if not self.walls[r][c][wall] and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append(path + [(nr, nc)])

def draw_maze_grid(c, maze, x_offset, y_offset, total_size, line_width=2.8, draw_solution=False):
    cell_w = total_size / maze.cols
    cell_h = total_size / maze.rows
    
    c.setStrokeColor(colors.HexColor("#0F172A"))
    c.setLineWidth(line_width)
    c.setLineCap(1)

    for r in range(maze.rows):
        for col in range(maze.cols):
            x = x_offset + (col * cell_w)
            y = y_offset + ((maze.rows - 1 - r) * cell_h)

            is_start = (r == 0 and col == 0)
            is_end = (r == maze.rows - 1 and col == maze.cols - 1)

            if maze.walls[r][col][0] and not is_start:
                c.line(x, y + cell_h, x + cell_w, y + cell_h)
            if maze.walls[r][col][1] and not is_end:
                c.line(x + cell_w, y, x + cell_w, y + cell_h)
            if maze.walls[r][col][2]:
                c.line(x, y, x + cell_w, y)
            if maze.walls[r][col][3]:
                c.line(x, y, x, y + cell_h)

    if draw_solution and maze.solution_path:
        c.setStrokeColor(colors.HexColor("#EF4444"))
        c.setLineWidth(max(1.3, line_width * 0.5))
        c.setDash(3, 3)
        path_points = []
        for r, col in maze.solution_path:
            px = x_offset + (col * cell_w) + (cell_w / 2.0)
            py = y_offset + ((maze.rows - 1 - r) * cell_h) + (cell_h / 2.0)
            path_points.append((px, py))

        for i in range(len(path_points) - 1):
            c.line(path_points[i][0], path_points[i][1], path_points[i+1][0], path_points[i+1][1])
        c.setDash()

# =========================================================
# PDF BUILDER (SUPPORTS BUILT-IN & CUSTOM CLIPART)
# =========================================================
def generate_kids_maze_book(num_mazes=20, grid_size=12, mode="preset", theme_mode="Cycle All", is_color=False, custom_starts=None, custom_goals=None, custom_prompt="Find your way through the maze!"):
    buf = BytesIO()
    pdf = canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))
    
    mazes = [Maze(cols=grid_size, rows=grid_size) for _ in range(num_mazes)]
    page_counter = 1

    for idx, maze in enumerate(mazes):
        left_m, right_m = get_margins(page_counter)
        content_w = PAGE_W - left_m - right_m
        c_x = left_m + (content_w / 2.0)

        # Maze Grid placement
        maze_size = 5.7 * inch
        maze_x = left_m + (content_w - maze_size) / 2.0
        maze_y = 2.4 * inch
        icon_dim = 1.15 * inch

        pdf.setFont("Helvetica-Bold", 24)
        pdf.setFillColor(colors.HexColor("#0F172A"))
        pdf.drawCentredString(c_x, 10.05 * inch, f"MAZE #{idx + 1}")

        # Handling Custom Clipart vs Built-In Themes
        if mode == "custom" and custom_starts and custom_goals:
            # Custom Upload Mode
            prompt_text = custom_prompt
            start_file = custom_starts[idx % len(custom_starts)]
            goal_file = custom_goals[idx % len(custom_goals)]
            
            # Reset streams to beginning
            start_file.seek(0)
            goal_file.seek(0)
            
            pdf.drawImage(ImageReader(start_file), maze_x - 0.15 * inch, maze_y + maze_size + 0.05 * inch, width=icon_dim, height=icon_dim, mask='auto')
            pdf.drawImage(ImageReader(goal_file), maze_x + maze_size - icon_dim + 0.15 * inch, maze_y - icon_dim - 0.05 * inch, width=icon_dim, height=icon_dim, mask='auto')
        else:
            # Built-In Presets
            if theme_mode == "Cycle All":
                theme = ANIMAL_THEMES[idx % len(ANIMAL_THEMES)]
            else:
                theme = next(t for t in ANIMAL_THEMES if t["name"] == theme_mode)
            prompt_text = theme["prompt"]

            # Animal image
            animal_img = theme["animal"](is_color=is_color)
            a_io = BytesIO()
            animal_img.save(a_io, format="PNG")
            a_io.seek(0)
            pdf.drawImage(ImageReader(a_io), maze_x - 0.15 * inch, maze_y + maze_size + 0.05 * inch, width=icon_dim, height=icon_dim, mask='auto')

            # Goal image
            goal_img = theme["goal"](is_color=is_color)
            g_io = BytesIO()
            goal_img.save(g_io, format="PNG")
            g_io.seek(0)
            pdf.drawImage(ImageReader(g_io), maze_x + maze_size - icon_dim + 0.15 * inch, maze_y - icon_dim - 0.05 * inch, width=icon_dim, height=icon_dim, mask='auto')

        # Mission Prompt Header
        pdf.setFont("Helvetica-Bold", 11.5)
        pdf.setFillColor(colors.HexColor("#475569"))
        pdf.drawCentredString(c_x, 9.65 * inch, prompt_text)

        # Entrance & Exit Text Badges
        pdf.setFillColor(colors.HexColor("#16A34A"))
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(maze_x + icon_dim, maze_y + maze_size + 0.45 * inch, "START ➔")

        pdf.setFillColor(colors.HexColor("#DC2626"))
        pdf.drawRightString(maze_x + maze_size - icon_dim, maze_y - 0.55 * inch, "FINISH ➔")

        # Draw the Maze Grid
        draw_maze_grid(pdf, maze, maze_x, maze_y, maze_size, line_width=2.8, draw_solution=False)

        # Page Number Footer
        pdf.setFont("Helvetica", 9)
        pdf.setFillColor(colors.HexColor("#94A3B8"))
        pdf.drawCentredString(c_x, 0.8 * inch, f"- {page_counter} -")

        pdf.showPage()
        page_counter += 1

    # Solutions Section Divider Page
    left_m, right_m = get_margins(page_counter)
    c_x = left_m + (PAGE_W - left_m - right_m) / 2.0
    pdf.setFont("Helvetica-Bold", 32)
    pdf.setFillColor(colors.HexColor("#0F172A"))
    pdf.drawCentredString(c_x, 5.6 * inch, "SOLUTIONS")
    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(colors.HexColor("#64748B"))
    pdf.drawCentredString(c_x, 5.1 * inch, "Great job! Check your paths below:")
    pdf.showPage()
    page_counter += 1

    # 4-Up Solution Pages
    chunk_size = 4
    for chunk_start in range(0, len(mazes), chunk_size):
        chunk = mazes[chunk_start:chunk_start + chunk_size]
        left_m, right_m = get_margins(page_counter)
        content_w = PAGE_W - left_m - right_m
        c_x = left_m + (content_w / 2.0)

        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor(colors.HexColor("#0F172A"))
        pdf.drawCentredString(c_x, 10.1 * inch, "SOLUTIONS")

        mini_size = 2.8 * inch
        gap_x = 0.5 * inch
        col_coords = [
            left_m + (content_w - (2 * mini_size + gap_x)) / 2.0,
            left_m + (content_w - (2 * mini_size + gap_x)) / 2.0 + mini_size + gap_x
        ]
        row_coords = [6.2 * inch, 2.8 * inch]
        positions = [
            (col_coords[0], row_coords[0]),
            (col_coords[1], row_coords[0]),
            (col_coords[0], row_coords[1]),
            (col_coords[1], row_coords[1])
        ]

        for s_idx, mini_maze in enumerate(chunk):
            mx, my = positions[s_idx]
            maze_num = chunk_start + s_idx + 1

            pdf.setFont("Helvetica-Bold", 9)
            pdf.setFillColor(colors.HexColor("#334155"))
            pdf.drawString(mx, my + mini_size + 6, f"Maze #{maze_num}")

            draw_maze_grid(pdf, mini_maze, mx, my, mini_size, line_width=1.2, draw_solution=True)

        pdf.setFont("Helvetica", 9)
        pdf.setFillColor(colors.HexColor("#94A3B8"))
        pdf.drawCentredString(c_x, 0.8 * inch, f"- {page_counter} -")

        pdf.showPage()
        page_counter += 1

    pdf.save()
    return buf.getvalue(), page_counter - 1

# =========================================================
# APP CUSTOM CSS & HERO BANNER
# =========================================================
st.markdown("""
<style>
    .hero-banner {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #DB2777 100%);
        padding: 30px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.3);
    }
    .hero-banner h1 {
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        margin-bottom: 8px !important;
        color: white !important;
    }
    .hero-banner p {
        font-size: 1.05rem !important;
        opacity: 0.95;
        margin-bottom: 14px !important;
    }
    .badge-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 8px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero-banner">
    <h1>🧩 KDP Activity & Puzzle Studio</h1>
    <p>Generate print-ready, high-converting children's adventure maze books with integrated animal mascots and verified KDP gutters.</p>
    <div>
        <span class="badge-pill">🐾 8 Mascot Pairs</span>
        <span class="badge-pill">🚀 Custom Clipart Support</span>
        <span class="badge-pill">🖍️ Coloring-Book Friendly</span>
        <span class="badge-pill">📐 8.5" × 11" Auto Gutter</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.write("### 🐾 Built-in Mascot Roster")
    st.caption("Included character pairs:")
    st.markdown("""
    * 🐰 **Bunny** ➔ 🥕 Sweet Carrot
    * 🐶 **Puppy** ➔ 🦴 Tasty Bone
    * 🐱 **Kitten** ➔ 🐟 Little Fish
    * 🐻 **Bear** ➔ 🍯 Honey Pot
    * 🐭 **Mouse** ➔ 🧀 Swiss Cheese
    * 🐵 **Monkey** ➔ 🍌 Ripe Banana
    * 🐿️ **Squirrel** ➔ 🌰 Golden Acorn
    * 🐸 **Frog** ➔ 🪷 Sunny Lily Pad
    """)
    st.divider()
    st.write("### ☕ Support This Engine")
    st.caption("Keep this generator open and free for self-publishers:")
    st.link_button("☕ Support on Ko-fi", "https://ko-fi.com", type="secondary")

# =========================================================
# MAIN APP TABS
# =========================================================
tab_maze, tab_wordsearch, tab_sudoku, tab_coloring = st.tabs([
    "🌀 Kids Animal Mazes",
    "🔠 Themed Word Search (Next)",
    "🔢 Sudoku Ladder (Next)",
    "🎨 Line Art & Coloring (Next)"
])

with tab_maze:
    st.subheader("Configure Your Kids' Adventure Maze Book")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        st.markdown("**1. Difficulty & Age Tier**")
        difficulty = st.selectbox(
            "Grid Density",
            [
                "Ages 4–6: Easy Starter (8 × 8 Grid)",
                "Ages 6–8: Medium Explorer (12 × 12 Grid)",
                "Ages 8–12: Advanced Challenger (18 × 18 Grid)",
                "Custom Size"
            ],
            index=1
        )
        if "8 × 8" in difficulty:
            grid_dim = 8
        elif "12 × 12" in difficulty:
            grid_dim = 12
        elif "18 × 18" in difficulty:
            grid_dim = 18
        else:
            grid_dim = st.slider("Grid Dimension", min_value=6, max_value=25, value=14)
            
    with col_c2:
        st.markdown("**2. Clipart / Mascot Mode**")
        art_source = st.radio(
            "Artwork Source",
            ["🐾 Built-in Mascots (8 Varied Themes)", "🎨 Upload Custom Clipart (Dinos, Space, etc.)"],
            index=0
        )

    with col_c3:
        st.markdown("**3. Page Count & Print Style**")
        num_mazes = st.selectbox("Number of Puzzles", [10, 20, 30, 40, 50, 80], index=1)
        art_style = st.radio(
            "Interior Art Style",
            ["🖤 Black & White (Coloring Friendly / Low KDP Cost)", "🎨 Full Color (For Printables/Etsy)"],
            index=0
        )
        is_color = "Full Color" in art_style

    # Conditional Art Source Configuration
    custom_starts = None
    custom_goals = None
    custom_prompt = "Find your way through the maze!"
    theme_key = "Cycle All"

    if "Built-in" in art_source:
        theme_options = ["Cycle All (Every page is a new adventure)"] + [t["name"] for t in ANIMAL_THEMES]
        selected_theme = st.selectbox("Built-in Theme Selection", theme_options, index=0)
        theme_key = "Cycle All" if "Cycle All" in selected_theme else selected_theme
    else:
        st.markdown("##### 🎨 Custom Clipart Uploader")
        st.caption("Upload your own transparent PNGs to publish specialized themes (e.g., Space Astronauts, Dinosaurs, Fairies). If you upload multiple files, they cycle automatically!")
        
        up_col1, up_col2 = st.columns(2)
        with up_col1:
            custom_starts = st.file_uploader("Upload Start Mascot PNG(s)", type=["png"], accept_multiple_files=True, key="custom_starts")
        with up_col2:
            custom_goals = st.file_uploader("Upload Finish Goal PNG(s)", type=["png"], accept_multiple_files=True, key="custom_goals")
            
        custom_prompt = st.text_input("Custom Story Prompt", value="Help find the path from START to FINISH!")

    # Blueprint info
    sol_pages = (num_mazes + 3) // 4
    total_pages = num_mazes + 1 + sol_pages
    st.info(f"📐 **Book Blueprint:** **{num_mazes}** Mazes + **1** Solutions Divider + **{sol_pages}** Solution Pages = **{total_pages} Total Interior Pages** (Standard 8.5\" × 11\" KDP Paperback)")

    can_generate = True
    if "Upload Custom" in art_source and (not custom_starts or not custom_goals):
        can_generate = False
        st.warning("⚠️ Please upload at least one Start Mascot PNG and one Finish Goal PNG to generate your custom-themed book.")

    if st.button("🚀 Generate Kids Adventure Maze Book", type="primary", disabled=not can_generate):
        with st.spinner("Generating mazes and positioning story mascots..."):
            pdf_bytes, final_pages = generate_kids_maze_book(
                num_mazes=num_mazes,
                grid_size=grid_dim,
                mode="custom" if "Upload Custom" in art_source else "preset",
                theme_mode=theme_key,
                is_color=is_color,
                custom_starts=custom_starts,
                custom_goals=custom_goals,
                custom_prompt=custom_prompt
            )
            
        st.success(f"✅ Generated a print-ready {final_pages}-page Kids Maze Book!")
        
        # Previews
        st.write("#### 👁️ Live Preflight Verification")
        pv1, pv2 = st.columns(2)
        
        img_p1 = render_pdf_page_to_image(pdf_bytes, page_index=0, scale=1.3)
        img_p2 = render_pdf_page_to_image(pdf_bytes, page_index=1, scale=1.3) if num_mazes > 1 else None
        
        with pv1:
            st.markdown("**Page 1 Preview (Adventure #1)**")
            if img_p1:
                st.image(img_p1, use_container_width=True)
                
        with pv2:
            st.markdown("**Page 2 Preview (Next Adventure)**")
            if img_p2:
                st.image(img_p2, use_container_width=True)

        st.divider()
        st.download_button(
            label="📥 Download Print-Ready Kids Maze Book (PDF)",
            data=pdf_bytes,
            file_name=f"kdp_kids_maze_book_{grid_dim}x{grid_dim}_{num_mazes}mazes.pdf",
            mime="application/pdf",
            type="primary"
        )

with tab_wordsearch:
    st.subheader("🔠 Themed Word Search Engine")
    st.info("🚧 Engine under construction. Next update will feature custom wordlists, multi-directional search grids, and automated 4-up solution keys.")

with tab_sudoku:
    st.subheader("🔢 Sudoku Ladder Generator")
    st.info("🚧 Engine under construction. Next update will feature Easy-to-Expert difficulty ladders with single unique solutions.")

with tab_coloring:
    st.subheader("🎨 Line Art & Coloring Utility")
    st.info("🚧 Engine under construction. Next update will feature line art cleanup and automatic blank bleed-through back sheets.")
