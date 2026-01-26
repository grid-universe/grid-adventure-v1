from __future__ import annotations

from collections.abc import Callable

from grid_universe.state import State
from grid_universe.renderer.image import ImageMap

from grid_adventure.env import GridAdventureEnv
from grid_adventure.rendering import IMAGE_MAP
from grid_adventure.levels import intro as adv_intro_levels

from grid_play.config.sources.level_selection import (
    Builder,
    make_level_selection_source,
)
from grid_play.config.sources.base import register_level_source

BUILDERS: dict[str, Builder] = {
    "A0 Basic Movement": adv_intro_levels.build_level_basic_movement,
    "A1 Maze Turns": adv_intro_levels.build_level_maze_turns,
    "A2 Optional Coin Path": adv_intro_levels.build_level_optional_coin,
    "A3 Multiple Required Gems": adv_intro_levels.build_level_required_multiple,
    "A4 Key & Door": adv_intro_levels.build_level_key_door,
    "A5 Hazard Detour": adv_intro_levels.build_level_hazard_detour,
    "A6 Pushable Box": adv_intro_levels.build_level_pushable_box,
    "A7 Shield Powerup": adv_intro_levels.build_level_power_shield,
    "A8 Ghost Powerup": adv_intro_levels.build_level_power_ghost,
    "A9 Boots Powerup": adv_intro_levels.build_level_power_boots,
    "A10 Combined Mechanics": adv_intro_levels.build_level_combined_mechanics,
    "A11 Boss Level": adv_intro_levels.build_level_boss,
}


def _env_factory(
    initial_state_fn: Callable[..., State], _image_map: ImageMap
) -> GridAdventureEnv:
    sample_state: State = initial_state_fn()
    return GridAdventureEnv(
        render_mode="rgb_array",
        initial_state_fn=initial_state_fn,
        width=sample_state.width,
        height=sample_state.height,
        render_image_map=IMAGE_MAP,  # fixed art set
    )


source = make_level_selection_source(
    name="Grid Adventure Intro",
    builders=BUILDERS,
    builder_returns_gridstate=True,  # builders return GridState
    env_factory=_env_factory,
    image_maps=[IMAGE_MAP],  # single pack -> no picker
)

register_level_source(source)
