# vex_search.py
# VEX AI - Web Search + Images + Videos + Answer Extraction

import re
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
}

STOPWORDS = {
    "what", "who", "when", "where", "why", "how", "is", "are",
    "was", "were", "the", "a", "an", "of", "in", "on", "at",
    "to", "for", "from", "with", "about", "and", "or", "but",
    "by", "tell", "me", "please", "explain", "give", "show",
    "find", "search", "information", "can", "could", "would",
    "should", "do", "does", "did", "it", "this", "that",
    "i", "you", "my", "your", "hai", "hain", "kya", "ka",
    "ki", "ke", "ko", "se", "mein", "aur", "kaun", "kab",
    "kahan", "kyun", "batao", "mujhe", "kaise"
}


def valid_url(value):
    if not isinstance(value, str):
        return False

    try:
        parsed = urlparse(value.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def clean_query(query):
    return re.sub(r"\s+", " ", str(query or "")).strip()


def is_image_request(query):
    q = clean_query(query).lower()

    keywords = [
        "generate image", "generating image",
        "create image", "make image",
        "create a picture", "make a picture",
        "draw", "show me image", "show image",
        "find image", "search image", "images of",
        "picture of", "photo of", "wallpaper",
        "image banao", "photo banao", "tasveer",
        "image dikhao", "photo dikhao",
        "tasveer dikhao", "picture dikhao",
        "ki image", "ki photo", "iski image",
        "iski photo", "ek image", "ek photo",
        "mujhe image", "mujhe photo"
    ]

    return any(word in q for word in keywords)


def is_video_request(query):
    q = clean_query(query).lower()

    keywords = [
        "video", "videos", "watch",
        "movie clip", "clips", "trailer",
        "documentary", "video dikhao",
        "video bhejo", "video search",
        "videos of", "video of",
        "youtube video", "tutorial video"
    ]

    return any(word in q for word in keywords)


def search_web(query, limit=5):
    query = clean_query(query)
    results = []

    if not query:
        return results

    try:
        with DDGS(timeout=20) as ddgs:
            raw_results = ddgs.text(
                query,
                max_results=limit
            )

            for item in raw_results:
                url = item.get("href") or item.get("url") or ""

                if not valid_url(url):
                    continue

                results.append({
                    "title": item.get("title") or "Web result",
                    "url": url,
                    "snippet": item.get("body") or item.get("description") or "",
                    "description": item.get("body") or item.get("description") or "",
                    "source": urlparse(url).netloc.replace("www.", "")
                })

    except Exception as error:
        print("Web search error:", repr(error))

    return results


def read_page(url):
    if not valid_url(url):
        return ""

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=12
        )

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()

        if content_type and "html" not in content_type:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup([
            "script", "style", "nav",
            "footer", "header", "noscript",
            "form", "iframe", "svg"
        ]):
            tag.decompose()

        text = soup.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text)

        return text[:10000]

    except Exception as error:
        print("Page read error:", repr(error))
        return ""


def search_images(query, limit=8):
    query = clean_query(query)
    images = []
    seen = set()

    if not query:
        return images

    try:
        with DDGS(timeout=20) as ddgs:
            raw_images = ddgs.images(
                query,
                max_results=limit,
                safesearch="moderate"
            )

            for item in raw_images:
                image_url = (
                    item.get("image")
                    or item.get("image_url")
                    or ""
                )

                thumbnail = (
                    item.get("thumbnail")
                    or item.get("thumbnail_url")
                    or image_url
                )

                source_url = (
                    item.get("url")
                    or item.get("source")
                    or ""
                )

                if not valid_url(image_url):
                    continue

                if image_url in seen:
                    continue

                seen.add(image_url)

                images.append({
                    "title": item.get("title") or "Related image",
                    "image": image_url,
                    "thumbnail": thumbnail if valid_url(thumbnail) else image_url,
                    "url": image_url,
                    "page_url": source_url if valid_url(source_url) else "",
                    "source": item.get("source") or ""
                })

    except Exception as error:
        print("Image search error:", repr(error))

    return images


