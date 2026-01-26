# GridState Representation
The GridState Representation is a grid centric representation, that is easiest for players to follow

## GridState Attributes
The GridState class has 3 categories of attributes

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
| `win` | `bool` | `False` | True if objective met |
| `lose` | `bool` | `False` | True if losing condition met |
| `message` | `str` or `None` | `None` | Optional status message for display |
| `turn_limit` | `int` or `None` | `None` | Max turns allowed |

&nbsp;
## Available Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GridState.add(pos, obj)` | `None` | Place entity at position `(x, y)` |
| `GridState.add_many(items)` | `None` | Place multiple entities from list of `(pos, obj)` tuples |
| `GridState.remove(pos, obj)` | `bool` | Remove specific entity by identity; returns `True` if found |
| `GridState.remove_if(pos, predicate)` | `int` | Remove entities where `predicate(obj)` is `True`; returns number of entities removed |
| `GridState.move_obj(from_pos, obj, to_pos)` | `bool` | Move entity between cells; returns `True` if successful |
| `GridState.clear_cell(pos)` | `int` | Remove all entities from cell; returns count |
| `GridState.objects_at(pos)` | `list[BaseEntity]` | Return shallow copy of entities at position |
| `step(gridState, action)` | `GridState` | Generates new `GridState` with action |
| `to_state(gridState)` | `None` | Converts mutable `gridState` to immutable `State` |

Note: `pos` is of class `Position`, a (int, int)  
Note: `obj` is of class `BaseEntity`, parent class of all Entities. For more details about entities, Please refer to [Entity Classes](entities.md#entities).

## Entities
&nbsp;
### Entity List
There are a total of 14 Entities that can be present on the grid. To view the appearance and interactions between the entities, refer to the [Player Guide](../player-guide/entities.md)

&nbsp;
#### AgentEntity
This is the entity controlled by the user.

|Attribute|Type|Description|
|---|---|---|
|health|Health Class|Health to give the agent, constitutes Max and current health|
|inventory|Inventory Class|List of Entity that represents the Agents inventory|
|status|Status Class|List of Entity that represents the Status Active on Agent|

|Available Methods|Inputs|Description|
|---|---|---|
|set_health|health: int|Sets agent health|

&nbsp;
#### LavaEntity
This is a damaging entity that the agent can walk through. When the Agent lands on a Lava tile, 2 damage is dealt.

&nbsp;
#### WallEntity
This is a wall entity that the agent cannot walk through nor push.

&nbsp;
#### BoxEntity
This is a pushable blocking entity, that the agent can push but not walk through.

&nbsp;
#### LockedDoorEntity
This is a blocking entity that the agent cannot push through nor push. This entity becomes a [UnlockedDoorEntity](#unlockeddoorentity), when a [KeyEntity](#keyentity) is used on it. 

note: Any key can be used to unlock a door, but each key can only be used once.

&nbsp;
#### CoinEntity
This is an **optional** collectible that provides a reward of 5 when picked up by the agent. 

&nbsp;
#### GemEntity
This is a **required** collectible to be collected by agent before it can enter the exit.

&nbsp;
#### KeyEntity
This is a collectible required to unlock a [LockedDoorEntity](#lockeddoorentity)

Note: Any key present in the grid can be used to unlock a door, but each key can only be used once.

&nbsp;
#### SpeedPowerUpEntity
This is a collectible granting agent the ability to walk 2 tiles in 1 turn.

Speed powerup lasts for 5 turns.

&nbsp;
#### ShieldPowerUpEntity
This is a collectible granting agent immunity. When the agent walks onto a lava tile, the shield is used once and the agent does not take damage.

Shield powerup has 5 uses.

&nbsp;
#### PhasingPowerUpEntity
This is a collectible granting agent ability to walk through walls and doors.

Phasing powerup lasts for 5 turns.

&nbsp;
#### ExitEntity
ExitEntity and serve as the exit objective. The agent completes the objective by collecting any gems present, then moving to the exit tile.

&nbsp;
#### FloorEntity 
Floor entities are not interactable with agent.

&nbsp;
#### UnlockedDoorEntity 
UnlockedDoorEntity are not interactable with agent, serving only aesthetic purpose. They are the unlocked version of the [LockedDoorEntity](#lockeddoorentity).