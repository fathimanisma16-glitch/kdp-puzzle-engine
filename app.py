import streamlit as st
import random
from io import BytesIO
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors

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
# ENGINE: MAZE GENERATION & RECURSIVE BACKTRACKING
# =========================================================
PAGE_W = 8.5 * inch
PAGE_H = 11.0 * inch
OUTSIDE_MARGIN = 0.5 * inch
GUTTER = 0.625 * inch  # Standard Amazon KDP gutter for 8.5" x 11"

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
        directions = [
            (-1, 0, 0, 2),  # Up
            (0, 1, 1, 3),   # Right
            (1, 0, 2, 0),   # Down
            (0, -1, 3, 1)   # Left
        ]

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

def draw_maze_grid(c, maze, x_offset, y_offset, total_size, line_width=2.5, draw_solution=False):
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
        c.setLineWidth(max(1.2, line_width * 0.5))
        c.setDash(3, 3)
        path_points = []
        for r, col in maze.solution_path:
            px = x_offset + (col * cell_w) + (cell_w / 2.0)
            py = y_offset + ((maze.rows - 1 - r) * cell_h) + (cell_h / 2.0)
            path_points.append((px, py))

        for i in range(len(path_points) - 1):
            c.line(path_points[i][0], path_points[i][1], path_points[i+1][0], path_points[i+1][1])
        c.setDash()

def generate_maze_book_pdf(num_mazes=20, grid_size=12, book_title="MY MAZE ADVENTURE"):
    buf = BytesIO()
    pdf = canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))
    
    mazes = [Maze(cols=grid_size, rows=grid_size) for _ in range(num_mazes)]
    page_counter = 1

    # 1. Individual Puzzle Pages
    for idx, maze in enumerate(mazes):
        left_m, right_m = get_margins(page_counter)
        content_w = PAGE_W - left_m - right_m
        c_x = left_m + (content_w / 2.0)

        pdf.setFont("Helvetica-Bold", 22)
        pdf.setFillColor(colors.HexColor("#0F172A"))
        pdf.drawCentredString(c_x, 10.0 * inch, f"MAZE #{idx + 1}")

        pdf.setFont("Helvetica", 10)
        pdf.setFillColor(colors.HexColor("#64748B"))
        pdf.drawCentredString(c_x, 9.65 * inch, "Find the path from START to FINISH!")

        maze_size = 6.2 * inch
        maze_x = left_m + (content_w - maze_size) / 2.0
        maze_y = 2.4 * inch

        # Start / Finish labels
        pdf.setFillColor(colors.HexColor("#16A34A"))
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(maze_x, maze_y + maze_size + 8, "➔ START")

        pdf.setFillColor(colors.HexColor("#DC2626"))
        pdf.drawRightString(maze_x + maze_size, maze_y - 18, "FINISH ➔")

        draw_maze_grid(pdf, maze, maze_x, maze_y, maze_size, line_width=2.8, draw_solution=False)

        pdf.setFont("Helvetica", 9)
        pdf.setFillColor(colors.HexColor("#94A3B8"))
        pdf.drawCentredString(c_x, 0.8 * inch, f"- {page_counter} -")

        pdf.showPage()
        page_counter += 1

    # 2. Solutions Divider Page
    left_m, right_m = get_margins(page_counter)
    c_x = left_m + (PAGE_W - left_m - right_m) / 2.0
    pdf.setFont("Helvetica-Bold", 32)
    pdf.setFillColor(colors.HexColor("#0F172A"))
    pdf.drawCentredString(c_x, 5.5 * inch, "SOLUTIONS")
    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(colors.HexColor("#64748B"))
    pdf.drawCentredString(c_x, 5.0 * inch, "Check your paths and see how you did!")
    pdf.showPage()
    page_counter += 1

    # 3. 4-Up Compact Solution Pages
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
# SIDEBAR
# =========================================================
with st.sidebar:
    st.write("### 🧩 Activity Engine Hub")
    st.caption("Generate print-ready, formatted activity books for Amazon KDP with zero manual layout work.")
    
    st.divider()
    
    st.write("### ☕ Support This Free Tool")
    st.caption("If this engine saves you subscription fees, consider buying a coffee to keep it online!")
    st.link_button("☕ Support on Ko-fi", "https://ko-fi.com", help="Keep the engine free & ad-free")
    
    st.divider()
    
    st.write("### 📐 KDP Print Standards")
    st.markdown("""
    * **Trim:** 8.5" × 11.0" Standard
    * **Gutters:** 0.625" Spine Safe
    * **Solutions:** 4-Up Auto Layout
    * **Bleed:** None (Vector Math)
    """)

