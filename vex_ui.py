```python
import flet as ft
import flet_webview as fwv


def main(page: ft.Page):
    page.title = "VEX AI"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#080808"
    page.theme_mode = ft.ThemeMode.DARK

    page.window_full_screen = True

    webview = fwv.WebView(
        url="https://eagleiam20-create.github.io/VEX-AI/",
        expand=True,
    )

    page.add(
        ft.SafeArea(
            content=webview,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
```
