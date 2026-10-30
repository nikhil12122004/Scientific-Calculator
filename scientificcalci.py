"""A small, safe, dark-themed scientific calculator built with Tkinter.

Run with: python scientific_calculator.py
Only the Python standard library is required.
"""

import ast
import math
import operator
import tkinter as tk
from tkinter import font as tkfont


class SafeEvaluator:
    """Evaluate a deliberately small subset of Python arithmetic syntax."""

    BINARY = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}

    def __init__(self, degrees=True):
        self.degrees = degrees

    def _trig_arg(self, value):
        return math.radians(value) if self.degrees else value

    def _inverse_result(self, value):
        return math.degrees(value) if self.degrees else value

    def evaluate(self, expression):
        names = {
            "pi": math.pi,
            "e": math.e,
            "sin": lambda x: math.sin(self._trig_arg(x)),
            "cos": lambda x: math.cos(self._trig_arg(x)),
            "tan": lambda x: math.tan(self._trig_arg(x)),
            "asin": lambda x: self._inverse_result(math.asin(x)),
            "acos": lambda x: self._inverse_result(math.acos(x)),
            "atan": lambda x: self._inverse_result(math.atan(x)),
            "log": math.log10,
            "ln": math.log,
            "sqrt": math.sqrt,
            "abs": abs,
            "fact": self._factorial,
        }
        tree = ast.parse(expression, mode="eval")
        return self._visit(tree.body, names)

    @staticmethod
    def _factorial(value):
        if isinstance(value, bool) or int(value) != value or value < 0:
            raise ValueError("Factorial requires a non-negative integer")
        if value > 170:
            raise ValueError("Result is too large")
        return math.factorial(int(value))

    def _visit(self, node, names):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Name) and node.id in names:
            return names[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in self.BINARY:
            left, right = self._visit(node.left, names), self._visit(node.right, names)
            if isinstance(node.op, ast.Pow) and abs(right) > 10000:
                raise ValueError("Exponent is too large")
            return self.BINARY[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self.UNARY:
            return self.UNARY[type(node.op)](self._visit(node.operand, names))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            function = names.get(node.func.id)
            if function is None or node.keywords or len(node.args) != 1:
                raise ValueError("Invalid function")
            return function(self._visit(node.args[0], names))
        raise ValueError("Invalid expression")


class ScientificCalculator(tk.Tk):
    BG = "#111318"
    PANEL = "#1b1e25"
    NUMBER = "#292d36"
    SCI = "#343a46"
    OP = "#e28a3b"
    ACTION = "#b84a55"
    TEXT = "#f3f5f7"
    MUTED = "#9ca4b2"
    ACCENT = "#73c8b5"

    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.configure(bg=self.BG)
        self.minsize(390, 600)
        self.geometry("440x700")
        self.expression = ""
        self.memory = 0.0
        self.degrees = True
        self.just_evaluated = False
        self._build_ui()
        self.bind_all("<Key>", self._on_key)

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        display = tk.Frame(self, bg=self.PANEL, padx=18, pady=14)
        display.grid(row=0, column=0, sticky="nsew", padx=12, pady=(12, 8))
        display.columnconfigure(0, weight=1)

        self.history_var = tk.StringVar(value="Ready")
        self.value_var = tk.StringVar(value="0")
        tk.Label(display, textvariable=self.history_var, anchor="e", bg=self.PANEL,
                 fg=self.MUTED, font=("Segoe UI", 11)).grid(row=0, column=0, sticky="ew")
        self.value_label = tk.Label(display, textvariable=self.value_var, anchor="e",
                                    bg=self.PANEL, fg=self.TEXT,
                                    font=("Segoe UI", 30, "bold"))
        self.value_label.grid(row=1, column=0, sticky="ew", pady=(9, 14))
        status = tk.Frame(display, bg=self.PANEL)
        status.grid(row=2, column=0, sticky="ew")
        self.mode_button = tk.Button(status, text="DEG", command=self._toggle_mode,
                                     relief="flat", bg="#283b3a", fg=self.ACCENT,
                                     activebackground="#283b3a", activeforeground=self.TEXT,
                                     font=("Segoe UI", 9, "bold"), padx=10, pady=4,
                                     cursor="hand2")
        self.mode_button.pack(side="left")
        self.memory_label = tk.Label(status, text="M: —", bg=self.PANEL, fg=self.MUTED,
                                     font=("Segoe UI", 9))
        self.memory_label.pack(side="right")

        pad = tk.Frame(self, bg=self.BG, padx=12, pady=4)
        pad.grid(row=1, column=0, sticky="nsew")
        for col in range(5):
            pad.columnconfigure(col, weight=1, uniform="key")
        for row in range(7):
            pad.rowconfigure(row, weight=1, uniform="key")

        rows = [
            [("MC", "mem"), ("MR", "mem"), ("M+", "mem"), ("M−", "mem"), ("AC", "action")],
            [("sin", "sci"), ("cos", "sci"), ("tan", "sci"), ("log", "sci"), ("ln", "sci")],
            [("asin", "sci"), ("acos", "sci"), ("atan", "sci"), ("√", "sci"), ("x²", "sci")],
            [("|x|", "sci"), ("n!", "sci"), ("xʸ", "sci"), ("π", "sci"), ("e", "sci")],
            [("7", "num"), ("8", "num"), ("9", "num"), ("DEL", "action"), ("÷", "op")],
            [("4", "num"), ("5", "num"), ("6", "num"), ("×", "op"), ("−", "op")],
            [("1", "num"), ("2", "num"), ("3", "num"), ("%", "op"), ("+", "op")],
        ]
        for r, row in enumerate(rows):
            for c, (label, kind) in enumerate(row):
                self._button(pad, label, kind, r, c)
        self._button(pad, "0", "num", 7, 0, colspan=2)
        self._button(pad, ".", "num", 7, 2)
        self._button(pad, "(", "sci", 7, 3)
        self._button(pad, ")", "sci", 7, 4)
        self._button(pad, "=", "equals", 8, 0, colspan=5)
        pad.rowconfigure(7, weight=1, uniform="key")
        pad.rowconfigure(8, weight=1, uniform="key")

    def _button(self, parent, label, kind, row, col, colspan=1):
        colors = {"num": self.NUMBER, "sci": self.SCI, "op": self.OP,
                  "action": self.ACTION, "mem": "#263a3a", "equals": "#258b79"}
        fg = self.TEXT
        button = tk.Button(parent, text=label,
                           command=lambda value=label: self._press(value),
                           bg=colors[kind], fg=fg, activebackground="#596170",
                           activeforeground=self.TEXT, relief="flat", bd=0,
                           font=("Segoe UI", 11 if kind in ("sci", "mem") else 14, "bold"),
                           cursor="hand2", takefocus=False)
        button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)

    def _set_expression(self, value):
        self.expression = value
        self.value_var.set(value if value else "0")

    def _press(self, key):
        if key == "AC":
            self.expression = ""
            self.history_var.set("Ready")
            self.value_var.set("0")
            self.just_evaluated = False
            return
        if key == "DEL":
            self._set_expression(self.expression[:-1])
            self.just_evaluated = False
            return
        if key == "=":
            self._calculate()
            return
        if key in ("MC", "MR", "M+", "M−"):
            self._memory_action(key)
            return

        mapping = {"÷": "/", "×": "*", "−": "-", "π": "pi",
                   "√": "sqrt(", "x²": "**2", "xʸ": "**",
                   "|x|": "abs(", "n!": "fact("}
        functions = {"sin", "cos", "tan", "asin", "acos", "atan", "log", "ln"}
        insertion = mapping.get(key, key + "(" if key in functions else key)
        if self.just_evaluated and (key[0].isdigit() or key in (".", "pi", "e")):
            self.expression = ""
            self.history_var.set("Ready")
        self.just_evaluated = False
        self.expression += insertion
        self.value_var.set(self.expression)

    def _calculate(self):
        if not self.expression.strip():
            return
        try:
            evaluator = SafeEvaluator(self.degrees)
            result = evaluator.evaluate(self.expression)
            if isinstance(result, complex) or not math.isfinite(float(result)):
                raise ValueError("Result is not a finite real number")
            formatted = self._format_number(result)
            self.history_var.set(self.expression + " =")
            self.expression = formatted
            self.value_var.set(formatted)
            self.just_evaluated = True
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError):
            self.history_var.set(self.expression)
            self.value_var.set("Error")
            self.expression = ""
            self.just_evaluated = True

    @staticmethod
    def _format_number(value):
        value = float(value)
        if value == 0:
            return "0"
        if value.is_integer() and abs(value) < 1e16:
            return str(int(value))
        return f"{value:.12g}"

    def _toggle_mode(self):
        self.degrees = not self.degrees
        self.mode_button.configure(text="DEG" if self.degrees else "RAD")

    def _current_value(self):
        return float(SafeEvaluator(self.degrees).evaluate(self.expression))

    def _memory_action(self, action):
        try:
            current = self._current_value() if self.expression else 0.0
            if action == "MC":
                self.memory = 0.0
            elif action == "MR":
                self.expression = self._format_number(self.memory)
                self.value_var.set(self.expression)
            elif action == "M+":
                self.memory += current
            elif action == "M−":
                self.memory -= current
            self.memory_label.configure(
                text="M: —" if self.memory == 0 else f"M: {self._format_number(self.memory)}")
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError):
            self.value_var.set("Error")

    def _on_key(self, event):
        char = event.char
        if char in "0123456789.+-*/%()":
            self._press(char)
            return "break"
        if event.keysym in ("Return", "KP_Enter"):
            self._calculate()
            return "break"
        if event.keysym == "BackSpace":
            self._press("DEL")
            return "break"
        if event.keysym == "Escape":
            self._press("AC")
            return "break"
        return None


if __name__ == "__main__":
    ScientificCalculator().mainloop()