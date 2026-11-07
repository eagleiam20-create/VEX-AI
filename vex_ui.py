
import asyncio
import flet as ft
from vex_search import ask_vex

BG = "#050505"
PANEL = "#111111"
WHITE = "#F5F5F5"
GREY = "#929292"
BORDER = "#292929"


def main(page: ft.Page):
    page.title = "VEX AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.padding = 0
    page.spacing = 0

    chats = []
    busy = False
    active_chat = None
    current_view = "home"

    messages = ft.ListView(
        expand=True,
        spacing=20,
        padding=16,
        auto_scroll=True
    )

    status_text = ft.Text("", color=GREY, size=11)

    question = ft.TextField(
        hint_text="Message VEX...",
        multiline=True,
        min_lines=1,
        max_lines=5,
        expand=True,
        border=ft.InputBorder.NONE,
        bgcolor="transparent",
        color=WHITE,
        text_size=15,
        content_padding=10
    )

    def text(value, size=14, color=WHITE, **kwargs):
        return ft.Text(
            str(value),
            size=size,
            color=color,
            selectable=True,
            **kwargs
        )

    def logo(size=36):
        return ft.Container(
            content=ft.Text(
                "V",
                color="#000000",
                size=size * 0.48,
                weight=ft.FontWeight.BOLD
            ),
            width=size,
            height=size,
            bgcolor=WHITE,
            border_radius=100,
            alignment=ft.Alignment.CENTER
        )

    def set_status(value):
        status_text.value = value
        page.update()

    def show_welcome():
        messages.controls.clear()
        messages.controls.append(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    [
                        logo(65),
                        text("What can I help with?", 24),
                        text(
                            "Ask anything. VEX searches the web.",
                            12,
                            GREY
                        ),
                        ft.Container(height=12),
                        text("YOUR AI. YOUR WORLD.", 10, GREY)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=13
                )
            )
        )

    def add_message(role, content):
        is_user = role == "user"

        bubble = ft.Container(
            content=text(content, 15),
            bgcolor="#202020" if is_user else "transparent",
            padding=14 if is_user else 0,
            border_radius=18
        )

        if is_user:
            messages.controls.append(
                ft.Row(
                    [bubble],
                    alignment=ft.MainAxisAlignment.END
                )
            )
        else:
            messages.controls.append(
                ft.Column(
                    [
                        ft.Row(
                            [logo(27), text("VEX", 13)],
                            spacing=9
                        ),
                        bubble
                    ],
                    spacing=10
                )
            )

    def add_images(images):
        controls = []

        for item in images[:4]:
            url = item.get("url")
            if url:
                controls.append(
                    ft.Container(
                        content=ft.Image(
                            src=url,
                            width=145,
                            height=110,
                            fit=ft.ImageFit.COVER
                        ),
                        border_radius=12,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        bgcolor=PANEL
                    )
                )

        if controls:
            messages.controls.append(
                ft.Column(
                    [
                        text("RELATED IMAGES", 10, GREY),
                        ft.Row(
                            controls,
                            wrap=True,
                            spacing=8
                        )
                    ],
                    spacing=9
                )
            )

    def add_sources(sources):
        if not sources:
            return

        cards = []

        for source in sources[:8]:
            title = source.get("title", "Web source")
            snippet = source.get("snippet", "")
            url = source.get("url", "")

            content = [
                text(title, 13),
                text(snippet[:200], 11, GREY)
            ]

            if url:
                content.append(
                    ft.TextButton(
                        "Open source ↗",
                        on_click=lambda e, link=url: page.launch_url(link)
                    )
                )

            cards.append(
                ft.Container(
                    content=ft.Column(
                        content,
                        spacing=5
                    ),
                    bgcolor=PANEL,
                    border=ft.Border.all(1, BORDER),
                    border_radius=13,
                    padding=12
                )
            )

        messages.controls.append(
            ft.Column(
                [
                    text("SOURCES", 10, GREY),
                    *cards
                ],
                spacing=9
            )
        )

    async def type_answer(target, answer):
        target.value = ""
        for i in range(0, len(answer), 5):
            target.value += answer[i:i + 5]
            page.update()
            await asyncio.sleep(0.012)

    def refresh_chat_list():
        items = []

        for i, chat in enumerate(chats):
            items.append(
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.CHAT_BUBBLE_OUTLINE,
                        color=GREY,
                        size=18
                    ),
                    title=text(chat["title"], 13),
                    on_click=lambda e, index=i: open_chat(index)
                )
            )

        return items

    def open_chat(index):
        nonlocal active_chat, current_view

        active_chat = index
        current_view = "home"
        messages.controls.clear()

        for role, content in chats[index]["messages"]:
            add_message(role, content)

        render()

    def new_chat():
        nonlocal active_chat, current_view

        active_chat = None
        current_view = "home"
        show_welcome()
        render()

    def show_profile():
        nonlocal current_view
        current_view = "profile"
        render()

    def show_settings():
        nonlocal current_view
        current_view = "settings"
        render()

    def show_menu():
        nonlocal current_view
        current_view = "menu"
        render()

    def back_home():
        nonlocal current_view
        current_view = "home"
        render()

    def render():
        page.controls.clear()

        header = ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        ft.Icons.MENU,
                        icon_color=WHITE,
                        tooltip="Menu",
                        on_click=lambda e: show_menu()
                    ),
                    logo(30),
                    text("VEX AI", 16, WHITE),
                    ft.Container(expand=True),
                    ft.IconButton(
                        ft.Icons.ADD,
                        icon_color=WHITE,
                        tooltip="New chat",
                        on_click=lambda e: new_chat()
                    )
                ],
                spacing=5
            ),
            padding=ft.Padding.symmetric(
                horizontal=7,
                vertical=5
            ),
            border=ft.Border.only(
                bottom=ft.BorderSide(1, BORDER)
            )
        )

        composer = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            question,
                            ft.IconButton(
                                ft.Icons.ARROW_UPWARD_ROUNDED,
                                icon_color="#000000",
                                bgcolor=WHITE,
                                tooltip="Send",
                                on_click=send_question
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.END
                    ),
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.SEARCH,
                                size=12,
                                color=GREY
                            ),
                            text("Web search enabled", 10, GREY),
                            ft.Container(expand=True),
                            text("VEX AI", 10, GREY)
                        ]
                    )
                ],
                spacing=3
            ),
            bgcolor=PANEL,
            border=ft.Border.all(1, "#333333"),
            border_radius=22,
            padding=10
        )

        bottom = ft.Container(
            content=ft.Column(
                [
                    status_text,
                    composer,
                    text(
                        "VEX can make mistakes. Verify important information.",
                        9,
                        "#666666",
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=7
            ),
            padding=ft.Padding.symmetric(
                horizontal=12,
                vertical=8
            )
        )

        if current_view == "menu":
            body = ft.Column(
                [
                    ft.Row(
                        [
                            logo(38),
                            text("VEX AI", 18),
                            ft.Container(expand=True),
                            ft.IconButton(
                                ft.Icons.CLOSE,
                                icon_color=WHITE,
                                on_click=lambda e: back_home()
                            )
                        ]
                    ),
                    ft.Divider(color=BORDER),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ADD, color=WHITE),
                        title=text("New Chat"),
                        on_click=lambda e: new_chat()
                    ),
                    ft.ListTile(
                        leading=ft.Icon(
                            ft.Icons.HOME_OUTLINED,
                            color=WHITE
                        ),
                        title=text("Home"),
                        on_click=lambda e: back_home()
                    ),
                    ft.Divider(color=BORDER),
                    text("YOUR CHATS", 10, GREY),
                    ft.Column(
                        refresh_chat_list(),
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    ),
                    ft.Divider(color=BORDER),
                    ft.ListTile(
                        leading=ft.Icon(
                            ft.Icons.PERSON_OUTLINE,
                            color=WHITE
                        ),
                        title=text("Profile"),
                        on_click=lambda e: show_profile()
                    ),
                    ft.ListTile(
                        leading=ft.Icon(
                            ft.Icons.SETTINGS_OUTLINED,
                            color=WHITE
                        ),
                        title=text("Settings"),
                        on_click=lambda e: show_settings()
                    ),
                    text("VEX AI  •  WEB INTELLIGENCE", 10, GREY)
                ],
                expand=True,
                spacing=5
            )

            page.add(
                ft.Container(
                    content=body,
                    bgcolor=BG,
                    padding=15,
                    expand=True
                )
            )

        elif current_view == "profile":
            page.add(header)
            page.add(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.ACCOUNT_CIRCLE,
                                size=65,
                                color=WHITE
                            ),
                            text("Your VEX Profile", 24),
                            text("Guest account", 13, GREY),
                            text("VEX AI", 15)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15
                    ),
                    expand=True,
                    alignment=ft.Alignment.CENTER
                )
            )

        elif current_view == "settings":
            page.add(header)
            page.add(
                ft.Container(
                    content=ft.Column(
                        [
                            text("Settings", 25),
                            ft.Divider(color=BORDER),
                            text("Appearance", 15),
                            text("Pure Black", 12, GREY),
                            ft.Divider(color=BORDER),
                            text("Search Engine", 15),
                            text("DuckDuckGo", 12, GREY),
                            ft.Divider(color=BORDER),
                            text("Answer Mode", 15),
                            text("Web-based answers", 12, GREY)
                        ],
                        spacing=12
                    ),
                    padding=22,
                    expand=True
                )
            )

        else:
            page.add(header)
            page.add(messages)
            page.add(bottom)

        page.update()

    async def send_question(e=None):
        nonlocal busy, active_chat

        query = (question.value or "").strip()

        if not query or busy:
            return

        busy = True
        question.value = ""

        if active_chat is None:
            chats.append({
                "title": query[:35],
                "messages": [],
                "finished": False
            })
            active_chat = len(chats) - 1

        chat = chats[active_chat]
        chat["messages"].append(("user", query))

        messages.controls.clear()
        add_message("user", query)

        answer_text = ft.Text(
            "",
            size=15,
            color=WHITE,
            selectable=True
        )

        messages.controls.append(
            ft.Column(
                [
                    ft.Row(
                        [logo(27), text("VEX", 13)],
                        spacing=9
                    ),
                    answer_text
                ],
                spacing=10
            )
        )

        render()
        set_status("Searching the web...")

        try:
            data = await asyncio.to_thread(ask_vex, query)

            answer = data.get(
                "answer",
                "I couldn't prepare an answer."
            )

            set_status("Analyzing search results...")
            await type_answer(answer_text, answer)

            chat["messages"].append(("assistant", answer))
            chat["finished"] = True

            images = data.get("images", [])
            sources = data.get("sources", [])

            if images:
                add_images(images)

            if sources:
                add_sources(sources)

        except Exception as error:
            answer_text.value = f"VEX error: {error}"

        finally:
            busy = False
            set_status("")
            page.update()

    question.on_submit = send_question

    show_welcome()
    render()


ft.run(main)
