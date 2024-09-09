import customtkinter
from tkinter import filedialog as fd
import yt_dlp  # Use yt-dlp instead of pytube

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry("1280x720")
        self.resizable(True, True)

        customtkinter.set_appearance_mode("dark") 
        customtkinter.set_default_color_theme("blue") 

        self.selected_folder = ""  # To store the folder path
        self.download_type = "video"  # Default download type

        # Header (YouTube Downloader Title)
        self.header = customtkinter.CTkLabel(self, text="YouTube Downloader", 
                                             font=("Arial", 36, "bold"), 
                                             text_color="#FFD700")
        self.header.pack(pady=(40, 20))  

        # Label (Enter URL)
        self.label = customtkinter.CTkLabel(self, text="Ingresa la URL del video", 
                                            font=("Arial", 24),
                                            text_color="#F5F5F5")
        self.label.pack(pady=(10, 20))

        # Entry (Input for the video URL)
        self.entry = customtkinter.CTkEntry(self, placeholder_text="https://youtube.com/...", 
                                            font=("Arial", 20), width=600)
        self.entry.pack(pady=(10, 20)) 

        # Select folder to save the video
        self.folder = customtkinter.CTkButton(self, text="Seleccionar carpeta", 
                                              font=("Arial", 24, "bold"), 
                                              fg_color="#1E90FF", 
                                              hover_color="#00BFFF", 
                                              text_color="white", 
                                              corner_radius=10, 
                                              command=self.select_folder)  # Link to folder selection
        self.folder.pack(pady=(10, 20))

        # Label to show the selected folder path
        self.folder_label = customtkinter.CTkLabel(self, text="No se ha seleccionado ninguna carpeta", 
                                                   font=("Arial", 18), 
                                                   text_color="#A9A9A9")
        self.folder_label.pack(pady=(10, 20))  # Added padding for visual separation

        # Radio buttons to select download type
        self.radio_video = customtkinter.CTkRadioButton(self, text="Video", 
                                                       font=("Arial", 20),
                                                       command=self.set_video_mode)
        self.radio_video.pack(pady=(10, 10))

        self.radio_audio = customtkinter.CTkRadioButton(self, text="Audio", 
                                                       font=("Arial", 20),
                                                       command=self.set_audio_mode)
        self.radio_audio.pack(pady=(10, 10))

        # Download button
        self.button = customtkinter.CTkButton(self, text="Descargar", 
                                              font=("Arial", 24, "bold"), 
                                              fg_color="#1E90FF", 
                                              hover_color="#00BFFF", 
                                              text_color="white", 
                                              corner_radius=10,
                                              command=self.download_video)
        self.button.pack(pady=(30, 20))

    def set_video_mode(self):
        self.download_type = "video"

    def set_audio_mode(self):
        self.download_type = "audio"

    def select_folder(self):
        # Open a folder selection dialog
        folder_path = fd.askdirectory()
        if folder_path:  # If a folder is selected
            self.selected_folder = folder_path
            self.folder_label.configure(text=f"Carpeta seleccionada: {self.selected_folder}")
        else:
            self.folder_label.configure(text="No se ha seleccionado ninguna carpeta")

    def download_video(self):
        video_url = self.entry.get()
        if not video_url:
            self.show_error = customtkinter.CTkLabel(self, text="Ingresa una URL válida", 
                                                     font=("Arial", 20), 
                                                     text_color="red")
            self.show_error.pack(pady=(10, 20))
            return

        if not self.selected_folder:
            self.show_error = customtkinter.CTkLabel(self, text="Selecciona una carpeta para guardar el archivo", 
                                                     font=("Arial", 20), 
                                                     text_color="red")
            self.show_error.pack(pady=(10, 20))
            return

        if self.download_type == "video":
            ydl_opts = {
                'outtmpl': f'{self.selected_folder}/%(title)s.%(ext)s',
                'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',  # Limit to 720p
            }
        else:  # Download audio
            ydl_opts = {
                'outtmpl': f'{self.selected_folder}/%(title)s.%(ext)s',
                'format': 'bestaudio[ext=m4a]/bestaudio',  # Extract best audio available in M4A format
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',  # Convert audio to m4a format
                    'preferredquality': '192',
                }],
                'postprocessor_args': [
                    '-c:a', 'aac',  # Use AAC codec for the m4a file
                    '-b:a', '192k'
                ],
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                
                self.success_message = customtkinter.CTkLabel(self, text="Descarga completada!", 
                                                              font=("Arial", 20), 
                                                              text_color="green")
                self.success_message.pack(pady=(10, 20))

        except Exception as e:
            self.show_error = customtkinter.CTkLabel(self, text=f"Error: {str(e)}", 
                                                     font=("Arial", 20), 
                                                     text_color="red")
            self.show_error.pack(pady=(10, 20))


# Create an instance and run the app
app = App()
app.mainloop()
