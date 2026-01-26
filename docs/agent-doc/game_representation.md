# Game Representation

Grid Adventure V1 operates as a turn based game. Players are supplied with a snapshot of a turn of the game. Players then return an action, which is then used to generate the snapshot of the game after the action is made.

## Representation types
There are 3 ways for a Game Snapshot to be represented.

| Representation Type | Description |
| --- | --- |
| [GridState](gridstate.md) | A grid based representation using a 2D Array. This is the most intuitive representation. |
| [ImageObservation](image_observation.md) | An RGBA Image representation using a 3D Array, with additional info stored in an information dictionary |
| [State](state.md) | An Immutable world state. This is the most comprehensive, but low level representation |

**Note**: The Capstone Project can be solved without using the **State Representation**.
