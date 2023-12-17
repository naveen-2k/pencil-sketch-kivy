from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics.texture import Texture
import cv2
import numpy as np
from PIL import Image as PILImage
from io import BytesIO

class ImageSketcher:
    @staticmethod
    def convert_to_pencil_sketch(image_path):
        # Load the image using OpenCV
        img = cv2.imread(image_path)
        # Convert the image to grayscale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Invert the grayscale image
        inverted_img = cv2.bitwise_not(gray_img)
        # Apply GaussianBlur to the inverted image
        blurred_img = cv2.GaussianBlur(inverted_img, (111, 111), 0)
        # Invert the blurred image to get the pencil sketch
        pencil_sketch = cv2.divide(gray_img, 255 - blurred_img, scale=256.0)
        return pencil_sketch

class ImageUploaderApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # FileChooser for image selection
        self.file_chooser = FileChooserListView()
        self.layout.add_widget(self.file_chooser)

        # Upload Button
        upload_button = Button(text="Upload Image")
        upload_button.bind(on_press=self.upload_image)
        self.layout.add_widget(upload_button)

        # Convert Button
        convert_button = Button(text="Convert to Pencil Sketch")
        convert_button.bind(on_press=self.convert_image)
        self.layout.add_widget(convert_button)

        # Image display
        self.image = Image()
        self.layout.add_widget(self.image)

        return self.layout

    def upload_image(self, instance):
        file_path = self.file_chooser.selection and self.file_chooser.selection[0] or None
        if file_path:
            self.image.source = file_path

    def convert_image(self, instance):
        if self.image.source:
            image_path = self.file_chooser.selection[0]
            pencil_sketch = ImageSketcher.convert_to_pencil_sketch(image_path)

            # Convert NumPy array to Kivy Texture
            buf1 = cv2.flip(pencil_sketch, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(pencil_sketch.shape[1], pencil_sketch.shape[0]), colorfmt='luminance')
            image_texture.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')
            self.image.texture = image_texture

            # Save the pencil sketch
            self.save_pencil_sketch(image_path, pencil_sketch)

    def save_pencil_sketch(self, original_path, pencil_sketch):
        output_path = original_path.replace('.jpg', '_sketch.jpg')

        # Convert NumPy array to PIL Image
        pil_image = PILImage.fromarray(pencil_sketch)

        # Save the PIL Image
        pil_image.save(output_path)
        
        # Show a popup with the download link
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f"Pencil sketch saved to:\n{output_path}"))
        content.add_widget(Button(text="OK", on_press=self.dismiss_popup))
        
        popup = Popup(title="Saved!", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

    def dismiss_popup(self, instance):
        instance.parent.dismiss()
        
        


if __name__ == '__main__':
    ImageUploaderApp().run()
