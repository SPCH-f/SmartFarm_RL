import socket
import json
import random
import mysql.connector as mysql

HOST = "127.0.0.1"
PORT = 65432

db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "root_password",
    "database": "smartfarm_analytics"
}

def save_to_database(day, weather, m_before, action, m_after):
    """ฟังก์ชันสำหรับบันทึกข้อมูล Log ลง MySQL ใน Docker"""
    try:
        connection = mysql.connect(**db_config)
        cursor = connection.cursor()
        
        query = """
        INSERT INTO greenhouse_logs (day_number, weather, moisture_before, action_taken, moisture_after)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (day, weather, m_before, action, m_after)
        
        cursor.execute(query, values)
        connection.commit() 
        
        cursor.close()
        connection.close()
        print(f"💾 [Database] Successfully logged Day {day} data to MySQL Container.")
    except Exception as e:
        print(f"❌ [Database Error] Cannot connect or insert data: {e}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("เปิดระบบควบคุมโรงเรือน... รอการเชื่อมต่อจาก Raspberry Pi")
    conn, addr = s.accept()
    
    with conn:
        print(f"✅ บอร์ดสมองกลเชื่อมต่อสำเร็จจากตำแหน่ง: {addr}")
        
        day = 1
        soil_moisture = 50.0 
        
        while day <= 30:
            if random.randint(0, 100) < 20:
                soil_moisture -= 35.0
                weather = "Hot"  
            else:
                soil_moisture -= 15.0
                weather = "Normal"
            
            if soil_moisture < 0: 
                soil_moisture = 0.0
            
            moisture_before = soil_moisture
            
            status_data = f"{soil_moisture},{weather}"
            conn.sendall(status_data.encode())
            
            action = int(conn.recv(1024).decode())
            
            if action == 1: 
                soil_moisture += 20.0
            elif action == 2: 
                soil_moisture += 45.0
            soil_moisture = min(soil_moisture, 100.0)
            
            print(f"วันที่ {day} [{weather}] -> รับคำสั่ง Action {action} | ความชื้นปัจจุบัน: {soil_moisture:.1f}%")
            
            save_to_database(day, weather, moisture_before, action, soil_moisture)
            
            day += 1

print("จบการจำลองรอบปลูก 30 วัน ปิดระบบ Server")