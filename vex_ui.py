
import asyncio
import json

import flet as ft
import flet_webview as fwv

from vex_search import ask_vex


def main(page: ft.Page):
    page.title = "VEX AI"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#000000"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_full_screen = True

    webview = None

    async def handle_console_message(e):
        message = e.message or ""
        prefix = "VEX_NATIVE_SEARCH:"

        if not message.startswith(prefix):
            return

        try:
            request = json.loads(message[len(prefix):])
            request_id = str(request.get("id", ""))
            query = str(request.get("query", "")).strip()

            if not query or len(query) > 500:
                return

            result = await asyncio.to_thread(ask_vex, query)

            response = {
                "id": request_id,
                "data": result
            }

        except Exception as error:
            response = {
                "id": request_id if "request_id" in locals() else "",
                "error": str(error)
            }

        javascript = (
            "window.dispatchEvent(new CustomEvent("
            "'vex-native-result',{detail:"
            + json.dumps(response, ensure_ascii=False)
            + "}));"
        )

        await webview.run_javascript(javascript)

    webview = fwv.WebView(
        url="https://eagleiam20-create.github.io/VEX-AI/",
        expand=True,
        on_console_message=handle_console_message,
        on_web_resource_error=lambda e: print(
            "WebView error:", e.data
        ),
    )

    page.add(
        ft.SafeArea(
            content=webview,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
