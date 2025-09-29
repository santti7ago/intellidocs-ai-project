import os
import shutil

# --- Configuración ---
# El script asume que lo ejecutas desde la carpeta raíz 'intellidocs-ai'
project_root = os.getcwd()

# La ubicación incorrecta de tu carpeta 'app'
source_path = os.path.join(project_root, 'venv', 'app')

# La ubicación correcta para tu carpeta 'app'
destination_path = os.path.join(project_root, 'app')

# --- Lógica Principal ---
print("--- Script de Organización de Carpetas ---")

# 1. Verificar si la carpeta 'app' está en la ubicación incorrecta
if not os.path.isdir(source_path):
    print(f"ERROR: No se encontró la carpeta 'app' en la ubicación incorrecta: {source_path}")
    print("Puede que tus carpetas ya estén organizadas. No se realizará ninguna acción.")
else:
    # 2. Prevenir sobrescrituras accidentales
    if os.path.isdir(destination_path):
        print(f"ERROR: Ya existe una carpeta 'app' en la ubicación correcta: {destination_path}")
        print("Por favor, revisa tus carpetas manualmente para evitar duplicados antes de correr el script.")
    else:
        # 3. Mover la carpeta a la raíz del proyecto
        try:
            print(f"Moviendo la carpeta desde '{source_path}'...")
            print(f"Hacia '{destination_path}'...")
            shutil.move(source_path, destination_path)
            print("\n¡ÉXITO! La carpeta 'app' ha sido movida a la ubicación correcta.")
            print("Tu estructura de proyecto ahora está organizada.")
            print("\nPróximos pasos:")
            print("1. Verifica la nueva estructura en tu explorador de archivos.")
            print("2. Inicia tu servidor con 'uvicorn app.main:app --reload' para confirmar que todo sigue funcionando.")
        except Exception as e:
            print(f"\nOcurrió un error inesperado al mover la carpeta: {e}")