# FF Sensi Lab - a standalone Free Fire sensitivity suggestion app
# Built with Kivy. It does NOT connect to or modify Free Fire.

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex


BG = "#090D18"
PANEL = "#121B2D"
PANEL_2 = "#18243A"
TEXT = "#F4F7FF"
MUTED = "#A8B4CC"
CYAN = "#29E6D2"
RED = "#FF4D6D"
PURPLE = "#9B7BFF"


class NeonCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [dp(14), dp(14), dp(14), dp(14)]
        self.spacing = dp(10)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter("height"))
        with self.canvas.before:
            Color(*get_color_from_hex(PANEL))
            self.bg_rect = RoundedRectangle(radius=[dp(16)])
            Color(*get_color_from_hex("#263653"))
            self.border = Line(rounded_rectangle=(0, 0, 100, 100, dp(16)), width=1)
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *_):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(16))


class SectionTitle(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(28)
        self.font_size = sp(15)
        self.bold = True
        self.color = get_color_from_hex(CYAN)
        self.halign = "left"
        self.valign = "middle"
        self.text_size = (None, None)


class QuestionRow(BoxLayout):
    def __init__(self, question, options, default, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(74)
        self.spacing = dp(5)

        label = Label(
            text=question, color=get_color_from_hex(TEXT),
            font_size=sp(13), bold=True, halign="left", valign="middle",
            size_hint_y=None, height=dp(25), text_size=(Window.width - dp(70), None)
        )
        self.add_widget(label)

        self.spinner = Spinner(
            text=default, values=options, size_hint_y=None, height=dp(42),
            background_normal="", background_down="",
            background_color=get_color_from_hex(PANEL_2),
            color=get_color_from_hex(TEXT), font_size=sp(13),
            option_cls=None
        )
        self.add_widget(self.spinner)


class SensiApp(App):
    def build(self):
        self.title = "FF Sensi Lab"
        Window.clearcolor = get_color_from_hex(BG)
        Window.softinput_mode = "below_target"

        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        self.page = BoxLayout(
            orientation="vertical", padding=[dp(16), dp(18), dp(16), dp(24)],
            spacing=dp(13), size_hint_y=None
        )
        self.page.bind(minimum_height=self.page.setter("height"))
        scroll.add_widget(self.page)

        self._build_header()
        self._build_device_card()
        self._build_gameplay_card()
        self._build_result_area()
        self._build_footer()
        return scroll

    def add_label(self, parent, text, size=13, color=TEXT, bold=False, height=dp(24)):
        label = Label(
            text=text, font_size=sp(size), color=get_color_from_hex(color),
            bold=bold, size_hint_y=None, height=height,
            halign="left", valign="middle"
        )
        label.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))
        parent.add_widget(label)
        return label

    def _build_header(self):
        top = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(8))
        brand = Label(
            text="[b]FF[/b] [color=29E6D2]SENSI LAB[/color]",
            markup=True, font_size=sp(21), color=get_color_from_hex(TEXT),
            halign="left", valign="middle"
        )
        top.add_widget(brand)
        tag = Label(
            text="BETA  •  1.0", font_size=sp(10),
            color=get_color_from_hex(CYAN), size_hint_x=None, width=dp(86)
        )
        top.add_widget(tag)
        self.page.add_widget(top)

        hero = NeonCard()
        hero.add_widget(Label(
            text="[b]FIND YOUR\nPERFECT SENSITIVITY[/b]",
            markup=True, font_size=sp(24), color=get_color_from_hex(TEXT),
            halign="left", valign="middle", size_hint_y=None, height=dp(76)
        ))
        hero.add_widget(Label(
            text="Answer a few gameplay questions. Get a custom starting setup made for your play style.",
            font_size=sp(12), color=get_color_from_hex(MUTED),
            halign="left", valign="middle", size_hint_y=None, height=dp(42)
        ))
        self.page.add_widget(hero)

    def _build_device_card(self):
        card = NeonCard()
        card.add_widget(SectionTitle(text="01  /  DEVICE DETAILS"))
        self.device_name = TextInput(
            hint_text="Phone model (optional, e.g. Infinix Hot)",
            multiline=False, size_hint_y=None, height=dp(42),
            font_size=sp(13), padding=[dp(10), dp(10)],
            background_normal="", background_active="",
            background_color=get_color_from_hex(PANEL_2),
            foreground_color=get_color_from_hex(TEXT),
            hint_text_color=get_color_from_hex(MUTED), cursor_color=get_color_from_hex(CYAN)
        )
        card.add_widget(self.device_name)
        self.ram = self._question(card, "How much RAM does your phone have?",
                                  ["2 GB", "3 GB", "4 GB", "6 GB", "8 GB", "12 GB or more"], "4 GB")
        self.fps = self._question(card, "Which FPS option do you usually get?",
                                  ["30 FPS", "40 FPS", "60 FPS", "90 FPS", "120 FPS"], "60 FPS")
        self.scale = self._question(card, "What sensitivity maximum does your game show?",
                                    ["100", "200"], "200")
        self.page.add_widget(card)

    def _build_gameplay_card(self):
        card = NeonCard()
        card.add_widget(SectionTitle(text="02  /  GAMEPLAY STYLE"))
        self.style = self._question(card, "Your main play style?",
                                    ["Rush / Fast drag", "One-tap headshots", "Balanced", "Long-range / Sniper"], "Balanced")
        self.aim = self._question(card, "How is your aim control?",
                                  ["Beginner", "Intermediate", "Experienced"], "Intermediate")
        self.drag = self._question(card, "Your usual screen drag?",
                                   ["Short drag", "Medium drag", "Long drag"], "Medium drag")
        self.fingers = self._question(card, "How many fingers do you play with?",
                                      ["2 fingers", "3 fingers", "4 fingers", "5 fingers or more"], "2 fingers")
        self.page.add_widget(card)

        generate = Button(
            text="⚡  GENERATE MY SENSITIVITY",
            size_hint_y=None, height=dp(52), font_size=sp(14), bold=True,
            background_normal="", background_down="",
            background_color=get_color_from_hex(CYAN),
            color=get_color_from_hex("#07111C")
        )
        generate.bind(on_release=self.generate_sensi)
        self.page.add_widget(generate)

    def _question(self, card, question, options, default):
        row = QuestionRow(question, options, default)
        card.add_widget(row)
        return row.spinner

    def _build_result_area(self):
        self.result_holder = BoxLayout(orientation="vertical", size_hint_y=None, height=0)
        self.result_holder.bind(minimum_height=self.result_holder.setter("height"))
        self.page.add_widget(self.result_holder)

    def _build_footer(self):
        self.add_label(
            self.page,
            "UNOFFICIAL FAN-MADE TOOL  •  No game login required  •  No game files changed",
            size=10, color=MUTED, height=dp(30)
        )

    def generate_sensi(self, *_):
        scale = int(self.scale.text)
        style = self.style.text
        aim = self.aim.text
        drag = self.drag.text
        fingers = self.fingers.text
        ram = int(self.ram.text.split()[0])
        fps = int(self.fps.text.split()[0])

        # Starting-point model: gameplay preferences matter most.
        base_ratio = {
            "Rush / Fast drag": 0.86,
            "One-tap headshots": 0.80,
            "Balanced": 0.74,
            "Long-range / Sniper": 0.66,
        }.get(style, 0.74)

        # Small, conservative adjustments; these are suggestions, not device measurements.
        if aim == "Beginner":
            base_ratio -= 0.045
        elif aim == "Experienced":
            base_ratio += 0.025

        if drag == "Short drag":
            base_ratio -= 0.025
        elif drag == "Long drag":
            base_ratio += 0.025

        if fingers.startswith("3"):
            base_ratio += 0.008
        elif fingers.startswith("4") or fingers.startswith("5"):
            base_ratio += 0.015

        # On lower-memory / lower-frame-rate devices, use a slightly calmer starting point.
        if ram <= 3:
            base_ratio -= 0.015
        if fps <= 40:
            base_ratio -= 0.015

        base_ratio = max(0.48, min(0.94, base_ratio))
        general = round(scale * base_ratio)
        values = {
            "General": general,
            "Red Dot": round(general - scale * 0.035),
            "2X Scope": round(general - scale * 0.105),
            "4X Scope": round(general - scale * 0.19),
            "Sniper Scope": round(scale * 0.39 + (scale * 0.025 if style == "Long-range / Sniper" else 0)),
            "Free Look": round(scale * 0.62),
        }
        values = {k: max(0, min(scale, v)) for k, v in values.items()}

        self.result_holder.clear_widgets()
        result = NeonCard()
        result.add_widget(SectionTitle(text="03  /  YOUR CUSTOM SENSITIVITY"))
        device = self.device_name.text.strip() or "Your device"
        self.add_result_intro(result, device, style, scale)

        grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(176))
        for name, value in values.items():
            tile = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(2))
            with tile.canvas.before:
                Color(*get_color_from_hex(PANEL_2))
                tile.bg = RoundedRectangle(pos=tile.pos, size=tile.size, radius=[dp(10)])
            tile.bind(pos=lambda inst, val: setattr(inst.bg, "pos", val),
                      size=lambda inst, val: setattr(inst.bg, "size", val))
            tile.add_widget(Label(text=name.upper(), font_size=sp(10),
                                  color=get_color_from_hex(MUTED)))
            tile.add_widget(Label(text=str(value), font_size=sp(25), bold=True,
                                  color=get_color_from_hex(CYAN)))
            grid.add_widget(tile)
        result.add_widget(grid)

        note = Label(
            text="START HERE: Test these values in Training Ground. If aim goes above the target, lower General/Red Dot by 3–5 points. If drag feels slow, raise them by 3–5.",
            font_size=sp(11), color=get_color_from_hex(TEXT),
            halign="left", valign="middle", size_hint_y=None, height=dp(66)
        )
        note.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))
        result.add_widget(note)

        copy_hint = Label(
            text="Tip: Change one setting at a time and test a few rounds before adjusting again.",
            font_size=sp(10), color=get_color_from_hex(MUTED),
            halign="left", valign="middle", size_hint_y=None, height=dp(34)
        )
        copy_hint.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))
        result.add_widget(copy_hint)
        self.result_holder.add_widget(result)

        self.result_holder.height = result.height
        self.result_holder.opacity = 1

    def add_result_intro(self, parent, device, style, scale):
        intro = Label(
            text=f"{device}  •  {style}\nScale: 0–{scale}",
            font_size=sp(11), color=get_color_from_hex(MUTED),
            halign="left", valign="middle", size_hint_y=None, height=dp(38)
        )
        intro.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))
        parent.add_widget(intro)


if __name__ == "__main__":
    SensiApp().run()
