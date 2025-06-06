
---

# 🛠️ Cookie-State-Machine (CSM)

**Cookie-State-Machine (CSM)** is the best Python FSM library (Totally not biased).

---

## 📦 Installation

```bash
pip install git+https://github.com/COOKIE-POLICE/cookie-state-machine.git
```

---

## 📖 How to Use

### 📥 Import the Library

```python
import csm
```

---

## 📌 Basic Workflow

### 1️⃣ Define Your State Classes

Each state is a class with optional lifecycle methods:

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
* `on_update(state_machine, delta_time)` — called every update cycle.
* `on_exit(state_machine)` — called when leaving the state.

---

### 2️⃣ Create a StateMachine

```python
state_machine = csm.StateMachine("MyStateMachine")
```

* `name` — (optional) identifier string for debugging/logging.

---

### 3️⃣ Add States

```python
state_machine.add_state("Idle", IdleState())
```

---

### 4️⃣ Set the Initial State

```python
state_machine.set_initial_state("Idle")
```

---

### 5️⃣ Add Transitions

Add conditional transitions between states:

```python
state_machine.add_transition("Idle", "Moving", lambda state_machine: state_machine.context.get("should_move", False))
```

Each transition has:

* `from_state` — name of the origin state
* `to_state` — name of the target state
* `condition(state_machine)` — function that returns `True` to trigger the transition

---

### 6️⃣ Set Context (Optional)

A **context** is a shared dictionary attached to the state machine.
It’s accessible to all states and transition conditions. Use it to store any dynamic values or flags your states and transitions might rely on.

**Example:**

```python
state_machine.set_context({"should_move": False})
```

You can read and modify `context` anytime like a normal dictionary:

```python
state_machine.context["should_move"] = True
```

States and conditions can access it via `state_machine.context`.

---

### 7️⃣ Run the Update Loop

Call `update(delta_time)` regularly to process state logic and check for transitions.

```python
state_machine.update(0.016)  # delta_time in seconds (e.g., 0.016 for 60 FPS)
```

---

## 📝 Available Methods

| Method                                            | Description                                                |
| :------------------------------------------------ | :--------------------------------------------------------- |
| `add_state(name, state)`                          | Adds a new state object                                    |
| `set_initial_state(name)`                         | Sets the starting state                                    |
| `add_transition(from_state, to_state, condition)` | Defines a conditional state transition                     |
| `set_context(context_dictionary)`                 | Initializes the shared context dictionary                  |
| `update(delta_time)`                              | Calls current state's `on_update` and checks transitions   |
| `force_state(name)`                               | Immediately switches to a specific state                   |
| `pause()` / `resume()`                            | Temporarily halts and resumes updates                      |
| `clone()`                                         | Deep copies the state machine                              |
| `print_current_state()`                           | Logs the current state                                     |
| `print_transitions()`                             | Logs all transitions                                       |
| `print_available_transitions()`                   | Logs transitions currently available from current state    |
| `get_current_state()`                             | Returns current state name                                 |
| `is_in_state(name)`                               | Returns `True` if currently in the given state             |
| `can_transition_to(name)`                         | Checks if a transition to a state is currently possible    |
| `get_available_transitions()`                     | Returns a list of allowed target states from current state |
| `clear_transitions()`                             | Removes all transitions                                    |

---

## 📌 Example Run

```python
import csm
import time

class IdleState:
    def on_enter(self, state_machine): print("→ Entering Idle")
    def on_update(self, state_machine, delta_time): print("Idle...", delta_time)
    def on_exit(self, state_machine): print("→ Exiting Idle")

class MovingState:
    def on_enter(self, state_machine): print("→ Entering Moving")
    def on_update(self, state_machine, delta_time): print("Moving...", delta_time)
    def on_exit(self, state_machine): print("→ Exiting Moving")

state_machine = csm.StateMachine("DemoMachine")
state_machine.add_state("Idle", IdleState())
state_machine.add_state("Moving", MovingState())

state_machine.add_transition("Idle", "Moving", lambda state_machine: state_machine.context.get("should_move", False))
state_machine.add_transition("Moving", "Idle", lambda state_machine: not state_machine.context.get("should_move", False))

state_machine.set_initial_state("Idle")
state_machine.set_context({"should_move": False})

for frame in range(5):
    state_machine.update(0.016)
    if frame == 2:
        state_machine.context["should_move"] = True
        print("→ Moving enabled")
    if frame == 4:
        state_machine.context["should_move"] = False
        print("→ Moving disabled")
    time.sleep(0.5)
```

**Sample Output:**

```
→ Entering Idle
Idle... 0.016
Idle... 0.016
→ Moving enabled
→ Exiting Idle
→ Entering Moving
Moving... 0.016
Moving... 0.016
→ Moving disabled
→ Exiting Moving
→ Entering Idle
Idle... 0.016
```

---

## 🧩 Notes

* Transitions are evaluated in the order they were added.
* `on_enter` and `on_exit` methods are optional in each state.

---