from shesh_media.server import take_screenshot, list_sinks, set_wallpaper

def test_screenshot():
    res = take_screenshot("/tmp/test_shesh.png")
    assert res["ok"]

def test_sinks():
    res = list_sinks()
    assert "sinks" in res

def test_wallpaper_missing():
    res = set_wallpaper("/nonexistent.jpg")
    assert "ok" in res
