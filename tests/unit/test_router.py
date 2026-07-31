"""Router tests."""

from echoui.router import Router


def test_static_route():
    r = Router()
    r.add("/", "Home")
    r.add("/about", "About")
    screen, params = r.navigate("/about")
    assert screen == "About"
    assert params == {}


def test_param_route():
    r = Router()
    r.add("/user/:id", "UserDetail")
    screen, params = r.navigate("/user/42")
    assert screen == "UserDetail"
    assert params["id"] == "42"


def test_wildcard_route():
    r = Router()
    r.add("/docs/*", "Docs")
    screen, params = r.navigate("/docs/guide/start")
    assert screen == "Docs"
    assert "rest" in params


def test_guard_redirect():
    r = Router()
    r.add("/admin", "Admin", guard=lambda: "/login")
    r.add("/login", "Login")
    screen, _ = r.navigate("/admin")
    assert screen == "Login"


def test_middleware():
    r = Router()
    seen = []

    def mw(ctx):
        seen.append(ctx["path"])
        return ctx

    r.middleware.append(mw)
    r.add("/", "Home")
    r.navigate("/")
    assert seen == ["/"]


def test_lazy_screen_loader_and_layout():
    loads: list[int] = []

    def load_settings():
        loads.append(1)
        return "SettingsScreen"

    r = Router()
    r.add("/", "Home", layout="Shell")
    r.add("/settings", load_settings, layout="Shell", lazy=True)
    screen, _ = r.navigate("/settings")
    assert screen == "SettingsScreen"
    assert r.current_layout() == "Shell"
    assert loads == [1]
    # second navigate reuses cache
    screen2, _ = r.navigate("/settings")
    assert screen2 == "SettingsScreen"
    assert loads == [1]

    home, _ = r.navigate("/")
    assert home == "Home"
    assert r.current_layout() == "Shell"


def test_nested_group_layouts_and_parent_chain():
    r = Router()
    r.add("/", "Home", layout="Root")
    app = r.group("/app", layout="AppShell")
    app.add("/", "AppHome")
    app.add("/settings", "Settings", layout="SettingsPane")
    # explicit parent inheritance
    r.add("/app/profile", "Profile", layout="ProfilePane", parent="/app")
    # register parent route so parent layout resolves
    r.add("/app", "AppIndex", layout="AppShell")

    screen, _ = r.navigate("/app/settings")
    assert screen == "Settings"
    assert r.current_layouts() == ["AppShell", "SettingsPane"]
    assert r.current_layout() == "SettingsPane"

    screen2, _ = r.navigate("/app/profile")
    assert screen2 == "Profile"
    assert r.current_layouts() == ["AppShell", "ProfilePane"]

    home, _ = r.navigate("/")
    assert home == "Home"
    assert r.current_layouts() == ["Root"]
