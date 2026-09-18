import os
import sys
import traceback


def _log_crash(exc_text):
    try:
        base = os.path.expanduser("~")
        log_path = os.path.join(base, "crash.log")
        with open(log_path, "w") as f:
            f.write(exc_text)
        print(f"[CRASH] Log salvo em: {log_path}")
        print(exc_text)
    except Exception as e:
        print(f"[CRASH] Falha ao salvar log: {e}")
        print(exc_text)


try:
    import kivy
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.core.window import Window
    import requests

    Window.clearcolor = (0.1, 0.1, 0.1, 1)

    class CutShortsLayout(BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

            self.add_widget(Label(
                text="RGB CutShorts",
                font_size='24sp',
                size_hint_y=0.2
            ))

            self.url_input = TextInput(
                hint_text="Cole o link do YouTube aqui",
                multiline=False,
                size_hint_y=0.2
            )
            self.add_widget(self.url_input)

            self.btn = Button(
                text="Processar Corte",
                size_hint_y=0.2
            )
            self.btn.bind(on_press=self.processar)
            self.add_widget(self.btn)

            self.status = Label(
                text="Pronto",
                size_hint_y=0.4
            )
            self.add_widget(self.status)

        def processar(self, instance):
            url = self.url_input.text.strip()
            if not url:
                self.status.text = "Informe um link válido."
                return
            self.status.text = "URL recebida com sucesso."

    class RGBCutShortsApp(App):
        def build(self):
            self.title = "RGB CutShorts"
            return CutShortsLayout()

    if __name__ == "__main__":
        RGBCutShortsApp().run()

except Exception:
    _log_crash(traceback.format_exc())
    raise
