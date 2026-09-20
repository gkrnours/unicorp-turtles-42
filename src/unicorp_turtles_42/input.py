import pyglet


class InputManager:
    def __init__(self):
        self.manager = pyglet.input.ControllerManager()
        for controller in self.manager.get_controllers():
            self._register_controller(controller)

        self.manager.on_connect = self.on_connect
        self.manager.on_disconnect = self.on_disconnect

    def _register_controller(self, controller):
        print("registering controller", controller.guid)
        controller.open()
        controller.on_button_press = self.on_button_press
        controller.on_button_release = self.on_button_release
        controller.on_stick_motion = self.on_stick_motion
        controller.on_dpad_motion = self.on_dpad_motion
        controller.on_trigger_motion = self.on_trigger_motion

    def on_connect(self, controller):
        self._register_controller(controller)

    def on_disconnect(self, controller):
        print(f"Disconnected: {controller.guid}")

    def on_button_press(self, controller, button_name):
        print(controller, button_name, "pressed")

    def on_button_release(self, controller, button_name):
        print(controller, button_name, "released")

    def on_stick_motion(self, controller, stick_name, vector):
        print(controller, stick_name, vector)

    def on_dpad_motion(self, controller, vector):
        print(controller, vector)

    def on_trigger_motion(self, controller, trigger_name, value):
        print(controller, trigger_name, value)
