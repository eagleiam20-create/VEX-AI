import flet as ft
import threading
from vex_search import ask_vex


BG = "#080808"
PANEL = "#111111"
WHITE = "#F5F5F5"
GREY = "#999999"
ACCENT = "#B9A0FF"


def main(page: ft.Page):
    page.title = "VEX AI V13"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.padding = 0
    page.window_width = 1100
    page.window_height = 800

    history = ft.ListView(
        expand=True,
        spacing=22,
        padding=25,
        auto_scroll=True
    )

    question = ft.TextField(
        hint_text="Ask VEX anything...",
        multiline=True,
        min_lines=1,
        max_lines=4,
        expand=True,
        border_color="transparent",
        bgcolor="transparent",
        color=WHITE,
        text_size=16,
        on_submit=lambda e: send_question()
    )

    def add_text(text, size=15, color=WHITE, selectable=True):
        return ft.Text(
            text,
            size=size,
            color=color,
            selectable=selectable,
            font_family="Bahnschrift",
        )

    def send_question():
        query = question.value.strip()

        if not query:
            return

        question.value = ""

        history.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=add_text(query, 15),
                        bgcolor="#202020",
                        padding=15,
                        border_radius=18,
                        width=650
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            )
        )

        loading = add_text("VEX is searching the web...", 14, GREY)
        history.controls.append(loading)
        page.update()

        def work():
            try:
                data = ask_vex(query)
                answer = data["answer"]
                sources = data["sources"]
                images = data["images"]

                def display():
                    if loading in history.controls:
                        history.controls.remove(loading)

                    history.controls.append(
                        ft.Column(
                            [
                                ft.Row([
                                    ft.Text(
                                        "VEX",
                                        color=ACCENT,
                                        weight=ft.FontWeight.BOLD,
                                        size=17
                                    )
                                ]),
                                add_text(answer, 16),
                            ],
                            spacing=12,
                            width=800
                        )
                    )

                    if images:
                        history.controls.append(
                            add_text("RELATED IMAGES", 12, GREY)
                        )

                        image_controls = []

                        for item in images[:4]:
                            image_controls.append(
                                ft.Image(
                                    src=item["url"],
                                    width=175,
                                    height=125,
                                    border_radius=12,
                                    error_content=ft.Text("Image unavailable")
                                )
                            )

                        history.controls.append(
                            ft.Row(
                                image_controls,
                                wrap=True,
                                spacing=10
                            )
                        )

                    if sources:
                        history.controls.append(
                            add_text("SOURCES", 12, GREY)
                        )

                        for source in sources:
                            history.controls.append(
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            add_text(source["title"], 14),
                                            add_text(
                                                source["snippet"][:220],
                                                12,
                                                GREY
                                            ),
                                            ft.Text(
                                                source["url"],
                                                size=12,
                                                color=ACCENT,
                                                selectable=True
                                            )
                                        ],
                                        spacing=5
                                    ),
                                    bgcolor=PANEL,
                                    padding=13,
                                    border_radius=12
                                )
                            )

                    page.update()

                page.run_thread(display)

            except Exception as error:
                def show_error():
                    if loading in history.controls:
                        history.controls.remove(loading)

                    history.controls.append(
                        add_text(f"Error: {error}", 14, "#FF7777")
                    )
                    page.update()

                page.run_thread(show_error)

        threading.Thread(target=work, daemon=True).start()

    def send_click(e):
        send_question()

    header = ft.Container(
        content=ft.Row(
            [
                ft.Text(
                    "VEX",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color=WHITE,
                    font_family="Bahnschrift"
                ),
                ft.Text(
                    "AI  /  V13",
                    size=12,
                    color=ACCENT
                ),
                ft.Container(expand=True),
                ft.Text("WEB INTELLIGENCE", size=11, color=GREY)
            ]
        ),
        padding=20,
        border=ft.Border(
            bottom=ft.BorderSide(1, "#252525")
        )
    )

    composer = ft.Container(
        content=ft.Row(
            [
                question,
                ft.IconButton(
                    icon=ft.Icons.ARROW_UPWARD_ROUNDED,
                    icon_color="#080808",
                    bgcolor=ACCENT,
                    on_click=send_click
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.END
        ),
        bgcolor=PANEL,
        padding=12,
        border_radius=22,
        border=ft.Border.all(1, "#292929"),
    )

    page.add(
        ft.Column(
            [
                header,
                history,
                ft.Container(
                    content=ft.Column(
                        [
                            composer,
                            ft.Text(
                                "VEX AI can make mistakes. Verify important information.",
                                size=10,
                                color=GREY,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        spacing=8
                    ),
                    padding=ft.Padding.only(
                        left=20, right=20, bottom=15
                    )
                )
            ],
            expand=True,
            spacing=0
        )
    )


ft.run(main)

