
# ============================================================
# VEX AI - LIVE INTERNET SEARCH ENGINE
# Multi-website search + page reading + answer extraction
# Images + Videos + Sources
# ============================================================

import re
import ipaddress
import socket
import requests
import concurrent.futures

from bs4 import BeautifulSoup
from ddgs import DDGS
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
}

SEARCH_LIMIT = 12
PAGE_LIMIT = 8
PAGE_CHAR_LIMIT = 14000

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

# ============================================================
# BASIC HELPERS
# ============================================================

def clean_query(query):
    return re.sub(r"\s+", " ", str(query or "")).strip()

def valid_url(value):
    if not isinstance(value, str):
        return False

    try:
        parsed = urlparse(value.strip())

        if parsed.scheme not in ("http", "https"):
            return False

        if not parsed.hostname:
            return False

        host = parsed.hostname.lower()

        if host in ("localhost", "localhost.localdomain"):
            return False

        try:
            addresses = socket.getaddrinfo(
                host, None, type=socket.SOCK_STREAM
            )

            for address in addresses:
                ip = ipaddress.ip_address(address[4][0])

                if (
                    ip.is_private
                    or ip.is_loopback
                    or ip.is_link_local
                    or ip.is_reserved
                    or ip.is_unspecified
                ):
                    return False

        except socket.gaierror:
            return False

        return True

    except Exception:
        return False

def get_keywords(query):
    words = re.findall(
        r"[a-zA-Z0-9\u0900-\u097F]+",
        clean_query(query).lower()
    )

    return {
        word for word in words
        if len(word) > 2 and word not in STOPWORDS
    }

# ============================================================
# REQUEST TYPE DETECTION
# ============================================================

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

# ============================================================
# LIVE WEB SEARCH
# Searches the wider web, not just Wikipedia.
# ============================================================

def search_web(query, limit=SEARCH_LIMIT):
    query = clean_query(query)
    results = []
    seen = set()

    if not query:
        return results

    try:
        with DDGS(timeout=30) as ddgs:
            raw_results = ddgs.text(
                query,
                max_results=limit,
                safesearch="moderate"
            )

            for item in raw_results:
                url = item.get("href") or item.get("url") or ""

                if not valid_url(url):
                    continue

                if url in seen:
                    continue

                seen.add(url)

                domain = urlparse(url).netloc.lower()
                domain = domain.removeprefix("www.")

                results.append({
                    "title": item.get("title") or "Web result",
                    "url": url,
                    "snippet": (
                        item.get("body")
                        or item.get("description")
                        or ""
                    ),
                    "description": (
                        item.get("body")
                        or item.get("description")
                        or ""
                    ),
                    "source": domain
                })

    except Exception as error:
        print("Web search error:", repr(error))

    return results

# ============================================================
# READ WEBSITE CONTENT
# ============================================================

def read_page(url):
    if not valid_url(url):
        return ""

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True,
            stream=True
        )

        response.raise_for_status()

        # Check redirect destination too.
        if not valid_url(response.url):
            response.close()
            return ""

        content_type = response.headers.get(
            "Content-Type", ""
        ).lower()

        if "html" not in content_type:
            response.close()
            return ""

        content_length = response.headers.get("Content-Length")

        if content_length and int(content_length) > 3_000_000:
            response.close()
            return ""

        content = response.raw.read(3_000_000 + 1)
        response.close()

        if len(content) > 3_000_000:
            return ""

        soup = BeautifulSoup(content, "html.parser")

        for tag in soup([
            "script", "style", "nav",
            "footer", "header", "noscript",
            "form", "iframe", "svg",
            "button", "aside"
        ]):
            tag.decompose()

        # Prefer main article content where available.
        main = (
            soup.find("article")
            or soup.find("main")
            or soup.body
            or soup
        )

        text = main.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text)

        return text[:PAGE_CHAR_LIMIT]

    except Exception as error:
        print("Page read error:", repr(error))
        return ""

# ============================================================
# READ MULTIPLE WEBSITES AT THE SAME TIME
# ============================================================

