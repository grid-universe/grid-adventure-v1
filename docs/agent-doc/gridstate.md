# GridState Representation
The GridState Representation is a grid centric representation, that is easiest for players to follow

## GridState Attributes
The GridState class has 3 categories of attributes:

- Overall Configuration
- Grid Structure
- Game Status

### Overall Configuration

| Attribute | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Grid width in tiles |
| `height` | `int` | Grid height in tiles |
| `movement` | `BaseMovement` | Movement function configuration |
| `objective` | `BaseObjective` | Win/lose condition configuration |
| `seed` | `int` or `None` | RNG seed for deterministic behavior |

### Grid Structure

| Attribute | Type | Description |
|-----------|------|-------------|
| `grid` | `list[list[list[BaseEntity]]]` | Grid representation where `grid[x][y]` is a list of entities at that cell |

### Game Status

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `turn` | `int` | `0` | Current turn number |
| `score` | `int` | `0` | Cumulative score |
| `win` | `bool` | `False` | True if the objective is met |
| `lose` | `bool` | `False` | True if the losing condition is met |
| `message` | `str` or `None` | `None` | Optional status message for display |
| `turn_limit` | `int` or `None` | `None` | Maximum turns allowed |

&nbsp;
## Available Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GridState.add(pos, obj)` | `None` | Place an entity at position `(x, y)` |
| `GridState.add_many(items)` | `None` | Places multiple entities from list of `(pos, obj)` tuples |
| `GridState.remove(pos, obj)` | `bool` | Removes a specific entity by identity; returns `True` if found |
| `GridState.remove_if(pos, predicate)` | `int` | Remove entities where `predicate(obj)` is `True`; returns number of entities removed |
| `GridState.move_obj(from_pos, obj, to_pos)` | `bool` | Move entity between cells; returns `True` if successful |
| `GridState.clear_cell(pos)` | `int` | Remove all entities from cell; returns count |
| `GridState.objects_at(pos)` | `list[BaseEntity]` | Return shallow copy of entities at position |
| `step(gridState, action)` | `GridState` | Generates a new `GridState` with action |
| `to_state(gridState)` | `State` | Converts mutable `GridState` to immutable `State` |

Note: `pos` is of class `Position`, represented as a `(int, int)`  
Note: `obj` is of class `BaseEntity`, parent class of all Entities. For more details about entities, please refer to [Entity Classes](#entities).

## Entities

### Entity List
There are a total of 14 entities that can be present on the grid. To view the appearance and interactions between the entities, refer to the [Player Guide](../player-guide/entities.md).

All entities have an `appearance.name` attribute, which is a string describing the entity. It can be used to determine the entities present in each cell of the grid. Each entity below is given with its entity class name as well as appearance name in brackets.

!!!note 
    When rendering the grid, each entity’s **appearance name** is used to determine which image to display. By default, images are loaded from the `DEFAULT_ASSET_ROOT` defined in `grid_adventure.rendering`, which provides public assets from Grid Adventure V1. A mapping from appearance name is also defined as `IMAGE_MAP` in the same package.

**[AgentEntity](../player-guide/entities.md#agent)** (`"human"`)

This is the entity controlled by the user. The Agent contains additional attributes and methods.

| Attribute | Type | Description |
|---|---|---|
|health|Health Class|Health to give the agent, constitutes Max and current health|
|inventory_list|list[BaseEntity]|List of Entity that represents the Agent's inventory|
|status_list|list[BaseEntity]|List of Entity that represents the statuses active on the agent|

|Available Methods|Inputs|Description|
|---|---|---|
|set_health|health: int|Sets the agent's health|

**[LavaEntity](../player-guide/entities.md#lava)** (`"lava"`)

**[WallEntity](../player-guide/entities.md#wall)** (`"wall"`)

**[BoxEntity](../player-guide/entities.md#box)** (`"box"`)

**[CoinEntity](../player-guide/entities.md#coin)** (`"coin"`)

**[GemEntity](../player-guide/entities.md#gem)** (`"gem"`)

**[KeyEntity](../player-guide/entities.md#key)** (`"key"`)

**[LockedDoorEntity](../player-guide/entities.md#door)** (`"locked"`)

**[UnlockedDoorEntity](../player-guide/entities.md#door)** (`"opened"`)

**[SpeedPowerUpEntity](../player-guide/entities.md#speed-powerup)** (`"boots"`)

**[ShieldPowerUpEntity](../player-guide/entities.md#shield-powerup)** (`"shield"`)

**[PhasingPowerUpEntity](../player-guide/entities.md#phasing-powerup)** (`"ghost"`)

**[ExitEntity](../player-guide/entities.md#exit)** (`"exit"`)

**[FloorEntity](../player-guide/entities.md#floor)** (`"floor"`)