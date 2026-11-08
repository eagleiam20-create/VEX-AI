import "package:flet/flet.dart";
import "package:flutter/widgets.dart";
import "package:material_ui/material_ui.dart";
import "package:google_mobile_ads/google_mobile_ads.dart";

const String _androidNativeTestAdUnitId =
    "ca-app-pub-3940256099942544/2247696110";

class VexNativeAdControl extends StatefulWidget {
  final Control control;

  const VexNativeAdControl({
    super.key,
    required this.control,
  });

  @override
  State<VexNativeAdControl> createState() => _VexNativeAdControlState();
}

class _VexNativeAdControlState extends State<VexNativeAdControl> {
  NativeAd? _nativeAd;
  bool _isLoaded = false;
  bool _hasFailed = false;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadNativeAd();
  }

  Future<void> _loadNativeAd() async {
    if (_isLoading) return;
    _isLoading = true;

    final String liveUnitId =
        widget.control.getString("unitId", "") ?? "";
    final bool testMode =
        widget.control.getBool("testMode", true) ?? true;
    final String adUnitId =
        testMode ? _androidNativeTestAdUnitId : liveUnitId;

    if (adUnitId.isEmpty) {
      if (mounted) {
        setState(() => _hasFailed = true);
      }
      return;
    }

    try {
      await MobileAds.instance.initialize();

      if (!mounted) return;

      final ad = NativeAd(
        adUnitId: adUnitId,
        request: const AdRequest(),
        nativeTemplateStyle: NativeTemplateStyle(
          templateType: TemplateType.small,
          mainBackgroundColor: const Color(0xFF101010),
          cornerRadius: 10,
          primaryTextStyle: NativeTemplateTextStyle(
            textColor: const Color(0xFFF5F5F5),
            style: NativeTemplateFontStyle.bold,
            size: 14,
          ),
          secondaryTextStyle: NativeTemplateTextStyle(
            textColor: const Color(0xFFBDBDBD),
            size: 11,
          ),
          tertiaryTextStyle: NativeTemplateTextStyle(
            textColor: const Color(0xFF888888),
            size: 10,
          ),
          callToActionTextStyle: NativeTemplateTextStyle(
            textColor: const Color(0xFF000000),
            backgroundColor: const Color(0xFFFFFFFF),
            style: NativeTemplateFontStyle.bold,
            size: 11,
          ),
        ),
        listener: NativeAdListener(
          onAdLoaded: (Ad loadedAd) {
            if (!mounted) {
              loadedAd.dispose();
              return;
            }
            setState(() => _isLoaded = true);
          },
          onAdFailedToLoad: (Ad failedAd, LoadAdError error) {
            failedAd.dispose();
            if (mounted) {
              setState(() => _hasFailed = true);
            }
          },
        ),
      );

      _nativeAd = ad;
      ad.load();
    } catch (_) {
      if (mounted) {
        setState(() => _hasFailed = true);
      }
    }
  }

  @override
  void dispose() {
    _nativeAd?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final double adHeight =
        widget.control.getDouble("height", 100.0) ?? 100.0;

    Widget content;

    if (_isLoaded && _nativeAd != null) {
      content = SizedBox(
        width: double.infinity,
        height: adHeight,
        child: AdWidget(ad: _nativeAd!),
      );
    } else if (_hasFailed) {
      content = const SizedBox.shrink();
    } else {
      content = SizedBox(
        width: double.infinity,
        height: adHeight,
        child: const Center(
          child: CircularProgressIndicator(
            strokeWidth: 1.5,
            color: Color(0xFF777777),
          ),
        ),
      );
    }

    return LayoutControl(
      control: widget.control,
      child: content,
    );
  }
}
