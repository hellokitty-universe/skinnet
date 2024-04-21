from multiprocessing import Process, Manager
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Label, RadioButton, RadioSet, Button, SelectionList, Header, Footer
from textual.reactive import reactive
from textual import on

from logic import run_expert_system

# Setup shared data structure
shared_data = Manager().dict()

class SkincareApp(App[None]):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("n", "go_next", "Go to Next Question"),
    ]
    selected_values = reactive([None])
    about_to_finish = False
    started = False
    has_radio = True

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Horizontal():
            yield Label(shared_data.get("curr_question", {"text": ""})["text"], id="curr_question")
        with Horizontal(id="focus_me"):
            pass
        with Horizontal():
            yield Button("Next", id="next_btn", variant="success")

    def action_go_next(self) -> None:
        if self.about_to_finish:
            self.exit()
            return
        # question just answered
        last_question = shared_data["curr_question"]["id"]
        shared_data[f"{last_question}_response"] = self.selected_values

        # wait for Prolog to send next question or conclusion
        while (shared_data["curr_question"]["id"] == last_question
            and not shared_data.get("done")):
            pass

        # Process reminders and conclusions
        if "reminders" in shared_data:
            self.display_reminders(shared_data["reminders"])
        if "conclusions" in shared_data:
            self.display_conclusions(shared_data["conclusions"])

        if not shared_data.get("done"):
            self.query_one("#curr_question", Label).update(
                shared_data["curr_question"]["text"]
            )

        self.setup_next_interaction()

    def display_reminders(self, reminders):
        reminders_text = "\n".join(reminders)
        self.query_one("#curr_question", Label).update(f"Daily Reminders:\n{reminders_text}")

    def display_conclusions(self, conclusions):
        conclusions_text = "\n".join(conclusions)
        self.query_one("#curr_question", Label).update(f"Analysis Conclusions:\n{conclusions_text}")

    def setup_next_interaction(self):
        # Initialize radio buttons or selection lists based on the type of the current question
        if shared_data.get("done"):
            self.query_one("#focus_me").remove()
            self.query_one("#next_btn", Button).label = "Finish"
            self.about_to_finish = True
        else:
            if shared_data["curr_question"]["type"] == "single_choice":
                self.setup_radio_buttons()
            elif shared_data["curr_question"]["type"] == "multi_choice":
                self.setup_selection_list()

    def setup_radio_buttons(self):
        radioset = RadioSet()
        self.query_one("#focus_me").mount(radioset)
        for opt in shared_data["curr_question"]["options"]:
            radioset.mount(
                RadioButton(opt["text"], id=opt["id"])
            )
        radioset.focus()

    def setup_selection_list(self):
        selection_list = SelectionList(
            *[opt["text"] for opt in shared_data["curr_question"]["options"]]
        )
        self.query_one("#focus_me").mount(selection_list)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.action_go_next()

    def on_mount(self) -> None:
        self.query_one("#focus_me").focus()

if __name__ == "__main__":
    manager = Manager()
    shared_data = manager.dict(
        {
            "curr_question": {
                "id": "no_id",
                "text": "Welcome to your Personalized Skincare Assistant. Please press [N] to begin the consultation.",
                "options": [],
                "default": "None",
            },
            "reminders": [],
            "conclusions": []
        }
    )
    p1 = Process(target=run_expert_system, args=(shared_data,))
    p1.start()
    SkincareApp().run()
    p1.join()
