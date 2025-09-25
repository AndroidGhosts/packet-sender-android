from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
import socket
import random
import threading
import time
from datetime import datetime

class CyberPacketSender(App):
    def build(self):
        # الواجهة الرئيسية
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # العنوان
        title = Label(
            text='[b]CYBER PACKET SENDER[/b]',
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(title)
        
        # حقل IP الهدف
        layout.add_widget(Label(text='Target IP:', size_hint_y=None, height=30))
        self.ip_input = TextInput(
            text='192.168.1.1',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.ip_input)
        
        # حقل المنفذ
        layout.add_widget(Label(text='Port Range:', size_hint_y=None, height=30))
        self.port_input = TextInput(
            text='80-100',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.port_input)
        
        # اختيار البروتوكول
        layout.add_widget(Label(text='Protocol:', size_hint_y=None, height=30))
        self.protocol_spinner = Spinner(
            text='TCP',
            values=('TCP', 'UDP'),
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.protocol_spinner)
        
        # عدد الحزم
        layout.add_widget(Label(text='Packets Count:', size_hint_y=None, height=30))
        self.packets_input = TextInput(
            text='10',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.packets_input)
        
        # أزرار التحكم
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.start_btn = Button(
            text='[b]🚀 START[/b]',
            markup=True,
            background_color=(0, 1, 0, 1),
            on_press=self.start_attack
        )
        btn_layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(
            text='[b]⏹️ STOP[/b]',
            markup=True,
            background_color=(1, 0, 0, 1),
            on_press=self.stop_attack,
            disabled=True
        )
        btn_layout.add_widget(self.stop_btn)
        
        layout.add_widget(btn_layout)
        
        # شريط الحالة
        self.status_label = Label(
            text='[b]Status:[/b] Ready',
            markup=True,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.status_label)
        
        # منطقة السجل
        self.log_label = Label(
            text='Application started successfully!\nEducational use only!',
            size_hint_y=1,
            halign='left',
            valign='top'
        )
        layout.add_widget(self.log_label)
        
        return layout
    
    def start_attack(self, instance):
        """بدء الهجوم"""
        try:
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
            self.status_label.text = '[b]Status:[/b] Attacking...'
            
            # الحصول على القيم من الواجهة
            target_ip = self.ip_input.text
            port_range = self.port_input.text
            protocol = self.protocol_spinner.text
            packets_count = int(self.packets_input.text)
            
            self.log(f'🚀 Starting {protocol} attack on {target_ip}')
            self.log(f'📦 Sending {packets_count} packets')
            
            # بدء الهجوم في thread منفصل
            thread = threading.Thread(
                target=self.run_attack,
                args=(target_ip, port_range, protocol, packets_count)
            )
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.log(f'❌ Error: {str(e)}')
            self.stop_attack(None)
    
    def stop_attack(self, instance):
        """إيقاف الهجوم"""
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = '[b]Status:[/b] Stopped'
        self.log('🛑 Attack stopped by user')
    
    def run_attack(self, target_ip, port_range, protocol, packets_count):
        """منطق إرسال الحزم"""
        try:
            for i in range(packets_count):
                # التحقق إذا تم الإيقاف
                if not self.stop_btn.disabled:
                    break
                
                # إرسال الحزمة
                if protocol == 'TCP':
                    self.send_tcp_packet(target_ip, port_range)
                else:
                    self.send_udp_packet(target_ip, port_range)
                
                # تحديث الواجهة
                packet_num = i + 1
                Clock.schedule_once(
                    lambda dt: self.update_progress(packet_num, packets_count), 
                    0
                )
                
                time.sleep(0.5)  # تأخير بين الحزم
            
            # إكمال الهجوم
            if self.stop_btn.disabled:
                Clock.schedule_once(lambda dt: self.complete_attack(), 0)
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.log(f'❌ Attack error: {str(e)}'), 0)
            Clock.schedule_once(lambda dt: self.stop_attack(None), 0)
    
    def update_progress(self, current, total):
        """تحديث تقدم الهجوم"""
        self.status_label.text = f'[b]Status:[/b] Sending {current}/{total}'
        self.log(f'📤 Sent packet {current}/{total}')
    
    def complete_attack(self):
        """إكمال الهجوم"""
        self.status_label.text = '[b]Status:[/b] Completed'
        self.log('✅ Attack completed successfully!')
        self.stop_attack(None)
    
    def send_tcp_packet(self, target_ip, port_range):
        """إرسال حزمة TCP"""
        try:
            # تحليل نطاق المنفذ
            if '-' in port_range:
                start_port, end_port = map(int, port_range.split('-'))
                port = random.randint(start_port, end_port)
            else:
                port = int(port_range)
            
            # إنشاء وإرسال الحزمة
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((target_ip, port))
            sock.close()
            
        except Exception:
            pass
    
    def send_udp_packet(self, target_ip, port_range):
        """إرسال حزمة UDP"""
        try:
            if '-' in port_range:
                start_port, end_port = map(int, port_range.split('-'))
                port = random.randint(start_port, end_port)
            else:
                port = int(port_range)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            sock.sendto(b'TEST_PACKET', (target_ip, port))
            sock.close()
            
        except Exception:
            pass
    
    def log(self, message):
        """إضافة رسالة للسجل"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        current_text = self.log_label.text
        self.log_label.text = f'[{timestamp}] {message}\n{current_text}'

if __name__ == '__main__':
    CyberPacketSender().run()
