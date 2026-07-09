# Data Model

Data Model สำหรับ Genshin Account Value V1

ใช้สำหรับเก็บข้อมูล Character Tier List ที่ดึงมาจาก Game8

---

## Entity Relationship Diagram

> Version: V1

![ER Diagram](images/data_model_v1.png)

---

## Entity

### CHARACTER

เก็บข้อมูลพื้นฐานของตัวละคร

| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | ชื่อตัวละคร (Primary Key) |
| rarity | int | ระดับดาวของตัวละคร (4 หรือ 5) |

---

### ROLE_TIER

เก็บ Tier ของตัวละครในแต่ละ Role

| Attribute | Type | Description |
|-----------|------|-------------|
| character_name | string | อ้างอิงไปยัง CHARACTER |
| role | string | บทบาทของตัวละคร |
| tier | string | Tier จาก Game8 |
| recommended_constellation | int | กลุ่มดาวที่ Game8 ใช้อ้างอิงในการจัด Tier |

Composite Primary Key

- character_name
- role

---

## Relationship

- Character 1 ตัว สามารถมีได้หลาย Role
- Role Tier แต่ละรายการอ้างอิง Character ได้ 1 ตัว (คือเราใช้ทั้งชื่อและตำแหน่งในการเป็นคีย์ ไม่ได้รับแค่เรื่องตำแหน่งแต่อย่างใด)

Relationship

```text
CHARACTER (1) ----< ROLE_TIER (N)
```

---

## Notes

- ใช้ `name` เป็น Primary Key ใน V1 เนื่องจากชื่อตัวละครไม่ซ้ำกัน
- `recommended_constellation` เป็นค่าที่อ้างอิงจาก Game8 ไม่ใช่กลุ่มดาวของบัญชีผู้เล่น
- ข้อมูล Constellation ของผู้เล่นจะถูกเก็บใน Data Model ของ Account ในอนาคต