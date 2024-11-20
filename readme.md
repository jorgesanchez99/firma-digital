# Firma Digital - Navegación con Pestañas

Este proyecto es una aplicación de firma digital que permite cargar, firmar y verificar archivos PDF utilizando claves RSA. La interfaz de usuario está construida con el framework Flet.

## Características

- **Carga de Archivos**: Permite cargar archivos PDF desde el sistema de archivos.
- **Generación de Hash**: Calcula el hash SHA-256 del archivo cargado.
- **Firma Digital**: Genera una firma digital del archivo utilizando una clave privada RSA.
- **Verificación de Firma**: Verifica la firma digital del archivo utilizando una clave pública RSA.

## Requisitos

- Python 3.8 o superior
- Flet
- cryptography

## Instalación

1. Clona este repositorio:
    ```sh
    git clone https://github.com/jorgesanchez99/firma-digital.git
    cd firma-digital
    ```

2. Instala las dependencias:
    ```sh
    pip install flet cryptography
    ```

## Uso

1. Ejecuta la aplicación:
    ```sh
    python main.py
    ```

2. Interactúa con la interfaz para cargar, firmar y verificar archivos PDF.

## Estructura del Proyecto

- `main.py`: Archivo principal que contiene la lógica de la aplicación.
- `signature.sig`: Archivo donde se guarda la firma digital generada.

## Funcionalidades

### Cargar Archivo

Permite seleccionar un archivo PDF desde el sistema de archivos y calcula su hash SHA-256.

### Firmar Archivo

Genera una firma digital del archivo cargado utilizando una clave privada RSA y guarda la firma en el archivo `signature.sig`.

### Verificar Firma

Verifica la firma digital del archivo cargado utilizando una clave pública RSA para asegurar que el archivo no ha sido alterado.

