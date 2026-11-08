import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"
}


def search_web(query, limit=5):
    results = []

    try:
        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=limit):
                results.append({
                    "title": item.get("title", "Web result"),
                    "url": item.get("href", ""),
                    "snippet": item.get("body", "")
                })
    except Exception as error:
        print("Search error:", error)

    return results


def read_page(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup([
            "script", "style", "nav", "footer", "header"
        ]):
            tag.decompose()

        text = soup.get_text(" ", strip=True)

        return text[:7000]

    except Exception:
        return ""


def search_images(query, limit=4):
    images = []

    try:
        with DDGS() as ddgs:
            for item in ddgs.images(
                query,
                max_results=limit
            ):
                image_url = item.get("image")

                if image_url:
                    images.append({
                        "url": image_url,
                        "title": item.get("title", query)
                    })

    except Exception as error:
        print("Image error:", error)

    return images


def make_answer(query, results, pages):
    if not results:
        return "I couldn't find reliable web results for this question."

    source_text = []

    for result, page in zip(results, pages):
        content = page if page else result["snippet"]

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
        for sentence in (
            text.replace("!", ".")
            .replace("?", ".")
            .split(".")
        ):
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
    results = search_web(query)
    pages = [
        read_page(item["url"])
        for item in results
    ]

    answer = make_answer(query, results, pages)
    images = search_images(query)

    return {
        "answer": answer,
        "sources": results,
        "images": images
    }
