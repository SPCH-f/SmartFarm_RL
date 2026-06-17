import socket
import time
import numpy as np

# ความชื้นกลุ่มต่างๆ ควรเลือกทำอะไร (0=ไม่ทำ, 1=รดน้ำน้อย, 2=รดน้ำมาก)
smart_actions = {0:2, 1:2, 2:2, 3:1, 4:1, 5:1, 6:0, 7:0, 8:0, 9:0, 10:0}

HOST = '127.0.0.1'
PORT = 65432

print("[Raspberry Pi] กำลังบูตระบบสมองกล...")
time.sleep(1)

# ต่อสายเน็ตเวิร์กไปยังตู้ปลูกพืช
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("เชื่อมต่อกับระบบควบคุมโรงเรือนเรียบร้อยแล้ว!")
    
    while True:
        try:
            # 1. รับข้อมูลความชื้นจากโรงเรือน
            data = s.recv(1024).decode()
            if not data: break
            
            moisture, weather = data.split(',')
            moisture = float(moisture)
            
            # 2. สมองบอทคำนวณหากลุ่มความชื้น
            state = int(moisture // 10)
            if state > 10: state = 10
            
            # 3. เลือก Action จากความจำที่ฉลาดแล้ว
            action = smart_actions.get(state, 1)
            
            time.sleep(0.5) 
            
            # 4. ส่งคำสั่ง Action กลับไปที่โรงเรือน
            s.sendall(str(action).encode())
            print(f"อ่านค่าความชื้นได้ {moisture:.1f}% -> ส่งคำสั่งรดน้ำ Action {action} กลับไป")
            
        except ConnectionResetError:
            break

print("จบการทำงาน บอทปิดระบบ")