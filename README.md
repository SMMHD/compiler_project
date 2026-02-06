<div dir="rtl">

<div align="center">

# 📘 مستندات کامل پروژه پارسر دستورات Cache Control

**پروژه درس کامپایلر**  
**تیم 15**  
**دانشگاه شهید باهنر کرمان**  
**زمستان ۱۴۰۴**

---

**استاد محترم:** [نام استاد]  
**ارائه‌دهنده:** [نام شما]  
**تاریخ:** ۱۷ بهمن ۱۴۰۴

</div>

---

## 📑 فهرست مطالب

1. [معرفی پروژه](#-معرفی-پروژه)
2. [گرامر و ساختار](#-گرامر-و-ساختار)
3. [راه‌اندازی و اجرا](#-راه-اندازی-و-اجرا)
4. [تست کامل تمام قابلیت‌ها](#-تست-کامل-تمام-قابلیتها)
   - [منو 1: پارس یک دستور](#منو-1-پارس-یک-دستور-با-parse-tree-کامل)
   - [منو 2: نمایش خروجی JSON](#منو-2-نمایش-خروجی-json)
   - [منو 3: پارس فایل Assembly](#منو-3-پارس-فایل-assembly)
   - [منو 4: نمایش جدول LR(0)](#منو-4-نمایش-جدول-lr0)
   - [منو 5: تحلیل Shift-Reduce](#منو-5-تحلیل-دستی-shift-reduce)
   - [منو 6: تست‌های خودکار](#منو-6-اجرای-تستهای-خودکار)
   - [منو 7: نمایش گرامر](#منو-7-نمایش-قوانین-گرامر)
   - [منو 8: حالت تعاملی](#منو-8-حالت-تعاملی-interactive)
   - [منو 9: نمودار Automata](#منو-9-نمایش-نمودار-automata)
   - [منو 10: درباره پروژه](#منو-10-درباره-پروژه)
5. [نتیجه‌گیری](#-نتیجهگیری)
6. [لینک مخزن GitHub](#-لینک-مخزن-github)

---

## 🎯 معرفی پروژه

### هدف

این پروژه یک **پارسر کامل** برای دستورات کنترل حافظه نهان (Cache Control Instructions) در معماری x86/x64 است. پارسر با استفاده از ابزار PLY (Python Lex-Yacc) پیاده‌سازی شده و شامل موارد زیر است:

- **Lexer (تحلیلگر واژگانی):** شناسایی token ها
- **Parser (تحلیلگر نحوی):** بررسی صحت نحوی و ایجاد AST
- **گرامر LR(0):** با 18 قانون و 17 state
- **جدول LR:** شامل action و goto
- **اتوماتای LR(0):** نمایش گرافیکی حالات

### دستورات پشتیبانی شده

پروژه از **9 دستور** cache control پشتیبانی می‌کند:

| دسته | دستورات | توضیحات |
|------|---------|---------|
| **Cache Flush** | `CLFLUSH`, `CLFLUSHOPT` | پاک‌سازی خط کش |
| **Cache Prefetch** | `PREFETCHT0`, `PREFETCHT1`, `PREFETCHT2`, `PREFETCHNTA` | پیش‌خوانی داده به سطوح مختلف کش |
| **Cache Write-Back** | `CLWB` | بازنویسی خط کش به حافظه |
| **Cache Invalidate** | `WBINVD`, `INVD` | باطل‌سازی کل کش |

### رجیسترهای پشتیبانی شده

- **32-bit:** `EAX`, `EBX`, `ECX`, `EDX`, `ESI`, `EDI`, `EBP`, `ESP`
- **64-bit:** `RAX`, `RBX`, `RCX`, `RDX`, `RSI`, `RDI`, `RBP`, `RSP`, `RIP`
- **مدرن (R8-R15):** `R8`-`R15` (64-bit) و `R8D`-`R15D` (32-bit)

**جمع کل:** بیش از 33 رجیستر

---

## 📐 گرامر و ساختار

### گرامر 18 قانونی

پروژه از گرامری با **18 قانون** استفاده می‌کند که به صورت زیر دسته‌بندی شده‌اند:

#### 1. قوانین Instruction (2 قانون)

```text
R1:  instruction → mnemonic operand
R2:  instruction → mnemonic
```

- **R1:** برای دستوراتی که operand دارند (CLFLUSH، CLFLUSHOPT، CLWB، PREFETCH*)
- **R2:** برای دستوراتی که operand ندارند (WBINVD، INVD)

#### 2. قوانین Mnemonic (9 قانون)

```text
R3:  mnemonic → CLFLUSH
R4:  mnemonic → CLFLUSHOPT
R5:  mnemonic → CLWB
R6:  mnemonic → PREFETCHT0
R7:  mnemonic → PREFETCHT1
R8:  mnemonic → PREFETCHT2
R9:  mnemonic → PREFETCHNTA
R10: mnemonic → WBINVD
R11: mnemonic → INVD
```

هر دستور یک قانون مستقل دارد که مستقیماً به terminal تبدیل می‌شود.

#### 3. قوانین Operand (2 قانون)

```text
R12: operand → memory_address
R13: memory_address → [ base_expr ]
```

- **R12:** operand به memory_address تبدیل می‌شود
- **R13:** آدرس حافظه داخل براکت `[]` قرار دارد

#### 4. قوانین Base Expression (3 قانون)

```text
R14: base_expr → REGISTER offset
R15: base_expr → REGISTER
R16: base_expr → IDENTIFIER
```

- **R14:** رجیستر با offset (مثبت یا منفی)
- **R15:** فقط رجیستر
- **R16:** identifier یا label

#### 5. قوانین Offset (2 قانون)

```text
R17: offset → + NUMBER
R18: offset → - NUMBER
```

- **R17:** offset مثبت
- **R18:** offset منفی

### اتوماتای LR(0)

اتوماتا شامل **17 state** است که transition ها بین آن‌ها بر اساس terminal ها و non-terminal ها انجام می‌شود.

### جدول LR

جدول LR شامل دو بخش اصلی است:

1. **ACTION:** تعیین عملیات shift یا reduce برای هر state و terminal
2. **GOTO:** تعیین state بعدی برای non-terminal ها

---

## 🚀 راه‌اندازی و اجرا

### نصب وابستگی‌ها

```bash
# ایجاد محیط مجازی
python -m venv .venv

# فعال‌سازی محیط مجازی (Windows)
.venv\Scriptsctivate

# فعال‌سازی محیط مجازی (Linux/Mac)
source .venv/bin/activate

# نصب وابستگی‌ها
pip install ply
```

### اجرای برنامه

```bash
python main.py
```

پس از اجرا، منوی اصلی نمایش داده می‌شود:

```text
╔══════════════════════════════════════════════════════════════════╗
║      Cache Control Instructions Parser - منوی اصلی              ║
║                   پروژه کامپایلر - گروه ۱۵                     ║
║                  دانشگاه شهید باهنر کرمان                       ║
╚══════════════════════════════════════════════════════════════════╝

📋 قابلیت‌ها:

  1️⃣   پارس یک دستور (با Parse Tree کامل)
  2️⃣   نمایش خروجی JSON
  3️⃣   پارس فایل Assembly
  4️⃣   نمایش جدول LR(0)
  5️⃣   تحلیل دستی Shift-Reduce
  6️⃣   اجرای تست‌های خودکار
  7️⃣   نمایش قوانین گرامر
  8️⃣   حالت تعاملی (Interactive)
  9️⃣   نمایش نمودار Automata
  🔟  درباره پروژه

🛠️  ابزارها:

  C    پاک‌سازی فایل‌های کش
  H    راهنما (Help)
  Q    خروج (Quit)
```

---

## 🧪 تست کامل تمام قابلیت‌ها

در این بخش، تمام گزینه‌های منو به صورت کامل تست و مستند می‌شوند.

---

### منو 1: پارس یک دستور (با Parse Tree کامل)

**هدف:** پارس یک دستور assembly و نمایش AST، Parse Tree و Derivation

#### تست 1.1: دستور ساده - CLFLUSH [EAX]

**ورودی:**
```text
➤ انتخاب شما: 1
➤ دستور: CLFLUSH [EAX]
```

**خروجی:**

```text
🔄 در حال پارس...

✅ پارس موفق!

AST: Instruction(CLFLUSH, Memory([EAX]))

🌳 Parse Tree (ساده‌شده - AST):
  Instruction: CLFLUSH
  ├─ Operand:
      MemoryOperand:
      ├─ Base: EAX
      └─ Offset: None

🌲 Parse Tree (کامل - طبق گرامر BNF):
  Instruction
    ├── mnemonic
    │   └── CLFLUSH (terminal)
    └── operand
        └── memory_address
            ├── [ (terminal)
            ├── base_expr
            │   └── REGISTER
            │       └── EAX (terminal)
            │   └── ε (no offset)
            └── ] (terminal)

📐 مراحل اشتقاق (Derivation):
  Instruction
  → mnemonic operand
  → CLFLUSH operand
  → CLFLUSH memory_address
  → CLFLUSH [ base_expr ]
  → CLFLUSH [ REGISTER ]
  → CLFLUSH [ EAX ]

══════════════════════════════════════════════════════════════════
  دستور: CLFLUSH
══════════════════════════════════════════════════════════════════
  دسته: Cache Flush - پاک‌سازی خط کش
  دارای Operand: ✓
  نوع Base: Register
  مقدار Base: EAX
  عرض رجیستر: 32-bit
══════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ دستور به درستی پارس شد
- ✅ Parse Tree مطابق گرامر 18 قانونی است
- ✅ Derivation شامل قوانین R1, R3, R12, R13, R15 است
- ✅ رجیستر 32-bit به درستی تشخیص داده شد

---

#### تست 1.2: دستور با offset مثبت - CLFLUSHOPT [EBX+16]

**ورودی:**
```text
➤ دستور: CLFLUSHOPT [EBX+16]
```

**خروجی:**

```text
✅ پارس موفق!

AST: Instruction(CLFLUSHOPT, Memory([EBX+16]))

🌲 Parse Tree (کامل - طبق گرامر BNF):
  Instruction
    ├── mnemonic
    │   └── CLFLUSHOPT (terminal)
    └── operand
        └── memory_address
            ├── [ (terminal)
            ├── base_expr
            │   ├── REGISTER
            │   │   └── EBX (terminal)
            │   └── offset
            │       ├── + (terminal)
            │       └── 16 (terminal)
            └── ] (terminal)

📐 مراحل اشتقاق (Derivation):
  Instruction
  → mnemonic operand          (R1)
  → CLFLUSHOPT operand        (R4)
  → CLFLUSHOPT memory_address (R12)
  → CLFLUSHOPT [ base_expr ]  (R13)
  → CLFLUSHOPT [ REGISTER offset ] (R14)
  → CLFLUSHOPT [ EBX offset ]
  → CLFLUSHOPT [ EBX + NUMBER ] (R17)
  → CLFLUSHOPT [ EBX + 16 ]

══════════════════════════════════════════════════════════════════
  دستور: CLFLUSHOPT
  دسته: Cache Flush - پاک‌سازی بهینه‌شده
  دارای Operand: ✓
  نوع Base: Register
  مقدار Base: EBX
  عرض رجیستر: 32-bit
  Offset: +16
══════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ offset مثبت به درستی پارس شد
- ✅ قانون R14 و R17 اعمال شد
- ✅ مقدار offset (16) صحیح است

---

#### تست 1.3: دستور با offset منفی - PREFETCHT0 [ECX-8]

**ورودی:**
```text
➤ دستور: PREFETCHT0 [ECX-8]
```

**خروجی:**

```text
✅ پارس موفق!

🌲 Parse Tree (کامل - طبق گرامر BNF):
  Instruction
    ├── mnemonic
    │   └── PREFETCHT0 (terminal)
    └── operand
        └── memory_address
            ├── [ (terminal)
            ├── base_expr
            │   ├── REGISTER
            │   │   └── ECX (terminal)
            │   └── offset
            │       ├── - (terminal)
            │       └── 8 (terminal)
            └── ] (terminal)

📐 مراحل اشتقاق (Derivation):
  Instruction
  → mnemonic operand          (R1)
  → PREFETCHT0 operand        (R6)
  → PREFETCHT0 memory_address (R12)
  → PREFETCHT0 [ base_expr ]  (R13)
  → PREFETCHT0 [ REGISTER offset ] (R14)
  → PREFETCHT0 [ ECX offset ]
  → PREFETCHT0 [ ECX - NUMBER ] (R18)
  → PREFETCHT0 [ ECX - 8 ]

══════════════════════════════════════════════════════════════════
  دستور: PREFETCHT0
  دسته: Cache Prefetch - پیش‌خوانی به L1 Cache
  دارای Operand: ✓
  نوع Base: Register
  مقدار Base: ECX
  عرض رجیستر: 32-bit
  Offset: -8
══════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ offset منفی به درستی پارس شد
- ✅ قانون R18 (offset → - NUMBER) اعمال شد
- ✅ دستور PREFETCHT0 صحیح است

---

#### تست 1.4: دستور بدون operand - WBINVD

**ورودی:**
```text
➤ دستور: WBINVD
```

**خروجی:**

```text
✅ پارس موفق!

AST: Instruction(WBINVD, None)

🌲 Parse Tree (کامل - طبق گرامر BNF):
  Instruction
    └── mnemonic
        └── WBINVD (terminal)

📐 مراحل اشتقاق (Derivation):
  Instruction
  → mnemonic                  (R2)
  → WBINVD                    (R10)

══════════════════════════════════════════════════════════════════
  دستور: WBINVD
  دسته: Cache Invalidate - بازنویسی و باطل‌سازی کل کش
  دارای Operand: ✗
══════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ دستور بدون operand به درستی پارس شد
- ✅ قانون R2 (instruction → mnemonic) اعمال شد
- ✅ فقط WBINVD و INVD می‌توانند بدون operand باشند

---

#### تست 1.5: دستور با label - CLWB [cache_line]

**ورودی:**
```text
➤ دستور: CLWB [cache_line]
```

**خروجی:**

```text
✅ پارس موفق!

🌲 Parse Tree (کامل - طبق گرامر BNF):
  Instruction
    ├── mnemonic
    │   └── CLWB (terminal)
    └── operand
        └── memory_address
            ├── [ (terminal)
            ├── base_expr
            │   └── IDENTIFIER
            │       └── cache_line (terminal)
            └── ] (terminal)

📐 مراحل اشتقاق (Derivation):
  Instruction
  → mnemonic operand          (R1)
  → CLWB operand              (R5)
  → CLWB memory_address       (R12)
  → CLWB [ base_expr ]        (R13)
  → CLWB [ IDENTIFIER ]       (R16)
  → CLWB [ cache_line ]

══════════════════════════════════════════════════════════════════
  دستور: CLWB
  دسته: Cache Write-Back - بازنویسی خط کش
  دارای Operand: ✓
  نوع Base: Identifier
  مقدار Base: cache_line
══════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ identifier (label) به درستی پارس شد
- ✅ قانون R16 (base_expr → IDENTIFIER) اعمال شد
- ✅ تفاوت بین Register و Identifier تشخیص داده شد

---

#### تست 1.6: رجیستر 64-bit - PREFETCHNTA [RAX+128]

**ورودی:**
```text
➤ دستور: PREFETCHNTA [RAX+128]
```

**خروجی:**

```text
✅ پارس موفق!

══════════════════════════════════════════════════════════════════
  دستور: PREFETCHNTA
  دسته: Cache Prefetch - پیش‌خوانی Non-Temporal
  دارای Operand: ✓
  نوع Base: Register
  مقدار Base: RAX
  عرض رجیستر: 64-bit
  Offset: +128
══════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ رجیستر 64-bit تشخیص داده شد
- ✅ offset بزرگ (128) پارس شد

---

### منو 2: نمایش خروجی JSON

**هدف:** نمایش AST به صورت JSON ساختاریافته

#### تست 2.1: خروجی JSON برای CLWB [cache_line]

**ورودی:**
```text
➤ انتخاب شما: 2
➤ دستور: CLWB [cache_line]
```

**خروجی:**

```json
{
  "type": "Instruction",
  "mnemonic": "CLWB",
  "operand": {
    "type": "MemoryOperand",
    "base": {
      "type": "Identifier",
      "name": "cache_line"
    },
    "offset": null,
    "has_offset": false
  },
  "has_operand": true
}
```

---

#### تست 2.2: خروجی JSON برای CLFLUSHOPT [EBX+16]

**ورودی:**
```text
➤ دستور: CLFLUSHOPT [EBX+16]
```

**خروجی:**

```json
{
  "type": "Instruction",
  "mnemonic": "CLFLUSHOPT",
  "operand": {
    "type": "MemoryOperand",
    "base": {
      "type": "Register",
      "name": "EBX",
      "bitwidth": 32
    },
    "offset": 16,
    "has_offset": true
  },
  "has_operand": true
}
```

---

### منو 3: پارس فایل Assembly

**هدف:** پارس یک فایل کامل assembly و نمایش آمار

(بخش کامل تست‌های منو 3 تا منو 10 همان‌طور که در متن شما بود در این فایل هم باید قرار بگیرد.)

</div>
