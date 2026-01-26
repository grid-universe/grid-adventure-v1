# State Representation
The state representation is the same internal representation used by the Grid Adventure game, stores information in various attributes, tracked by EntityID of each Entity. It is the most comprehensive of the 3 representations, and the used to generate the GridState and Observation representations. 

!!! warning "WARNING ON STATE SPACE"
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
| `agent` | [`Agent`](#agententity) | Player-controlled entities |
| `appearance` | `Appearance` | Visual rendering properties |
| `blocking` | [`Blocking`](entities.md#blockingentity) | Obstacles that block movement |
| `collectible` | [`Collectible`](#collectibleentity) | Items that can be picked up |
| `collidable` | [`Collidable`](#collidable-entities) | Entities triggering collision events |
| `cost` | `Cost` | Entities that inflict movement cost |
| `damage` | [`Damage`](#lava-entity) | Entities that deal damage on contact |
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
## Entity list and Attributes
&nbsp;

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
This are entities which can pass through each other but will trigger interactions when this happens. These entities are recognisable for possession of `collidable` attribute of `Collidable` class.  

There are in total 2 relevant Collidable Entities.

- AgentEntity 
- LavaEntity  

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
#### Lava Entity
This is a damaging entity that the agent can walk through

Note: Lava has a fixed Damage of 2.

&nbsp;

### BlockingEntity
This are entities which cannot be passed through by Collidable Entities. These entities are recognisable for possession of `blocking` attribute of `Blocking` class.  

There are in total 3 relevant BlockingEntity. 

- WallEntity
- LockedDoorEntity 
- BoxEntity  

Note that the Box is also a PushableEntity.  

&nbsp;
#### WallEntity
This is a wall entity that the agent cannot walk through nor push. The wall entity has no atributes.

&nbsp;
#### BoxEntity
This is a movable blocking entity, that the agent can push but not walk through. The box entity has no attributes.

Note: that the box is also a Pushable Entity

&nbsp;
#### LockedDoorEntity
This is a blocking entity that the agent cannot push through nor push. This entity becomes a [UnlockedDoorEntity](#unlockeddoorentity), when a [KeyEntity](#keyentity) is used on it

|Attribute|Type|Description|
|---|---|---|
|locked|Locked Class|Locked door that can be unlocked by a Key|

Note: Each level can have multiple key - door pairs. Any key can be used to unlock a door, but each key can only be used once.

&nbsp;

### PushableEntity
This are entities which are pushable by the Agent. These entities are recognisable for possession of `pushable` attribute of `Pushable` class. 

There is only 1 relevant PushableEntity, it is the BoxEntity. For documentation of box, see the [BoxEntity](#boxentity).

&nbsp;

### CollectibleEntity
This are entities which are collectable by the Agent. These entities are recognisable for possession of `collectible` attribute of `Collectible` class. 

There are in total 6 relevant CollectibleEntity.

- CoinEntity
- GemEntity
- KeyEntity
- SpeedPowerUpEntity
- ShieldPowerUpEntity
- PhasingPowerUpEntity  

&nbsp;
#### CoinEntity
This is an **optional** collectible that provides a score when collected by the agent. 

|Attribute|Type|Description|
|---|---|---|
|rewardable|Rewardable Class|The score provided for picking up the coin|

Note: Score received for collecting a coin is fixed at 5.

&nbsp;
#### GemEntity
This is a **compulsory** Collectible to be collected by agent before it can enter the exit. The GemEntity has no attributes.


&nbsp;
#### KeyEntity
This is a Collectible required to unlock a [LockedDoorEntity](#lockeddoorentity)

|Attribute|Type|Description|
|---|---|---|
|key|Key Class|Key class that can be used to unlock LockedDoorEntity|

Note: Any key present in the grid can be used to unlock a door, but each key can only be used once.

&nbsp;
#### SpeedPowerUpEntity
This is a collectible granting agent the ability to walk 2 tiles in 1 turn for a duration of time.

|Attribute|Type|Description|
|---|---|---|
|speed|Speed Class|Speed class that saves multiplier, indicating speed up provided|
|time_limit|TimeLimit Class|TimeLimit class that saves amount, indicating number of turns powerup is active|

Note: Time limit is a constant at 5 steps.

&nbsp;
#### ShieldPowerUpEntity
This is a collectible granting agent immunity while walking on damaging tiles for 5 uses.

|Attribute|Type|Description|
|---|---|---|
|usage_limit|UsageLimit Class|UsageLimit class that shows durability of the shield|

Note: Usage limit is a constant at 5 uses.

&nbsp;
#### PhasingPowerUpEntity
This is a collectible granting agent ability to walk through [BlockingEntity](#blockingentity) for a duration of time.

|Attribute|Type|Description|
|---|---|---|
|time_limit|TimeLimit Class|TimeLimit class that saves amount, indicating number of turns powerup is active|

Note: Time limit is a constant at 5 steps.

&nbsp;
#### Other Entities
These Entities extend directly from BaseEntity. They are either non interactable entities which are purely for aesthetic purposes, or in the case of ExitEntity & FloorEntity, entities with special purposes.

&nbsp;
#### ExitEntity
This are unique Exit Entity and serve as the exit objective. The ExitEntity has no other attributes.

&nbsp;
#### FloorEntity 
Floor entities are not interactable with agent.

&nbsp;
#### UnlockedDoorEntity 
UnlockedDoorEntity is not interactable with agent, serving only aesthetic purpose. It is the unlocked version of the [LockedDoorEntity](#lockeddoorentity). The UnlockedDoorEntity has no attributes.

&nbsp;
## Usage Example
All effects and components are represented by Entities in the Grid Adventure game. Each entity is assigned a unique EntityID at creation. This EntityID is used to map to each attribute of the Entity. For more details about entities, Please refer to [Entity Classes](entities.md#entities).

---                                                                                                                                                                               
Example 1: Player Entity
                                                                
A player entity with EntityID = 1 that has position, health, appearance, and agent components:  
    
&emsp;&emsp;state.position[1]   = Position(x=3, y=5)  
&emsp;&emsp;state.health[1]     = Health(health=100, max_health=100)  
&emsp;&emsp;state.appearance[1] = Appearance(name="human", priority=10)  
&emsp;&emsp;state.agent[1]      = AgentEntity()  
&emsp;&emsp;state.inventory[1]  = Inventory(item_ids=pset([2, 3]))  # holds items 2 and 3   

The same EntityID appears in multiple component stores, each holding a different aspect of that entity.

---
Example 2: Status Effect Entity

An immunity effect with EntityID = 50 applied to the player (EntityID = 1):

&emsp;&emsp;state.immunity[50]   = Immunity()  
&emsp;&emsp;state.time_limit[50] = TimeLimit(amount=10)  # lasts 10 turns  
&emsp;&emsp;state.status[1]      = Status(effect_ids=pset([50]))  # player has effect 50  

The effect itself is an entity (EntityID = 50) stored in immunity and time_limit. The player's status component references this effect by its ID.
