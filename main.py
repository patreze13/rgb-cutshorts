import sys
import os
import traceback

# Redireciona mensagens de erro para um ficheiro de registo no armazenamento interno
log_file = os.path.expanduser("/sdcard/rgb_cutshorts_crash.log")

try:
    # Coloque aqui as importacoes e o codigo da aplicacao
    import kivy
    from kivy.app import App
    from kivy.uix.label import Label

    class RGBCutShortsApp(App):
        def build(self):
            return Label(text="RGB CutShorts a funcionar!")

    if __name__ == "__main__":
        RGBCutShortsApp().run()

except Exception as e:
    with open(log_file, "w") as f:
        f.write(traceback.format_exc())
    sys.exit(1)
