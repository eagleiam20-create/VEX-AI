
import asyncio
import flet as ft
from vex_search import ask_vex

BG = "#050505"
SIDEBAR = "#0B0B0B"
PANEL = "#121212"
WHITE = "#F5F5F5"
GREY = "#929292"
BORDER = "#292929"


def main(page: ft.Page):
    page.title = "VEX AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.padding = 0
    page.spacing = 0
    page.window_width = 1200
    page.window_height = 820
    page.window_min_width = 760
    page.window_min_height = 600

    chats = []
    busy = False

    messages = ft.ListView(
        expand=True,
        spacing=22,
        padding=25,
        auto_scroll=True
    )

    chat_list = ft.ListView(expand=True, spacing=5)

    status_text = ft.Text("", color=GREY, size=12)

    orb = ft.Container(
        width=13,
        height=13,
        bgcolor=WHITE,
        border_radius=50,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color="#BFFFFFFF"
        )
    )

    status_row = ft.Row(
        [orb, status_text],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
        visible=False
    )

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
        on_submit=None
    )

    def txt(value, size=14, color=WHITE):
        return ft.Text(
            str(value),
            size=size,
            color=color,
            selectable=True,
            font_family="Segoe UI"
        )

    def status(value, visible=True):
        status_text.value = value
        status_row.visible = visible
        page.update()

    def add_message(role, content):
        user = role == "user"

        bubble = ft.Container(
            content=txt(content, 15),
            bgcolor="#202020" if user else "transparent",
            padding=15 if user else 0,
            border_radius=18,
            width=700 if user else 850
        )

        messages.controls.append(
            ft.Row(
                [bubble],
                alignment=(
                    ft.MainAxisAlignment.END
                    if user else ft.MainAxisAlignment.START
                )
            )
        )

    def assistant_header():
        return ft.Row(
            [
                ft.Container(
                    content=ft.Text(
                        "V",
                        color="#000000",
                        weight=ft.FontWeight.BOLD
                    ),
                    width=28,
                    height=28,
                    bgcolor=WHITE,
                    border_radius=50,
                    alignment=ft.Alignment.CENTER
                ),
                txt("VEX", 14),
                txt("WEB INTELLIGENCE", 10, GREY)
            ],
            spacing=9
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
                            width=165,
                            height=120,
                            border_radius=12
                        ),
                        bgcolor=PANEL,
                        border=ft.Border.all(1, BORDER),
                        border_radius=12,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS
                    )
                )

        if controls:
            messages.controls.append(
                ft.Column(
                    [
                        txt("RELATED IMAGES", 11, GREY),
                        ft.Row(controls, wrap=True, spacing=10)
                    ],
                    spacing=10
                )
            )

    def add_sources(sources):
        if not sources:
            return

        cards = []

        for source in sources:
            cards.append(
                ft.Container(
                    content=ft.Column(
                        [
                            txt(source.get("title", "Web source"), 14),
                            txt(
                                source.get("snippet", "")[:220],
                                11,
                                GREY
                            ),
                            ft.Text(
                                source.get("url", ""),
                                size=11,
                                color="#C8C8C8",
                                selectable=True
                            )
                        ],
                        spacing=6
                    ),
                    bgcolor=PANEL,
                    border=ft.Border.all(1, BORDER),
                    border_radius=13,
                    padding=13,
                    width=850
                )
            )

        messages.controls.append(
            ft.Column(
                [
                    txt("SOURCES", 11, GREY),
                    *cards
                ],
                spacing=9
            )
        )

    def refresh_chats():
        chat_list.controls.clear()

        for index, chat in enumerate(chats):
            async def select_chat(e, i=index):
                messages.controls.clear()
                for role, content in chats[i]["messages"]:
                    add_message(role, content)
                page.update()

            chat_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CHAT_BUBBLE_OUTLINE,
                                color=GREY,
                                size=15
                            ),
                            ft.Text(
                                chat["title"],
                                color="#D0D0D0",
                                size=12,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                expand=True
                            )
                        ],
                        spacing=9
                    ),
                    padding=10,
                    border_radius=10,
                    on_click=select_chat
                )
            )

    async def show_home(e=None):
        messages.controls.clear()

        messages.controls.append(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "V",
                                color="#000000",
                                size=24,
                                weight=ft.FontWeight.BOLD
                            ),
                            width=60,
                            height=60,
                            bgcolor=WHITE,
                            border_radius=50,
                            alignment=ft.Alignment.CENTER,
                            shadow=ft.BoxShadow(
                                blur_radius=30,
                                color="#66FFFFFF"
                            )
                        ),
                        ft.Text(
                            "What can I help with?",
                            size=27,
                            color=WHITE
                        ),
                        txt(
                            "Ask anything. VEX will search the web for you.",
                            12,
                            GREY
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=14
                )
            )
        )

        status_row.visible = False
        page.update()

    async def show_profile(e=None):
        messages.controls.clear()
        messages.controls.append(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.ACCOUNT_CIRCLE,
                            size=65,
                            color=WHITE
                        ),
                        ft.Text(
                            "Your VEX Profile",
                            size=25,
                            color=WHITE
                        ),
                        txt("Guest account", 13, GREY),
                        ft.Container(
                            content=ft.Column(
                                [
                                    txt("ACCOUNT", 10, GREY),
                                    txt("VEX User", 16),
                                    ft.Divider(color=BORDER),
                                    txt("ASSISTANT", 10, GREY),
                                    txt("VEX AI", 15)
                                ],
                                spacing=8
                            ),
                            width=320,
                            padding=20,
                            bgcolor=PANEL,
                            border=ft.Border.all(1, BORDER),
                            border_radius=18
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12
                )
            )
        )
        page.update()

    async def show_settings(e=None):
        messages.controls.clear()
        messages.controls.append(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.SETTINGS_OUTLINED,
                            size=55,
                            color=WHITE
                        ),
                        ft.Text("Settings", size=25, color=WHITE),
                        ft.Container(
                            content=ft.Column(
                                [
                                    txt("Appearance", 14),
                                    txt("Pure Black", 12, GREY),
                                    ft.Divider(color=BORDER),
                                    txt("Search Engine", 14),
                                    txt("DuckDuckGo", 12, GREY),
                                    ft.Divider(color=BORDER),
                                    txt("Answer Mode", 14),
                                    txt("Web-based answers", 12, GREY)
                                ],
                                spacing=8
                            ),
                            width=350,
                            padding=20,
                            bgcolor=PANEL,
                            border=ft.Border.all(1, BORDER),
                            border_radius=18
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12
                )
            )
        )
        page.update()

    async def new_chat(e=None):
        await show_home()

    async def type_answer(target, answer):
        target.value = ""

        for i in range(0, len(answer), 5):
            target.value += answer[i:i + 5]
            page.update()
            await asyncio.sleep(0.015)

    async def send_question(e=None):
        nonlocal busy

        query = (question.value or "").strip()

        if not query or busy:
            return

        busy = True
        question.value = ""

        if not chats or chats[-1]["finished"]:
            chats.append({
                "title": query[:35],
                "messages": [],
                "finished": False
            })

        chat = chats[-1]
        chat["messages"].append(("user", query))

        messages.controls.clear()
        add_message("user", query)

        answer_text = ft.Text(
            "",
            size=15,
            color=WHITE,
            selectable=True,
            font_family="Segoe UI"
        )

        messages.controls.append(
            ft.Column(
                [assistant_header(), answer_text],
                spacing=12,
                width=850
            )
        )

        status("Searching the web...")
        refresh_chats()
        page.update()

        try:
            # Keep the original search engine unchanged.
            data = await asyncio.to_thread(ask_vex, query)

            answer = data.get(
                "answer",
                "I couldn't prepare an answer."
            )

            images = data.get("images", [])
            sources = data.get("sources", [])

            status("Analyzing search results...")
            await type_answer(answer_text, answer)

            chat["messages"].append(("assistant", answer))
            chat["finished"] = True

            if images:
                add_images(images)

            if sources:
                add_sources(sources)

        except Exception as error:
            answer_text.value = f"VEX error: {error}"

        finally:
            status("", False)
            busy = False
            page.update()

    async def send_click(e):
        await send_question()

    question.on_submit = send_question

    def nav_item(name, icon, handler):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, color=GREY, size=17),
                    ft.Text(name, color="#D0D0D0", size=13)
                ],
                spacing=11
            ),
            padding=11,
            border_radius=10,
            on_click=handler
        )

    sidebar = ft.Container(
        width=245,
        bgcolor=SIDEBAR,
        padding=13,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(
                                "V",
                                color="#000000",
                                weight=ft.FontWeight.BOLD
                            ),
                            width=30,
                            height=30,
                            bgcolor=WHITE,
                            border_radius=50,
                            alignment=ft.Alignment.CENTER
                        ),
                        ft.Text(
                            "VEX AI",
                            size=17,
                            color=WHITE,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Container(expand=True),
                        ft.Icon(ft.Icons.MENU_OPEN, color=GREY)
                    ],
                    spacing=9
                ),
                ft.Container(height=12),
                nav_item("New Chat", ft.Icons.ADD, new_chat),
                nav_item("Home", ft.Icons.HOME_OUTLINED, show_home),
                txt("YOUR CHATS", 10, "#686868"),
                chat_list,
                ft.Divider(color=BORDER),
                nav_item("Profile", ft.Icons.PERSON_OUTLINE, show_profile),
                nav_item("Settings", ft.Icons.SETTINGS_OUTLINED, show_settings),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.ACCOUNT_CIRCLE,
                                color=WHITE,
                                size=29
                            ),
                            ft.Column(
                                [
                                    txt("VEX User", 12),
                                    txt("Free workspace", 10, GREY)
                                ],
                                spacing=2
                            )
                        ],
                        spacing=9
                    ),
                    padding=10
                )
            ],
            spacing=5,
            expand=True
        )
    )

    composer = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        question,
                        ft.IconButton(
                            icon=ft.Icons.ARROW_UPWARD_ROUNDED,
                            icon_color="#000000",
                            bgcolor=WHITE,
                            icon_size=20,
                            tooltip="Send",
                            on_click=send_click
                        )
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END
                ),
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.SEARCH,
                            color=GREY,
                            size=13
                        ),
                        txt("Web search enabled", 10, GREY),
                        ft.Container(expand=True),
                        txt("VEX AI", 10, GREY)
                    ]
                )
            ],
            spacing=5
        ),
        bgcolor=PANEL,
        border=ft.Border.all(1, "#333333"),
        border_radius=23,
        padding=14,
        width=850
    )

    main_area = ft.Container(
        expand=True,
        bgcolor=BG,
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                "VEX AI",
                                color=WHITE,
                                size=13,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Container(expand=True),
                            txt("INDEPENDENT WEB INTELLIGENCE", 9, "#666666")
                        ]
                    ),
                    padding=18,
                    border=ft.Border.only(
                        bottom=ft.BorderSide(1, "#202020")
                    )
                ),
                messages,
                ft.Container(
                    content=ft.Column(
                        [
                            status_row,
                            composer,
                            ft.Text(
                                "VEX can make mistakes. Verify important information.",
                                color="#666666",
                                size=10,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=9
                    ),
                    padding=ft.Padding.only(
                        left=20,
                        right=20,
                        bottom=14,
                        top=7
                    )
                )
            ],
            spacing=0,
            expand=True
        )
    )

    page.add(
        ft.Row(
            [sidebar, main_area],
            spacing=0,
            expand=True
        )
    )

    # Initial screen
    page.run_task(show_home)
    refresh_chats()


ft.run(main)
