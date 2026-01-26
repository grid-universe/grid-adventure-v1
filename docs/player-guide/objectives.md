The objective for Grid Adventure: V1 is to complete the following tasks:

- If any gems are present in the grid, collect all of them  
- Move to the exit tile

## Optimal Solution

An optimal solution achieves all objectives while maximising the total reward. There is no requirement to finish with nonnegative reward or maximum HP. To achieve a higher reward, the agent should either complete the level in fewer turns or collect more coins.

### Reward
- Each turn taken by the agent incurs a reward of -3.
- Each coin collected provides a reward of 5.
