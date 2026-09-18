import os
import threading
import json
import yt_dlp
import google.generativeai as genai
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

Window.clearcolor = get_color_from_hex("#0E0E10")

class RGBCutShorts(App):
    def build(self):
        self.title = "RGB CutShorts"
        layout = BoxLayout(orientation='vertical', padding=25, spacing=15)

        titulo = Label(
            text="[b][color=ff3344]RGB[/color] [color=00e676]Cut[/color][color=00b0ff]Shorts[/color][/b]",
            markup=True,
            font_size='28sp',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(titulo)

        self.key_input = TextInput(
            hint_text="Cole sua Google Gemini API Key aqui",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=45,
            background_color=get_color_from_hex("#1E1E24"),
            foreground_color=(1, 1, 1, 1),
            cursor_color=get_color_from_hex("#00B0FF")
        )
        layout.add_widget(self.key_input)

        self.url_input = TextInput(
            hint_text="Cole o link do YouTube aqui...",
            multiline=False,
            size_hint_y=None,
            height=45,
            background_color=get_color_from_hex("#1E1E24"),
            foreground_color=(1, 1, 1, 1),
            cursor_color=get_color_from_hex("#00B0FF")
        )
        layout.add_widget(self.url_input)

        self.btn_cortar = Button(
            text="GERAR SHORT COM IA",
            bold=True,
            size_hint_y=None,
            height=55,
            background_normal='',
            background_color=get_color_from_hex("#FF3344")
        )
        self.btn_cortar.bind(on_press=self.iniciar_processamento)
        layout.add_widget(self.btn_cortar)

        self.progress = ProgressBar(max=100, value=0, size_hint_y=None, height=20)
        layout.add_widget(self.progress)

        self.status_label = Label(
            text="Pronto para criar cortes.",
            color=get_color_from_hex("#00E676"),
            font_size='14sp'
        )
        layout.add_widget(self.status_label)

        return layout

    def log(self, texto, progresso=None):
        self.status_label.text = texto
        if progresso is not None:
            self.progress.value = progresso

    def iniciar_processamento(self, instance):
        url = self.url_input.text.strip()
        api_key = self.key_input.text.strip()

        if not url or not api_key:
            self.log("Preencha a API Key e o link do vídeo!", 0)
            return

        self.btn_cortar.disabled = True
        threading.Thread(target=self.processar_video, args=(url, api_key), daemon=True).start()

    def processar_video(self, url, api_key):
        try:
            self.log("Baixando vídeo e legendas...", 25)
            pasta = "/sdcard/Download"
            base = os.path.join(pasta, "rgb_temp")

            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': f"{base}.mp4",
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['pt', 'en'],
                'subtitlesformat': 'vtt',
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.log("IA analisando melhor momento...", 60)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            legenda_path = f"{base}.pt.vtt" if os.path.exists(f"{base}.pt.vtt") else f"{base}.en.vtt"
            with open(legenda_path, 'r', encoding='utf-8') as f:
                linhas = [l.strip() for l in f.readlines() if "-->" in l or (l.strip() and not l.startswith("WEBVTT"))]
                contexto = "\n".join(linhas[:300])

            prompt = f"""
            Identifique um momento dinâmico e viral entre 30 e 50 segundos para YouTube Shorts.
            Retorne APENAS um JSON: {{"start": "00:01:00", "end": "00:01:45"}}
            Legenda:
            {contexto}
            """
            res = model.generate_content(prompt)
            tempos = json.loads(res.text.replace("```json", "").replace("```", "").strip())

            self.log(f"Cortando em 9:16 ({tempos['start']} -> {tempos['end']})...", 85)
            saida = os.path.join(pasta, "RGB_Short_Final.mp4")

            cmd = f"ffmpeg -y -ss {tempos['start']} -to {tempos['end']} -i {base}.mp4 -vf 'crop=ih*(9/16):ih' -c:v libx264 -preset ultrafast -c:a aac {saida}"
            os.system(cmd)

            self.log("Corte salvo em Downloads com sucesso!", 100)

        except Exception as e:
            self.log(f"Erro: {str(e)[:40]}...", 0)
        finally:
            self.btn_cortar.disabled = False

if __name__ == '__main__':
    RGBCutShorts().run()
a
