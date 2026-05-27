# WebKit Quirks 配置（ItBrowser）

通过 ItBrowser 配置 JSON 里的 `quirks` 字段，可在运行期强制开启/关闭 WebKit 的「站点特定 quirk」（`SiteSpecificQuirk`），无需再改 `Quirks.cpp` 源码。

## 原理

- `quirks` 是一个**通用 map**：key = `WebCore::QuirksData::SiteSpecificQuirk` 的枚举名（字符串），value = `bool`。
  - `true`  → 强制开启该 quirk
  - `false` → 强制关闭该 quirk
  - 未列出的 key → 保持 WebKit 默认（按站点判定）
- 配置随 `--itbrowser-config`(base64 JSON) 进入 UIProcess，再经 IPC(`itBrowserConfig`) 传到 **WebProcess**；`Quirks` 运行在 WebProcess。
- 应用时机（两个全局钩子，注册在 WebProcess 的 `WebKit::ItBrowser::registerQuirksHooks()`）：
  - `onInitQuirks`：在任何站点 handler **之前**执行（设定基线）。
  - `onInitQuirksAfterDocumentHandler`：在站点 handler **之后**执行（最终覆盖，**配置优先于站点判定**）。
- 这些 quirk 都是布尔开关（底层 `QuirksData::setQuirkState`），所以**全部用 `true/false`**，没有需要对象/数值的特殊配置项。

## 注意事项

- **依赖 `NeedsSiteSpecificQuirks`**：大多数 quirk 的 getter（如 `needsCustomUserAgentData()`）开头会先判 `settings().needsSiteSpecificQuirks()`。WebKit2 默认 `true`，所以通常无需额外开启；若被关闭则这些 quirk 一律返回 false。
- **平台门控**：`SiteSpecificQuirk` 里很多枚举值用 `#if PLATFORM(IOS_FAMILY)/MAC/VISION` 或 `#if ENABLE(...)` 包裹。Windows 构建里被编译掉的枚举值**不可设置**；映射表已按 `QuirksData.h` 同样的门控生成。
- **未知 key 静默忽略**：写错枚举名或设置当前平台不存在的 quirk，不报错、不生效。

## 指纹相关（重点）

```jsonc
{
  // ……（userAgent / platform / canvas / webgl 等其它 ItBrowser 配置）

  "quirks": {
    // 让 navigator.userAgentData(Client Hints) 走自定义 UA 数据，
    // 而不是 WebKit 内置值——指纹浏览器伪装 UA 时通常要开。
    "NeedsCustomUserAgentData": true,

    // 配套：navigator.userAgentData 相关的 quirk。
    "NeedsNavigatorUserAgentDataQuirk": true
  }
}
```

## 完整可设置列表（参考）

下面是 `quirks` 支持的所有 key（jsonc，注释标注门控）。在 Windows 构建里，`PLATFORM(IOS_FAMILY)/MAC/IOS/VISION` 门控的项**不可用**（被编译掉）；`ENABLE(...)` 门控的项取决于本次构建是否开启该特性。

