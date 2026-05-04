from PIL import Image, ImageOps
import os

def remove_white_background(img, threshold=235):
    """
    Convierte los píxeles blancos o casi blancos del fondo de una imagen en transparentes.
    
    Args:
        img (PIL.Image): La imagen original (logo).
        threshold (int): Valor de 0-255. Píxeles con R, G y B mayores a este valor se harán transparentes.
    
    Returns:
        PIL.Image: Imagen en formato RGBA con fondo transparente y recortada a su contenido visible.
    """
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        # Si el píxel es casi blanco (R, G y B altos)
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_data.append((255, 255, 255, 0)) # Blanco con 0% de opacidad (transparente)
        else:
            new_data.append(item)
    img.putdata(new_data)
    
    # Recortar el exceso transparente para que el borde superior sea real
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    return img


def process_image(product_path, logo_path, output_path, target_size=(1500, 1500), logo_width_ratio=0.25, logo_x_center=750, logo_y=30):
    """
    Realiza el flujo completo de procesamiento para una imagen de producto.
    
    Flujo:
    1. Crea lienzo blanco de 1500x1500px.
    2. Procesa el logo (quita fondo, escala y recorta).
    3. Redimensiona el producto para que encaje manteniendo proporción.
    4. Compone la imagen final pegando producto y luego el logo (capa superior).
    5. Guarda el resultado en disco.
    """
    try:
        # 1. Crear el lienzo blanco
        canvas = Image.new("RGB", target_size, (255, 255, 255))
        
        # 2. Cargar y redimensionar el logo (y remover fondo blanco)
        logo = Image.open(logo_path)
        logo = remove_white_background(logo)
            
        l_width = int(target_size[0] * logo_width_ratio)
        l_height = int(logo.height * (l_width / logo.width))
        logo = logo.resize((l_width, l_height), Image.Resampling.LANCZOS)
        
        # 3. Cargar y redimensionar la imagen del producto
        product = Image.open(product_path)
        if product.mode != 'RGB':
            product = product.convert('RGB')
            
        # Redimensionar producto para que quepa en el lienzo (manteniendo proporción)
        # Dejamos un pequeño margen para que no toque los bordes ni el logo
        # Usamos 1300 como tamaño máximo interno para dejar espacio al logo y márgenes
        max_internal_size = (target_size[0] - 100, target_size[1] - 150) 
        product.thumbnail(max_internal_size, Image.Resampling.LANCZOS)
        
        # 4. Pegar el producto en el centro
        p_x = (target_size[0] - product.width) // 2
        p_y = (target_size[1] - product.height) // 2 + 50 # Desplazado un poco hacia abajo para el logo
        canvas.paste(product, (p_x, p_y))
        
        # 5. Pegar el logo
        l_x = int(logo_x_center - (logo.width / 2))
        l_y = int(logo_y)
        canvas.paste(logo, (l_x, l_y), logo)
        
        # 6. Guardar
        canvas.save(output_path, "JPEG", quality=95)
        return True
    except Exception as e:
        print(f"Error procesando {product_path}: {e}")
        return False

def get_preview(product_path, logo_path, target_size=(1500, 1500), logo_width_ratio=0.25, logo_x_center=750, logo_y=30):
    """
    Genera un objeto Image de PIL con el resultado (sin guardar en disco).
    Útil para la previsualización en la GUI.
    """
    try:
        canvas = Image.new("RGB", target_size, (255, 255, 255))
        
        logo = Image.open(logo_path)
        logo = remove_white_background(logo)
        
        l_width = int(target_size[0] * logo_width_ratio)
        l_height = int(logo.height * (l_width / logo.width))
        logo = logo.resize((l_width, l_height), Image.Resampling.LANCZOS)
        
        product = Image.open(product_path)
        if product.mode != 'RGB':
            product = product.convert('RGB')
            
        max_internal_size = (target_size[0] - 100, target_size[1] - 150)
        product.thumbnail(max_internal_size, Image.Resampling.LANCZOS)
        
        p_x = (target_size[0] - product.width) // 2
        p_y = (target_size[1] - product.height) // 2 + 50
        canvas.paste(product, (p_x, p_y))
        
        l_x = int(logo_x_center - (logo.width / 2))
        l_y = int(logo_y)
        canvas.paste(logo, (l_x, l_y), logo)
        
        return canvas
    except Exception as e:
        print(f"Error en preview: {e}")
        return None
