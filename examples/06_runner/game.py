"""Endless runner logic (EchoUI Store + frame tick)."""

from __future__ import annotations

import random

from echoui import Store

PLAYER_X = 80
PLAYER_W = 32
PLAYER_H = 32
GROUND_Y = 300
GRAVITY = 1400.0
JUMP_V = -480.0
OBS_W = 28
OBS_H = 40
MAX_OBS = 4


class RunnerStore(Store):
    player_y: float = GROUND_Y
    score: int = 0
    game_over: bool = False
    speed: float = 280.0
    vy: float = 0.0
    grounded: bool = True
    spawn_t: float = 1.5
    obs0_x: float = -200.0
    obs1_x: float = -200.0
    obs2_x: float = -200.0
    obs3_x: float = -200.0
    bg_url: str = ""
    player_url: str = ""
    costume0: str = ""
    costume1: str = ""
    costume_count: int = 0
    player_costume_i: int = 0


def save_player_costume() -> None:
    s = RunnerStore()
    if not s.player_url:
        return
    if s.costume_count == 0:
        s.costume0 = s.player_url
        s.costume_count = 1
        s.player_costume_i = 0
        return
    s.costume1 = s.player_url
    s.costume_count = 2
    s.player_costume_i = 1


def cycle_player_costume() -> None:
    s = RunnerStore()
    if s.costume_count < 2:
        return
    if s.player_costume_i == 0:
        s.player_costume_i = 1
        s.player_url = s.costume1
        return
    s.player_costume_i = 0
    s.player_url = s.costume0


def _obs_fields() -> list[str]:
    return [f"obs{i}_x" for i in range(MAX_OBS)]


def jump() -> None:
    s = RunnerStore()
    if s.game_over or not s.grounded:
        return
    s.vy = JUMP_V
    s.grounded = False


def reset_game() -> None:
    s = RunnerStore()
    s.player_y = GROUND_Y
    s.score = 0
    s.game_over = False
    s.speed = 280.0
    s.vy = 0.0
    s.grounded = True
    s.spawn_t = 1.5
    for field in _obs_fields():
        setattr(s, field, -200.0)


def tick(dt: float) -> None:
    s = RunnerStore()
    if s.game_over:
        return
    s.score += max(1, int(dt * 12))
    s.speed = min(520.0, s.speed + dt * 6.0)

    if not s.grounded:
        s.vy += GRAVITY * dt
    s.player_y += s.vy * dt
    if s.player_y >= GROUND_Y:
        s.player_y = GROUND_Y
        s.vy = 0.0
        s.grounded = True

    for field in _obs_fields():
        ox = getattr(s, field)
        if ox < -OBS_W:
            continue
        ox -= s.speed * dt
        setattr(s, field, ox)
        if _hit(ox):
            s.game_over = True
            return

    s.spawn_t -= dt
    if s.spawn_t <= 0:
        for field in _obs_fields():
            if getattr(s, field) < -OBS_W:
                setattr(s, field, 660.0)
                s.spawn_t = random.uniform(1.0, 2.2)
                break


def _hit(obs_x: float) -> bool:
    s = RunnerStore()
    if obs_x + OBS_W < PLAYER_X or obs_x > PLAYER_X + PLAYER_W:
        return False
    return s.player_y + PLAYER_H > GROUND_Y + 4
