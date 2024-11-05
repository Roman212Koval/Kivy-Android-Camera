from android.permissions import request_permissions, check_permission, Permission
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from camera4kivy import Preview

class CameraApp(App):
    def build(self):
        self.camera_connected = False
        
        # Основний макет додатку
        layout = BoxLayout(orientation='vertical')

        # Віджет для відображення відео
        self.image_widget = Preview(size_hint_y=0.7)
        layout.add_widget(self.image_widget)

        # Статусний ярлик
        self.status_label = Label(text="Статус: Очікування підключення до камери...")
        layout.add_widget(self.status_label)

        # Панель кнопок
        button_layout = BoxLayout(size_hint_y=0.2)
        
        start_button = Button(text="Підключитися до камери")
        start_button.bind(on_press=self.request_permissions_and_start_camera)
        button_layout.add_widget(start_button)

        stop_button = Button(text="Зупинити камеру")
        stop_button.bind(on_press=self.stop_camera)
        button_layout.add_widget(stop_button)

        layout.add_widget(button_layout)
        return layout

    def request_permissions_and_start_camera(self, instance):
        # Запит дозволів
        request_permissions([
            Permission.CAMERA,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_MEDIA_IMAGES
        ])
        self.check_permissions_and_start_camera()

    def check_permissions_and_start_camera(self):
        # Перевірка дозволів після запиту
        if all(check_permission(perm) for perm in [
            Permission.CAMERA, 
            Permission.WRITE_EXTERNAL_STORAGE, 
            Permission.READ_MEDIA_IMAGES
        ]):
            self.start_camera()
        else:
            self.status_label.text = "Необхідні дозволи не надано. Спробуйте знову."

    def start_camera(self):
        if not self.camera_connected:
            try:
                self.image_widget.connect_camera()  # Підключення до камери через Preview
                self.camera_connected = True
                self.status_label.text = "Статус: Камера підключена"
            except Exception as e:
                self.status_label.text = f"Помилка підключення до камери: {e}"

    def stop_camera(self, instance):
        if self.camera_connected:
            self.image_widget.disconnect_camera()  # Відключення камери
            self.camera_connected = False
            self.status_label.text = "Статус: Камера відключена"

    def on_stop(self):
        if self.camera_connected:
            self.image_widget.disconnect_camera()

if __name__ == '__main__':
    CameraApp().run()
