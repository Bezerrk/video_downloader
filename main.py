from pytubefix import YouTube
from pytubefix.cli import on_progress
import customtkinter
import tkinter.filedialog as fd
import os
import tkinter as tk
import sqlite3

database = sqlite3.connect('historico.db')
command = database.cursor()

command.execute("CREATE TABLE IF NOT EXISTS historico_de_downloads (url text,title text,extension text)")
#command.execute("DROP TABLE historico_de_downloads")

def download_yt_audio():
    url = url_entry.get()
    if not url.strip():
        print("URL vazia")
        return
    
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(f"Baixando: {yt.title}")
        ys = yt.streams.get_audio_only()

        caminho_salvar = fd.asksaveasfilename(
            defaultextension=".m4a",
            filetypes=[("Audio Files", "*.m4a"), ("Todos os arquivos", "*.*")],
            title="Salvar áudio como...",
            parent=download_screen
        )

        if caminho_salvar:
            ys.download(
                output_path=os.path.dirname(caminho_salvar),
                filename=os.path.basename(caminho_salvar)
            )
            command.execute("INSERT INTO historico_de_downloads VALUES('"+url+"','"+yt.title+"','.M4A')")
            database.commit()
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

        caminho_salvar = fd.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("Video Files", "*.mp4"), ("Todos os arquivos", "*.*")],
            title="Salvar vídeo como...",
            parent=download_screen
        )

        if caminho_salvar:
            ys.download(
                output_path=os.path.dirname(caminho_salvar),
                filename=os.path.basename(caminho_salvar)
            )
            command.execute("INSERT INTO historico_de_downloads VALUES('"+url+"','"+yt.title+"','.MP4')")
            database.commit()
        else:
            print("Download cancelado.")

    except Exception as e:
        print("Erro:", e)
    url_entry.delete(0, tk.END)

def baixar_novamente(url, formato,parent):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(f"Baixando novamente: {yt.title} ({formato})")

        if formato.upper() == ".MP4":
            ys = yt.streams.get_highest_resolution()
            defaultext = ".mp4"
            filetype = ("Video Files", "*.mp4")
        else:
            ys = yt.streams.get_audio_only()
            defaultext = ".m4a"
            filetype = ("Audio Files", "*.m4a")

        caminho_salvar = fd.asksaveasfilename(
            defaultextension=defaultext,
            filetypes=[filetype, ("Todos os arquivos", "*.*")],
            title=f"Salvar {formato.upper()} como...",
            parent=parent
        )

        if caminho_salvar:
            ys.download(
                output_path=os.path.dirname(caminho_salvar),
                filename=os.path.basename(caminho_salvar)
            )
            print("Download concluído.")
        else:
            print("Download cancelado.")

    except Exception as e:
        print("Erro ao baixar novamente:", e)


def open_history():
    history_screen = customtkinter.CTkToplevel(download_screen)
    history_screen.title("Download history")
    history_screen.geometry("600x300")
    history_screen.minsize(600,300)
    history_screen.maxsize(600,300)
    history_screen.attributes("-topmost",True)

    history_scroll = customtkinter.CTkScrollableFrame(master=history_screen)
    history_scroll.pack(padx = 20, pady = 20, fill = 'both', expand = True)
    command.execute("SELECT rowid, url, title, extension FROM historico_de_downloads")
    for line in command:
        frame = customtkinter.CTkFrame(master=history_scroll)
        frame.pack(padx=5,pady=2, fill="both", expand= True)
        frame.configure(fg_color="#9b9b9b")
        frame2 = customtkinter.CTkFrame(master=frame, width=200, height=100)
        frame2.grid(column=0,row=0,padx=2,pady=5,sticky='e')
        frame3 = customtkinter.CTkFrame(master=frame, width=200, height=100)
        frame3.grid(column=1,row=0,padx=2,pady=5,sticky='e')
        label = customtkinter.CTkLabel(master=frame2, text=line[0], wraplength=3)
        label.pack(padx=5,pady=5)
        label2 = customtkinter.CTkLabel(master=frame3, text=line[2], wraplength=420)
        label2.pack(padx=5,pady=5)
        dw_again = customtkinter.CTkButton(master=frame, text="Download",command=lambda u=line[1], f=line[3]: baixar_novamente(u, f,parent=history_screen))
        dw_again.configure(width=70,height=30)
        dw_again.grid(column=2,row=0,padx=5,pady=5,sticky='e')

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

download_button2 = customtkinter.CTkButton(download_screen,text="M4A",command=download_yt_audio,width=100,height=40,fg_color="#ffffff",hover_color="#9b9b9b",text_color="black")
download_button2.place(x=210,y=179)

history_download_button = customtkinter.CTkButton(download_screen,text="History",command=open_history,width=55,height=25,fg_color="#ffffff",hover_color="#9b9b9b",text_color="black")
history_download_button.place(x=12,y=14)

download_screen.mainloop()
#endregion