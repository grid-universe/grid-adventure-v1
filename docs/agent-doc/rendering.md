# Image Rendering

##
When the grid is rendered, the image will be populated with all the entities present. For more information on the different entities and their appearances, please refer to the [Player Guide](../player-guide/entities.md). An example of a rendered grid is shown below.

![Grid Example](../assets/grid_example.png)

## Rendering Constraints
It is given that all levels do not have any overlapping entities at the start. This is to reduce the possible states for the agent to consider when reading an `ImageObservation.image`. 

**Note**: The only exception is the overlap on `FloorEntity` with all other Entities.

## Overlapping Entities
### Agent with Collectible items
When overlapping Agent with collectible items such as Gem, Coin, Key or any Power Ups, the collectible item will be minimised and shown in the top left of the grid cell.

![Agent Overlapping with Collectible](../assets/rendering_agent_collectible.png)

### Agent or Box with Background Entities
When overlapping Agent with background entities, such as Lava, Unlocked Door, Exit & Floor, the Agent will be poitioned before the background entity.

![Agent Overlapping with Non Background entities](../assets/rendering_agent_background.png)