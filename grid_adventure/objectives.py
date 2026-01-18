"""Objective functions for Grid Adventure environments."""

from dataclasses import dataclass
from grid_universe.objectives import CollectAndExitObjective


@dataclass(frozen=True)
class CollectGemsAndExitObjective(CollectAndExitObjective):
    """Objective where the agent must collect all gems (if any) and then exit."""

    description: str = "Collect all gems (if any) and reach an exit tile."


OBJECTIVES = {
    "collect_gems_and_exit": CollectGemsAndExitObjective(),
}
