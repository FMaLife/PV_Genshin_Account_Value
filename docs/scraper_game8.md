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