# =========================================================
# MAIN APP INTERFACE
# =========================================================
st.title("🧩 KDP Activity & Puzzle Studio")
st.caption("Generate print-on-demand activity book interiors for Amazon KDP.")

tab_maze, tab_wordsearch, tab_sudoku, tab_coloring = st.tabs([
    "🌀 Kids Maze Generator",
    "🔠 Word Search (Upcoming)",
    "🔢 Sudoku Ladder (Upcoming)",
    "🎨 Line Art & Coloring (Upcoming)"
])

# ---------------------------------------------------------
# TAB 1: KIDS MAZE GENERATOR
# ---------------------------------------------------------
with tab_maze:
    st.subheader("Algorithmic Kids' Maze Generator")
    st.markdown("Create a complete, unique, print-ready 8.5\" × 11\" maze book interior with alternating margins and integrated answer keys.")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        difficulty = st.selectbox(
            "Target Age & Difficulty",
            [
                "Ages 4–6: Easy Starter (8 × 8 Grid)",
                "Ages 6–8: Medium Explorer (12 × 12 Grid)",
                "Ages 8–12: Advanced Challenger (18 × 18 Grid)",
                "Custom Complexity"
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
            grid_dim = st.slider("Custom Grid Dimension", min_value=6, max_value=30, value=15)
            
    with c2:
        num_mazes = st.selectbox(
            "Number of Mazes",
            [10, 20, 30, 40, 50, 80],
            index=1,
            help="Solution pages will automatically be calculated and appended at 4 per page."
        )
        
    with c3:
        book_title = st.text_input("Puzzle Header Title", value="AMAZING MAZES")
        
    # Page Math Summary
    solution_pages = (num_mazes + 3) // 4
    total_book_pages = num_mazes + 1 + solution_pages  # Mazes + Divider + Solutions
    
    st.info(f"📊 **Book Blueprint:** **{num_mazes}** Unique Mazes + **1** Solutions Divider + **{solution_pages}** Solution Pages = **{total_book_pages} Total Interior Pages** (Trim: 8.5\" × 11\")")
    
    if st.button("🚀 Generate Print-Ready Maze Book", type="primary"):
        with st.spinner(f"Running recursive maze algorithms for {num_mazes} puzzles..."):
            pdf_bytes, final_pages = generate_maze_book_pdf(
                num_mazes=num_mazes,
                grid_size=grid_dim,
                book_title=book_title
            )
            
        st.success(f"✅ Generated a complete {final_pages}-page KDP interior ready for upload!")
        
        # Live Previews
        st.write("#### 👁️ Live Preflight Verification")
        pv_c1, pv_c2 = st.columns(2)
        
        img_puzzle = render_pdf_page_to_image(pdf_bytes, page_index=0, scale=1.3)
        img_solution = render_pdf_page_to_image(pdf_bytes, page_index=num_mazes + 1, scale=1.3)
        
        with pv_c1:
            st.markdown("**Sample Puzzle Page (Page 1)**")
            if img_puzzle:
                st.image(img_puzzle, use_container_width=True)
                
        with pv_c2:
            st.markdown("**Sample Solution Page (4-Up Answer Key)**")
            if img_solution:
                st.image(img_solution, use_container_width=True)
                
        st.divider()
        st.download_button(
            label="📥 Download Print-Ready Maze Book (PDF)",
            data=pdf_bytes,
            file_name=f"kdp_maze_book_{grid_dim}x{grid_dim}_{num_mazes}mazes.pdf",
            mime="application/pdf",
            type="primary"
        )

# ---------------------------------------------------------
# TAB 2: WORD SEARCH (PLACEHOLDER)
# ---------------------------------------------------------
with tab_wordsearch:
    st.subheader("🔠 Themed Word Search Engine")
    st.info("🚧 Engine under construction. Next update will include custom wordlist imports, multi-directional word placement, letter matrices, and automated answer highlights.")

# ---------------------------------------------------------
# TAB 3: SUDOKU (PLACEHOLDER)
# ---------------------------------------------------------
with tab_sudoku:
    st.subheader("🔢 Sudoku Ladder Generator")
    st.info("🚧 Engine under construction. Next update will feature Easy-to-Expert difficulty balancing with verified unique solutions.")

# ---------------------------------------------------------
# TAB 4: COLORING BOOK UTILITY (PLACEHOLDER)
# ---------------------------------------------------------
with tab_coloring:
    st.subheader("🎨 Line Art & Coloring Page Prep")
    st.info("🚧 Engine under construction. Next update will include contrast enhancers to turn sketches and AI art into crisp 300 DPI coloring book pages with blank left backing sheets.")
