# VEX AI AdMob integration notes

1. The app currently uses Google's official Native Ads test unit in `vex_ui.py`:
   `ca-app-pub-3940256099942544/2247696110`
2. The live Native Ad Unit ID is stored in `AD_UNIT_ID`, but `AD_TEST_MODE = True` means the live unit is NOT requested during development.
3. The AdMob App ID is configured in `pyproject.toml`.
4. Do not click test ads or production ads yourself.
5. After the test APK builds and the ad renders correctly, set `AD_TEST_MODE = False` to request the live ad unit. Real ad serving still depends on AdMob account/app review, policy compliance, consent requirements, and fill availability.
6. The ad is a persistent compact native slot at the bottom of the Android app. It is not recreated on every search, avoiding artificial repeated ad requests.
