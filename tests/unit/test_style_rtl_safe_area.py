"""RTL / safe-area style helpers."""

from echoui.style import css_hash, ltr, rtl, rules_to_css, safe_area, writing_mode


def test_rtl_and_ltr_helpers():
    r = rtl(text_align="right")
    assert r["direction"] == "rtl"
    assert r["text_align"] == "right"
    assert ltr()["direction"] == "ltr"


def test_safe_area_padding_env():
    s = safe_area(top=True, bottom=True, left=False, right=False)
    assert s["padding_top"] == "env(safe-area-inset-top)"
    assert s["padding_bottom"] == "env(safe-area-inset-bottom)"
    assert "padding_left" not in s


def test_rtl_rules_to_css():
    rules = rtl(color="#111")
    css = rules_to_css(css_hash(rules), rules)
    assert "direction:rtl" in css
    assert "color:#111" in css


def test_safe_area_rules_to_css():
    rules = safe_area()
    css = rules_to_css("esa", rules)
    assert "env(safe-area-inset-top)" in css
    assert "padding-top" in css


def test_writing_mode_helper():
    w = writing_mode("vertical-rl", color="red")
    assert w["writing_mode"] == "vertical-rl"
    assert w["color"] == "red"
