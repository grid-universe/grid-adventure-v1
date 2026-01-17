from __future__ import annotations

from grid_universe.state import State
from grid_universe.levels.grid import Level
from grid_universe.levels.convert import from_state as base_from_state
from grid_universe.levels.convert import to_state as base_to_state
from grid_universe.levels.entity import BaseEntity, copy_entity_components

# Specialized entity classes from Grid Adventure
from grid_adventure.entities import (
    AgentEntity,
    FloorEntity,
    WallEntity,
    ExitEntity,
    CoinEntity,
    GemEntity,
    KeyEntity,
    LockedDoorEntity,
    UnlockedDoorEntity,
    BoxEntity,
    LavaEntity,
    SpeedPowerUpEntity,
    ShieldPowerUpEntity,
    PhasingPowerUpEntity,
)

SpecializedTypes = (
    AgentEntity,
    FloorEntity,
    WallEntity,
    ExitEntity,
    CoinEntity,
    GemEntity,
    KeyEntity,
    LockedDoorEntity,
    UnlockedDoorEntity,
    BoxEntity,
    LavaEntity,
    SpeedPowerUpEntity,
    ShieldPowerUpEntity,
    PhasingPowerUpEntity,
)


def _specialize_single(obj: BaseEntity) -> BaseEntity:
    """
    Return a specialized Grid Adventure entity based on components/appearance.
    Keeps obj unchanged if it is already specialized.
    """
    if isinstance(obj, SpecializedTypes):
        return obj

    def has(name: str) -> bool:
        return getattr(obj, name, None) is not None

    app_name: str | None = getattr(getattr(obj, "appearance", None), "name", None)

    # Agent
    if has("agent"):
        return copy_entity_components(obj, AgentEntity())

    # Exit
    if has("exit"):
        return copy_entity_components(obj, ExitEntity())

    # Doors (Locked vs Unlocked)
    if app_name == "door":
        if has("locked"):
            return copy_entity_components(obj, LockedDoorEntity())
        return copy_entity_components(obj, UnlockedDoorEntity())

    # Key
    if has("key"):
        return copy_entity_components(obj, KeyEntity())

    # Collectibles
    if has("collectible"):
        # Power-ups first
        if has("speed"):
            return copy_entity_components(obj, SpeedPowerUpEntity())
        if has("immunity"):
            return copy_entity_components(obj, ShieldPowerUpEntity())
        if has("phasing"):
            return copy_entity_components(obj, PhasingPowerUpEntity())
        # Gem/core vs coin
        if app_name == "core" or has("requirable"):
            return copy_entity_components(obj, GemEntity())
        return copy_entity_components(obj, CoinEntity())

    # Boxes
    if app_name == "box":
        return copy_entity_components(obj, BoxEntity())

    # Hazards
    if app_name == "lava":
        return copy_entity_components(obj, LavaEntity())

    # Background tiles
    if app_name == "floor":
        return copy_entity_components(obj, FloorEntity())
    if app_name == "wall":
        return copy_entity_components(obj, WallEntity())

    # Fallback
    return obj


def _specialize_nested_list(items: list[BaseEntity] | None) -> list[BaseEntity]:
    """Specialize nested inventory/status entity lists."""
    if not items:
        return []
    return [_specialize_single(item) for item in items]


def specialize_entities(level: Level) -> Level:
    """
    Returns a new Level with entities replaced by specialized Grid Adventure subclasses.
    Also remaps cross-entity references to the new instances.
    """
    new_level = Level(
        width=level.width,
        height=level.height,
        move_fn=level.move_fn,
        objective_fn=level.objective_fn,
        seed=level.seed,
        turn=level.turn,
        score=level.score,
        win=level.win,
        lose=level.lose,
        message=level.message,
        turn_limit=level.turn_limit,
    )

    # First pass: specialize and map original object id -> new specialized object
    obj_map: dict[int, BaseEntity] = {}
    for y in range(level.height):
        for x in range(level.width):
            specialized_cell: list[BaseEntity] = []
            for orig_obj in level.grid[y][x]:
                spec_obj = _specialize_single(orig_obj)

                # Specialize nested lists if attributes exist (inventory_list, status_list)
                if hasattr(spec_obj, "inventory_list"):
                    inv_list = getattr(spec_obj, "inventory_list", None)
                    if inv_list:
                        setattr(
                            spec_obj,
                            "inventory_list",
                            _specialize_nested_list(inv_list),
                        )
                if hasattr(spec_obj, "status_list"):
                    st_list = getattr(spec_obj, "status_list", None)
                    if st_list:
                        setattr(
                            spec_obj, "status_list", _specialize_nested_list(st_list)
                        )

                obj_map[id(orig_obj)] = spec_obj
                specialized_cell.append(spec_obj)

            new_level.grid[y][x] = specialized_cell
    return new_level


def from_state(state: State) -> Level:
    """Convert a State to a specialized Level using Grid Adventure entity subclasses."""
    base_level = base_from_state(state)
    return specialize_entities(base_level)


def to_state(level: Level) -> State:
    """Convert a Level (with specialized Grid Adventure entities) to a State."""
    return base_to_state(level)
