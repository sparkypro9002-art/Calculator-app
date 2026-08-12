import re
import ast
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivy.uix.scrollview import ScrollView

def format_number(val):
    val = round(val, 10)
    return str(int(val)) if val.is_integer() else str(val)

def safe_eval(expr):
    try:
        cleaned_expr = expr.replace("×", "*").replace("÷", "/")
        node = ast.parse(cleaned_expr, mode="eval")
        res = float(_eval_node(node.body))
        return format_number(res)
    except Exception:
        return "Error"

def _eval_node(node):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -_eval_node(node.operand)
        elif isinstance(node.op, ast.UAdd):
            return +_eval_node(node.operand)
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
    raise ValueError("Unsupported operation")

def calculate_instant_percent(expr):
    if not expr:
        return ""
    try:
        match_add_sub = re.match(r"^([0-9.]+)\s*([+\-])\s*([0-9.]+)$", expr.strip())
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

        val = float(safe_eval(expr)) / 100.0
        return format_number(val)
    except Exception:
        return "Error"

class CalculatorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.output = ""

        main_layout = MDBoxLayout(orientation="vertical", padding=15, spacing=15)

        display_box = MDBoxLayout(
            size_hint=(1, 0.25),
            md_bg_color=(0.11, 0.11, 0.11, 1),
            padding=(15, 10),
            radius=[12, 12, 12, 12],
        )

        self.scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_y=False,
            do_scroll_x=True,
            bar_width=0,
        )

        self.display = MDLabel(
            text="0",
            font_size="40sp",
            halign="right",
            valign="center",
            size_hint=(None, 1),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
        )

        self.display.bind(texture_size=self._update_label_width)
        self.scroll_view.add_widget(self.display)
        display_box.add_widget(self.scroll_view)
        main_layout.add_widget(display_box)

        grid = MDGridLayout(cols=4, spacing=10, size_hint=(1, 0.75))

        buttons = [
            ("C", (1, 0.8, 0, 1)), ("+/-", (1, 0.8, 0, 1)), ("%", (1, 0.8, 0, 1)), ("/", (0.9, 0.2, 0.2, 1)),
            ("7", (0.2, 0.2, 0.3, 1)), ("8", (0.2, 0.2, 0.3, 1)), ("9", (0.2, 0.2, 0.3, 1)), ("*", (0.9, 0.2, 0.2, 1)),
            ("4", (0.2, 0.2, 0.3, 1)), ("5", (0.2, 0.2, 0.3, 1)), ("6", (0.2, 0.2, 0.3, 1)), ("-", (0.9, 0.2, 0.2, 1)),
            ("1", (0.2, 0.2, 0.3, 1)), ("2", (0.2, 0.2, 0.3, 1)), ("3", (0.2, 0.2, 0.3, 1)), ("+", (0.9, 0.2, 0.2, 1)),
            ("0", (0.2, 0.2, 0.3, 1)), (".", (0.2, 0.2, 0.3, 1)), ("DEL", (1, 0.8, 0, 1)), ("=", (0.2, 0.8, 0.2, 1)),
        ]

        for text, bg_color in buttons:
            btn = MDFillRoundFlatButton(
                text=text,
                size_hint=(1, 1),
                font_size="20sp",
                md_bg_color=bg_color,
                text_color=(1, 1, 1, 1),
            )
            btn.bind(on_release=self.on_button_press)
            grid.add_widget(btn)

        main_layout.add_widget(grid)
        return main_layout

    def _update_label_width(self, instance, value):
        instance.width = max(instance.texture_size[0], self.scroll_view.width)
        self.scroll_view.scroll_x = 1

    def update_display(self, text):
        display_text = text if text != "" else "0"
        self.display.text = display_text
        char_count = len(display_text)
        if char_count > 18:
            self.display.font_size = "22sp"
        elif char_count > 12:
            self.display.font_size = "28sp"
        elif char_count > 8:
            self.display.font_size = "34sp"
        else:
            self.display.font_size = "40sp"

    def on_button_press(self, instance):
        text = instance.text
        operators = ("+", "-", "*", "/")

        if self.output == "Error":
            self.output = ""

        if text == "C":
            self.output = ""

        elif text == "DEL":
            self.output = self.output[:-1]

        elif text == "+/-":
            if self.output != "":
                val = safe_eval(self.output)
                if val != "Error":
                    self.output = format_number(-float(val))
                else:
                    self.output = "Error"

        elif text == "%":
            if self.output != "":
                self.output = calculate_instant_percent(self.output)

        elif text == "=":
            if self.output != "":
                self.output = safe_eval(self.output)

        elif text == ".":
            last_segment = re.split(r"[+\-*/]", self.output)[-1]
            if "." not in last_segment:
                if not self.output or self.output[-1] in operators:
                    self.output += "0."
                else:
                    self.output += "."

        elif text in operators:
            if not self.output:
                if text == "-":
                    self.output += text
            elif self.output[-1] in operators:
                self.output = self.output[:-1] + text
            else:
                self.output += text

        elif text.isdigit():
            last_segment = re.split(r"[+\-*/]", self.output)[-1]
            digits_only = last_segment.replace(".", "")
            if len(digits_only) >= 15:
                MDSnackbar(MDSnackbarText(text="Maximum limit reached")).open()
                return
            else:
                self.output += text

        self.update_display(self.output)

if __name__ == "__main__":
    CalculatorApp().run()
