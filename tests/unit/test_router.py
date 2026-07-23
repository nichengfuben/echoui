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
