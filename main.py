import flet as ft
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


# Pantalla de Configuración con Pestañas
class ConfigScreen:
    def __init__(self, page):
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(self.file_picker)

        # Variables internas para almacenar el estado
        self.selected_file_path = None  # Ruta completa del archivo cargado
        self.file_hash_value = None  # Valor del hash
        self.signature_value = None  # Firma en formato binario

        # Componentes de la interfaz
        self.uploaded_file_path = ft.Text(value="Archivo no seleccionado")
        self.file_hash = ft.Text(value="Hash no calculado")

        # Claves públicas y privadas
        self.private_key, self.public_key = self.generate_keys()
        
        

    def build(self):
        self.page.clean()
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Inicio", content=self.build_inicio_tab()),
                ft.Tab(text="Cargar Archivo", content=self.build_cargar_archivo_tab()),
                ft.Tab(text="Firmar Archivo", content=self.build_firmar_archivo_tab()),
                ft.Tab(text="Verificar Firma", content=self.build_verificar_firma_tab()),
            ],
        )
        self.page.add(
            ft.Text("Configuración de Parámetros", size=24, weight="bold"),
            tabs,
        )

    def build_inicio_tab(self):
        return ft.Column(
            controls=[ft.Text("Esta es la pestaña de inicio.", size=18)]
        )

    def build_cargar_archivo_tab(self):
        def upload_file(e):
            self.file_picker.pick_files(allowed_extensions=["pdf"])

        return ft.Column(
            controls=[
                ft.Text("Carga de Archivos PDF", size=18),
                ft.ElevatedButton("Cargar Archivo", on_click=upload_file),
                self.uploaded_file_path,
                self.file_hash,
            ]
        )

    def on_file_picked(self, result):
        if result.files:
            file = result.files[0]
            self.selected_file_path = file.path  # Guardar la ruta completa del archivo
            self.uploaded_file_path.value = f"Archivo seleccionado: {file.name}"
            self.calculate_hash(file.path)
        else:
            self.uploaded_file_path.value = "Archivo no seleccionado"
            self.selected_file_path = None
        self.page.update()

    def calculate_hash(self, file_path):
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
                digest = hashes.Hash(hashes.SHA256())
                digest.update(file_data)
                self.file_hash_value = digest.finalize()  # Guardar el hash internamente
                self.file_hash.value = f"Hash (SHA-256): {self.file_hash_value.hex()}"
        except Exception as e:
            self.file_hash.value = f"Error al calcular el hash: {e}"
        self.page.update()

    def generate_keys(self):
        # Genera las claves pública y privada
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key

    def sign_file(self, e):
        if not self.selected_file_path:
            snack_bar = ft.SnackBar(
                ft.Text("Error: No se ha cargado un archivo para verificar."),
                duration=3000,
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()
            return
        try:
            with open(self.selected_file_path, "rb") as f:
                file_data = f.read()
                # Generar la firma
                self.signature_value = self.private_key.sign(
                    file_data,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH,
                    ),
                    hashes.SHA256(),
                )
                snack_bar = ft.SnackBar(
                    ft.Text("Exito: Firma generada."),
                    duration=3000,
                )
                self.page.overlay.append(snack_bar)
                snack_bar.open = True
                self.page.update()
                print(f"Firma generada correctamente: {self.signature_value.hex()[:50]}")  # Depuración
        except Exception as ex:
            # Mostrar mensaje de error en caso de fallo
            snack_bar = ft.SnackBar(
                ft.Text(f"Error al firmar el archivo: {ex}"), duration=3000
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()
            print(f"Error al firmar el archivo: {ex}")  # Depuración

        # Forzar renderizado de la interfaz
        self.page.update()
        self.page.update()  # Llamada adicional para garantizar el renderizado


    def save_signature(self, e):
        if not self.signature_value:
            snack_bar = ft.SnackBar(
                ft.Text("Error: No se ha generado una firma válida."), duration=3000
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()  # Actualizar la página para reflejar cambios
            return
        try:
            # Guardar la firma en un archivo
            with open("signature.sig", "wb") as f:
                f.write(self.signature_value)  # Usar directamente la variable interna
            snack_bar = ft.SnackBar(
                ft.Text("Firma guardada como 'signature.sig'"), duration=3000
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()  # Actualizar la página para reflejar cambios
        except Exception as ex:
            snack_bar = ft.SnackBar(
                ft.Text(f"Error al guardar la firma: {ex}"), duration=3000
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()  # Actualizar la página para reflejar cambios

    def build_firmar_archivo_tab(self):
        return ft.Column(
            controls=[
                ft.Text("Firma Digital", size=18),
                ft.ElevatedButton("Firmar Archivo", on_click=self.sign_file),
                ft.ElevatedButton("Guardar Firma", on_click=self.save_signature),
            ]
        )
    
    

    def verify_signature(self, e):
        if not self.selected_file_path:
            # Mostrar error si no se ha cargado un archivo
            snack_bar = ft.SnackBar(
                ft.Text("Error: No se ha cargado un archivo para verificar."),
                duration=3000,
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()
            return
    
        try:
            # Leer el archivo firmado
            with open(self.selected_file_path, "rb") as f:
                file_data = f.read()
    
            # Leer la firma desde el archivo signature.sig
            with open("signature.sig", "rb") as sig_file:
                loaded_signature = sig_file.read()
    
            # Verificar la firma con la clave pública
            self.public_key.verify(
                loaded_signature,
                file_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
    
            # Mostrar mensaje si la firma es válida
            snack_bar = ft.SnackBar(
                ft.Text("Firma válida: El archivo no ha sido alterado."), duration=3000
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
        except Exception as ex:
            # Mostrar mensaje si la firma no es válida o ocurre un error
            snack_bar = ft.SnackBar(
                ft.Text(f"Firma no válida: el archivo fue alterado"), duration=3000
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
        self.page.update()
    
    def build_verificar_firma_tab(self):
        return ft.Column(
            controls=[
                ft.Text("Verificación de Firma Digital", size=18),
                ft.ElevatedButton(
                    "Cargar Archivo PDF",
                    on_click=lambda _: self.file_picker.pick_files(allowed_extensions=["pdf"]),
                ),
                ft.ElevatedButton("Verificar Firma", on_click=self.verify_signature),
            ]
        )




# Función principal
def main(page: ft.Page):
    page.title = "Firma Digital - Navegación con Pestañas"
    page.window.width = 800
    page.window.height = 600
    ConfigScreen(page).build()


# Ejecutar la aplicación
ft.app(target=main)
