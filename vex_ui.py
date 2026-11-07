import asyncio
import json

import flet as ft
import flet_webview as fwv

from vex_search import ask_vex


def normalize_result(raw):
    raw = raw if isinstance(raw, dict) else {}

    sources = raw.get("results") or raw.get("sources") or []
    results = []
    for item in sources:
        if not isinstance(item, dict):
            continue
        url = item.get("url") or item.get("href") or ""
        if not url.startswith(("https://", "http://")):
            continue
        results.append({
            "title": item.get("title") or "Web result",
            "url": url,
            "description": item.get("description") or item.get("snippet") or "",
            "source": item.get("source") or "WEB SOURCE",
        })

    raw_images = raw.get("images") or []
    images = []
    for item in raw_images:
        if not isinstance(item, dict):
            continue
        image_url = item.get("image") or item.get("url") or ""
        if not image_url.startswith(("https://", "http://")):
            continue
        # vex_search.py currently returns image URLs without a separate page URL.
        images.append({
            "title": item.get("title") or "Related image",
            "image": image_url,
            "url": item.get("page_url") or item.get("source_url") or image_url,
        })

    return {
        "answer": raw.get("answer") or "No information found.",
        "results": results,
        "images": images,
    }


def main(page: ft.Page):
    page.title = "VEX AI"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#000000"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_full_screen = True

    webview = None

    async def handle_console_message(e):
        message = getattr(e, "message", "") or ""
        prefix = "VEX_NATIVE_SEARCH:"
        if not message.startswith(prefix):
            return

        request_id = ""
        try:
            request = json.loads(message[len(prefix):])
            request_id = str(request.get("id", ""))
            query = str(request.get("query", "")).strip()

            if not request_id:
                return
            if not query or len(query) > 500:
                raise ValueError("Please enter a search query under 500 characters.")

            raw_result = await asyncio.to_thread(ask_vex, query)
            response = {
                "id": request_id,
                "data": normalize_result(raw_result),
            }

        except Exception as error:
            response = {
                "id": request_id,
                "error": str(error),
            }

        javascript = (
            "window.dispatchEvent(new CustomEvent("
            "'vex-native-result',{detail:"
            + json.dumps(response, ensure_ascii=False)
            + "}));"
        )

        if webview is not None:
            await webview.run_javascript(javascript)

    webview = fwv.WebView(
        url="https://eagleiam20-create.github.io/VEX-AI/",
        expand=True,
        on_console_message=handle_console_message,
        on_web_resource_error=lambda e: print("WebView error:", e.data),
    )

    page.add(
        ft.SafeArea(
            content=webview,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
