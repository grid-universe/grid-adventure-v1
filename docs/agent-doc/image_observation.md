
# ImageObservation Representation
The ImageObservation representation is created by Grid Adventure. It contains a 3D image array with additional information in a dictionary.

For how the rules on how the image is rendered, refer to [Image Rendering](rendering.md).

## ImageObservation Attribute Hierarchy
The ImageObservation Class represents the game snapshot as a dictionary with the following hierarchy.

```
ImageObservation: TypedDict
├── image: ndarray[H, W, 4] (uint8)
│   └── RGBA pixel data for the rendered grid
│
└── info: InfoDict # Dictionary subclass
    │
    ├── agent: AgentInfo # Dictionary subclass
    │   │
    │   ├── health: HealthInfo # Dictionary subclass
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
    │           ├── type: str ("key" | "gem" | "coin" | "item")
    │           └── appearance_name: str ("" if unknown)
    │
    ├── status: StatusInfo # Dictionary subclass
    │   ├── score: int
    │   ├── phase: str ("ongoing" | "win" | "lose")
    │   └── turn: int
    │
    ├── config: ConfigInfo # Dictionary subclass
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
import numpy as np

env = GridAdventureEnv(
    initial_state_fn=generate,
    width=9,
    height=9
)
obs, info = env.reset()

image = obs["image"]  # Shape: (H, W, 4), dtype: uint8

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

# Access the rendered image data
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