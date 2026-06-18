import random
import mysql.connector as mysql

db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "root_password",
    "database": "smartfarm_analytics"
}

def generate_bulk_data(total_records=100000):
    print(f"กำลังเริ่มปั๊มข้อมูลจำลองจำนวน {total_records} แถว ลงฐานข้อมูล...")
    
    try:
        connection = mysql.connect(**db_config)
        cursor = connection.cursor()
        
        # ล้างข้อมูลเก่า 30 แถว
        cursor.execute("TRUNCATE TABLE greenhouse_logs;")
        connection.commit()

        # สร้างชุดข้อมูลแบบรวดเร็ว (Bulk Insert เพื่อความเร็วสูง)
        query = """
        INSERT INTO greenhouse_logs (day_number, weather, moisture_before, action_taken, moisture_after)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        data_batch = []
        soil_moisture = 50.0
        
        for i in range(1, total_records + 1):
            day_num = (i % 30) + 1  
            
            if random.randint(0, 100) < 20:
                soil_moisture -= 35.0
                weather = "Hot"
            else:
                soil_moisture -= 15.0
                weather = "Normal"
                
            if soil_moisture < 0: soil_moisture = 0.0
            moisture_before = soil_moisture
            
            # จำลองการเลือก Action ของ AI แบบสุ่ม (0=ไม่รด, 1=รดน้อย, 2=รดมาก)
            action = random.choice([0, 1, 2])
            if action == 1: soil_moisture += 20.0
            elif action == 2: soil_moisture += 45.0
            soil_moisture = min(soil_moisture, 100.0)
            
            # เติมข้อมูลเข้า Batch
            data_batch.append((day_num, weather, moisture_before, action, soil_moisture))
            
            # ทุกๆ 5,000 แถว ให้ยิงเข้าฐานข้อมูลทีหนึ่ง 
            if i % 5000 == 0:
                cursor.executemany(query, data_batch)
                connection.commit()
                data_batch = []
                print(f"บันทึกเข้าไปแล้ว {i} แถว...")

        cursor.close()
        connection.close()
        print("สำเร็จ! ตอนนี้ฐานข้อมูลของคุณมีข้อมูล Smart Farm อยู่ 100,000 แถวเรียบร้อยแล้ว!")
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    generate_bulk_data(100000) # ปั๊มหนึ่งแสนแถว