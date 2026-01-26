from grid_universe.grid.gridstate import GridState
from grid_adventure.movements import MOVEMENTS
from grid_adventure.objectives import OBJECTIVES
from grid_adventure.entities import (
    create_agent_entity,
    FloorEntity,
    WallEntity,
    ExitEntity,
    CoinEntity,
    GemEntity,
    KeyEntity,
    LockedDoorEntity,
    LavaEntity,
    BoxEntity,
    SpeedPowerUpEntity,
    ShieldPowerUpEntity,
    PhasingPowerUpEntity,
)


TURN_LIMIT = 50


def _floors(gridstate: GridState) -> None:
    for y in range(gridstate.height):
        for x in range(gridstate.width):
            gridstate.add((x, y), FloorEntity())


def _border(gridstate: GridState) -> None:
    for x in range(gridstate.width):
        gridstate.add((x, 0), WallEntity())
        gridstate.add((x, gridstate.height - 1), WallEntity())
    for y in range(gridstate.height):
        gridstate.add((0, y), WallEntity())
        gridstate.add((gridstate.width - 1, y), WallEntity())


def build_level_basic_movement(seed: int = 100) -> GridState:
    w, h = 7, 5
    gridstate = GridState(
        w,
        h,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)
    gridstate.add((1, h // 2), create_agent_entity())
    gridstate.add((w - 2, h // 2), ExitEntity())
    for y in range(h):
        if y != h // 2:
            gridstate.add((w // 2, y), WallEntity())
    return gridstate


def build_level_maze_turns(seed: int = 101) -> GridState:
    w, h = 9, 7
    gridstate = GridState(
        w,
        h,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)
    _border(gridstate)
    for x in range(2, w - 2):
        gridstate.add((x, 2), WallEntity())
    for x in range(2, w - 2):
        if x != w // 2:
            gridstate.add((x, h - 3), WallEntity())
    gridstate.add((1, 1), create_agent_entity())
    gridstate.add((w - 2, h - 2), ExitEntity())
    return gridstate


def build_level_optional_coin(seed: int = 102) -> GridState:
    w, h = 9, 7
    gridstate = GridState(
        w,
        h,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)
    _border(gridstate)
    gridstate.add((1, 2), WallEntity())
    gridstate.add((3, 3), WallEntity())
    for x in range(3, w - 2):
        gridstate.add((x, 2), WallEntity())
    for x in range(2, w - 2):
        if x != w // 2:
            gridstate.add((x, h - 3), WallEntity())
    gridstate.add((1, 1), create_agent_entity())
    gridstate.add((w - 2, h - 2), ExitEntity())
    for x in range(1, w - 2, 1):
        gridstate.add((x, h - 2), CoinEntity())
    return gridstate


def build_level_required_multiple(seed: int = 104) -> GridState:
    w, h = 11, 9
    gridstate = GridState(
        w,
        h,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)
    _border(gridstate)
    midx, midy = w // 2, h // 2
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            if x != midx and y != midy:
                gridstate.add((x, y), WallEntity())
    gridstate.add((1, midy), create_agent_entity())
    gridstate.add((w - 2, midy), ExitEntity())
    gridstate.add((midx, 1), GemEntity())
    gridstate.add((midx, h - 2), GemEntity())
    return gridstate


def build_level_key_door(seed: int = 105) -> GridState:
    w, h = 11, 9
    gridstate = GridState(
        w,
        h,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)
    for y in range(h):
        if y != h // 2:
            gridstate.add((w // 2, y), WallEntity())
    gridstate.add((1, h // 2), create_agent_entity())
    gridstate.add((w - 2, h // 2), ExitEntity())
    gridstate.add((2, h // 2 - 1), KeyEntity())
    gridstate.add((w // 2, h // 2), LockedDoorEntity())
    return gridstate


def build_level_hazard_detour(seed: int = 106) -> GridState:
    w, h = 11, 9
    gridstate = GridState(
        w,
        h,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)
    gridstate.add((1, h // 2), create_agent_entity(health=3))
    gridstate.add((w - 2, h // 2), ExitEntity())
    gridstate.add((w // 2 - 1, h // 2), LavaEntity())
    gridstate.add((w - 3, h // 2), LavaEntity())

    for y in range(1, h - 1):
        if y != h // 2:
            gridstate.add((w // 2 - 1, y), WallEntity())
    for y in range(2, h - 2):
        if y != h // 2:
            gridstate.add((w - 3, y), WallEntity())

    return gridstate


def build_level_pushable_box(seed: int = 108) -> GridState:
    w, h = 11, 9
    gridstate = GridState(
        w,
        h,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)
    for y in range(h):
        if y != h // 2:
            gridstate.add((w // 2, y), WallEntity())
    gridstate.add((1, h // 2), create_agent_entity())
    gridstate.add((w - 2, h // 2), ExitEntity())
    gridstate.add((w // 2 - 1, h // 2), BoxEntity())
    return gridstate


def build_level_power_shield(seed: int = 110) -> GridState:
    w, h = 11, 9
    gridstate = GridState(
        w,
        h,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)
    gridstate.add((1, h // 2), create_agent_entity(2))
    gridstate.add((w - 2, h // 2), ExitEntity())
    for y in range(h):
        if y != h // 2:
            gridstate.add((w // 2, y), WallEntity())
    gridstate.add((2, h // 2 - 3), ShieldPowerUpEntity())
    gridstate.add((w // 2, h // 2), LavaEntity())
    return gridstate


def build_level_power_ghost(seed: int = 111) -> GridState:
    w, h = 13, 9
    gridstate = GridState(
        w,
        h,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)
    gridstate.add((1, h // 2), create_agent_entity())
    gridstate.add((w - 2, h // 2), ExitEntity())
    for y in range(h):
        gridstate.add((w // 2, y), WallEntity())
    gridstate.add((2, h // 2 - 3), PhasingPowerUpEntity())
    return gridstate


def build_level_power_boots(seed: int = 112) -> GridState:
    w, h = 13, 9
    gridstate = GridState(
        w,
        h,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)
    gridstate.add((1, h // 2), create_agent_entity(1))
    gridstate.add((w - 2, h // 2), ExitEntity())
    for y in range(h):
        if y not in [h // 2, h // 2 + 1]:
            gridstate.add((w // 2, y), WallEntity())
            gridstate.add((w // 2 + 1, y), WallEntity())
            gridstate.add((w // 2 + 2, y), WallEntity())
    gridstate.add((w // 2 - 1, h // 2 + 1), SpeedPowerUpEntity())
    return gridstate


def build_level_combined_mechanics(seed: int = 113) -> GridState:
    gridstate = GridState(
        width=7,
        height=7,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )

    _floors(gridstate)

    # Agent
    gridstate.add((0, 0), create_agent_entity())

    # Walls (grouped and added in one pass)
    wall_coords = [
        # Row 0
        (3, 0),
        (5, 0),
        # Row 1
        (1, 1),
        # Row 2
        (1, 2),
        (3, 2),
        (4, 2),
        (6, 2),
        # Row 3
        (0, 3),
        (3, 3),
        (5, 3),
        # Row 4
        (1, 4),
        # Row 5
        (3, 5),
        (5, 5),
        (6, 5),
        # Row 6
        (1, 6),
        (3, 6),
    ]
    gridstate.add_many([(pos, WallEntity()) for pos in wall_coords])

    # Items and doors
    gridstate.add((6, 3), GemEntity())
    gridstate.add((0, 4), KeyEntity())
    gridstate.add((3, 4), LockedDoorEntity())

    # Exit
    gridstate.add((6, 6), ExitEntity())

    return gridstate


def build_level_boss(seed: int = 113) -> GridState:
    gridstate = GridState(
        width=7,
        height=7,
        movement=MOVEMENTS["cardinal"],
        objective=OBJECTIVES["collect_gems_and_exit"],
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(gridstate)

    # Agent and Exit
    gridstate.add((0, 0), create_agent_entity(health=1))
    gridstate.add((0, 6), ExitEntity())

    # Walls
    wall_pos = [
        (3, 0),
        (0, 1),
        (1, 1),
        (3, 1),
        (5, 1),
        (3, 2),
        (5, 2),
        (1, 3),
        (1, 4),
        (3, 4),
        (5, 4),
        (1, 5),
        (2, 5),
        (3, 5),
        (5, 5),
    ]
    for p in wall_pos:
        gridstate.add(p, WallEntity())

    # Pushable box
    gridstate.add((2, 1), BoxEntity())

    # Gems
    gridstate.add((0, 5), GemEntity())
    gridstate.add((6, 3), GemEntity())

    # Coins
    coin_pos = [(1, 2), (4, 2), (3, 3), (6, 5), (2, 6), (3, 6)]
    for p in coin_pos:
        gridstate.add(p, CoinEntity())

    # Powerups
    gridstate.add((0, 2), SpeedPowerUpEntity())
    gridstate.add((2, 3), PhasingPowerUpEntity())
    gridstate.add((4, 0), ShieldPowerUpEntity())

    # Key-door pair
    gridstate.add((4, 4), KeyEntity())
    gridstate.add((1, 6), LockedDoorEntity())

    # Hazards
    gridstate.add((5, 3), LavaEntity())

    return gridstate
