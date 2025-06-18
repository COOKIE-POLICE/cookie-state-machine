
---

# Cookie-State-Machine (CSM)

This is the best Python finite state machine library. Totally not biased.

---

## Table of Contents And Stuff

- [Cookie-State-Machine (CSM)](#cookie-state-machine-csm)
  - [Table of Contents And Stuff](#table-of-contents-and-stuff)
  - [Installation](#installation)
  - [How to Use](#how-to-use)
    - [Import the Library](#import-the-library)
  - [Basic Stuff](#basic-stuff)
    - [Define Your State Classes](#define-your-state-classes)
    - [Create a StateMachine](#create-a-statemachine)
    - [Add States](#add-states)
    - [Set the Initial State](#set-the-initial-state)
    - [Add Transitions](#add-transitions)
    - [Set Context (Optional)](#set-context-optional)
    - [Run the Update Loop](#run-the-update-loop)
  - [Available Methods](#available-methods)
  - [Example](#example)
  - [Notes](#notes)

---

## Installation

```bash
pip install git+https://github.com/COOKIE-POLICE/cookie-state-machine.git
```

---

## How to Use

### Import the Library

```python
import csm
```

---

## Basic Stuff

### Define Your State Classes

Each state is a class with optional lifecycle methods.

```python
class IdleState:
    def on_enter(self, state_machine):
        print("Entering Idle")

    def on_update(self, state_machine, delta_time):
        print(f"Idling... ({delta_time}s)")

    def on_exit(self, state_machine):
        print("Exiting Idle")
```

* `on_enter(state_machine)` — called when the state is entered.
* `on_update(state_machine, delta_time)` — called every update.
* `on_exit(state_machine)` — called when leaving the state.

---

### Create a StateMachine

```python
state_machine = csm.StateMachine("MyStateMachine")
```

* `name` — optional string for debugging/logging.

---

### Add States

```python
state_machine.add_state("Idle", IdleState())
```

---

### Set the Initial State

```python
state_machine.set_initial_state("Idle")
```

---

### Add Transitions

Add conditional transitions between states.

```python
state_machine.add_transition("Idle", "Moving", lambda sm: sm.context.get("should_move", False))

state_machine.add_transition(
    ["Idle", "Moving"],
    "Reset",
    lambda sm: sm.context.get("force_reset", False)
)
```

Each transition has:

* `from_state` — name of the origin state or list of them
* `to_state` — name of the target state
* `condition(state_machine)` — function that returns `True` to trigger the transition

---

### Set Context (Optional)

A context is a shared dictionary attached to the state machine.

```python
state_machine.set_context({"should_move": False})
```

You can read and modify it anytime like a normal dictionary.

```python
state_machine.context["should_move"] = True
```

---

### Run the Update Loop

Call `update(delta_time)` regularly to process state logic and check transitions.

```python
state_machine.update(0.016)
```

---

## Available Methods

| Method                                            | Description                                              |
| :------------------------------------------------ | :------------------------------------------------------- |
| `add_state(name, state)`                          | Adds a new state object                                  |
| `set_initial_state(name)`                         | Sets the starting state                                  |
| `add_transition(from_state, to_state, condition)` | Defines a conditional transition                         |
| `set_context(context_dictionary)`                 | Sets the shared context dictionary                       |
| `update(delta_time)`                              | Calls current state's `on_update` and checks transitions |
| `force_state(name)` / `change_state(name)`        | Instantly switches to a state                            |
| `pause()` / `resume()`                            | Temporarily stops/resumes update calls                   |
| `clone()`                                         | Deep copies the state machine                            |
| `print_current_state()`                           | Logs the current state                                   |
| `print_transitions()`                             | Logs all transitions                                     |
| `print_available_transitions()`                   | Logs currently valid transitions                         |
| `get_current_state()`                             | Returns current state name                               |
| `is_in_state(name)`                               | Returns `True` if currently in the given state           |
| `can_transition_to(name)`                         | Checks if a transition to a state is currently possible  |
| `get_available_transitions()`                     | Returns list of allowed target states                    |
| `clear_transitions()`                             | Removes all transitions                                  |

---

## Example

```python
import csm
import time

class IdleState:
    def on_enter(self, sm): print("→ Entering Idle")
    def on_update(self, sm, dt): print("Idle...", dt)
    def on_exit(self, sm): print("→ Exiting Idle")

class MovingState:
    def on_enter(self, sm): print("→ Entering Moving")
    def on_update(self, sm, dt): print("Moving...", dt)
    def on_exit(self, sm): print("→ Exiting Moving")

sm = csm.StateMachine("DemoMachine")
sm.add_state("Idle", IdleState())
sm.add_state("Moving", MovingState())

sm.add_transition("Idle", "Moving", lambda sm: sm.context.get("should_move", False))
sm.add_transition("Moving", "Idle", lambda sm: not sm.context.get("should_move", False))

sm.set_initial_state("Idle")
sm.set_context({"should_move": False})

for frame in range(5):
    sm.update(0.016)
    if frame == 2:
        sm.context["should_move"] = True
        print("→ Moving enabled")
    if frame == 4:
        sm.context["should_move"] = False
        print("→ Moving disabled")
    time.sleep(0.5)
```

---

## Notes

* Transitions are evaluated in the order you added them.
* You don't really need a delta time (Dt), just pass in 1 if you arent going to use it.

---