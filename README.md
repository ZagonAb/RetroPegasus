# RetroPegasus Converter Tool

RetroPegasus es una herramienta de línea de comandos que facilita la migración de tu biblioteca de RetroArch a Pegasus Frontend, automatizando la creación de metadatos y la organización de assets.

## 🚀 Características

- Detección automática de instalaciones de RetroArch en Windows, Linux y macOS
- Soporte para rutas de instalación personalizadas
- Migración automática de imágenes (boxarts y screenshots)
- Generación automática de archivos metadata.txt compatibles con Pegasus Frontend
- Interfaz de línea de comandos con colores para mejor legibilidad
- Barra de progreso para operaciones largas
- Manejo de errores y validación de rutas

## 📋 Requisitos Previos

### Dependencias Python
```
colorama
tqdm
```

### Instalación de Dependencias
```bash
pip install colorama tqdm
```

## 💻 Sistemas Operativos Soportados

### Windows
- Rutas automáticas soportadas:
  - %APPDATA%/RetroArch
  - C:\Program Files\RetroArch
  - C:\Program Files (x86)\RetroArch

### Linux
- Rutas automáticas soportadas:
  - /usr/bin/retroarch
  - ~/.var/app/org.libretro.RetroArch/config/retroarch/
  - ~/snap/retroarch/current/retroarch
  - ~/.config/retroarch

### macOS
- Rutas automáticas soportadas:
  - ~/Library/Application Support/RetroArch
  - /Applications/RetroArch.app

## 🎮 Sistemas de Juego Soportados

- Amstrad CPC
- Amstrad GX4000
- Arduboy
- Atari 2600
- Wolfenstein 3D
- [Y otros sistemas definidos en SYSTEM_SHORTNAMES]

## 📁 Estructura de Archivos Generada

```
~/pegasus-frontend/
├── [sistema]/
│   ├── metadata.txt
│   └── media/
│       ├── boxFront/
│       │   └── [imágenes de cajas]
│       └── screenshot/
│           └── [capturas de pantalla]
```

## 🛠️ Uso

1. Ejecuta el script:
```bash
python retropegasus.py
```

2. Selecciona una opción:
   - `1`: Escaneo automático de instalación de RetroArch
   - `2`: Introducir ruta personalizada
   - `3`: Salir

3. El script:
   - Buscará las carpetas necesarias (thumbnails y playlists)
   - Procesará las miniaturas y las copiará a la estructura de Pegasus
   - Generará los archivos metadata.txt necesarios

## 📄 Archivos Generados

### metadata.txt
Contiene la información necesaria para Pegasus Frontend:
- Nombre de la colección
- Comando de lanzamiento
- Lista de juegos con sus rutas y assets
- Rutas a imágenes (boxart y screenshots)

## ⚠️ Requisitos de RetroArch

Tu instalación de RetroArch debe tener:
1. Carpeta `thumbnails` con:
   - Named_Boxarts
   - Named_Snaps
2. Carpeta `playlists` con archivos .lpl

## 🔍 Validación

El script verifica:
- Existencia de la instalación de RetroArch
- Presencia de carpetas requeridas
- Contenido válido en las carpetas
- Formatos de archivo correctos

## 🤝 Contribución

Si encuentras bugs o tienes mejoras que sugerir:
1. Abre un issue
2. Describe el problema o mejora
3. Si es posible, proporciona ejemplos

## 📝 Notas

- Las rutas de los juegos en metadata.txt son absolutas
- Las rutas de los assets son relativas a la carpeta del sistema
- El script conserva la estructura original de las playlists de RetroArch

## 📜 Licencia

[Especifica tu licencia aquí]
