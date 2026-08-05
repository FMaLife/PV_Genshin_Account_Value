# Game8 Scraper Design

## วัตถุประสงค์

Scraper นี้มีหน้าที่ดึงข้อมูล Character Tier List และ Constellation Rating จากเว็บไซต์ Game8

## แหล่งข้อมูล (Data Source)

Tier List: <https://game8.co/games/Genshin-Impact/archives/297465>

หน้าตัวละครแต่ละตัว: `https://game8.co/games/Genshin-Impact/archives/{id}` (ลิงก์มาจากคอลัมน์ `character_url` ในผลลัพธ์ของ `scrape_tier.py`)

---

## ขอบเขตของ V1 (อัปเดต)

### เก็บข้อมูล

- Character Name
- Rarity
- Tier
- Role
- Constellation ที่ Game8 ให้ Rating เป็นดาว (**ทุกตัว ไม่ใช่แค่ตัวเดียว** — เปลี่ยนจากดีไซน์เดิม ดูหัวข้อ "การเปลี่ยนแปลงจาก V1 เดิม")

### ยังไม่เก็บ

- Build
- Weapon
- Artifact
- Team Composition
- Character Guide

---

## การเปลี่ยนแปลงจาก V1 เดิม

ดีไซน์เดิมของ V1 เลือก "Recommended Constellation" แค่ **ตัวเดียว** ต่อตัวละคร (ดูหัวข้อ Recommended Constellation Selection ด้านล่าง ซึ่งเก็บไว้เป็นบันทึกทางประวัติศาสตร์) โดยมีเหตุผลว่า:

- ตัวละคร 5★ ผู้เล่นมีโอกาสได้แค่ C1/C2 เป็นหลัก
- ตัวละคร 4★ สะสมได้ถึง C6 ในระยะยาว

แต่พบว่า **ตัวละครส่วนใหญ่ Game8 ติดดาวมากกว่า 1 Constellation พร้อมกัน** (เช่น C1, C2, C4) การบีบเหลือ "ดีที่สุดตัวเดียว" ทำให้ข้อมูลหายไปเยอะ และไม่สอดคล้องกับวิธีคิดคะแนนที่ต้องการ (บวกโบนัสสะสมทุกระดับที่ผู้เล่นมี ไม่ใช่ยึดตัวเดียว)

**V2 (ปัจจุบัน)**: scrape เก็บทุก Constellation ที่ติดดาว (1-3 ดาว) พร้อมจำนวนดาว ออกเป็นไฟล์แยก `G8_character_constellations.csv` แทนการยัดรวมในไฟล์ character info

---

## Design Decisions

### การเลือก Tier List

ใช้ Main Tier List เป็นข้อมูลหลัก

### Constellation Parsing — จุดที่แก้บั๊กไปแล้ว

พบและแก้ 2 บั๊กสำคัญระหว่างพัฒนา:

1. **ชื่อตัวละครมี " C0" ติดท้าย** — สาเหตุจาก alt text ของไอคอนใน Tier List เป็นรูปแบบ `"Genshin - {ชื่อ} C0 {Role} Rank"` (C0 หมายถึง Tier ถูกประเมินที่ Constellation 0) ตัว `.replace()` เดิมจับได้แค่ส่วน `DPS Rank` ไม่ได้ตัดคำว่า `C0` ที่แทรกอยู่กลางข้อความ แก้โดยเพิ่ม regex `re.sub(r"\s+C\d$", "", name)` ตัดท้ายชื่อ
2. **ดึง Constellation Rating ผิด table** — หน้า Game8 มี 2 จุดที่ heading มีคำว่า "Best Constellation" ปรากฏอยู่ (หัวข้อ section ใหญ่ที่ตามด้วยตาราง "Constellation and Effects" ซึ่งไม่มีดาว, และหัวข้อย่อย "...Rating and Explanation" ที่มีดาวจริง) โค้ดเดิมใช้ `header.find_next("table")` ซึ่งหยิบ table แรกที่เจอโดยไม่ตรวจสอบเนื้อหา ทำให้บางหน้าได้ table ผิด (ไม่มีดาวเลย → ได้ค่าว่าง/C0 เสมอ) แก้โดยเปลี่ยนเป็น `find_all_next("table")` แล้ววนเช็คว่า table นั้นมีสัญลักษณ์ `★` จริงก่อนถึงจะใช้

### Recommended Constellation Selection (ดีไซน์เดิม — เก็บไว้อ้างอิง ไม่ได้ใช้แล้ว)

- ตัวละคร 5★: พิจารณาเฉพาะ C1/C2, เลือกตัวที่ Rating เต็ม
- ตัวละคร 4★: พิจารณาทุก Constellation, เลือกตัวที่ Rating สูงสุด

ปัจจุบันไม่เลือก "ตัวเดียว" อีกต่อไป — เก็บทุก Constellation ที่ติดดาว (>0) ทั้งหมด

---

## Output Schema

### `G8_character_tiers.csv`

| Column         | Type   | Description                     |
| -------------- | ------ | -------------------------------- |
| character_name | string | Character name (ตัดคำต่อท้ายผิดๆ ออกแล้ว) |
| role           | string | Character role                  |
| tier           | string | Tier จาก Main Tier List         |
| character_url  | string | ลิงก์หน้าตัวละครใน Game8         |

### `G8_character_info.csv`

| Column         | Type   | Description             |
| -------------- | ------ | ------------------------ |
| character_name | string | Character name          |
| role           | string | Role ตอน dedupe (ค่าแรกที่เจอ) |
| tier           | string | Tier ตอน dedupe          |
| character_url  | string | ลิงก์หน้าตัวละคร          |
| rarity         | int    | 4 หรือ 5                 |

### `G8_character_constellations.csv` (ใหม่)

| Column         | Type   | Description                          |
| -------------- | ------ | -------------------------------------- |
| character_name | string | Character name                        |
| constellation  | string | เช่น "C1", "C2", ... (เฉพาะที่ติดดาว)   |
| stars          | int    | 1-3                                    |