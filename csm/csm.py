from collections.abc import Iterable


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
        def add_single_transition(from_state_name):
            if from_state_name not in self.transitions:
                self.transitions[from_state_name] = []
            self.transitions[from_state_name].append({
                "to": to_state,
                "condition": condition
            })

        if isinstance(from_state, Iterable) and not isinstance(from_state, (str, bytes)):
            for from_state_name in from_state:
                add_single_transition(from_state_name)
        else:
            add_single_transition(from_state)

    def clear_transitions(self):
        self.transitions.clear()

    def can_transition_to(self, state_name):
        possible_transitions = self.transitions.get(self.current_state, [])
        return any(
            transition["to"] == state_name and transition["condition"](self)
            for transition in possible_transitions
        )

    def get_available_transitions(self):
        possible_transitions = self.transitions.get(self.current_state, [])
        return [
            transition["to"]
            for transition in possible_transitions
            if transition["condition"](self)
        ]

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

        possible_transitions = self.transitions.get(self.current_state, [])
        for transition in possible_transitions:
            if transition["condition"](self):
                self.change_state(transition["to"])
                break

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def clone(self):
        from copy import deepcopy

        new_machine = StateMachine(self.name)
        new_machine.states = self.states.copy()
        new_machine.transitions = deepcopy(self.transitions)
        new_machine.context = deepcopy(self.context)
        new_machine.current_state = self.current_state
        return new_machine

    def print_current_state(self):
        print(f"[{self.name}] Current State: {self.current_state}")

    def print_available_transitions(self):
        available_transitions = self.get_available_transitions()
        print(f"[{self.name}] Available Transitions from {self.current_state}:")
        for to_state in available_transitions:
            print(f"  → {to_state}")

    def print_transitions(self):
        print(f"[{self.name}] All Transitions:")
        for from_state_name, transitions_list in self.transitions.items():
            for transition in transitions_list:
                print(f"  {from_state_name} → {transition['to']}")


if __name__ == "__main__":
    import time

    class IdleState:
        def on_enter(self, machine):
            print("Entering Idle")

        def on_update(self, machine, dt):
            print(f"Idle... ({dt:.3f}s)")

        def on_exit(self, machine):
            print("Exiting Idle")

    class MovingState:
        def on_enter(self, machine):
            print("Entering Moving")

        def on_update(self, machine, dt):
            print(f"Moving... ({dt:.3f}s)")

        def on_exit(self, machine):
            print("Exiting Moving")

    class ResetState:
        def on_enter(self, machine):
            print("Entering Reset")

        def on_update(self, machine, dt):
            print(f"Resetting system... ({dt:.3f}s)")
            machine.context["force_reset"] = False

        def on_exit(self, machine):
            print("Exiting Reset")

    sm = StateMachine("TestMachine")
    sm.add_state("Idle", IdleState())
    sm.add_state("Moving", MovingState())
    sm.add_state("Reset", ResetState())

    sm.add_transition("Idle", "Moving", lambda m: m.context.get("should_move", False))
    sm.add_transition("Moving", "Idle", lambda m: not m.context.get("should_move", False))

    sm.add_transition(
        ["Idle", "Moving"],
        "Reset",
        lambda m: m.context.get("force_reset", False)
    )

    sm.set_initial_state("Idle")
    sm.set_context({"should_move": False, "force_reset": False})

    for frame in range(8):
        sm.update(0.016)
        if frame == 2:
            print("→ Triggering move")
            sm.context["should_move"] = True
        if frame == 4:
            print("→ Stopping move")
            sm.context["should_move"] = False
        if frame == 6:
            print("→ Forcing reset from current state")
            sm.context["force_reset"] = True
        time.sleep(0.5)

    print("\nFinal Transition Map:")
    sm.print_transitions()
