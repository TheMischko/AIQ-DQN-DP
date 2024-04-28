# Agent reference module
- To add a new agent for parameter search you need to create a new class in this module.
- Each new agent should implement [AgentReference](AgentReference.py) base class.
  - Implement `get_test_agent_name` to return name of the AIQ agent.
  - Implement `get_generators` so it returns array of function that generates parameters for the AIQ agent.
    - It is important that these functions are in the same order as final parameters will be.

## [Q_l agent](Q_l.py) example
- The original [AIQ agent](../../agents/Q_l.py) has this constructor:
```python
class Q_l(Agent):
    def __init__( self, refm, disc_rate, init_Q, Lambda, alpha, epsilon, gamma=0 ):
        ...
```
- First two parameters (`refm` and `disc_rate`) are provided automatically from AIQ test.
- We need to implement generators for the rest.
- Some naive solution can look like this:
```python
    def get_generators(self):
        return [
            lambda: random.randint(1, 100) / 100, # init_Q
            lambda: random.randint(1, 100) / 100, # Lambda
            lambda: random.randint(1, 100) / 100, # alpha
            lambda: random.randint(1, 100) / 100, # epsilon
            lambda: random.randint(1, 100) / 100, # gamma
        ]
```
- First lambda function will be used to create first parameter, so `init_Q`.
- Second function will be used for second parameter, so `Lambda`.

- We also need to create reference to the AIQ agent.
- As we can see that class name is `Q_l`, so we need to implement `get_test_agent_name` so it return this name.
```python
    def get_test_agent_name(self):
        return "Q_l"
```

- After that we can use `Q_l` agent in genetic algorithm like this:
```bash
python FindParamsGenetic.py -a Q_l ...
```
- `-a` value is used to find reference in this module.
- So you can create multiple configuration for the same agent if you reference the AIQ agent correctly and name the classes in this module differently.