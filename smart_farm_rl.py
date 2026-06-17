import numpy as np
import random

# =====================================================================
# ส่วนที่ 1: ตู้ปลูกพืชจำลอง "อากาศแปรปรวน" 
# =====================================================================
class SmartFarmEnv:
    def __init__(self):
        self.soil_moisture = 50.0  
        self.day = 1               
        self.max_days = 30         
        
    def step(self, action):
        # สุ่มเลขระหว่าง 0 ถึง 100 ถ้าได้น้อยกว่า 20 แปลว่าวันนั้นเกิด "ภัยแล้งแดดจัด"
        if random.randint(0, 100) < 20:
            evaporation = 35.0  
            weather_status = "☀️ แดดแรงจัด"
        else:
            evaporation = 15.0  
            weather_status = "☁️ อากาศปกติ"
            
        # หักน้ำตามสภาพอากาศของวันนั้น
        self.soil_moisture -= evaporation
        
        # 2. บอทเลือกว่าจะรดน้ำแบบไหน (0 = ไม่รด, 1 = รดน้ำปกติ, 2 = รดน้ำจัดเต็ม)
        water_cost = 0
        if action == 1:    
            self.soil_moisture += 20.0
            water_cost = 5   
        elif action == 2:  
            self.soil_moisture += 45.0
            water_cost = 15  
            
        self.soil_moisture = min(self.soil_moisture, 100.0)
        if self.soil_moisture < 0: 
            self.soil_moisture = 0.0
        
        # 3. รางวัลบอท
        reward = 0
        if 40.0 <= self.soil_moisture <= 70.0:
            reward += 10  
        elif self.soil_moisture < 20.0 or self.soil_moisture > 90.0:
            reward -= 50  
            
        reward -= water_cost
        
        self.day += 1
        done = self.day > self.max_days
            
        return self.soil_moisture, reward, done, weather_status

def get_state_index(moisture):
    return int(moisture // 10)


# =====================================================================
# ส่วนที่ 2: เทรนบอทในสภาวะปกติ (คอร์สฝึกเดิม 1,000 รอบ)
# =====================================================================
q_table = np.zeros((11, 3))
alpha = 0.1     
gamma = 0.9     
epsilon = 0.2   

print("--- 1. กำลังฝึกบอทในตู้ทดลองสภาวะปกติ 1,000 รอบ ---")
for episode in range(1, 1001):
    env = SmartFarmEnv() 
    done = False
    while not done:
        state = get_state_index(env.soil_moisture)
        if random.uniform(0, 1) < epsilon:
            action = random.choice([0, 1, 2])
        else:
            action = np.argmax(q_table[state])
            
        next_moisture, reward, done, _ = env.step(action)
        next_state = get_state_index(next_moisture)
        
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        q_table[state, action] = old_value + alpha * (reward + gamma * next_max - old_value)

print("ฝึกเสร็จแล้ว! บอทจำแผนการรดน้ำแบบเดิมไว้ในสมองเรียบร้อย\n")


# =====================================================================
# ส่วนที่ 3: สเตป MLOps - ส่งบอทไปเผชิญโลกจริงที่เจอภัยแล้งแบบไม่ทันตั้งตัว
# =====================================================================
print("--- 2. เริ่มปล่อยบอทลงโรงเรือนจริงที่มีภัยแล้งแปรปรวน 30 วัน ---")
env = SmartFarmEnv()
total_reward = 0
done = False

while not done:
    state = get_state_index(env.soil_moisture)
    
    if env.soil_moisture < 35.0:
        action = 2          
        safety_status = "⚠️ [Safety Override!]"
    else:
        action = np.argmax(q_table[state]) 
        safety_status = "[บอทเลือก]"
    
    next_moisture, reward, done, weather = env.step(action)
    total_reward += reward
    
    print(f"วันที่ {env.day-1} [{weather}] -> {safety_status} เลือก Action {action} | ความชื้นเหลือ {next_moisture:.1f}% | คะแนน {reward}")

print("---------------------------------------------")
print(f"จบการทดลอง คะแนนรวมของบอทคือ: {total_reward} คะแนน")