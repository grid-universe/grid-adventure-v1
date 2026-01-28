# State Representation
The state representation is the internal representation used by the Grid Adventure game. It stores information in various attributes, tracked by EntityID of each Entity. It is the most comprehensive of the 3 representations, and is used to generate the GridState and ImageObservation representations. 

!!! warning "WARNING ON STATE SPACE"
    The Capstone Project can be solved without using the **State Representation**, however the State Representation is included for a lower level access to the representation.

## State Attributes
The state Class represents the Game snapshot with the following 4 types of attributes.

- Level Configuration
- Effect Configuration
- Property Components
- Game Status

### Level Configuration

| Attribute | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Grid width in tiles |
| `height` | `int` | Grid height in tiles |
| `movement` | `BaseMovement` | Movement functions allowed |
| `objective` | `BaseObjective` | Objective of the level |

### Effect Components

All effect stores are of type `PMap[EntityID, Component]`.  
Note: `PMap` is an immutable dictionary, standard dictionary methods are available.

| Attribute | Mapped Component | Description |
|-----------|-----------|-------------|
| `immunity` | `Immunity` | Damage immunity effects |
| `phasing` | `Phasing` | Pass-through-walls effects |
| `speed` | `Speed` | Movement multiplier effects |
| `time_limit` | `TimeLimit` | Effect duration (remaining steps) |
| `usage_limit` | `UsageLimit` | Effect uses (remaining count) |

### Property Components

All property stores are of type `PMap[EntityID, Component]`.  
Note: `PMap` is an immutable dictionary, standard dictionary methods are available.

