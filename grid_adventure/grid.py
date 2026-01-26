from __future__ import annotations

from grid_universe.state import State
from grid_universe.grid.gridstate import GridState
from grid_universe.grid.convert import from_state as base_from_state
from grid_universe.grid.convert import to_state as base_to_state
from grid_universe.grid.entity import BaseEntity, copy_entity_components
from grid_universe.grid.step import step as base_step
from grid_universe.actions import Action

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
        return copy_entity_components(obj, AgentEntity(), preserve_entity_id=True)

    # Exit
    if has("exit"):
        return copy_entity_components(obj, ExitEntity(), preserve_entity_id=True)
    # Doors (Locked vs Unlocked)
    if app_name == "door":
        if has("locked"):
            return copy_entity_components(
                obj, LockedDoorEntity(), preserve_entity_id=True
            )
        return copy_entity_components(
            obj, UnlockedDoorEntity(), preserve_entity_id=True
        )

    # Key
    if has("key"):
        return copy_entity_components(obj, KeyEntity(), preserve_entity_id=True)

    # Collectibles
    if has("collectible"):
        # Power-ups first
        if has("speed"):
            return copy_entity_components(
                obj, SpeedPowerUpEntity(), preserve_entity_id=True
            )
        if has("immunity"):
            return copy_entity_components(
                obj, ShieldPowerUpEntity(), preserve_entity_id=True
            )
        if has("phasing"):
            return copy_entity_components(
                obj, PhasingPowerUpEntity(), preserve_entity_id=True
            )
        # Gem vs coin
        if app_name == "core" or has("requirable"):
            return copy_entity_components(obj, GemEntity(), preserve_entity_id=True)
        return copy_entity_components(obj, CoinEntity(), preserve_entity_id=True)

    # Boxes
    if app_name == "box":
        return copy_entity_components(obj, BoxEntity(), preserve_entity_id=True)

    # Hazards
    if app_name == "lava":
        return copy_entity_components(obj, LavaEntity(), preserve_entity_id=True)
    # Background tiles
    if app_name == "floor":
        return copy_entity_components(obj, FloorEntity(), preserve_entity_id=True)
    if app_name == "wall":
        return copy_entity_components(obj, WallEntity(), preserve_entity_id=True)

    # Fallback
    return obj


def _specialize_nested_list(items: list[BaseEntity] | None) -> list[BaseEntity]:
    """Specialize nested inventory/status entity lists."""
    if not items:
        return []
    return [_specialize_single(item) for item in items]


def specialize_entities(gridstate: GridState) -> GridState:
    """
    Returns a new GridState with entities replaced by specialized Grid Adventure subclasses.
    Also remaps cross-entity references to the new instances.
    """
    new_grid_state = GridState(
        width=gridstate.width,
        height=gridstate.height,
        movement=gridstate.movement,
        objective=gridstate.objective,
        seed=gridstate.seed,
        turn=gridstate.turn,
        score=gridstate.score,
        win=gridstate.win,
        lose=gridstate.lose,
        message=gridstate.message,
        turn_limit=gridstate.turn_limit,
    )

    # First pass: specialize and map original object id -> new specialized object
    obj_map: dict[int, BaseEntity] = {}
    for x in range(gridstate.width):
        for y in range(gridstate.height):
            specialized_cell: list[BaseEntity] = []
            for orig_obj in gridstate.grid[x][y]:
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

            new_grid_state.grid[x][y] = specialized_cell
    return new_grid_state


def from_state(state: State) -> GridState:
    """Convert a State to a specialized GridState using Grid Adventure entity subclasses."""
    base_grid_state = base_from_state(state)
    return specialize_entities(base_grid_state)


def to_state(gridstate: GridState) -> State:
    """Convert a GridState (with specialized Grid Adventure entities) to a State."""
    return base_to_state(gridstate)


def step(gridstate: GridState, action: Action) -> GridState:
    """Perform one step in the GridState using the base step function."""
    return specialize_entities(base_step(gridstate, action))


__all__ = ["from_state", "to_state", "specialize_entities", "step", "GridState"]
