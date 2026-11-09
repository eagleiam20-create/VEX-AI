# vex_ui.py
# VEX AI - Android WebView + Native Search Bridge

import asyncio
import json

import flet as ft
import flet_webview as fwv

from vex_search import (
    search_web,
    read_page,
    make_answer,
    search_images,
    search_videos,
)


APP_URL = "https://eagleiam20-create.github.io/VEX-AI/"


def normalize_results(results):
    output = []

    for item in results or []:
        url = item.get("url") or item.get("href") or ""

        if not url:
            continue

        output.append({
            "title": item.get("title") or "Web result",
            "url": url,
            "description": (
                item.get("description")
                or item.get("snippet")
                or ""
            ),
            "source": item.get("source") or ""
        })

    return output


def normalize_images(images):
    output = []

    for item in images or []:
        image_url = (
            item.get("image")
            or item.get("image_url")
            or item.get("url")
            or ""
        )

        if not image_url:
            continue

        output.append({
            "title": item.get("title") or "Related image",
            "image": image_url,
            "thumbnail": item.get("thumbnail") or image_url,
            "url": image_url,
            "page_url": item.get("page_url") or item.get("source") or ""
        })

    return output


def normalize_videos(videos):
    output = []

    for item in videos or []:
        url = (
            item.get("url")
            or item.get("href")
            or item.get("content")
            or ""
        )

        if not url:
            continue

        output.append({
            "title": item.get("title") or "Video result",
            "url": url,
            "description": item.get("description") or "",
            "thumbnail": item.get("thumbnail") or "",
            "embed_url": item.get("embed_url") or "",
            "duration": item.get("duration") or "",
            "publisher": item.get("publisher") or ""
        })

    return output


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

        safe_payload = json.dumps(
            payload,
            ensure_ascii=False
        )

        js = (
            "window.dispatchEvent(new CustomEvent("
            + json.dumps(event_name)
            + ", {detail:"
            + safe_payload
            + "}));"
        )

        await webview.run_javascript(js)

    async def send_progress(request_id, stage):
        await send_event(
            "vex-native-progress",
            {
                "id": request_id,
                "stage": stage
            }
        )

    async def send_result(payload):
        await send_event(
            "vex-native-result",
            payload
        )

    async def process_request(request_id, query, mode):
        if mode not in ("chat", "search", "images", "videos"):
            mode = "chat"

        if mode == "images":
            await send_progress(
                request_id,
                "Searching for images..."
            )

            images = await asyncio.to_thread(
                search_images,
                query,
                10
            )

            await send_result({
                "id": request_id,
                "data": {
                    "mode": "images",
                    "answer": "",
                    "results": [],
                    "images": normalize_images(images),
                    "videos": [],
                    "followups": []
                }
            })

            return

        if mode == "videos":
            await send_progress(
                request_id,
                "Searching for videos..."
            )

            videos = await asyncio.to_thread(
                search_videos,
                query,
                10
            )

            await send_result({
                "id": request_id,
                "data": {
                    "mode": "videos",
                    "answer": "",
                    "results": [],
                    "images": [],
                    "videos": normalize_videos(videos),
                    "followups": []
                }
            })

            return

        await send_progress(
            request_id,
            "Searching the web..."
        )

        results = await asyncio.to_thread(
            search_web,
            query,
            6
        )

        if not results:
            await send_result({
                "id": request_id,
                "data": {
                    "mode": "chat",
                    "answer": (
                        "VEX couldn't find web results for this question. "
                        "Please try different keywords."
                    ),
                    "results": [],
                    "images": [],
                    "videos": [],
                    "followups": []
                }
            })

            return

        await send_progress(
            request_id,
            "Reading relevant web pages..."
        )

        # Keep each page at the same index as its search result.
        pages = await asyncio.gather(*[
            asyncio.to_thread(
                read_page,
                item.get("url", "")
            )
            for item in results
        ])

        await send_progress(
            request_id,
            "Preparing an explanation..."
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
            6
        )

        videos = []

        if any(word in query.lower() for word in (
            "video", "videos", "watch",
            "trailer", "documentary", "tutorial"
        )):
            await send_progress(
                request_id,
                "Finding related videos..."
            )

            videos = await asyncio.to_thread(
                search_videos,
                query,
                6
            )

        await send_progress(
            request_id,
            "Preparing your answer..."
        )

        await send_result({
            "id": request_id,
            "data": {
                "mode": "chat",
                "answer": answer,
                "results": normalize_results(results),
                "images": normalize_images(images),
                "videos": normalize_videos(videos),
                "followups": []
            }
        })

    async def handle_console_message(e):
        message = e.message or ""
        prefix = "VEX_NATIVE_SEARCH:"

        if not message.startswith(prefix):
            return

        request_id = ""

        try:
            request = json.loads(
                message[len(prefix):]
            )

            request_id = str(
                request.get("id", "")
            )

            query = str(
                request.get("query", "")
            ).strip()

            mode = str(
                request.get("mode", "chat")
            ).lower().strip()

            if not request_id:
                raise ValueError("Missing request ID.")

            if not query or len(query) > 500:
                raise ValueError(
                    "Enter a question between 1 and 500 characters."
                )

            await send_progress(
                request_id,
                "Understanding your request..."
            )

            await process_request(
                request_id,
                query,
                mode
            )

        except Exception as error:
            print("VEX request error:", repr(error))

            if request_id:
                try:
                    await send_result({
                        "id": request_id,
                        "error": str(error)
                    })
                except Exception as send_error:
                    print(
                        "Could not send error to WebView:",
                        repr(send_error)
                    )

    webview = fwv.WebView(
        url=APP_URL,
        expand=True,
        on_console_message=handle_console_message,
        on_web_resource_error=lambda e: print(
            "WebView error:",
            e.data
        ),
    )

    page.add(
        ft.SafeArea(
            content=webview,
            expand=True
        )
    )


if __name__ == "__main__":
    ft.run(main)
