# Game Representation

Grid Adventure operates as a turn based game. Players are supplied a snapshot of a turn of the Game. Players then return an action, which is then used to generate the snapshot.

## Types of representation
There are 3 ways for a Game Snapshot to be represented.

| Representation Type | Description |
| --- | --- |
| GridState Representation | A grid based representation using 2D Array. This is the most intuitive Representation. |
| Observation Representation | An RGBA Image representation using #D Array, accompanied  additional info stored in an Information Dictionary |
| State Representation | An Immutable world state. This is the most Comprehensive, but low level representation |

**Note**: The Capstone Project can be solved without using the **State Representation**.

&nbsp;
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
| `grid` | `list[list[list[BaseEntity]]]` | 2D array where `grid[y][x]` is a list of entities at that cell |

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
| `GridState.remove_if(pos, predicate)` | `int` | Remove entities where `predicate(obj)` is `True`; returns count |
| `GridState.move_obj(from_pos, obj, to_pos)` | `bool` | Move entity between cells; returns `True` if successful |
| `GridState.clear_cell(pos)` | `int` | Remove all entities from cell; returns count |
| `GridState.objects_at(pos)` | `list[BaseEntity]` | Return shallow copy of entities at position |
| `step(gridState, action)` | `GridState` | Generates new `GridState` with action |
| `to_state(gridState)` | `None` | Converts mutable `gridState` to immutable `State` |

