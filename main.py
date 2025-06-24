from pytubefix import YouTube
from pytubefix.cli import on_progress
import customtkinter
import tkinter.filedialog as fd
import os
import tkinter as tk

def download_yt_audio():
    url = url_entry.get()
    if not url.strip():
        print("URL vazia")
        return
    
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(f"Baixando: {yt.title}")
        ys = yt.streams.get_audio_only()

        # Caixa de diálogo "Salvar como"
        caminho_salvar = fd.asksaveasfilename(
            defaultextension=".m4a",
            filetypes=[("Audio Files", "*.m4a"), ("Todos os arquivos", "*.*")],
            title="Salvar áudio como..."
        )

        if caminho_salvar:
            ys.download(
                output_path=os.path.dirname(caminho_salvar),
                filename=os.path.basename(caminho_salvar)
            )
            print("Download de áudio concluído.")
        else:
            print("Download cancelado.")

    except Exception as e:
        print("Erro:", e)
    url_entry.delete(0, tk.END)

def download_yt_vid():
    url = url_entry.get()
    if not url.strip():
        print("URL vazia")
        return

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(f"Baixando: {yt.title}")
        ys = yt.streams.get_highest_resolution()

        # Caixa de diálogo "Salvar como"
        caminho_salvar = fd.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("Video Files", "*.mp4"), ("Todos os arquivos", "*.*")],
            title="Salvar vídeo como..."
        )

        if caminho_salvar:
            ys.download(
                output_path=os.path.dirname(caminho_salvar),
                filename=os.path.basename(caminho_salvar)
            )
            print("Download de vídeo concluído.")
        else:
            print("Download cancelado.")

    except Exception as e:
        print("Erro:", e)
    url_entry.delete(0, tk.END)

#region window_settings
download_screen = customtkinter.CTk()
download_screen.geometry("400x300")
download_screen.title("yt downloader")
download_screen.configure(fg_color="#E30D02")
download_screen.minsize(400,300)
download_screen.maxsize(400,300)

fonte = customtkinter.CTkFont(size=20)
instruction_label = customtkinter.CTkLabel(download_screen, text="YOUTUBE DOWNLOADER",width=200,height=30,font=fonte)
instruction_label.place(x=85,y=67)

url_entry = customtkinter.CTkEntry(download_screen,placeholder_text="Paste URL here",width=220,height=40,fg_color="#ffffff",text_color="black",placeholder_text_color="#9b9b9b",border_color="#9b9b9b")
url_entry.place(x=90,y=130)

download_button1 = customtkinter.CTkButton(download_screen,text="MP4",command=download_yt_vid,width=100,height=40,fg_color="#ffffff",hover_color="#9b9b9b",text_color="black")
download_button1.place(x=90,y=179)

download_button2 = customtkinter.CTkButton(download_screen,text=".m4a",command=download_yt_audio,width=100,height=40,fg_color="#ffffff",hover_color="#9b9b9b",text_color="black")
download_button2.place(x=210,y=179)

history_download_button = customtkinter.CTkButton(download_screen,text="History",width=55,height=25,fg_color="#ffffff",hover_color="#9b9b9b",text_color="black")
history_download_button.place(x=12,y=14)

download_screen.mainloop()
#endregion