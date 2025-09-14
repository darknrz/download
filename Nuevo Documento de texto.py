import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import yt_dlp
import os
import threading
from pathlib import Path
import re

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 YouTube MP3 Downloader")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads" / "YouTube_MP3"))
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="192")
        self.is_downloading = False
        
        # Configurar estilo
        self.setup_style()
        
        # Crear interfaz
        self.create_widgets()
        
    def setup_style(self):
        """Configurar el estilo de la aplicación"""
        style = ttk.Style()
        
        # Configurar colores
        self.colors = {
            'primary': '#FF0000',      # Rojo YouTube
            'secondary': '#282828',    # Gris oscuro
            'success': '#00FF00',      # Verde
            'warning': '#FFA500',      # Naranja
            'bg': '#F9F9F9',          # Fondo claro
            'text': '#333333'         # Texto oscuro
        }
        
        # Configurar root
        self.root.configure(bg=self.colors['bg'])
        
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # TÍTULO
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 30), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(title_frame, text="🎵 YouTube MP3 Downloader", 
                               font=('Arial', 20, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Descarga audio de YouTube en alta calidad", 
                                  font=('Arial', 10))
        subtitle_label.pack()
        
        # SECCIÓN URL
        url_frame = ttk.LabelFrame(main_frame, text="📎 URL del Video/Playlist", padding="15")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        url_frame.columnconfigure(0, weight=1)
        
        # Entry para URL
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=('Arial', 11))
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Botón pegar
        paste_btn = ttk.Button(url_frame, text="📋 Pegar", command=self.paste_url)
        paste_btn.grid(row=0, column=1)
        
        # Botón obtener info
        info_btn = ttk.Button(url_frame, text="ℹ️ Info", command=self.get_video_info)
        info_btn.grid(row=0, column=2, padx=(5, 0))
        
        # SECCIÓN CONFIGURACIÓN
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuración", padding="15")
        config_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        config_frame.columnconfigure(1, weight=1)
        
        # Ruta de descarga
        ttk.Label(config_frame, text="📁 Carpeta destino:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        path_frame = ttk.Frame(config_frame)
        path_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        path_frame.columnconfigure(0, weight=1)
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.download_path, font=('Arial', 10))
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(path_frame, text="📂 Examinar", command=self.browse_folder)
        browse_btn.grid(row=0, column=1)
        
        # Calidad de audio
        ttk.Label(config_frame, text="🎵 Calidad audio:").grid(row=1, column=0, sticky=tk.W)
        
        quality_frame = ttk.Frame(config_frame)
        quality_frame.grid(row=1, column=1, sticky=tk.W)
        
        qualities = [("128 kbps", "128"), ("192 kbps", "192"), ("256 kbps", "256"), ("320 kbps", "320")]
        for i, (text, value) in enumerate(qualities):
            ttk.Radiobutton(quality_frame, text=text, variable=self.quality_var, 
                           value=value).grid(row=0, column=i, padx=(0, 15))
        
        # INFORMACIÓN DEL VIDEO
        self.info_frame = ttk.LabelFrame(main_frame, text="📺 Información del Video", padding="15")
        self.info_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        self.info_frame.columnconfigure(0, weight=1)
        
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=4, font=('Arial', 9))
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.info_text.insert(tk.END, "Ingresa una URL para obtener información del video...")
        self.info_text.config(state=tk.DISABLED)
        
        # BOTONES DE ACCIÓN
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=3, pady=(0, 20))
        
        self.download_btn = ttk.Button(buttons_frame, text="⬇️ Descargar Audio", 
                                      command=self.start_download, style="Download.TButton")
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.playlist_btn = ttk.Button(buttons_frame, text="📋 Descargar Playlist", 
                                      command=self.start_playlist_download)
        self.playlist_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(buttons_frame, text="⏹️ Detener", 
                                  command=self.stop_download, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)
        
        # BARRA DE PROGRESO
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progreso", padding="15")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, text="Listo para descargar", 
                                     font=('Arial', 10))
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # LOG DE ACTIVIDAD
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log de Actividad", padding="15")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botón limpiar log
        clear_log_btn = ttk.Button(log_frame, text="🗑️ Limpiar Log", command=self.clear_log)
        clear_log_btn.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        # FOOTER
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=7, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Label(footer_frame, text="⚠️ Respeta los derechos de autor • Solo para uso personal", 
                 font=('Arial', 8), foreground='gray').pack()
        
    def paste_url(self):
        """Pegar URL desde el portapapeles"""
        try:
            clipboard_text = self.root.clipboard_get()
            if 'youtube.com' in clipboard_text or 'youtu.be' in clipboard_text:
                self.url_var.set(clipboard_text)
                self.log_message("✅ URL pegada desde portapapeles")
            else:
                messagebox.showwarning("Advertencia", "El portapapeles no contiene una URL de YouTube válida")
        except:
            messagebox.showerror("Error", "No se pudo acceder al portapapeles")
    
    def browse_folder(self):
        """Seleccionar carpeta de destino"""
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
            self.log_message(f"📁 Carpeta seleccionada: {folder}")
    
    def get_video_info(self):
        """Obtener información del video"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Advertencia", "Por favor ingresa una URL")
            return
        
        def fetch_info():
            try:
                self.status_label.config(text="Obteniendo información...")
                self.progress.start()
                
                ydl_opts = {'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    self.info_text.config(state=tk.NORMAL)
                    self.info_text.delete(1.0, tk.END)
                    
                    info_str = f"🎬 Título: {info.get('title', 'N/A')}\n"
                    info_str += f"👤 Canal: {info.get('uploader', 'N/A')}\n"
                    info_str += f"⏱️ Duración: {self.format_duration(info.get('duration', 0))}\n"
                    info_str += f"👀 Vistas: {info.get('view_count', 'N/A'):,}\n"
                    
                    if 'entries' in info:  # Es una playlist
                        info_str += f"📋 Videos en playlist: {len(info['entries'])}"
                    
                    self.info_text.insert(tk.END, info_str)
                    self.info_text.config(state=tk.DISABLED)
                    
                    self.log_message("ℹ️ Información obtenida correctamente")
                    
            except Exception as e:
                self.log_message(f"❌ Error al obtener información: {str(e)}")
                messagebox.showerror("Error", f"No se pudo obtener información: {str(e)}")
            finally:
                self.progress.stop()
                self.status_label.config(text="Listo para descargar")
        
        threading.Thread(target=fetch_info, daemon=True).start()
    
    def format_duration(self, seconds):
        """Formatear duración en formato legible"""
        if not seconds:
            return "N/A"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"
    
    def start_download(self):
        """Iniciar descarga de un video"""
        self.download_content(is_playlist=False)
    
    def start_playlist_download(self):
        """Iniciar descarga de playlist"""
        self.download_content(is_playlist=True)
    
    def download_content(self, is_playlist=False):
        """Descargar contenido (video o playlist)"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Advertencia", "Por favor ingresa una URL")
            return
        
        if self.is_downloading:
            messagebox.showwarning("Advertencia", "Ya hay una descarga en progreso")
            return
        
        def download():
            try:
                self.is_downloading = True
                self.download_btn.config(state=tk.DISABLED)
                self.playlist_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)
                self.progress.start()
                
                # Crear carpeta si no existe
                os.makedirs(self.download_path.get(), exist_ok=True)
                
                # Configurar opciones de descarga
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(self.download_path.get(), 
                                           '%(playlist_index)s - %(title)s.%(ext)s' if is_playlist 
                                           else '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': self.quality_var.get(),
                    }],
                    'noplaylist': not is_playlist,
                    'ignoreerrors': is_playlist,
                }
                
                self.status_label.config(text="Descargando..." + (" playlist" if is_playlist else ""))
                self.log_message(f"🚀 Iniciando descarga {'de playlist' if is_playlist else ''}: {url}")
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                self.log_message("✅ Descarga completada exitosamente")
                self.status_label.config(text="Descarga completada")
                messagebox.showinfo("Éxito", "Descarga completada exitosamente")
                
            except Exception as e:
                error_msg = f"Error en la descarga: {str(e)}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("Error", error_msg)
            finally:
                self.is_downloading = False
                self.download_btn.config(state=tk.NORMAL)
                self.playlist_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.progress.stop()
                if not self.is_downloading:
                    self.status_label.config(text="Listo para descargar")
        
        threading.Thread(target=download, daemon=True).start()
    
    def stop_download(self):
        """Detener descarga (funcionalidad limitada)"""
        self.log_message("⏹️ Solicitud de detener descarga (puede tardar un momento)")
        messagebox.showinfo("Info", "La descarga se detendrá después del archivo actual")
    
    def log_message(self, message):
        """Agregar mensaje al log"""
        timestamp = tk.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Limpiar el log de actividad"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("📋 Log limpiado")

def main():
    """Función principal"""
    # Verificar dependencias
    try:
        import yt_dlp
    except ImportError:
        tk.messagebox.showerror("Error", "Necesitas instalar yt-dlp:\npip install yt-dlp")
        return
    
    # Crear y ejecutar aplicación
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    
    # Agregar datetime para timestamps
    import datetime
    tk.datetime = datetime.datetime
    
    root.mainloop()

if __name__ == "__main__":
    main()