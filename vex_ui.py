
import asyncio
import json

import flet as ft
import flet_webview as fwv

from vex_search import search_web, read_page, make_answer, search_images


APP_URL = "https://eagleiam20-create.github.io/VEX-AI/"


def main(page: ft.Page):
    page.title = "VEX AI"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#000000"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_full_screen = True

    webview = None

    async def send_event(event_name, payload):
        if webview is None:
            return

        javascript = (
            "window.dispatchEvent(new CustomEvent("
            + json.dumps(event_name)
            + ", {detail:"
            + json.dumps(payload, ensure_ascii=False)
            + "}));"
        )

        await webview.run_javascript(javascript)

    async def send_progress(request_id, stage):
        await send_event(
            "vex-native-progress",
            {
                "id": request_id,
                "stage": stage
            }
        )

    async def send_result(payload):
        await send_event("vex-native-result", payload)

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
                raise ValueError("Missing request ID.")

            if not query or len(query) > 500:
                raise ValueError(
                    "Enter a question between 1 and 500 characters."
                )

            await send_progress(
                request_id,
                "Understanding your question..."
            )

            await send_progress(
                request_id,
                "Searching the web..."
            )

            results = await asyncio.to_thread(
                search_web,
                query,
                5
            )

            if not results:
                await send_result({
                    "id": request_id,
                    "data": {
                        "answer": (
                            "I couldn't find web results for this question. "
                            "Please try different keywords."
                        ),
                        "results": [],
                        "images": []
                    }
                })
                return

            await send_progress(
                request_id,
                "Reading relevant web pages..."
            )

            pages = await asyncio.gather(*[
                asyncio.to_thread(
                    read_page,
                    item.get("url", "")
                )
                for item in results
                if isinstance(item, dict)
                and item.get("url")
            ])

            await send_progress(
                request_id,
                "Analyzing the collected information..."
            )

            answer = await asyncio.to_thread(
                make_answer,
                query,
                results,
                pages
            )

            await send_progress(
                request_id,
                "Finding related images..."
            )

            images = await asyncio.to_thread(
                search_images,
                query,
                4
            )

            normalized_results = []

            for item in results:
                if not isinstance(item, dict):
                    continue

                url = item.get("url") or item.get("href") or ""

                if not url.startswith(("https://", "http://")):
                    continue

                normalized_results.append({
                    "title": item.get("title") or "Web result",
                    "url": url,
                    "description": (
                        item.get("snippet")
                        or item.get("description")
                        or ""
                    ),
                    "source": "WEB RESULT"
                })

            normalized_images = []

            for item in images:
                if not isinstance(item, dict):
                    continue

                image_url = (
                    item.get("image")
                    or item.get("url")
                    or ""
                )

                if not image_url.startswith(("https://", "http://")):
                    continue

                normalized_images.append({
                    "title": item.get("title") or "Related image",
                    "image": image_url,
                    "url": (
                        item.get("page_url")
                        or item.get("source_url")
                        or image_url
                    )
                })

            await send_progress(
                request_id,
                "Preparing your answer..."
            )

            await send_result({
                "id": request_id,
                "data": {
                    "answer": (
                        answer
                        or "I found sources, but couldn't extract a useful answer."
                    ),
                    "results": normalized_results,
                    "images": normalized_images
                }
            })

        except Exception as error:
            print("VEX search error:", repr(error))

            await send_result({
                "id": request_id,
                "error": str(error)
            })

    webview = fwv.WebView(
        url=APP_URL,
        expand=True,
        on_console_message=handle_console_message,
        on_web_resource_error=lambda e: print(
            "WebView error:",
            getattr(e, "data", e)
        )
    )

    page.add(
        ft.SafeArea(
            content=webview,
            expand=True
        )
    )


if __name__ == "__main__":
    ft.run(main)