def read_multiple_pages(results):
    selected = results[:PAGE_LIMIT]

    pages = [""] * len(selected)

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=5
    ) as executor:

        futures = {
            executor.submit(
                read_page,
                item.get("url", "")
            ): index
            for index, item in enumerate(selected)
        }

        for future in concurrent.futures.as_completed(futures):
            index = futures[future]

            try:
                pages[index] = future.result()
            except Exception:
                pages[index] = ""

    return pages

# ============================================================
# IMAGE SEARCH
# ============================================================

def search_images(query, limit=8):
    query = clean_query(query)
    images = []
    seen = set()

    if not query:
        return images

    try:
        with DDGS(timeout=25) as ddgs:
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
                    "thumbnail": (
                        thumbnail
                        if valid_url(thumbnail)
                        else image_url
                    ),
                    "url": image_url,
                    "page_url": (
                        source_url
                        if valid_url(source_url)
                        else ""
                    ),
                    "source": item.get("source") or ""
                })

    except Exception as error:
        print("Image search error:", repr(error))

    return images

# ============================================================
# VIDEO SEARCH
# ============================================================

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
                candidates = [
                    item.get("url"),
                    item.get("href"),
                    item.get("content"),
                    item.get("embed_url")
                ]

                video_url = next(
                    (
                        value for value in candidates
                        if valid_url(value)
                    ),
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
                    "thumbnail": (
                        thumbnail
                        if valid_url(thumbnail)
                        else ""
                    ),
                    "embed_url": (
                        embed_url
                        if valid_url(embed_url)
                        else ""
                    ),
                    "duration": item.get("duration") or "",
                    "publisher": item.get("publisher") or ""
                })

    except Exception as error:
        print("Video search error:", repr(error))

    return videos

# ============================================================
# ANSWER EXTRACTION FROM MULTIPLE SOURCES
# This is extractive synthesis, not an LLM.
# ============================================================

def make_answer(query, results, pages):
    if not results:
        return (
            "VEX couldn't retrieve web results right now. "
            "Please try again with different keywords."
        )

    source_text = []

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
            return "\n\n".join(snippets[:5])

        return (
            "I found some websites, but their content "
            "could not be retrieved."
        )

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

            if query_words:
                score += (
                    len(matches) / len(query_words)
                ) * 5

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

        if len(selected) >= 8:
            break

    if not selected:
        return source_text[0][:2500]

    return "\n\n".join(selected)

# ============================================================
# MAIN VEX RESPONSE FUNCTION
# ============================================================

def ask_vex(query):
    query = clean_query(query)

    if not query:
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "results": [],
            "images": [],
            "videos": [],
            "followups": []
        }

    # IMAGE ONLY MODE
    if is_image_request(query):
        images = search_images(query, 8)

        return {
            "answer": (
                "Here are images related to your request."
                if images else
                "I couldn't find images for this request."
            ),
            "sources": [],
            "results": [],
            "images": images,
            "videos": [],
            "followups": []
        }

    # VIDEO ONLY MODE
    if is_video_request(query):
        videos = search_videos(query, 8)

        return {
            "answer": (
                "Here are videos related to your request."
                if videos else
                "I couldn't find videos for this request."
            ),
            "sources": [],
            "results": [],
            "images": [],
            "videos": videos,
            "followups": []
        }

    # GENERAL INTERNET SEARCH
    results = search_web(query, SEARCH_LIMIT)

    if not results:
        return {
            "answer": (
                "VEX couldn't connect to the web search service. "
                "Please try again in a moment."
            ),
            "sources": [],
            "results": [],
            "images": [],
            "videos": [],
            "followups": []
        }

    # Read several different websites in parallel.
    pages = read_multiple_pages(results)

    # Extract relevant information from those pages.
    answer = make_answer(
        query,
        results[:PAGE_LIMIT],
        pages
    )

    return {
        "answer": answer,
        "sources": results,
        "results": results,
        "images": [],
        "videos": [],
        "followups": []
    }

# ============================================================
# QUICK TEST
# Run this file directly to test web access.
# ============================================================

if __name__ == "__main__":
    question = input("Ask VEX: ")

    response = ask_vex(question)

    print("\n========== VEX AI ==========\n")
    print(response["answer"])

    print("\n========== SOURCES ==========\n")

    for source in response["sources"]:
        print(source["title"])
        print(source["url"])
        print()