Note: `pos` is of class `Position`, a (int, int)  
Note: `obj` is of class `BaseEntity`, parent class of all Entities. For more details about entities, Please refer to [Entity Classes](entities.md#entities).

&nbsp;
# Observation Representation
The observation representation is created by the grid Adventures game engine, and is non reversible. Players are not able to convert observation representation into Level or State representation.

## Observation Attribute Hierachy
The observation Class represents the Game snapshot as a dictionary with the following hierachy.

```
Observation: TypedDict
├── image: ndarray[H, W, 4] (uint8)
│   └── RGBA pixel data for rendered grid
│
└── info: InfoDict #Dictionary subclass
    │
    ├── agent: AgentInfo #Dictionary subclass
    │   │
    │   ├── health: HealthInfo #Dictionary subclass
    │   │   ├── current_health: int (-1 if missing)
    │   │   └── max_health: int (-1 if missing)
    │   │
    │   ├── effects: list[EffectEntry]
    │   │   └── [each entry]
    │   │       ├── id: int
    │   │       ├── type: str ("" | "IMMUNITY" | "PHASING" | "SPEED")
    │   │       ├── limit_type: str ("" | "TIME" | "USAGE")
    │   │       ├── limit_amount: int (-1 if unlimited)
    │   │       └── multiplier: int (-1 if not SPEED)
    │   │
    │   └── inventory: list[InventoryItem]
    │       └── [each item]
    │           ├── id: int
    │           ├── type: str ("key" | "core" | "coin" | "item")
    │           ├── key_id: str ("" if not a key)
    │           └── appearance_name: str ("" if unknown)
    │
    ├── status: StatusInfo #Dictionary subclass
    │   ├── score: int
    │   ├── phase: str ("ongoing" | "win" | "lose")
    │   └── turn: int
    │
    ├── config: ConfigInfo #Dictionary subclass
    │   ├── movement: str (movement function name)
    │   ├── objective: str (objective function name)
    │   ├── seed: int (-1 if None)
    │   ├── width: int
    │   ├── height: int
    │   └── turn_limit: int (-1 if unlimited)
    │
    └── message: str ("" if None)
```

&nbsp;
## Image Usage Example
```python
from grid_adventure.gym_env import GridAdventureEnv
from grid_adventure.examples.maze import generate

env = GridAdventureEnv(
    initial_state_fn=generate,
    width=9,
    height=9
)
obs, info = env.reset()

image = obs["image"]  # shape: (H, W, 4), dtype: uint8

# Get image dimensions
height, width, channels = image.shape

# Save as PNG
from PIL import Image
pil_image = Image.fromarray(image)
pil_image.save("screenshot.png")

# Display with matplotlib
import matplotlib.pyplot as plt
plt.imshow(image)
plt.axis("off")
plt.show()

# Stack frames for temporal context (e.g., last 4 frames)
frame_stack = np.stack([obs1["image"], obs2["image"], obs3["image"], obs4["image"]], axis=0)
```


&nbsp;
## InfoDict Usage Example

```python
from grid_adventure.gym_env import GridAdventureEnv
from grid_adventure.examples.maze import generate

env = GridAdventureEnv(
    initial_state_fn=generate,
    width=9,
    height=9
)
obs, info = env.reset()

# Access the rendered image
image = obs["image"]  # shape: (H, W, 4), dtype: uint8

# Access agent health
current_health = obs["info"]["agent"]["health"]["current_health"]
max_hp = obs["info"]["agent"]["health"]["max_health"]

# Check game phase
phase = obs["info"]["status"]["phase"]  # "ongoing", "win", or "lose"

# Get active effects
for effect in obs["info"]["agent"]["effects"]:
    print(f"Effect {effect['type']}: {effect['limit_amount']} remaining")

# Check inventory
for item in obs["info"]["agent"]["inventory"]:
    print(f"Item: {item['type']} (id={item['id']})")
```


&nbsp;
# State Representation
The state representation is the same internal representation used by the Grid Adventure game engine, stores information in various attributes, tracked by EntityID of each Entity. It is the most comprehensive of the 3 representations, and the used to generate the Level and Observation representations. 

## WARNING ON STATE SPACE
The Capstone Project can be solved without using the **State Representation**, however the State Representation is included for a lower level acess to the representation.

## State Attributes
The state Class represents the Game snapshot with the following 4 types of attributes.

- Level Configuration
- Effect Configuration
- Property Componenets
- Game Status

### Level Configuration

| Attribute | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Grid width in tiles |
| `height` | `int` | Grid height in tiles |
| `movement` | `BaseMovement` | Movement functions allowed |
| `objective` | `BaseObjective` | Objective of the level |

### Effect Components

All effect stores are `PMap[EntityID, Component]`.  
Note: `PMap` is an Immutable Dictionary, dictionary methods are available.

| Attribute | Mapped Component | Description |
|-----------|-----------|-------------|
| `immunity` | `Immunity` | Damage immunity effects |
| `phasing` | `Phasing` | Pass-through-walls effects |
| `speed` | `Speed` | Movement multiplier effects |
| `time_limit` | `TimeLimit` | Effect duration (remaining steps) |
| `usage_limit` | `UsageLimit` | Effect uses (remaining count) |

### Property Components

All property stores are `PMap[EntityID, Component]`.  
Note: `PMap` is an Immutable Dictionary, dictionary methods are available.

| Attribute | Mapped Component | Description |
|-----------|-----------|-------------|
| `agent` | `Agent` | Player-controlled entities |
| `appearance` | `Appearance` | Visual rendering properties |
| `blocking` | `Blocking` | Obstacles that block movement |
| `collectible` | `Collectible` | Items that can be picked up |
| `collidable` | `Collidable` | Entities triggering collision events |
| `cost` | `Cost` | Entities that inflict movement cost |
| `damage` | `Damage` | Entities that deal damage on contact |
| `dead` | `Dead` | Dead/incapacitated entities |
| `exit` | `Exit` | Level exit points |
| `health` | `Health` | Entity health (current/max) |
| `inventory` | `Inventory` | Items held by entities |
| `key` | `Key` | Keys that unlock `Locked` entities |
| `lethal_damage` | `LethalDamage` | Instant-kill damage sources |
| `locked` | `Locked` | Locked doors/entities |
| `position` | `Position` | Entity grid positions |
| `pushable` | `Pushable` | Entities that can be pushed |
| `requirable` | `Requirable` | Must-collect items for objectives |
| `rewardable` | `Rewardable` | Entities granting score rewards |
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

&nbsp;
## Usage Example
All effects and components are represented by Entities in the Grid Adventure game engine. Each entity is assigned a unique EntityID at creation. This EntityID is used to map to each attribute of the Entity. For more details about entities, Please refer to [Entity Classes](entities.md#entities).

---                                                                                                                                                                               
Example 1: Player Entity
                                                                
A player entity with EntityID = 1 that has position, health, appearance, and agent components:  
    
&emsp;&emsp;state.position[1]   = Position(x=3, y=5)  
&emsp;&emsp;state.health[1]     = Health(health=100, max_health=100)  
&emsp;&emsp;state.appearance[1] = Appearance(name="human", priority=10)  
&emsp;&emsp;state.agent[1]      = Agent()  
&emsp;&emsp;state.inventory[1]  = Inventory(item_ids=pset([2, 3]))  # holds items 2 and 3   

The same EntityID appears in multiple component stores, each holding a different aspect of that entity.

---
Example 2: Status Effect Entity

An immunity effect with EntityID = 50 applied to the player (EntityID = 1):

&emsp;&emsp;state.immunity[50]   = Immunity()  
&emsp;&emsp;state.time_limit[50] = TimeLimit(amount=10)  # lasts 10 turns  
&emsp;&emsp;state.status[1]      = Status(effect_ids=pset([50]))  # player has effect 50  

The effect itself is an entity (EntityID = 50) stored in immunity and time_limit. The player's status component references this effect by its ID.

---

## Useful Methods

| Method | Description |
|--------|-------------|
| `state.description` | Property returning `PMap` of all non-empty state attributes |
| `from_state(state)` | Converts immutable `State` to mutable `Level` |
