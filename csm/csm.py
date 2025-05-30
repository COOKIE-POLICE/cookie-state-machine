class CSM:
    def __init__(self, config: dict):
        self.config = config
        self.current_state = config.get("initial")
        self._create_event_methods()

    def _create_event_methods(self):
        for event in self.config["events"]:
            setattr(
                self,
                event["name"],
                self._define_event_method(
                    event["name"],
                    event["from"],
                    event["to"],
                    event.get("guard"),
                ),
            )

    def _define_event_method(self, event_name, from_state, to_state, guard=None):
        def transition(*args, **kwargs):
            self._call_callback(
                "onbefore" + event_name,
                event_name,
                from_state,
                to_state,
                *args,
                **kwargs,
            )
            if guard is None or guard():
                if self.current_state == from_state:
                    self._call_callback(
                        "leave" + from_state,
                        event_name,
                        from_state,
                        to_state,
                        *args,
                        **kwargs,
                    )
                    self.current_state = to_state
                    self._call_callback(
                        "enter" + to_state,
                        event_name,
                        from_state,
                        to_state,
                        *args,
                        **kwargs,
                    )
                else:
                    print(
                        f"Cannot transition from {self.current_state} via {event_name}"
                    )
            self._call_callback(
                "onafter" + event_name,
                event_name,
                from_state,
                to_state,
                *args,
                **kwargs,
            )

        return transition

    def _call_callback(self, callback_name, *args, **kwargs):
        callback = self.config.get("callbacks", {}).get(callback_name)
        if callback:
            callback(self, *args, **kwargs)

    def is_state(self, state):
        return self.current_state == state


if __name__ == "__main__":
    config = {
        "initial": "green",
        "events": [
            {"name": "warn", "from": "green", "to": "yellow"},
            {"name": "panic", "from": "yellow", "to": "red"},
            {"name": "calm", "from": "red", "to": "yellow"},
            {"name": "clear", "from": "yellow", "to": "green"},
        ],
        "callbacks": {
            "onbeforewarn": lambda self, e, f, t: print("Before warn"),
            "leavegreen": lambda self, e, f, t: print("Leaving green"),
            "enteryellow": lambda self, e, f, t: print("Entering yellow"),
            "onafterwarn": lambda self, e, f, t: print("After warn"),
            "onbeforered": lambda self, e, f, t: print("Before entering red"),
            "onafterclear": lambda self, e, f, t: print("After clear"),
        },
    }

    fsm = CSM(config)

    print(f"Initial state: {fsm.current_state}")
    fsm.warn()
    print(f"State after warn: {fsm.current_state}")
    fsm.panic()
    print(f"State after panic: {fsm.current_state}")
    fsm.calm()
    print(f"State after calm: {fsm.current_state}")
    fsm.clear()
    print(f"State after clear: {fsm.current_state}")
