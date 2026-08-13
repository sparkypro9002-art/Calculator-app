import re
import sys
import pygame

pygame.init()
pygame.font.init()

display_info = pygame.display.Info()
WIDTH = display_info.current_w if display_info.current_w > 0 else 720
HEIGHT = display_info.current_h if display_info.current_h > 0 else 1280

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Android Calculator")
clock = pygame.time.Clock()

output = ""


def update_layout(w, h):
    font_size = max(16, int(w * 0.06))
    font = pygame.font.Font(None, font_size)

    padding_x = int(w * 0.02)
    padding_y = int(h * 0.015)
    start_x = padding_x
    start_y = int(h * 0.22)

    btn_w = (w - (padding_x * 5)) // 4
    btn_h = int(h * 0.13)

    button_rects = []
    current_y = start_y

    for row in range(5):
        current_x = start_x
        for col in range(4):
            button_rects.append(pygame.Rect(current_x, current_y, btn_w, btn_h))
            current_x += btn_w + padding_x
        current_y += btn_h + padding_y

    (
        button_c,
        button_modlus,
        button_percent,
        button_div,
        button7,
        button8,
        button9,
        button_multi,
        button4,
        button5,
        button6,
        button_sub,
        button1,
        button2,
        button3,
        button_plus,
        button_0,
        button_dot,
        button_del,
        button_eq,
    ) = button_rects

    buttons = [
        (button1, "1"),
        (button2, "2"),
        (button3, "3"),
        (button4, "4"),
        (button5, "5"),
        (button6, "6"),
        (button7, "7"),
        (button8, "8"),
        (button9, "9"),
        (button_0, "0"),
        (button_plus, "+"),
        (button_sub, "-"),
        (button_multi, "*"),
        (button_div, "/"),
        (button_modlus, "mod"),
        (button_percent, "%"),
        (button_dot, "."),
        (button_c, "C"),
        (button_del, "Del"),
        (button_eq, "="),
    ]

    box_rect = pygame.Rect(
        padding_x, int(h * 0.03), w - (padding_x * 2), int(h * 0.16)
    )

    return (
        font,
        padding_x,
        box_rect,
        buttons,
        (button_modlus, button_eq, button_c, button_del, button_percent),
    )


font, PADDING_X, box_rect, buttons, special_btns = update_layout(WIDTH, HEIGHT)
button_modlus, button_eq, button_c, button_del, button_percent = special_btns


def format_number(val):
    val = round(val, 10)
    return str(int(val)) if val.is_integer() else str(val)


def calculate_instant_percent(expr):
    if not expr:
        return ""

    try:
        match_add_sub = re.match(
            r"^([0-9.]+)\s*([+\-])\s*([0-9.]+)$", expr.strip()
        )
        if match_add_sub:
            base = float(match_add_sub.group(1))
            op = match_add_sub.group(2)
            pct = float(match_add_sub.group(3))
            val = base * (pct / 100.0)
            res = (base + val) if op == "+" else (base - val)
            return format_number(res)

        match_div = re.match(r"^([0-9.]+)\s*(/)\s*([0-9.]+)$", expr.strip())
        if match_div:
            base = float(match_div.group(1))
            pct = float(match_div.group(3)) / 100.0
            return format_number(base / pct)

        match_mul = re.match(r"^([0-9.]+)\s*(\*)\s*([0-9.]+)$", expr.strip())
        if match_mul:
            base = float(match_mul.group(1))
            pct = float(match_mul.group(3)) / 100.0
            return format_number(base * pct)

        val = float(eval(expr)) / 100.0
        return format_number(val)

    except Exception:
        return "Error"


def handle_click(pos):
    global output
    if output == "Error":
        output = ""

    clicked_standard = False

    if button_modlus.collidepoint(pos):
        try:
            if output != "":
                val = float(eval(output))
                output = format_number(-val)
        except Exception:
            output = "Error"
        clicked_standard = True

    elif button_eq.collidepoint(pos):
        try:
            res = float(eval(output))
            output = format_number(res)
        except Exception:
            output = "Error"
        clicked_standard = True

    elif button_c.collidepoint(pos):
        output = ""
        clicked_standard = True

    elif button_del.collidepoint(pos):
        output = output[:-1]
        clicked_standard = True

    elif button_percent.collidepoint(pos):
        if output != "":
            output = calculate_instant_percent(output)
        clicked_standard = True

    if not clicked_standard:
        for button_rect, value in buttons:
            if value not in ["=", "C", "Del", "%", "mod"]:
                if button_rect.collidepoint(pos):
                    output += value
                    break


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            font, PADDING_X, box_rect, buttons, special_btns = update_layout(
                WIDTH, HEIGHT
            )
            button_modlus, button_eq, button_c, button_del, button_percent = (
                special_btns
            )

        elif event.type == pygame.KEYDOWN:
            back_key = getattr(pygame, "K_AC_BACK", pygame.K_ESCAPE)
            if event.key in (pygame.K_ESCAPE, back_key):
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)

    screen.fill("black")

    pygame.draw.rect(screen, (28, 28, 28), box_rect, border_radius=15)

    display_text = output if output != "" else "0"
    display_surface = font.render(display_text, True, "WHITE")

    text_x = box_rect.right - display_surface.get_width() - int(WIDTH * 0.03)
    text_y = box_rect.centery - (display_surface.get_height() // 2)

    screen.set_clip(box_rect)
    screen.blit(display_surface, (max(box_rect.left + 10, text_x), text_y))
    screen.set_clip(None)

    for btn_rect, btn_text_str in buttons:
        display_label = btn_text_str
        if btn_text_str == "mod":
            display_label = "+/-"
        elif btn_text_str == "Del":
            display_label = "DEL"

        if display_label in ["C", "+/-", "%", "DEL"]:
            bg_color = (255, 255, 0)
            text_color = "BLACK"
        elif display_label in ["/", "*", "-", "+"]:
            bg_color = (255, 0, 0)
            text_color = "BLACK"
        elif display_label == "=":
            bg_color = (0, 255, 0)
            text_color = "BLACK"
        else:
            bg_color = (0, 0, 255)
            text_color = "BLACK"

        pygame.draw.rect(screen, bg_color, btn_rect, border_radius=12)
        btn_text_surface = font.render(display_label, True, text_color)
        text_rect = btn_text_surface.get_rect(center=btn_rect.center)
        screen.blit(btn_text_surface, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
    