```jsonc
{
  "quirks": {
    // ===== 无条件可用（任意平台/构建都在） =====
    "EnsureCaptionVisibilityInFullscreenAndPictureInPicture": false,
    "HasBrokenEncryptedMediaAPISupportQuirk": false,
    "ImplicitMuteWhenVolumeSetToZero": false,
    "InputMethodUsesCorrectKeyEventOrder": false,
    "MaybeBypassBackForwardCache": false,
    "NeedsBodyScrollbarWidthNoneDisabledQuirk": false,
    "NeedsCanPlayAfterSeekedQuirk": false,
    "NeedsChromeMediaControlsPseudoElementQuirk": false,
    "NeedsCustomUserAgentData": false,              // ★ 指纹相关
    "NeedsFacebookRemoveNotSupportedQuirk": false,
    "NeedsGeforcenowWarningDisplayNoneQuirk": false,
    "NeedsHotelsAnimationQuirk": false,
    "NeedsMediaRewriteRangeRequestQuirk": false,
    "NeedsMozillaFileTypeForDataTransferQuirk": false,
    "NeedsNavigatorUserAgentDataQuirk": false,      // ★ 指纹相关
    "NeedsNowPlayingFullscreenSwapQuirk": false,
    "NeedsResettingTransitionCancelsRunningTransitionQuirk": false,
    "NeedsReuseLiveRangeForSelectionUpdateQuirk": false,
    "NeedsScrollbarWidthThinDisabledQuirk": false,
    "NeedsSeekingSupportDisabledQuirk": false,
    "NeedsSuppressPostLayoutBoundaryEventsQuirk": false,
    "NeedsTikTokOverflowingContentQuirk": false,
    "NeedsVP9FullRangeFlagQuirk": false,
    "NeedsVideoShouldMaintainAspectRatioQuirk": false,
    "NeedsWebKitMediaTextTrackDisplayQuirk": false,
    "NeedsZeroMaxTouchPointsQuirk": false,          // 触摸点数=0，桌面端指纹可参考
    "ReturnNullPictureInPictureElementDuringFullscreenChangeQuirk": false,
    "ShouldAutoplayWebAudioForArbitraryUserGestureQuirk": false,
    "ShouldAvoidResizingWhenInputViewBoundsChangeQuirk": false,
    "ShouldAvoidScrollingWhenFocusedContentIsVisibleQuirk": false,
    "ShouldBlockFetchWithNewlineAndLessThan": false,
    "ShouldBypassAsyncScriptDeferring": false,
    "ShouldDelayReloadWhenRegisteringServiceWorker": false,
    "ShouldDisableDataURLPaddingValidation": false,
    "ShouldDisableDOMAudioSession": false,
    "ShouldDisableFetchMetadata": false,
    "ShouldDisableLazyIframeLoadingQuirk": false,
    "ShouldDisablePushStateFilePathRestrictions": false,
    "ShouldDisableWritingSuggestionsByDefaultQuirk": false,
    "ShouldDispatchPlayPauseEventsOnResume": false,
    "ShouldDispatchSyntheticMouseEventsWhenModifyingSelectionQuirk": false,
    "ShouldDispatchSimulatedMouseEventsAssumeDefaultPreventedQuirk": false,
    "ShouldEnableFontLoadingAPIQuirk": false,
    "ShouldEnterNativeFullscreenWhenCallingElementRequestFullscreen": false,
    "ShouldExposeShowModalDialog": false,
    "ShouldIgnorePlaysInlineRequirementQuirk": false,
    "ShouldLayOutAtMinimumWindowWidthWhenIgnoringScalingConstraintsQuirk": false,
    "ShouldPreventOrientationMediaQueryFromEvaluatingToLandscapeQuirk": false,
    "ShouldUseLegacySelectPopoverDismissalBehaviorInDataActivationQuirk": false,
    "ShouldUnloadHeavyFrames": false,
    "ShouldAvoidStartingSelectionOnMouseDownOverPointerCursor": false,
    "ShouldAllowNotificationPermissionWithoutUserGesture": false,
    "NeedsInstagramResizingReelsQuirk": false,

    // ===== ENABLE(...) 特性门控（取决于本次构建） =====
    "BlocksEnteringStandardFullscreenFromPictureInPictureQuirk": false, // FULLSCREEN_API && VIDEO_PRESENTATION_MODE
    "BlocksReturnToFullscreenFromPictureInPictureQuirk": false,         // FULLSCREEN_API && VIDEO_PRESENTATION_MODE
    "RequiresUserGestureToLoadInPictureInPictureQuirk": false,          // VIDEO_PRESENTATION_MODE
    "RequiresUserGestureToPauseInPictureInPictureQuirk": false,         // VIDEO_PRESENTATION_MODE
    "ShouldDisableEndFullscreenEventWhenEnteringPictureInPictureFromFullscreenQuirk": false, // VIDEO_PRESENTATION_MODE
    "ShouldDisableImageCaptureQuirk": false,                            // MEDIA_STREAM
    "ShouldEnableCameraAndMicrophonePermissionStateQuirk": false,       // MEDIA_STREAM
    "ShouldEnableEnumerateDeviceQuirk": false,                          // MEDIA_STREAM
    "ShouldEnableFacebookFlagQuirk": false,                             // MEDIA_STREAM
    "ShouldEnableLegacyGetUserMediaQuirk": false,                       // MEDIA_STREAM
    "ShouldEnableRemoteTrackLabelQuirk": false,                         // MEDIA_STREAM
    "ShouldEnableSpeakerSelectionPermissionsPolicyQuirk": false,        // MEDIA_STREAM
    "ShouldEnableRTCEncodedStreamsQuirk": false,                        // WEB_RTC
    "ShouldDisableAdSkippingInPip": false,                              // HAVE(PIP_SKIP_PREROLL)
    "ShouldFlipScreenDimensionsQuirk": false,                          // FLIP_SCREEN_DIMENSIONS_QUIRKS（屏幕宽高翻转，指纹可参考）
    "ShouldIgnoreTextAutoSizingQuirk": false,                          // TEXT_AUTOSIZING
    "ShouldIgnoreViewportArgumentsToAvoidExcessiveZoomQuirk": false,    // META_VIEWPORT
    "ShouldIgnoreViewportArgumentsToAvoidEnlargedViewQuirk": false,     // META_VIEWPORT
    "ShouldDispatchPointerOutAndLeaveAfterHandlingSyntheticClick": false, // TOUCH_EVENTS
    "ShouldPreventDispatchOfTouchEventQuirk": false,                    // TOUCH_EVENTS
    "ShouldReportDocumentAsVisibleIfActivePIPQuirk": false,            // PICTURE_IN_PICTURE_API
    "ShouldSupportHoverMediaQueriesQuirk": false,                      // DESKTOP_CONTENT_MODE_QUIRKS
    "ShouldTreatAddingMouseOutEventListenerAsContentChange": false,    // CONTENT_CHANGE_OBSERVER

    // ===== 平台门控（Windows 构建不可用，列出仅供参考） =====
    // PLATFORM(IOS) || PLATFORM(VISION)
    "AllowLayeredFullscreenVideos": false,
    "ShouldSilenceMediaQueryListChangeEvents": false,
    "ShouldSilenceResizeObservers": false,
    // PLATFORM(MAC)
    "IsNeverRichlyEditableForTouchBarQuirk": false,
    "IsTouchBarUpdateSuppressedForHiddenContentEditableQuirk": false,
    "NeedsFormControlToBeMouseFocusableQuirk": false,
    "NeedsPrimeVideoUserSelectNoneQuirk": false,
    "NeedsZomatoEmailLoginLabelQuirk": false,
    // PLATFORM(IOS_FAMILY)
    "MayNeedToIgnoreContentObservation": false,
    "NeedsClaudeSidebarViewportUnitQuirk": false,
    "NeedsDeferKeyDownAndKeyPressTimersUntilNextEditingCommandQuirk": false,
    "NeedsFullscreenDisplayNoneQuirk": false,
    "NeedsFullscreenObjectFitQuirk": false,
    "NeedsGMailOverflowScrollQuirk": false,
    "NeedsGoogleMapsScrollingQuirk": false,
    "NeedsGoogleTranslateScrollingQuirk": false,
    "NeedsPreloadAutoQuirk": false,
    "NeedsScriptToEvaluateBeforeRunningScriptFromURLQuirk": false,
    "NeedsYouTubeMouseOutQuirk": false,
    "NeedsYouTubeOverflowScrollQuirk": false,
    "ShouldAllowPopupFromMicrosoftOfficeToOneDrive": false,
    "ShouldDisablePointerEventsQuirk": false,
    "ShouldHideCoarsePointerCharacteristicsQuirk": false,
    "ShouldHideSoftTopScrollEdgeEffectDuringFocusQuirk": false,
    "ShouldIgnoreAriaForFastPathContentObservationCheckQuirk": false,
    "ShouldIgnoreInputModeNone": false,
    "ShouldNavigatorPluginsBeEmpty": false,
    "ShouldSilenceWindowResizeEventsDuringApplicationSnapshotting": false,
    "ShouldSuppressAutocorrectionAndAutocapitalizationInHiddenEditableAreasQuirk": false,
    "ShouldSynthesizeTouchEventsAfterNonSyntheticClickQuirk": false,
    "NeedsChromeOSNavigatorUserAgentQuirk": false,
    // PLATFORM(VISION)
    "ShouldDisableFullscreenVideoAspectRatioAdaptiveSizingQuirk": false
  }
}
```

## 涉及源码

- 钩子声明：`Source/WebCore/page/Quirks.h`（`g_onInitQuirks` / `g_onInitQuirksAfterDocumentHandler`）
- 钩子调用：`Source/WebCore/page/Quirks.cpp` 的 `Quirks::determineRelevantQuirks()`
- 枚举名→枚举值映射 + 钩子实现 + 注册：`Source/WebKit/Shared/API/APIItBrowser.cpp`
- 枚举定义（门控来源）：`Source/WebCore/page/QuirksData.h`
