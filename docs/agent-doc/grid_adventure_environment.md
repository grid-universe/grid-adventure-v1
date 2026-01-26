# GridAdventureEnv

GridAdventureEnv is the main environment that runs the Grid Adventure V1 game. It implements the Gymnasium API, providing a standard interface for agents to interact with the game.

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `initial_state_fn` | `Callable[..., State]` | required | Function that generates the initial internal game state |
| `render_mode` | `str` | `"rgb_array"` | Rendering mode |
| `observation_type` | `str` | `"image"` or `"gridstate"` | This determines if the game representation returned is of image ([ImageObservation](image_observation.md) class) or gridstate ([GridState](#gridstate) class)|

Note: For more details about `ImageObservation` class and `GridState` class, please refer to [Game Representation](game_representation.md).

&nbsp;
## Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GridAdventureEnv.reset(seed, options)` | `tuple[Observation, dict]` | Resets the internal game state and returns the game representation|
| `GridAdventureEnv.step(action)` | `tuple[Observation, float, bool, bool, dict]` | Applies one action, and returns the game representation |
| `GridAdventureEnv.render()` | `PILImage` or `None` | Renders the current state |
| `GridAdventureEnv.close()` | `None` | Releases resources |