# 🛠️ Cookie-State-Machine (CSM)

Cookie-State-Machine (CSM) is a easy-to-use python state machine library inspired by Lua-State-Machine.

---

## 📦 Installation

pip install git+https://github.com/COOKIE-POLICE/cookie-state-machine.git

---

## 📖 How to Use

### 1️⃣ Define your machine configuration:

```python
import csm
config = {
    "initial": "green",
    "events": [
        { "name": "warn",  "from": "green",  "to": "yellow" },
        { "name": "panic", "from": "yellow", "to": "red"    },
        { "name": "calm",  "from": "red",    "to": "yellow" },
        { "name": "clear", "from": "yellow", "to": "green"  }
    ],
    "callbacks": {
        "onbeforewarn": lambda self, event, from_state, to_state, *args: print("Before warn", args),
        "leavegreen":   lambda self, event, from_state, to_state, *args: print("Leaving green", args),
        "enteryellow":  lambda self, event, from_state, to_state, *args: print("Entering yellow", args),
        "onafterwarn":  lambda self, event, from_state, to_state, *args: print("After warn", args)
    }
}
```

* **initial** — starting state
* **events** — possible transitions (`name`, `from`, `to`)
* **callbacks** (optional) — functions run at specific points:

  * `onbefore<Event>`
  * `leave<State>`
  * `enter<State>`
  * `onafter<Event>`

⚠️ **Optional callback parameters:**

* `self` — the state machine instance
* `event` — the event name
* `from_state` — state before the transition
* `to_state` — state after the transition
* `*args` — any additional arguments you pass when calling the event method

---

### 2️⃣ Create your Machine instance:

```python
fsm = CSM(config)
```

---

### 3️⃣ Call event methods:

```python
fsm.warn()
# transitions green → yellow
fsm.panic("killer bees")
# transitions yellow → red, passes extra argument to callbacks
fsm.calm()
# transitions red → yellow
fsm.clear("sedatives ready")
# transitions yellow → green, passes extra argument to callbacks
```

---

### 4️⃣ Check current state:

```python
if fsm.is_state("yellow"):
    print("Caution: yellow light")
```

---

## 📌 Example Run

```python
print(fsm.current_state)  # 'green'
fsm.warn()                # triggers callbacks and transitions to 'yellow'
print(fsm.current_state)  # 'yellow'
fsm.panic("killer bees")  # triggers callbacks, passes extra argument, transitions to 'red'
print(fsm.current_state)  # 'red'
```

---