| Attribute | Mapped Component | Description |
|-----------|-----------|-------------|
| `agent` | [`Agent`](#agententity) | Player-controlled entities |
| `appearance` | `Appearance` | Visual rendering properties |
| `blocking` | [`Blocking`](#blockingentity) | Obstacles that block movement |
| `collectible` | [`Collectible`](#collectibleentity) | Items that can be picked up |
| `collidable` | [`Collidable`](#collidable-entities) | Entities triggering collision events |
| `cost` | `Cost` | Entities that inflict movement cost |
| `damage` | [`Damage`](#lavaentity) | Entities that deal damage on contact |
| `dead` | `Dead` | Dead/incapacitated entities |
| `exit` | [`Exit`](#exitentity) | Level exit points |
| `health` | `Health` | Entity health (current/max) |
| `inventory` | `Inventory` | Items held by entities |
| `key` | [`Key`](#keyentity) | Keys that unlock `Locked` entities |
| `locked` | [`Locked`](#lockeddoorentity) | Locked doors/entities |
| `position` | `Position` | Entity grid positions |
| `pushable` | [`Pushable`](#pushableentity) | Entities that can be pushed |
| `requirable` | [`Requirable`](#gementity) | Must-collect items for objectives |
| `rewardable` | [`Rewardable`](#coinentity) | Entities granting score rewards |
| `status` | `Status` | Active status effects on entities |

### Game Status

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `turn` | `int` | `0` | Current turn number |
| `score` | `int` | `0` | Cumulative score |
| `win` | `bool` | `False` | True if objective met |
| `lose` | `bool` | `False` | True if losing condition met |
| `message` | `str` or `None` | `None` | Optional status message for display |
| `turn_limit` | `int` or `None` | `None` | Max turns allowed |
| `seed` | `int` or `None` | `None` | RNG seed for deterministic behavior |

## Useful Methods

| Method | Description |
|--------|-------------|
| `state.description` | Property returning `PMap` of all non-empty state attributes |
| `from_state(state)` | Converts immutable `State` to mutable `GridState` |

&nbsp;
## Entities
All effects and components are represented by Entities in the Grid Adventure game. Each entity is assigned a unique EntityID at creation. This EntityID is used to map to each attribute of the Entity.

### Entity Types
There are in general 5 types of Entities

|Entity Types|Description|
|---|---|
| CollidableEntity | Recognisable for possession of `collidable` attribute of `Collidable` class|
| BlockingEntity | Recognisable for possession of `blocking` attribute of `Blocking` class|
| PushableEntity | Recognisable for possession of `pushable` attribute of `Pushable` class|
| CollectibleEntity | Recognisable for possession of `collectible` attribute of `Collectible` class|
| Others | All other entities|

&nbsp;
### Collidable Entities
These are entities which can pass through each other but trigger interactions when they do. These entities are recognisable for possession of `collidable` attribute of `Collidable` class.  

There are in total 2 relevant Collidable Entities.

- AgentEntity 
- LavaEntity  

&nbsp;
#### [AgentEntity](../player-guide/entities.md#agent)
This is the entity controlled by the user.

|Attribute|Type|Description|
|---|---|---|
|health|Health Class|Health to give the agent, constitutes Max and current health|
|inventory_list|Inventory Class|List of Entity that represents the Agent's inventory|
|status_list|Status Class|List of Entity that represents the statuses active on the agent|

|Available Methods|Inputs|Description|
|---|---|---|
|set_health|health: int|Sets the agent's health|

&nbsp;
#### [LavaEntity](../player-guide/entities.md#lava)
This is a damaging entity that the agent can walk through.

&nbsp;

### BlockingEntity
These are entities which cannot be passed through by Collidable Entities. These entities are recognisable for possession of `blocking` attribute of `Blocking` class.  

There are in total 3 relevant BlockingEntity. 

- WallEntity
- LockedDoorEntity 
- BoxEntity  

&nbsp;

### PushableEntity
These are entities which are pushable by the Agent. These entities are recognisable for possession of `pushable` attribute of `Pushable` class. 

There is 1 relevant pushable entity, [BoxEntity](#boxentity)

&nbsp;
#### [WallEntity](../player-guide/entities.md#wall)
This is a wall entity that the agent cannot walk through or push. The wall entity has no attributes.

&nbsp;
#### [BoxEntity](../player-guide/entities.md#box)
This is a pushable blocking entity that the agent can push but not walk through. The box entity has no attributes.

Note: that the box is both [Blocking](#blockingentity) and a [Pushable](#pushableentity) Entity

&nbsp;
#### [LockedDoorEntity](../player-guide/entities.md#door)
This is a blocking entity that the agent cannot push through or push. This entity becomes a [UnlockedDoorEntity](#unlockeddoorentity), when a [KeyEntity](#keyentity) is used on it

|Attribute|Type|Description|
|---|---|---|
|locked|Locked Class|Locked door that can be unlocked by a Key|

Note: Each level can have multiple key - door pairs. Any key can be used to unlock a door, but each key can only be used once.

&nbsp;

### CollectibleEntity
These are entities which are collectible by the agent. These entities are recognisable for possession of `collectible` attribute of `Collectible` class. 

There are in total 6 relevant CollectibleEntity.

- CoinEntity
- GemEntity
- KeyEntity
- SpeedPowerUpEntity
- ShieldPowerUpEntity
- PhasingPowerUpEntity  

&nbsp;
#### [CoinEntity](../player-guide/entities.md#coin)
This is an **optional** collectible that provides a score when collected by the agent. 

|Attribute|Type|Description|
|---|---|---|
|rewardable|Rewardable Class|The score provided for picking up the coin|

Note: Score received for collecting a coin is fixed at 5.

&nbsp;
#### [GemEntity](../player-guide/entities.md#gem)
This is a **compulsory** collectible to be collected by agent before it can enter the exit. The GemEntity has no attributes.


&nbsp;
#### [KeyEntity](../player-guide/entities.md#key)
This is a collectible required to unlock a [LockedDoorEntity](#lockeddoorentity)

|Attribute|Type|Description|
|---|---|---|
|key|Key Class|Key class that can be used to unlock LockedDoorEntity|

Note: Any key present in the grid can be used to unlock a door, but each key can only be used once.

&nbsp;
#### [SpeedPowerUpEntity](../player-guide/entities.md#powerup-speed)
This is a collectible power-up granting agent the ability to walk 2 tiles in 1 turn for a duration of time.

|Attribute|Type|Description|
|---|---|---|
|speed|Speed Class|Speed class that saves multiplier, indicating speed up provided|
|time_limit|TimeLimit Class|TimeLimit class that saves amount, indicating number of turns powerup is active|

Note: Time limit is a constant at 5 steps.

&nbsp;
#### [ShieldPowerUpEntity](../player-guide/entities.md#powerup-shield)
This is a collectible power-up granting agent immunity while walking on damaging tiles for 5 uses.

|Attribute|Type|Description|
|---|---|---|
|usage_limit|UsageLimit Class|UsageLimit class that shows durability of the shield|

Note: Usage limit is a constant at 5 uses.

&nbsp;
#### [PhasingPowerUpEntity](../player-guide/entities.md#powerup-phasing)
This is a collectible power-up granting agent ability to walk through [BlockingEntity](#blockingentity) for a duration of time.

|Attribute|Type|Description|
|---|---|---|
|time_limit|TimeLimit Class|TimeLimit class that saves amount, indicating number of turns powerup is active|

Note: Time limit is a constant at 5 steps.

&nbsp;
#### Other Entities
These Entities extend directly from BaseEntity. They are either non interactable entities which are purely for aesthetic purposes, or in the case of ExitEntity & FloorEntity, entities with special purposes.

&nbsp;
#### [ExitEntity](../player-guide/entities.md#exit)
This serves as the final tile the agent has to reach to complete the objective. The ExitEntity has no other attributes.

&nbsp;
#### [FloorEntity](../player-guide/entities.md#floor)
Floor entities are not interactable with the agent.

&nbsp;
#### [UnlockedDoorEntity](../player-guide/entities.md#door)
UnlockedDoorEntity is not interactable with agent and serves only an aesthetic purpose. It is the unlocked version of the [LockedDoorEntity](#lockeddoorentity). The UnlockedDoorEntity has no attributes.

&nbsp;
## Usage Example
 Use the code examples given below to familiarise yourself on the `State` representation and explore the different components.

--- 

### Useful Operations

- **Get agent ID**
  ```python
  next(iter(state.agent.keys()), None)
  ```

- **Lookup components by EntityId**
  ```python
  state.position.get(eid)
  eid in state.blocking
  ```

- **Iterate entities in a cell**  
  Invert `state.position` to obtain a mapping of:
  ```text
  Position -> [EntityID]
  ```

- **Sparse debug view**
  ```python
  state.description
  ```
  Returns a `PMap` containing only populated component stores.

- **Apply an action**
  ```python
  step(State, Action) -> State
---

### Full Example

```python
from grid_adventure.step import step

# Creation of the grid still requires use of GridState
gridstate = GridState(width=4, height=3, movement=MOVEMENTS["cardinal"], objective=OBJECTIVES["collect_gems_and_exit"], seed=0,)
for y in range(gridstate.height):
    for x in range(gridstate.width):
        gridstate.add((x, y), FloorEntity())
# Add an agent entity, box and exit to the grid
gridstate.add((0, 1), AgentEntity())
gridstate.add((1,1), BoxEntity())
gristate.add((3,1), ExitEntity())

# Convert GridState to the immutable State representation
state = to_state(gridstate)

# state.description contains only populated component stores
# (e.g. position, agent, blocking, etc.)

# state.position maps EntityID -> (x, y) coordinates and can be used to locate entities in the grid

# Retrieve the agent's EntityID
agent_id = next(iter(state.agent.keys()))
box_entity_ids = list(state.pushable.keys()) # Find all entities that are pushable. Since only 1 box is added, it contains the entity id of the box
box_id = box_entity_ids[0]

# Look up current position
agent_position = state.position.get(agent_id) #(0,1)
box_position = state.position.get(box_id) #(1,1)

# Check whether the entity is considered blocking
is__agent_blocking = agent_id in state.blocking # False
is_box_blocking = box_id in state.blocking # True

# Apply an action using step. step returns a new State
state = step(state, Action.RIGHT)

# After stepping, the agent's position in state_3_1.position is updated
new_agent_position = state.position.get(agent_id) #(1,1)
```