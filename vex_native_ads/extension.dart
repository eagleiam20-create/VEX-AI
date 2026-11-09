import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'vex_native_ad_control.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    if (control.type == "VexNativeAd") {
      return VexNativeAdControl(
        key: key,
        control: control,
      );
    }

    return null;
  }
}
