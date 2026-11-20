#!/usr/bin/env python3
"""
character_puppet.py — High-Performance 2D Modular Character Puppet Rig & Comedy Skit Engine.
Part of the Faceless Video Production Engine.

Supports:
- Articulated 2-segment limbs with joint smoothing
- Expressive cartoon sneakers with rubber toe caps, soles, and laces
- Expressive cartoon facial features: panting, shocked, smug, talking, dizzy (spiral eyes), smile
- Dynamic character states:
  * Dave: carrying heavy weights, frantic knocking, squished accordion, bandaged, shocked
  * Alex: lounging in beach chair with sunglasses & iced coffee, explaining, laughing
- Physics props & comic visualizers:
  * Drop physics, acceleration, bounce wobble, camera screen shake
  * Comic starburst stickers (BONK!, THUD!, 429 ERROR!)
  * Expanding cartoon dust puffs
  * Floating cards & notification envelopes
  * Side-by-side technical visualizer cards (e.g. Polling vs Webhooks, SVG vs PNG)
  * Signature Outro Conversion Sequence
"""

from __future__ import annotations
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Dict, Any, Optional, List

FONT_PATH = "d:/Faceless/fonts/InterDisplay-Bold.otf"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

# Universal Color Palette
C_WHITE = (255, 255, 255)
C_BLACK = (18, 20, 26)
C_CYAN = (0, 220, 255)
C_RED = (235, 60, 50)
C_GREEN = (40, 200, 100)
C_YELLOW = (255, 205, 50)
C_SWEAT = (110, 215, 255)
C_WOOD = (195, 130, 80)
C_BOX_BROWN = (205, 145, 95)
C_BOX_DARK = (165, 110, 65)
C_TAPE = (235, 195, 130)

