# Game8 Scraper Design

## วัตถุประสงค์
Scraper นี้มีหน้าที่ดึงข้อมูล Character Tier List จากเว็บไซต์ Game8

## แหล่งข้อมูล (Data Source)
https://game8.co/games/Genshin-Impact/archives/297465

---

## ขอบเขตของ V1

### เก็บข้อมูล

- Character Name
- Rarity
- Tier
- Role
- recommended_constellation

### ยังไม่เก็บ

- Build
- Weapon
- Artifact
- Team Composition
- Character Guide

---

## Design Decisions

### การเลือก Tier List
ใช้ Main Tier List เป็นข้อมูลหลัก
- เป็น tier ที่จะให้คะแนนจากกลุ่มดาวที่เหมาะสมที่สุด 
- 4 ดาวมักจะมีศักยภาพที่ดีอาจะเป็น C2 / C6 
- 5 ดาวมักจะคิดที่ C0 / C1 เพราะมีมูลค่าสูงกว่า 4 ดาว
- ระบบจะคำนวณ Constellation เพิ่มภายหลัง 

### Constellation
- หาก Constellation ไม่ครบ ระบบจะหักคะแนนตามจำนวนที่ขาด
- มีเพิ่มอาจจะบวกคะแนนให้เดี๋ยวขอออกแบบอีกที
- V1 ใช้วิธีคำนวณแบบง่ายก่อน
- V2 จะพัฒนาเป็น Character-specific (อาจจะเน้นที่ C2 กับ C6 ตามประสบการณ์น่ะนะ)

### Recommended Constellation Selection
- ตัวละคร 5
  - พิจารณาเฉพาะ C1 และ C2
  - เลือก Constellation ที่มีคะแนน Rating เต็ม
  - ถ้าทั้ง C1 และ C2 มีคะแนนเท่ากัน ให้เลือก Constellation ที่ต่ำกว่า (เช่น C1)
  - ถ้าทั้ง C1 และ C2 มีคะแนนไม่เต็มจะนับให้เป็น 0

- ตัวละคร 4
  - พิจารณาทุก Constellation
  - เลือก Constellation ที่มีคะแนน Rating สูงที่สุด
  - หากมีหลาย Constellation ที่ได้คะแนนสูงสุด ให้เลือก Constellation ที่สูงกว่า (เช่น C6)

เหตุผล

- ผู้เล่นส่วนใหญ่มีโอกาสได้รับตัวละคร 5★ ถึงระดับ C1 หรือ C2 มากกว่าระดับ C6
- ตัวละคร 4★ สามารถสะสมจนถึง C6 ได้จากการเล่นและการสุ่มในระยะยาว

## Output Schema

| Column | Type | Description |
|--------|------|-------------|
| character_name | string | Character name |
| rarity | int | 4 หรือ 5 |
| role | string | Character role |
| tier | string | Tier จาก Main Tier List |
| recommended_constellation | int | Recommended Constellation จาก Game8 |