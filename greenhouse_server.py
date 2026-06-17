import socket
import random

HOST = '127.0.0.1'
PORT = 65432

soil_moisture = 50.0
day = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🌍 [Greenhouse Server] เปิดระบบควบคุมโรงเรือน... รอการเชื่อมต่อจาก Raspberry Pi")
    conn, addr = s.accept()
    with conn:
        print(f"✅ บอร์ดสมองกลเชื่อมต่อสำเร็จจากตำแหน่ง: {addr}")
        
        while day <= 30:
            # 1. จำลองสภาพอากาศระเหยน้ำ
            if random.randint(0, 100) < 20:
                soil_moisture -= 35.0
                weather = "☀️ แดดแรงจัด"
            else:
                soil_moisture -= 15.0
                weather = "☁️ อากาศปกติ"
            
            if soil_moisture < 0: soil_moisture = 0.0
            
            # 2. ส่งค่าความชื้นและสภาพอากาศไปให้ Raspberry Pi
            status_data = f"{soil_moisture},{weather}"
            conn.sendall(status_data.encode())
            
            action = int(conn.recv(1024).decode())
            
            if action == 1: soil_moisture += 20.0
            elif action == 2: soil_moisture += 45.0
            soil_moisture = min(soil_moisture, 100.0)
            
            print(f"วันที่ {day} [{weather}] -> รับคำสั่ง Action {action} | ความชื้นปัจจุบัน: {soil_moisture:.1f}%")
            day += 1

print("จบการจำลองรอบปลูก 30 วัน ปิดระบบ Server")