from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
import threading
import time

class PacketSenderApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.ip_input = TextInput(text='192.168.1.1', size_hint_y=None, height=40)
        layout.add_widget(Label(text='Target IP:', size_hint_y=None, height=30))
        layout.add_widget(self.ip_input)
        
        self.start_btn = Button(text='START', size_hint_y=None, height=50)
        self.start_btn.bind(on_press=self.start_attack)
        layout.add_widget(self.start_btn)
        
        self.status_label = Label(text='Status: Ready', size_hint_y=None, height=30)
        layout.add_widget(self.status_label)
        
        return layout
    
    def start_attack(self, instance):
        self.status_label.text = 'Status: Sending packets...'
        threading.Thread(target=self.send_packets).start()
    
    def send_packets(self):
        for i in range(10):
            print(f"Sending packet {i}")
            time.sleep(1)
        self.status_label.text = 'Status: Completed'

if __name__ == '__main__':
    PacketSenderApp().run()
