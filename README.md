# Procesador de Imágenes de Productos - MARCA IMAGEN

Este proyecto es una herramienta de escritorio profesional diseñada para automatizar la aplicación de logos de marca en imágenes de productos, garantizando un formato estandarizado y de alta calidad para catálogos o sitios web.

## 🚀 Estado del Proyecto: Finalizado y Funcional

El programa permite transformar carpetas completas de imágenes de productos en un lote listo para su publicación, con un lienzo estandarizado de **1500x1500px** y fondo blanco.

## ✨ Características Principales

- **Interfaz Gráfica (GUI) Moderna**: Desarrollada con `customtkinter` para una experiencia de usuario fluida.
- **Control Total del Logo**:
  - **Remoción de Fondo Automática**: Convierte logos con fondo blanco en capas transparentes automáticamente.
  - **Recorte Inteligente**: Elimina bordes invisibles para permitir un posicionamiento exacto.
  - **Sliders Interactivos**: Ajuste en tiempo real de **Tamaño (Escala)**, **Posición X** y **Posición Y**.
- **Vista Previa en Tiempo Real**: Visualiza cómo quedará cada imagen del lote antes de iniciar el procesamiento masivo.
- **Procesamiento por Lotes**: Genera todas las imágenes procesadas en una carpeta independiente llamada `PROCESADAS`.
- **Estandarización**: Salida garantizada de 1500x1500px con centrado automático del producto.

## 🛠️ Requerimientos Técnicos

- **Lenguaje**: Python 3.x
- **Librerías**:
  - `Pillow` (Procesamiento de imagen)
  - `customtkinter` (Interfaz gráfica)
- **Control de Versiones**: Git (Repositorio inicializado).

## 📂 Estructura de Archivos

- `main.py`: Archivo principal que ejecuta la interfaz gráfica.
- `image_processor.py`: Motor de lógica para redimensionamiento, transparencia y composición.
- `ejecutar_programa.bat`: Acceso directo para verificar dependencias y lanzar la aplicación en Windows.
- `requirements.txt`: Lista de dependencias de Python.
- `README.md`: Documentación del proyecto (este archivo).

## 📖 Instrucciones de Uso

1. Ejecute el archivo `ejecutar_programa.bat`.
2. Haga clic en **Seleccionar Carpeta** y elija el origen de sus fotos de productos.
3. Haga clic en **Seleccionar Logo** y elija su imagen de marca (ej. MOOG.jpg).
4. Use los **Sliders de Configuración** para ajustar el logo a su gusto en la vista previa.
5. Presione **PROCESAR TODO** y espere a que la barra de progreso llegue al 100%.

---
*Desarrollado con asistencia de Antigravity AI - Abril 2026*
