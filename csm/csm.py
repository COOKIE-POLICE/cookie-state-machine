class StateMachine:
    def __init__(self, name="UnnamedStateMachine"):
        self.name = name
        self.states = {}
        self.transitions = {}
        self.current_state = None
        self.context = {}
        self.is_paused = False

    def add_state(self, name, state):
        self.states[name] = state

    def set_initial_state(self, name):
        self.current_state = name
        state = self.states.get(name)
        if state and hasattr(state, "on_enter"):
            state.on_enter(self)

    def get_current_state(self):
        return self.current_state

    def is_in_state(self, name):
        return self.current_state == name

    def force_state(self, name):
        self.change_state(name)

    def add_transition(self, from_state, to_state, condition):
        if from_state not in self.transitions:
            self.transitions[from_state] = []
        self.transitions[from_state].append({"to": to_state, "condition": condition})

    def clear_transitions(self):
        self.transitions.clear()

    def can_transition_to(self, state_name):
        possible = self.transitions.get(self.current_state, [])
        return any(t["to"] == state_name and t["condition"](self) for t in possible)

    def get_available_transitions(self):
        possible = self.transitions.get(self.current_state, [])
        return [t["to"] for t in possible if t["condition"](self)]

    def change_state(self, new_state_name):
        old_state = self.states.get(self.current_state)
        if old_state and hasattr(old_state, "on_exit"):
            old_state.on_exit(self)
        self.current_state = new_state_name
        new_state = self.states.get(new_state_name)
        if new_state and hasattr(new_state, "on_enter"):
            new_state.on_enter(self)

    def set_context(self, context):
        self.context = context

    def update(self, dt):
        if self.is_paused:
            return
        state = self.states.get(self.current_state)
        if state and hasattr(state, "on_update"):
            state.on_update(self, dt)
        possible = self.transitions.get(self.current_state, [])
        for transition in possible:
            if transition["condition"](self):
                self.change_state(transition["to"])
                break

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def clone(self):
        from copy import deepcopy

        copy = StateMachine(self.name)
        copy.states = self.states.copy()
        copy.transitions = deepcopy(self.transitions)
        copy.context = deepcopy(self.context)
        copy.current_state = self.current_state
        return copy

    def print_current_state(self):
        print(f"[{self.name}] Current State: {self.current_state}")

    def print_available_transitions(self):
        available = self.get_available_transitions()
        print(f"[{self.name}] Available Transitions from {self.current_state}:")
        for to_state in available:
            print(f"  → {to_state}")

    def print_transitions(self):
        print(f"[{self.name}] All Transitions:")
        for from_state, transitions in self.transitions.items():
            for t in transitions:
                print(f"  {from_state} → {t['to']}")


if __name__ == "__main__":
    import time

    class IdleState:
        def on_enter(self, machine):
            print("Entering Idle")

        def on_update(self, machine, dt):
            print(f"Idle... ({dt}s)")

        def on_exit(self, machine):
            print("Exiting Idle")

    class MovingState:
        def on_enter(self, machine):
            print("Entering Moving")

        def on_update(self, machine, dt):
            print(f"Moving... ({dt}s)")

        def on_exit(self, machine):
            print("Exiting Moving")

    sm = StateMachine("TestMachine")
    sm.add_state("Idle", IdleState())
    sm.add_state("Moving", MovingState())
    sm.add_transition("Idle", "Moving", lambda m: m.context.get("should_move", False))
    sm.add_transition(
        "Moving", "Idle", lambda m: not m.context.get("should_move", False)
    )
    sm.set_initial_state("Idle")
    sm.set_context({"should_move": False})

    for i in range(5):
        sm.update(0.016)
        if i == 2:
            print("→ Triggering move")
            sm.context["should_move"] = True
        if i == 4:
            print("→ Stopping move")
            sm.context["should_move"] = False
        time.sleep(0.5)
