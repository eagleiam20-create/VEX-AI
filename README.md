# VEX Native Ads Flet extension

This extension renders a Google Mobile Ads Native small template inside a Flet app.

- It uses Google's official `google_mobile_ads` Flutter plugin.
- It uses `NativeTemplateStyle`, so no custom Android `MainActivity` or `NativeAdFactory` is required.
- The app's AdMob App ID is configured in the main VEX AI `pyproject.toml`.
- Test mode is enabled by default. Switch `test_mode=False` only after the test build has been verified and the app is ready for production ads.
