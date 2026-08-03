# Data Model

Data Model สำหรับ Genshin Account Value V1

ใช้สำหรับเก็บข้อมูล Character Tier List และ Constellation Rating ที่ดึงมาจาก Game8
พร้อมข้อมูล Constellation ปัจจุบันของผู้เล่น เพื่อใช้คำนวณคะแนนบัญชี

---

## Entity Relationship Diagram

```
CHARACTER (1) ----< CHARACTER_TIER (N)
CHARACTER (1) ----< CHARACTER_CONSTELLATION (N)
```
> จะทำ diagram ใหม่ทีหลังถ้าจำเป็น ตอนนี้ยึดตาม schema จริงใน `src/sql/schema.sql` เป็นหลัก

---

## Entity

### CHARACTER

เก็บข้อมูลพื้นฐานของตัวละคร

| Attribute      | Type    | Description                       |
| -------------- | ------- | ---------------------------------- |
| character_id   | serial  | Primary Key (auto-generated)      |
| character_name | string  | ชื่อตัวละคร (Unique)              |
| rarity         | smallint| ระดับดาวของตัวละคร (4 หรือ 5)     |

> `recommended_constellation` ที่เคยอยู่ใน entity นี้ถูกย้ายออกไปเป็น entity แยก
> (ดู CHARACTER_CONSTELLATION ด้านล่าง) เพราะตัวละคร 1 ตัวมีได้หลาย constellation ที่แนะนำ

---

### CHARACTER_TIER

เก็บ Tier ของตัวละครในแต่ละ Role 

| Attribute          | Type    | Description                         |
| ------------------ | ------- | ------------------------------------ |
| character_tier_id  | serial  | Primary Key (auto-generated)         |
| character_id        | int     | Foreign Key อ้างอิง CHARACTER         |
| role                | string  | บทบาทของตัวละคร (Main DPS/Sub-DPS/Support) |
| tier                | string  | Tier จาก Game8 (SS/S/A/B/C/D)         |

Unique Constraint

- (character_id, role)

---

### CHARACTER_CONSTELLATION

เก็บทุก Constellation ที่ Game8 ให้คะแนนดาวไว้ 

| Attribute                   | Type     | Description                                 |
| --------------------------- | -------- | -------------------------------------------- |
| character_constellation_id  | serial   | Primary Key (auto-generated)                 |
| character_id                | int      | Foreign Key อ้างอิง CHARACTER                 |
| constellation                | string   | เช่น "C1", "C2", ... "C6"                    |
| stars                        | smallint | จำนวนดาวที่ Game8 ให้ (1-3), เก็บเฉพาะที่ > 0 |

Unique Constraint

- (character_id, constellation)

> ตัวละคร (`recommended_constellation` เดี่ยว) แต่ในทางปฏิบัติ constellation ที่แนะนำ
> มักมาไม่ครบ 1-6 (เช่น C1, C2, C4) และแต่ละตัวก็ควรมีค่าคะแนนของตัวเอง
> เก็บทุกแถวที่ติดดาวไว้ แล้วให้ scoring engine เป็นคนตัดสินใจว่าจะใช้ยังไง

---

### PLAYER_OWNED_CHARACTER (ยังไม่อยู่ใน DB — เป็นไฟล์ CSV)

เก็บ constellation ปัจจุบันของตัวละครที่ผู้เล่นมีอยู่จริง

| Attribute              | Type   | Description                          |
| ----------------------- | ------ | ------------------------------------- |
| character_name          | string | ชื่อตัวละคร (อ้างอิง CHARACTER.character_name) |
| current_constellation   | string | Constellation ปัจจุบันของผู้เล่น เช่น "C0", "C4" |

ปัจจุบันอยู่ในไฟล์ `data/raw/player_owned_characters.csv` ให้ผู้เล่นกรอกเอง
ตัวละครที่ไม่อยู่ในไฟล์นี้ = ผู้เล่นไม่ได้ครอบครอง (ไม่ถูกนับคะแนนเลย)

> แผนในอนาคต: ดึงข้อมูลนี้อัตโนมัติจาก Enka.Network API แทนการกรอกมือ
> (ผู้เล่นใส่ UID → ระบบดึง constellation จาก Character Showcase ในเกม)
> เมื่อทำแล้วค่อยพิจารณาย้าย entity นี้เข้า DB จริง

---

## Relationship

- Character 1 ตัว สามารถมีได้หลาย Role (ผ่าน CHARACTER_TIER)
- Character 1 ตัว สามารถมีได้หลาย Constellation ที่ติดดาว (ผ่าน CHARACTER_CONSTELLATION)
- Player 1 คน มีได้หลาย Owned Character (ปัจจุบันอยู่นอก DB เป็น CSV)

```
CHARACTER (1) ----< CHARACTER_TIER (N)
CHARACTER (1) ----< CHARACTER_CONSTELLATION (N)
```

---

## Notes
- `recommended_constellation` (ค่าเดี่ยว) ถูกยกเลิก เปลี่ยนเป็น CHARACTER_CONSTELLATION
  ที่เก็บได้หลายแถวต่อตัวละคร พร้อมจำนวนดาว
- ข้อมูล Constellation ปัจจุบันของผู้เล่นยังอยู่นอก DB (CSV) เพราะยังไม่มี UI/Auth
  ให้ผู้เล่นแต่ละคนบันทึกข้อมูลแยกกัน — จะย้ายเข้า DB เมื่อ scope ของโปรเจกต์โตขึ้น