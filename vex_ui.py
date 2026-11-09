
import asyncio
import json

import flet as ft
import flet_webview as fwv

from vex_native_ads import VexNativeAd
from vex_search import (
    search_web,
    read_page,
    make_answer,
    search_images,
)


AD_UNIT_ID = "ca-app-pub-9779772194429691/6487151094"

# Keep test mode enabled during development.
AD_TEST_MODE = True


def main(page: ft.Page):
    page.title = "VEX AI"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#000000"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_full_screen = True

    webview = None

    async def dispatch(event_name, payload):
        if webview is None:
            return

        javascript = (
            "window.dispatchEvent(new CustomEvent("
            + json.dumps(event_name)
            + ",{detail:"
            + json.dumps(payload, ensure_ascii=False)
            + "}));"
        )

        await webview.run_javascript(javascript)

    async def handle_console_message(e):
        message = e.message or ""
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

            async def progress(stage):
                await dispatch(
                    "vex-native-progress",
                    {
                        "id": request_id,
                        "stage": stage,
                    },
                )

            await progress("Understanding your question...")

            await progress("Searching the web...")

            results = await asyncio.to_thread(
                search_web,
                query,
                5,
            )

            if not results:
                await dispatch(
                    "vex-native-result",
                    {
                        "id": request_id,
                        "data": {
                            "answer": (
                                "I couldn't find web results for this "
                                "question. Please try different keywords."
                            ),
                            "results": [],
                            "images": [],
                        },
                    },
                )
                return

            await progress("Reading relevant web pages...")

            pages = await asyncio.gather(
                *[
                    asyncio.to_thread(
                        read_page,
                        item.get("url", ""),
                    )
                    for item in results
                ]
            )

            await progress("Analyzing the collected information...")

            answer = await asyncio.to_thread(
                make_answer,
                query,
                results,
                pages,
            )

            await progress("Finding related images...")

            images = await asyncio.to_thread(
                search_images,
                query,
                4,
            )

            normalized_results = []

            for item in results:
                url = item.get("url") or item.get("href") or ""

                if url:
                    normalized_results.append(
                        {
                            "title": item.get("title") or "Web result",
                            "url": url,
                            "description": (
                                item.get("snippet")
                                or item.get("description")
                                or ""
                            ),
                            "source": "WEB RESULT",
                        }
                    )

            normalized_images = []

            for item in images:
                image_url = (
                    item.get("image")
                    or item.get("url")
                    or ""
                )

                if image_url:
                    normalized_images.append(
                        {
                            "title": item.get("title") or "Related image",
                            "image": image_url,
                            "url": image_url,
                        }
                    )

            await progress("Preparing your answer...")

            await dispatch(
                "vex-native-result",
                {
                    "id": request_id,
                    "data": {
                        "answer": (
                            answer
                            or "I found sources, but couldn't extract "
                            "a useful answer."
                        ),
                        "results": normalized_results,
                        "images": normalized_images,
                    },
                },
            )

        except Exception as error:
            print("VEX search error:", repr(error))

            if request_id:
                try:
                    await dispatch(
                        "vex-native-result",
                        {
                            "id": request_id,
                            "error": str(error),
                        },
                    )
                except Exception as dispatch_error:
                    print(
                        "VEX dispatch error:",
                        repr(dispatch_error),
                    )

    webview = fwv.WebView(
        url="https://eagleiam20-create.github.io/VEX-AI/",
        expand=True,
        on_console_message=handle_console_message,
        on_web_resource_error=lambda e: print(
            "WebView error:", e.data
        ),
    )

    ad_panel = ft.Container(
        content=VexNativeAd(
            unit_id=AD_UNIT_ID,
            test_mode=AD_TEST_MODE,
            height=100,
        ),
        bgcolor="#000000",
        padding=0,
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    webview,
                    ad_panel,
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
