import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import threading
from image_processor import process_image, get_preview

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    """
    Clase principal de la aplicación.
    Gestiona la interfaz de usuario, la carga de archivos, la navegación de previews
    y el procesamiento por lotes en segundo plano (threading).
    """
    def __init__(self):
        super().__init__()

        self.title("Procesador de Imágenes - MARCA IMAGEN")
        self.geometry("1100x700")

        self.folder_path = ""
        self.logo_path = ""
        self.image_list = []
        self.current_preview_index = 0

        # --- Layout ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="CONFIGURACIÓN", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)

        self.btn_select_folder = ctk.CTkButton(self.sidebar, text="Seleccionar Carpeta", command=self.select_folder)
        self.btn_select_folder.pack(pady=10, padx=20, fill="x")

        self.btn_select_logo = ctk.CTkButton(self.sidebar, text="Seleccionar Logo", command=self.select_logo)
        self.btn_select_logo.pack(pady=10, padx=20, fill="x")

        # Controles de Logo
        self.ctrl_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.ctrl_frame.pack(pady=10, padx=20, fill="x")
        
        self.lbl_scale = ctk.CTkLabel(self.ctrl_frame, text="Tamaño del Logo: 25%")
        self.lbl_scale.pack()
        self.slider_scale = ctk.CTkSlider(self.ctrl_frame, from_=0.05, to=1.0, command=self.on_slider_change)
        self.slider_scale.set(0.25)
        self.slider_scale.pack(fill="x", pady=(0, 10))

        self.lbl_x = ctk.CTkLabel(self.ctrl_frame, text="Posición X: 750 (Centro)")
        self.lbl_x.pack()
        self.slider_x = ctk.CTkSlider(self.ctrl_frame, from_=0, to=1500, command=self.on_slider_change)
        self.slider_x.set(750)
        self.slider_x.pack(fill="x", pady=(0, 10))

        self.lbl_y = ctk.CTkLabel(self.ctrl_frame, text="Posición Y: 30")
        self.lbl_y.pack()
        self.slider_y = ctk.CTkSlider(self.ctrl_frame, from_=0, to=1500, command=self.on_slider_change)
        self.slider_y.set(30)
        self.slider_y.pack(fill="x", pady=(0, 10))

        self.btn_center = ctk.CTkButton(self.ctrl_frame, text="Restaurar al Centro", fg_color="gray40", hover_color="gray30", command=self.reset_logo_position)
        self.btn_center.pack(pady=5)

        self.info_label = ctk.CTkLabel(self.sidebar, text="Sin carpeta seleccionada", wraplength=250)
        self.info_label.pack(pady=20)

        self.progress_bar = ctk.CTkProgressBar(self.sidebar)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20, padx=20, fill="x")
        
        self.status_label = ctk.CTkLabel(self.sidebar, text="Listo")
        self.status_label.pack(pady=5)

        self.btn_process = ctk.CTkButton(self.sidebar, text="PROCESAR TODO", fg_color="green", hover_color="darkgreen", command=self.start_processing, state="disabled")
        self.btn_process.pack(pady=20, padx=20, fill="x")

        # Main Content (Preview)
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.preview_title = ctk.CTkLabel(self.preview_frame, text="VISTA PREVIA", font=ctk.CTkFont(size=18, weight="bold"))
        self.preview_title.pack(pady=10)

        self.canvas_preview = ctk.CTkLabel(self.preview_frame, text="Selecciona una carpeta y logo\npara ver el preview", width=600, height=500, fg_color="gray20")
        self.canvas_preview.pack(pady=10, expand=True)

        self.nav_frame = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        self.nav_frame.pack(pady=10)

        self.btn_prev = ctk.CTkButton(self.nav_frame, text="< Anterior", width=100, command=self.prev_image)
        self.btn_prev.grid(row=0, column=0, padx=10)

        self.img_counter = ctk.CTkLabel(self.nav_frame, text="0 / 0")
        self.img_counter.grid(row=0, column=1, padx=10)

        self.btn_next = ctk.CTkButton(self.nav_frame, text="Siguiente >", width=100, command=self.next_image)
        self.btn_next.grid(row=0, column=2, padx=10)

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path = path
            self.image_list = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            self.info_label.configure(text=f"Carpeta: {os.path.basename(path)}\nImágenes: {len(self.image_list)}")
            self.current_preview_index = 0
            self.update_preview()
            self.check_ready()

    def select_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp")])
        if path:
            self.logo_path = path
            self.update_preview()
            self.check_ready()

    def check_ready(self):
        if self.folder_path and self.logo_path and self.image_list:
            self.btn_process.configure(state="normal")
        else:
            self.btn_process.configure(state="disabled")

    def update_preview(self):
        """
        Actualiza el panel de vista previa central. 
        Lee los valores actuales de los sliders y genera la imagen compuesta.
        """

        img_name = self.image_list[self.current_preview_index]
        img_path = os.path.join(self.folder_path, img_name)
        
        # Generar preview usando el motor con los valores de los sliders
        logo_scale = self.slider_scale.get()
        logo_x = int(self.slider_x.get())
        logo_y = int(self.slider_y.get())
        
        pil_img = get_preview(img_path, self.logo_path, logo_width_ratio=logo_scale, logo_x_center=logo_x, logo_y=logo_y)
        if pil_img:
            # Redimensionar para que quepa en el label de la UI
            display_size = (600, 600)
            pil_img.thumbnail(display_size, Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
            self.canvas_preview.configure(image=ctk_img, text="")
            self.img_counter.configure(text=f"{self.current_preview_index + 1} / {len(self.image_list)}")

    def next_image(self):
        if self.image_list:
            self.current_preview_index = (self.current_preview_index + 1) % len(self.image_list)
            self.update_preview()

    def on_slider_change(self, value=None):
        scale = int(self.slider_scale.get() * 100)
        x = int(self.slider_x.get())
        y = int(self.slider_y.get())
        
        self.lbl_scale.configure(text=f"Tamaño del Logo: {scale}%")
        x_text = f"Posición X: {x}" + (" (Centro)" if x == 750 else "")
        self.lbl_x.configure(text=x_text)
        self.lbl_y.configure(text=f"Posición Y: {y}")
        
        self.update_preview()

    def reset_logo_position(self):
        self.slider_scale.set(0.25)
        self.slider_x.set(750)
        self.slider_y.set(30)
        self.on_slider_change()

    def prev_image(self):
        if self.image_list:
            self.current_preview_index = (self.current_preview_index - 1) % len(self.image_list)
            self.update_preview()

    def start_processing(self):
        self.btn_process.configure(state="disabled")
        self.btn_select_folder.configure(state="disabled")
        self.btn_select_logo.configure(state="disabled")
        
        thread = threading.Thread(target=self.process_all)
        thread.start()

    def process_all(self):
        output_dir = os.path.join(self.folder_path, "PROCESADAS")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        total = len(self.image_list)
        for i, img_name in enumerate(self.image_list):
            self.status_label.configure(text=f"Procesando {i+1}/{total}...")
            self.progress_bar.set((i + 1) / total)
            
            in_path = os.path.join(self.folder_path, img_name)
            out_path = os.path.join(output_dir, img_name)
            
            logo_scale = self.slider_scale.get()
            logo_x = int(self.slider_x.get())
            logo_y = int(self.slider_y.get())
            
            process_image(in_path, self.logo_path, out_path, logo_width_ratio=logo_scale, logo_x_center=logo_x, logo_y=logo_y)

        self.status_label.configure(text="¡Completado!")
        messagebox.showinfo("Éxito", f"Se han procesado {total} imágenes en la carpeta 'PROCESADAS'.")
        
        self.btn_process.configure(state="normal")
        self.btn_select_folder.configure(state="normal")
        self.btn_select_logo.configure(state="normal")
        self.progress_bar.set(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