def draw_limb(draw: ImageDraw.ImageDraw, p0: Tuple[int, int], p1: Tuple[int, int], p2: Tuple[int, int], width: int = 12, fill: Tuple[int, int, int] = C_BLACK):
    """Draws a 2-segment articulated limb with smoothed joint caps."""
    draw.line([p0, p1], fill=fill, width=width)
    draw.ellipse([p1[0] - width//2, p1[1] - width//2, p1[0] + width//2, p1[1] + width//2], fill=fill)
    draw.line([p1, p2], fill=fill, width=width)

def draw_sneaker(draw: ImageDraw.ImageDraw, pos: Tuple[int, int], color: Tuple[int, int, int] = C_RED, size: int = 28, facing: str = "right"):
    """Draws a stylish cartoon sneaker with laces, white sole, and rubber toe cap."""
    x, y = pos
    w, h = size * 1.5, size * 0.85
    if facing == "right":
        draw.rounded_rectangle([x - 6, y - h, x + w, y + 2], radius=6, fill=color, outline=C_BLACK, width=2)
        draw.rounded_rectangle([x - 8, y - 2, x + w + 4, y + 10], radius=4, fill=C_WHITE, outline=C_BLACK, width=2)
        draw.chord([x + w - 10, y - h, x + w + 4, y + 2], 270, 90, fill=C_WHITE, outline=C_BLACK, width=2)
        for lx in [x + 8, x + 18, x + 28]:
            draw.line([(lx, y - h + 4), (lx + 6, y - h + 10)], fill=C_WHITE, width=2)
    else:
        draw.rounded_rectangle([x - w, y - h, x + 6, y + 2], radius=6, fill=color, outline=C_BLACK, width=2)
        draw.rounded_rectangle([x - w - 4, y - 2, x + 8, y + 10], radius=4, fill=C_WHITE, outline=C_BLACK, width=2)
        draw.chord([x - w - 4, y - h, x - w + 10, y + 2], 90, 270, fill=C_WHITE, outline=C_BLACK, width=2)
        for lx in [x - 8, x - 18, x - 28]:
            draw.line([(lx, y - h + 4), (lx - 6, y - h + 10)], fill=C_WHITE, width=2)

def draw_red_cap(draw: ImageDraw.ImageDraw, cx: int, cy: int, facing: str = "right"):
    """Draws a backward or forward cartoon baseball cap."""
    cap_r = 54
    draw.chord([cx - cap_r, cy - cap_r - 20, cx + cap_r, cy + cap_r - 20], 180, 360, fill=C_RED, outline=C_BLACK, width=3)
    draw.ellipse([cx - 5, cy - cap_r - 24, cx + 5, cy - cap_r - 16], fill=C_BLACK)
    if facing == "right":
        draw.polygon([(cx - 10, cy - 26), (cx + cap_r + 30, cy - 14), (cx + cap_r + 25, cy - 4), (cx - 10, cy - 16)], fill=(205, 45, 35), outline=C_BLACK)
    else:
        draw.polygon([(cx + 10, cy - 26), (cx - cap_r - 30, cy - 14), (cx - cap_r - 25, cy - 4), (cx + 10, cy - 16)], fill=(205, 45, 35), outline=C_BLACK)

def draw_green_tie(draw: ImageDraw.ImageDraw, cx: int, cy: int):
    """Draws a crisp green necktie."""
    draw.polygon([(cx - 7, cy + 50), (cx + 7, cy + 50), (cx + 5, cy + 62), (cx - 5, cy + 62)], fill=C_GREEN, outline=C_BLACK)
    draw.polygon([(cx - 5, cy + 62), (cx + 5, cy + 62), (cx + 10, cy + 120), (cx, cy + 135), (cx - 10, cy + 120)], fill=C_GREEN, outline=C_BLACK)

def draw_sweat_drops(draw: ImageDraw.ImageDraw, cx: int, cy: int, count: int = 3, t: float = 0.0):
    """Draws flying blue teardrop sweat particles."""
    for i in range(count):
        drop_x = cx + int(45 + i * 18 + math.sin(t * 8.0 + i) * 6)
        drop_y = cy - int(30 + i * 14 + math.cos(t * 8.0 + i) * 6)
        r = 6 + (i % 2) * 2
        draw.ellipse([drop_x - r, drop_y - r, drop_x + r, drop_y + r], fill=C_SWEAT, outline=C_BLACK, width=2)
        draw.polygon([(drop_x - r + 1, drop_y), (drop_x + r - 1, drop_y), (drop_x, drop_y - r * 2)], fill=C_SWEAT, outline=C_BLACK)

def draw_face(draw: ImageDraw.ImageDraw, cx: int, cy: int, expression: str = "neutral", facing: str = "right"):
    """Renders expressive cartoon face features: shocked, panting, talking, smug, dizzy, smile, neutral."""
    x_off = 10 if facing == "right" else -10
    
    if expression == "shocked":
        eye_r = 18
        draw.ellipse([cx + x_off - 26 - eye_r, cy - 10 - eye_r, cx + x_off - 26 + eye_r, cy - 10 + eye_r], fill=C_WHITE, outline=C_BLACK, width=3)
        draw.ellipse([cx + x_off + 14 - eye_r, cy - 10 - eye_r, cx + x_off + 14 + eye_r, cy - 10 + eye_r], fill=C_WHITE, outline=C_BLACK, width=3)
        draw.ellipse([cx + x_off - 29, cy - 13, cx + x_off - 23, cy - 7], fill=C_BLACK)
        draw.ellipse([cx + x_off + 11, cy - 13, cx + x_off + 17, cy - 7], fill=C_BLACK)
        draw.arc([cx + x_off - 46, cy - 42, cx + x_off - 10, cy - 22], 190, 350, fill=C_BLACK, width=3)
        draw.arc([cx + x_off + 4, cy - 42, cx + x_off + 40, cy - 22], 190, 350, fill=C_BLACK, width=3)
        draw.ellipse([cx + x_off - 16, cy + 12, cx + x_off + 16, cy + 46], fill=(160, 35, 45), outline=C_BLACK, width=3)
        draw.chord([cx + x_off - 12, cy + 30, cx + x_off + 12, cy + 44], 0, 180, fill=(245, 120, 130))
        
    elif expression == "panting":
        draw.ellipse([cx + x_off - 26, cy - 14, cx + x_off - 10, cy + 4], fill=C_BLACK)
        draw.ellipse([cx + x_off + 10, cy - 14, cx + x_off + 26, cy + 4], fill=C_BLACK)
        draw.line([(cx + x_off - 36, cy - 24), (cx + x_off - 8, cy - 18)], fill=C_BLACK, width=3)
        draw.line([(cx + x_off + 8, cy - 18), (cx + x_off + 36, cy - 24)], fill=C_BLACK, width=3)
        draw.arc([cx + x_off - 20, cy + 10, cx + x_off + 20, cy + 32], 0, 180, fill=C_BLACK, width=3)
        draw.ellipse([cx + x_off - 8, cy + 22, cx + x_off + 14, cy + 40], fill=(245, 100, 115), outline=C_BLACK, width=2)
        
    elif expression == "talking":
        draw.ellipse([cx + x_off - 24, cy - 12, cx + x_off - 10, cy + 2], fill=C_BLACK)
        draw.ellipse([cx + x_off + 10, cy - 12, cx + x_off + 24, cy + 2], fill=C_BLACK)
        draw.arc([cx + x_off - 30, cy - 24, cx + x_off - 6, cy - 12], 200, 340, fill=C_BLACK, width=3)
        draw.arc([cx + x_off + 6, cy - 24, cx + x_off + 30, cy - 12], 200, 340, fill=C_BLACK, width=3)
        draw.ellipse([cx + x_off - 14, cy + 12, cx + x_off + 14, cy + 28], fill=(160, 35, 45), outline=C_BLACK, width=2)
        
    elif expression == "smug":
        draw.ellipse([cx + x_off - 24, cy - 8, cx + x_off - 10, cy + 4], fill=C_BLACK)
        draw.ellipse([cx + x_off + 10, cy - 8, cx + x_off + 24, cy + 4], fill=C_BLACK)
        draw.arc([cx + x_off - 30, cy - 30, cx + x_off - 6, cy - 10], 200, 340, fill=C_BLACK, width=4)
        draw.line([(cx + x_off + 6, cy - 14), (cx + x_off + 30, cy - 10)], fill=C_BLACK, width=3)
        draw.arc([cx + x_off - 6, cy + 8, cx + x_off + 24, cy + 26], 0, 180, fill=C_BLACK, width=3)
        
    elif expression == "dizzy":
        # Spiral cartoon eyes
        for ex in [cx + x_off - 18, cx + x_off + 18]:
            draw.arc([ex - 12, cy - 18, ex + 12, cy + 6], 0, 360, fill=C_BLACK, width=2)
            draw.arc([ex - 7, cy - 13, ex + 7, cy + 1], 0, 360, fill=C_BLACK, width=2)
        draw.arc([cx + x_off - 15, cy + 18, cx + x_off + 15, cy + 32], 0, 180, fill=C_BLACK, width=3)
        
    else:  # neutral / smile
        draw.ellipse([cx + x_off - 22, cy - 10, cx + x_off - 10, cy + 2], fill=C_BLACK)
        draw.ellipse([cx + x_off + 10, cy - 10, cx + x_off + 22, cy + 2], fill=C_BLACK)
        draw.arc([cx + x_off - 28, cy - 20, cx + x_off - 6, cy - 8], 200, 340, fill=C_BLACK, width=2)
        draw.arc([cx + x_off + 6, cy - 20, cx + x_off + 28, cy - 8], 200, 340, fill=C_BLACK, width=2)
        draw.arc([cx + x_off - 16, cy + 10, cx + x_off + 16, cy + 24], 0, 180, fill=C_BLACK, width=3)

# -------------------------------------------------------------------------
# Comic Effects (Starbursts, Dust Puffs, Screen Shake)
# -------------------------------------------------------------------------
def render_comic_starburst(draw: ImageDraw.ImageDraw, center_x: int, center_y: int, main_text: str = "THUD!", sub_text: str = "", scale: float = 1.0, star_color: Tuple[int, int, int] = C_YELLOW, text_color: Tuple[int, int, int] = C_RED):
    """Draws a multi-point comic explosion starburst with bold centered comic text."""
    cx, cy = center_x, center_y
    n_points = 14
    pts = []
    for i in range(n_points * 2):
        angle = i * math.pi / n_points
        r = (140 if i % 2 == 0 else 80) * scale
        pts.append((cx + int(math.cos(angle) * r), cy + int(math.sin(angle) * r)))
    draw.polygon(pts, fill=star_color, outline=C_BLACK)
    
    f_main = get_font(int(44 * scale))
    draw.text((cx - int(len(main_text) * 11 * scale), cy - int(32 * scale)), main_text, font=f_main, fill=text_color, stroke_width=4, stroke_fill=C_BLACK)
    if sub_text:
        f_sub = get_font(int(20 * scale))
        draw.text((cx - int(len(sub_text) * 5 * scale), cy + int(14 * scale)), sub_text, font=f_sub, fill=C_WHITE, stroke_width=2, stroke_fill=C_BLACK)

def render_dust_puffs(draw: ImageDraw.ImageDraw, base_x: int, floor_y: int, progress: float, width_span: int = 400):
    """Draws spreading cartoon dust cloud puffs shooting outward upon impact."""
    if progress > 1.0 or progress < 0.0:
        return
    dist = int(120 * progress)
    puff_r = int(24 * (1.0 - 0.3 * progress))
    
    lx = base_x - dist
    draw.ellipse([lx - puff_r, floor_y - puff_r * 2, lx + puff_r, floor_y], fill=(220, 215, 200), outline=C_BLACK, width=2)
    rx = base_x + dist + width_span
    draw.ellipse([rx - puff_r, floor_y - puff_r * 2, rx + puff_r, floor_y], fill=(220, 215, 200), outline=C_BLACK, width=2)

def compute_screen_shake(t: float, hit_time: float, max_amp: float = 20.0, decay: float = 10.0, freq: float = 75.0) -> Tuple[int, int]:
    """Computes decaying harmonic screen shake offsets (dx, dy)."""
    if t < hit_time or t > hit_time + 0.6:
        return (0, 0)
    dt = t - hit_time
    amp = int(max_amp * math.exp(-decay * dt) * math.sin(freq * dt))
    return (amp, -abs(amp) // 2)

# -------------------------------------------------------------------------
# High-Level Puppet Rig Classes
# -------------------------------------------------------------------------
class ComicCharacter:
    """Rig for fully articulated comic characters with expressive poses."""
    def __init__(self, name: str = "Dave", cap_color: Optional[Tuple[int, int, int]] = C_RED, sneaker_color: Tuple[int, int, int] = C_RED, tie_color: Optional[Tuple[int, int, int]] = None):
        self.name = name
        self.cap_color = cap_color
        self.sneaker_color = sneaker_color
        self.tie_color = tie_color

    def draw(self, draw: ImageDraw.ImageDraw, x: int, y: int, pose: str = "idle", expression: str = "neutral", t: float = 0.0, facing: str = "right"):
        feet_y = y
        head_cx = x

        if pose == "squished":
            head_cy = feet_y - 70
            head_r = 44
            draw.ellipse([head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r], fill=C_WHITE, outline=C_BLACK, width=4)
            draw_face(draw, head_cx, head_cy, expression="dizzy", facing=facing)
            if self.cap_color:
                draw_red_cap(draw, head_cx, head_cy, facing=facing)
            draw.line([(head_cx - 80, head_cy + 40), (head_cx + 80, head_cy + 40)], fill=C_BLACK, width=14)
            draw_sneaker(draw, (head_cx - 90, feet_y), color=self.sneaker_color, size=24, facing="left")
            draw_sneaker(draw, (head_cx + 90, feet_y), color=self.sneaker_color, size=24, facing="right")
            for s in range(3):
                star_angle = t * 8.0 + s * (2 * math.pi / 3)
                sx = head_cx + int(math.cos(star_angle) * 65)
                sy = head_cy - 60 + int(math.sin(star_angle) * 20)
                draw.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=C_YELLOW, outline=C_BLACK, width=1)
            return

        head_cy = feet_y - 340
        torso_y0 = head_cy + 52
        torso_y1 = torso_y0 + 135
        hip_pos = (head_cx, torso_y1)

        draw.line([(head_cx, torso_y0), hip_pos], fill=C_BLACK, width=14)
        if self.tie_color:
            draw_green_tie(draw, head_cx, torso_y0)

        # Standard Leg Rig
        knee_l = (head_cx - 35, hip_pos[1] + 75)
        foot_l = (head_cx - 45, feet_y)
        knee_r = (head_cx + 35, hip_pos[1] + 75)
        foot_r = (head_cx + 45, feet_y)
        draw_limb(draw, hip_pos, knee_l, foot_l, width=12)
        draw_limb(draw, hip_pos, knee_r, foot_r, width=12)
        draw_sneaker(draw, (foot_l[0] - 15, foot_l[1]), color=self.sneaker_color, size=28, facing=facing)
        draw_sneaker(draw, (foot_r[0] - 15, foot_r[1]), color=self.sneaker_color, size=28, facing=facing)

        # Arms based on Pose
        if pose == "carry":
            elbow_l = (head_cx + 50, torso_y0 + 70)
            hand_l = (head_cx + 120, torso_y0 + 95)
            elbow_r = (head_cx + 70, torso_y0 + 80)
            hand_r = (head_cx + 150, torso_y0 + 110)
            draw_limb(draw, (head_cx, torso_y0 + 15), elbow_l, hand_l, width=12)
            draw_limb(draw, (head_cx, torso_y0 + 15), elbow_r, hand_r, width=12)
        elif pose == "knocking":
            knock_bob = int(math.sin(t * 24.0) * 14)
            elbow_r = (head_cx - 45, torso_y0 + 40)
            hand_r = (head_cx - 100 + knock_bob, torso_y0 + 20)
            draw_limb(draw, (head_cx, torso_y0 + 15), elbow_r, hand_r, width=12)
            elbow_l = (head_cx + 40, torso_y0 + 50)
            hand_l = (head_cx + 70, torso_y0 + 20)
            draw_limb(draw, (head_cx, torso_y0 + 15), elbow_l, hand_l, width=12)
        elif pose == "shocked":
            elbow_l = (head_cx - 65, torso_y0 - 15)
            hand_l = (head_cx - 42, head_cy + 12)
            elbow_r = (head_cx + 65, torso_y0 - 15)
            hand_r = (head_cx + 42, head_cy + 12)
            draw_limb(draw, (head_cx, torso_y0 + 15), elbow_l, hand_l, width=12)
            draw_limb(draw, (head_cx, torso_y0 + 15), elbow_r, hand_r, width=12)
        elif pose == "explaining":
            elbow_back = (head_cx + 40, torso_y0 + 55)
            hand_back = (head_cx + 15, torso_y1)
            draw_limb(draw, (head_cx, torso_y0 + 15), elbow_back, hand_back, width=12)
            elbow_front = (head_cx - 60, torso_y0 + 10)
            hand_front = (head_cx - 110, torso_y0 - 35)
            draw_limb(draw, (head_cx, torso_y0 + 15), elbow_front, hand_front, width=12)
        else: # idle
            elbow_l = (head_cx - 45, torso_y0 + 60)
            hand_l = (head_cx - 15, torso_y1)
            draw_limb(draw, (head_cx, torso_y0 + 15), elbow_l, hand_l, width=12)
            elbow_r = (head_cx + 45, torso_y0 + 60)
            hand_r = (head_cx + 15, torso_y1)
            draw_limb(draw, (head_cx, torso_y0 + 15), elbow_r, hand_r, width=12)

        # Head & Cap
        head_r = 52
        draw.ellipse([head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r], fill=C_WHITE, outline=C_BLACK, width=4)
        draw_face(draw, head_cx, head_cy, expression=expression, facing=facing)
        if self.cap_color:
            draw_red_cap(draw, head_cx, head_cy, facing=facing)
        if expression in ["panting", "shocked"]:
            draw_sweat_drops(draw, head_cx, head_cy, count=3, t=t)
