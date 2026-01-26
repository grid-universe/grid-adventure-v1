from grid_adventure.env import GridAdventureEnv
from grid_adventure.levels import intro
from grid_universe.grid.gridstate import GridState
from grid_universe.grid.convert import grid_state_fn_to_initial_state_fn


def test_env_returns_level_observation():
    env = GridAdventureEnv(
        initial_state_fn=grid_state_fn_to_initial_state_fn(
            intro.build_level_capstone_simple
        ),
        observation_type="gridstate",
    )
    obs, _ = env.reset()
    print(obs)
    assert isinstance(obs, GridState)
    # Step with a valid action (e.g., WAIT)
    from grid_universe.actions import Action

    obs2, reward, terminated, truncated, info2 = env.step(Action.WAIT)
    assert isinstance(obs2, GridState)
    assert isinstance(reward, float)
    assert terminated in (True, False)
    assert truncated in (True, False)
    assert isinstance(info2, dict)
    env.close()
