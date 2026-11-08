import flet as ft


@ft.control("VexNativeAd")
class VexNativeAd(ft.LayoutControl):
    """Compact Google AdMob Native Advanced ad for Android."""

    unit_id: str = ""
    test_mode: bool = True
