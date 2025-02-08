import os

def get_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

path = "C:\\" if os.name == "nt" else "/home"  # Cambia esto según la ruta que quieras analizar

folders = [(f, get_size(os.path.join(path, f)) / (1024**3)) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

folders.sort(key=lambda x: x[1], reverse=True)

for folder, size in folders[:10]:  # Muestra las 10 carpetas más grandes
    print(f"{folder}: {size:.2f} GB")

