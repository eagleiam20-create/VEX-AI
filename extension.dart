import "package:flet/flet.dart";
import "package:flutter/widgets.dart";

import "vex_native_ad_control.dart";

class Extension extends FletExtension {
  @override
  Widget? createWidget(Control control) {
    if (control.type == "VexNativeAd") {
      return VexNativeAdControl(control: control);
    }
    return null;
  }
}
