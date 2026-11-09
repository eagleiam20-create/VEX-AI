
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
}


def is_image_request(query):
    q = query.lower().strip()

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
        "mujhe image", "mujhe photo",
    ]

    return any(word in q for word in keywords)


def search_web(query, limit=5):
    results = []

    try:
        with DDGS() as ddgs:
            for item in ddgs.text(
                query,
                max_results=limit
            ):
                url = item.get("href", "")

                if url:
                    results.append({
                        "title": item.get("title", "Web result"),
                        "url": url,
                        "snippet": item.get("body", "")
                    })

    except Exception as error:
        print("Search error:", repr(error))

    return results


def read_page(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=12
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup([
            "script", "style", "nav",
            "footer", "header", "noscript"
        ]):
            tag.decompose()

        return soup.get_text(" ", strip=True)[:7000]

    except Exception as error:
        print("Page read error:", repr(error))
        return ""


def search_images(query, limit=4):
    images = []
    seen = set()

    try:
        with DDGS() as ddgs:
            for item in ddgs.images(
                query,
                max_results=limit
            ):
                image_url = item.get("image", "")
                source_url = item.get("url", "")

                if not image_url:
                    continue

                if image_url in seen:
                    continue

                seen.add(image_url)

                images.append({
                    "title": item.get("title", "Related image"),
                    "image": image_url,
                    "url": image_url,
                    "source": source_url,
                    "thumbnail": item.get("thumbnail", ""),
                })

    except Exception as error:
        print("Image search error:", repr(error))

    return images


def make_answer(query, results, pages):
    if not results:
        return "I couldn't find reliable web results for this question."

    source_text = []

    for result, page in zip(results, pages):
        content = page if page else result.get("snippet", "")

        if content:
            source_text.append(content)

    if not source_text:
        return "I found some pages, but couldn't read their content."

    query_words = {
        word.lower().strip(".,?!")
        for word in query.split()
        if len(word) > 2
    }

    candidates = []

    for text in source_text:
        sentences = (
            text.replace("!", ".")
            .replace("?", ".")
            .split(".")
        )

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence) < 45:
                continue

            words = set(sentence.lower().split())
            score = len(query_words.intersection(words))

            if score:
                candidates.append((score, sentence))

    candidates.sort(
        key=lambda x: x[0],
        reverse=True
    )

    selected = []
    seen = set()

    for _, sentence in candidates:
        key = sentence.lower()

        if key not in seen:
            selected.append(sentence)
            seen.add(key)

        if len(selected) >= 7:
            break

    if not selected:
        return source_text[0][:1800]

    return "\n\n".join(selected)


def ask_vex(query):
    if is_image_request(query):
        images = search_images(query, 4)

        return {
            "answer": (
                "Here are some images related to your request."
                if images else
                "I couldn't find images for this request. Try different keywords."
            ),
            "sources": [],
            "images": images
        }

    results = search_web(query, 5)

    pages = [
        read_page(item["url"])
        for item in results
    ]

    answer = make_answer(query, results, pages)

    return {
        "answer": answer,
        "sources": results,
        "images": []
    }