def search_videos(query, limit=8):
    query = clean_query(query)
    videos = []
    seen = set()

    if not query:
        return videos

    try:
        with DDGS(timeout=25) as ddgs:
            raw_videos = ddgs.videos(
                query,
                max_results=limit,
                safesearch="moderate"
            )

            for item in raw_videos:
                # DDGS backends may expose the page URL under
                # different keys. Select the first valid URL.
                candidates = [
                    item.get("url"),
                    item.get("href"),
                    item.get("content"),
                    item.get("embed_url")
                ]

                video_url = next(
                    (value for value in candidates if valid_url(value)),
                    ""
                )

                if not video_url or video_url in seen:
                    continue

                seen.add(video_url)

                images = item.get("images") or {}

                thumbnail = ""

                if isinstance(images, dict):
                    thumbnail = (
                        images.get("large")
                        or images.get("medium")
                        or images.get("small")
                        or ""
                    )

                elif isinstance(images, list) and images:
                    first = images[0]

                    if isinstance(first, dict):
                        thumbnail = (
                            first.get("url")
                            or first.get("image")
                            or ""
                        )
                    elif isinstance(first, str):
                        thumbnail = first

                thumbnail = (
                    thumbnail
                    or item.get("thumbnail")
                    or item.get("image")
                    or ""
                )

                embed_url = item.get("embed_url") or ""

                videos.append({
                    "title": item.get("title") or "Video result",
                    "url": video_url,
                    "description": item.get("description") or "",
                    "thumbnail": thumbnail if valid_url(thumbnail) else "",
                    "embed_url": embed_url if valid_url(embed_url) else "",
                    "duration": item.get("duration") or "",
                    "publisher": item.get("publisher") or ""
                })

    except Exception as error:
        print("Video search error:", repr(error))

    return videos


def get_keywords(query):
    words = re.findall(
        r"[a-zA-Z0-9\u0900-\u097F]+",
        clean_query(query).lower()
    )

    return {
        word for word in words
        if len(word) > 2 and word not in STOPWORDS
    }


def make_answer(query, results, pages):
    if not results:
        return (
            "I couldn't find web results for this question. "
            "Try changing the wording or using different keywords."
        )

    source_text = []

    # Keep page/result indexes aligned.
    for index, result in enumerate(results):
        page = pages[index] if index < len(pages) else ""
        content = page or result.get("snippet", "")

        if content:
            source_text.append(content)

    if not source_text:
        snippets = [
            item.get("snippet", "")
            for item in results
            if item.get("snippet")
        ]

        if snippets:
            return "\n\n".join(snippets[:3])

        return "I found web pages, but couldn't read their content."

    query_words = get_keywords(query)
    candidates = []
    seen_sentences = set()

    for source in source_text:
        source = re.sub(r"\s+", " ", source)

        sentences = re.split(
            r"(?<=[.!?])\s+",
            source
        )

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence) < 45:
                continue

            sentence_words = set(
                re.findall(
                    r"[a-zA-Z0-9\u0900-\u097F]+",
                    sentence.lower()
                )
            )

            matches = query_words.intersection(sentence_words)

            if not matches:
                continue

            score = len(matches)

            # Prefer sentences with more query-topic coverage.
            if query_words:
                score += (
                    len(matches) / len(query_words)
                ) * 5

            # Avoid extremely long navigation-like text.
            if len(sentence) > 900:
                score -= 2

            key = sentence.lower()

            if key not in seen_sentences:
                candidates.append((score, sentence))
                seen_sentences.add(key)

    candidates.sort(
        key=lambda item: item[0],
        reverse=True
    )

    selected = []

    for score, sentence in candidates:
        if sentence not in selected:
            selected.append(sentence)

        if len(selected) >= 7:
            break

    if not selected:
        return source_text[0][:1800]

    return "\n\n".join(selected)


def ask_vex(query):
    query = clean_query(query)

    if not query:
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "images": [],
            "videos": []
        }

    if is_image_request(query):
        images = search_images(query, 8)

        return {
            "answer": (
                "Here are images related to your request."
                if images else
                "I couldn't find images for this request. Try another keyword."
            ),
            "sources": [],
            "images": images,
            "videos": []
        }

    if is_video_request(query):
        videos = search_videos(query, 8)

        return {
            "answer": (
                "Here are videos related to your request."
                if videos else
                "I couldn't find videos for this request. Try another keyword."
            ),
            "sources": [],
            "images": [],
            "videos": videos
        }

    results = search_web(query, 5)

    pages = [
        read_page(item.get("url", ""))
        for item in results
    ]

    answer = make_answer(query, results, pages)

    return {
        "answer": answer,
        "sources": results,
        "images": [],
        "videos": []
    }
