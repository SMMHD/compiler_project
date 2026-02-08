<div dir="rtl">

<div align="center">

# 📘 مستندات کامل پروژه پارسر دستورات Cache Control

**پروژه درس کامپایلر**  
**تیم 15**  
**دانشگاه شهید باهنر کرمان**  
**زمستان ۱۴۰۴**

---

**استاد محترم:** سرکار خانم دکتر شیما شفیعی  
**ارائه‌دهندگان:** سید محمد امین حسینی و سید محمد معین حسینی   

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


### منو 3: پارس فایل Assembly

**هدف:** پارس یک فایل کامل assembly و نمایش آمار

#### تست 3.1: فایل cache_instructions.asm (44 دستور)

**ورودی:**
```
➤ انتخاب شما: 3
➤ نام فایل: cache_instructions.asm
```

**خروجی:**

```
📁 فایل یافت شد: examples/cache_instructions.asm

🔄 در حال پارس فایل...

📊 نتیجه:
✓ موفق: 44 دستور
✗ خطا: 0 دستور

✅ دستورات معتبر:
خط 13: CLFLUSH [EAX] → flush
خط 14: CLFLUSH [EBX+64] → flush
خط 15: CLFLUSH [ECX-16] → flush
خط 17: CLFLUSHOPT [EDX] → flush
خط 18: CLFLUSHOPT [ESI+128] → flush
خط 19: CLFLUSHOPT [cache_data] → flush
خط 25: PREFETCHT0 [EDI] → prefetch
خط 26: PREFETCHT0 [EBP+32] → prefetch
خط 28: PREFETCHT1 [ESP] → prefetch
خط 29: PREFETCHT1 [RAX+256] → prefetch
خط 31: PREFETCHT2 [RBX] → prefetch
خط 32: PREFETCHT2 [RCX-64] → prefetch
خط 34: PREFETCHNTA [RDX+512] → prefetch
خط 35: PREFETCHNTA [data_buffer] → prefetch
خط 41: CLWB [RSI] → writeback
... و 29 دستور دیگر
```

**تحلیل:**
- ✅ 44 دستور همگی موفق پارس شدند
- ✅ هیچ خطایی وجود ندارد
- ✅ انواع مختلف دستورات، رجیسترها و offset ها

---

#### تست 3.2: فایل advanced_test.asm (90 دستور)

**ورودی:**
```
➤ نام فایل: advanced_test.asm
```

**خروجی:**

```
📊 نتیجه:
✓ موفق: 90 دستور
✗ خطا: 0 دستور

✅ دستورات معتبر:
خط 12: CLFLUSH [EAX] → flush
خط 13: CLFLUSH [EBX+1] → flush
خط 14: CLFLUSH [ECX+16] → flush
خط 15: CLFLUSH [EDX+256] → flush
خط 16: CLFLUSH [ESI-1] → flush
خط 17: CLFLUSH [EDI-32] → flush
خط 18: CLFLUSH [EBP-512] → flush
خط 19: CLFLUSH [ESP+0] → flush
خط 25: CLFLUSHOPT [RAX] → flush
خط 26: CLFLUSHOPT [RBX+128] → flush
... و 80 دستور دیگر
```

**تحلیل:**
- ✅ 90 دستور پیشرفته همگی موفق
- ✅ شامل تمام حالات: offset های کوچک، بزرگ، مثبت، منفی، صفر
- ✅ تمام رجیسترها: 32-bit، 64-bit، مدرن (R8-R15)

---

#### تست 3.3: فایل test_mixed.asm (ترکیب صحیح و خطا)

**ورودی:**
```
➤ نام فایل: test_mixed.asm
```

**خروجی:**

```
🔄 در حال پارس فایل...

❌ SYNTAX ERROR at 'INVALID' (type: IDENTIFIER, line: 1)
[پیام راهنمای کامل]

❌ SYNTAX ERROR at 'MOV' (type: IDENTIFIER, line: 1)
کاراکتر غیرمجاز ',' در خط 1
[پیام راهنمای کامل]

❌ SYNTAX ERROR at 'EAX' (type: REGISTER, line: 1)
⚠️ رجیستر بدون '[' و ']'؟
[پیام راهنمای کامل]

... [خطاهای دیگر]

📊 نتیجه:
✓ موفق: 15 دستور
✗ خطا: 7 دستور

✅ دستورات معتبر:
خط 11: CLFLUSH [EAX]
خط 12: CLFLUSHOPT [EBX+32]
خط 13: PREFETCHT0 [ECX-16]
خط 14: WBINVD
خط 15: CLWB [cache_buffer]
... و 10 دستور دیگر

❌ خطاها:
خط 21: INVALID [EAX]
→ پارس ناموفق (دستور نامعتبر)
خط 22: MOV EAX, EBX
→ پارس ناموفق (خارج از scope)
خط 23: CLFLUSH EAX
→ پارس ناموفق (بدون براکت)
خط 24: PREFETCH [ECX]
→ پارس ناموفق (نام اشتباه)
خط 49: ADD EAX, EBX
→ پارس ناموفق (دستور x86 عادی)
خط 50: CLFLUSH [EAX] [EBX]
→ پارس ناموفق (دو operand)
خط 51: CLFLUSHOPT
→ پارس ناموفق (بدون operand - نیاز به operand)
```

**تحلیل:**
- ✅ 15 دستور صحیح به درستی پارس شدند
- ✅ 7 خطا به درستی شناسایی شدند
- ✅ پیام‌های خطا دقیق و راهنما هستند
- ✅ خطای جدید: CLFLUSHOPT بدون operand (نیاز به operand دارد)

---

### منو 4: نمایش جدول LR(0)

**هدف:** نمایش جدول Action-Goto کامل

**ورودی:**
```
➤ انتخاب شما: 4
```

**خروجی:**

```
════════════════════════════════════════════════════════════════════
جدول LR(0) Parser
════════════════════════════════════════════════════════════════════

📊 آمار جدول:
• تعداد States: 17
• تعداد Terminals: 7 (CLFLUSH، CLFLUSHOPT، CLWB، ... ، NUMBER)
• تعداد Non-terminals: 5 (instruction، mnemonic، operand، ...)
• تعداد Actions: 120+
• تعداد Gotos: 60+

════════════════════════════════════════════════════════════════════

┌────────┬─────────────── ACTION ───────────────┬─────── GOTO ───────┐
│ State │ CLFLUSH CLWB [ + - $ │ inst mnem oper │
├────────┼──────────────────────────────────────┼────────────────────┤
│ 0 │ s3 s5 - - - - │ 1 2 - │
│ 1 │ - - - - - acc │ - - - │
│ 2 │ - - s6 - - r2 │ - - 7 │
│ 3 │ - - - - - r3 │ - - - │
│ 4 │ - - - - - r4 │ - - - │
│ 5 │ - - - - - r5 │ - - - │
│ 6 │ - - - - - - │ - - 8 │
│ 7 │ - - - - - r1 │ - - - │
│ 8 │ - - - - - - │ - - - │
│ ... │ ... │ ... │
│ 16 │ - - - s15 s16 - │ - - - │
└────────┴──────────────────────────────────────┴────────────────────┘

راهنما:
• s# : shift به state #
• r# : reduce با قانون #
• acc : accept
• - : error

════════════════════════════════════════════════════════════════════
تعداد Shift Actions: 85
تعداد Reduce Actions: 42
تعداد Accept: 1
تعداد Errors: 73
════════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ جدول کامل با 17 state
- ✅ action های shift و reduce مشخص
- ✅ goto برای non-terminal ها
- ✅ accept در state 1 با $

---

### منو 5: تحلیل دستی Shift-Reduce

**هدف:** نمایش گام‌به‌گام پردازش parser

#### تست 5.1: CLFLUSHOPT [EBX+16]

**ورودی:**
```
➤ انتخاب شما: 5
➤ دستور: CLFLUSHOPT [EBX+16]
```

**خروجی:**

```
════════════════════════════════════════════════════════════════════
تحلیل Shift-Reduce Parser
════════════════════════════════════════════════════════════════════

دستور: CLFLUSHOPT [EBX+16]

Token Stream:
['CLFLUSHOPT', 'LBRACKET', 'REGISTER(EBX)', 'PLUS', 'NUMBER(16)', 'RBRACKET', '$']

────────────────────────────────────────────────────────────────────

گام‌های پردازش:

┌──────┬─────────────────────────┬─────────────────────┬─────────────┐
│ گام │ Stack │ Input │ Action │
├──────┼─────────────────────────┼─────────────────────┼─────────────┤
│ 1 │ [0] │ CLFLUSHOPT [EBX+... │ SHIFT 4 │
│ 2 │ [0, CLFLUSHOPT, 4] │ [EBX+16] $ │ REDUCE R4 │
│ 3 │ [0, mnemonic, 2] │ [EBX+16] $ │ SHIFT 6 │
│ 4 │ [0, mnemonic, 2, [, 6] │ EBX+16] $ │ SHIFT 9 │
│ 5 │ [0, ..., REGISTER, 9] │ +16] $ │ SHIFT 15 │
│ 6 │ [0, ..., +, 15] │ 16] $ │ SHIFT 17 │
│ 7 │ [0, ..., NUMBER, 17] │ ] $ │ REDUCE R17 │
│ 8 │ [0, ..., offset, 16] │ ] $ │ REDUCE R14 │
│ 9 │ [0, ..., base_expr, 8] │ ] $ │ SHIFT 11 │
│ 10 │ [0, ..., ], 11] │ $ │ REDUCE R13 │
│ 11 │ [0, ..., mem_addr, 10] │ $ │ REDUCE R12 │
│ 12 │ [0, mnem, 2, oper, 7] │ $ │ REDUCE R1 │
│ 13 │ [0, instruction, 1] │ $ │ ACCEPT │
└──────┴─────────────────────────┴─────────────────────┴─────────────┘

════════════════════════════════════════════════════════════════════
✅ پارس موفق! (13 گام)

قوانین استفاده شده:
• R4: mnemonic → CLFLUSHOPT
• R17: offset → + NUMBER
• R14: base_expr → REGISTER offset
• R13: memory_address → [ base_expr ]
• R12: operand → memory_address
• R1: instruction → mnemonic operand
════════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ 13 گام تا Accept
- ✅ ترکیب صحیح shift و reduce
- ✅ قوانین R1، R4، R12-R14، R17 استفاده شدند
- ✅ stack و input در هر گام نمایش داده می‌شوند

---

#### تست 5.2: WBINVD (بدون operand)

**ورودی:**
```
➤ دستور: WBINVD
```

**خروجی:**

```
Token Stream:
['WBINVD', '$']

گام‌های پردازش:

┌──────┬─────────────────────────┬─────────────────────┬─────────────┐
│ گام │ Stack │ Input │ Action │
├──────┼─────────────────────────┼─────────────────────┼─────────────┤
│ 1 │ [0] │ WBINVD $ │ SHIFT 10 │
│ 2 │ [0, WBINVD, 10] │ $ │ REDUCE R10 │
│ 3 │ [0, mnemonic, 2] │ $ │ REDUCE R2 │
│ 4 │ [0, instruction, 1] │ $ │ ACCEPT │
└──────┴─────────────────────────┴─────────────────────┴─────────────┘

✅ پارس موفق! (4 گام)

قوانین استفاده شده:
• R10: mnemonic → WBINVD
• R2: instruction → mnemonic
```

**تحلیل:**
- ✅ فقط 4 گام (بدون operand)
- ✅ قانون R2 (instruction → mnemonic) استفاده شد
- ✅ سریع‌تر از دستورات با operand

---

### منو 6: اجرای تست‌های خودکار

**هدف:** اجرای تمام تست‌های واحد

**ورودی:**
```
➤ انتخاب شما: 6
```

**خروجی:**

```
════════════════════════════════════════════════════════════════════
اجرای تست‌های خودکار
════════════════════════════════════════════════════════════════════

🔄 در حال اجرای تست‌ها...

──────────────────────────────────────────────────────────────────
تست 1: Import Parser
──────────────────────────────────────────────────────────────────
✅ موفق - Parser قابل import است

──────────────────────────────────────────────────────────────────
تست 2: پارس دستورات ساده
──────────────────────────────────────────────────────────────────
✅ موفق - CLFLUSH [EAX]
✅ موفق - CLFLUSHOPT [EBX+16]
✅ موفق - PREFETCHT0 [ECX-8]
✅ موفق - WBINVD
✅ موفق - CLWB [cache_line]
✅ موفق - PREFETCHNTA [RAX+128]

──────────────────────────────────────────────────────────────────
تست 3: بررسی AST
──────────────────────────────────────────────────────────────────
✅ موفق - mnemonic صحیح است
✅ موفق - operand وجود دارد
✅ موفق - نوع base صحیح است
✅ موفق - offset صحیح است

──────────────────────────────────────────────────────────────────
تست 4: بررسی Parse Tree
──────────────────────────────────────────────────────────────────
✅ موفق - Parse Tree بدون non-terminal واسطه
✅ موفق - mnemonic مستقیم به terminal می‌رود

──────────────────────────────────────────────────────────────────
تست 5: بررسی Derivation
──────────────────────────────────────────────────────────────────
✅ موفق - Derivation بدون لایه واسطه
✅ موفق - قوانین R1-R18 صحیح هستند

──────────────────────────────────────────────────────────────────
تست 6: بررسی operand requirement
──────────────────────────────────────────────────────────────────
✅ موفق - WBINVD بدون operand (صحیح)
✅ موفق - INVD بدون operand (صحیح)
✅ موفق - CLFLUSHOPT بدون operand → خطا (صحیح)
✅ موفق - CLFLUSH بدون operand → خطا (صحیح)

════════════════════════════════════════════════════════════════════
📊 نتیجه نهایی: 21 موفق، 0 ناموفق
🎉 همه تست‌ها با موفقیت انجام شد!
════════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ 21 تست مختلف
- ✅ تست import، پارس، AST، Parse Tree، Derivation
- ✅ تست operand requirement
- ✅ 100% موفق

---

### منو 7: نمایش قوانین گرامر

**هدف:** نمایش کامل 18 قانون گرامر

**ورودی:**
```
➤ انتخاب شما: 7
```

**خروجی:**

```
════════════════════════════════════════════════════════════════════
قوانین گرامر (18 قانون)
════════════════════════════════════════════════════════════════════

📚 دسته‌بندی قوانین:

┌────────────────────────────────────────────────────────────────┐
│ 1. قوانین Instruction (2 قانون) │
└────────────────────────────────────────────────────────────────┘

R1: instruction → mnemonic operand
(برای دستوراتی که operand دارند)

R2: instruction → mnemonic
(فقط برای WBINVD و INVD)

┌────────────────────────────────────────────────────────────────┐
│ 2. قوانین Mnemonic (9 قانون) │
└────────────────────────────────────────────────────────────────┘

Cache Flush:
R3: mnemonic → CLFLUSH
R4: mnemonic → CLFLUSHOPT

Cache Write-Back:
R5: mnemonic → CLWB

Cache Prefetch:
R6: mnemonic → PREFETCHT0
R7: mnemonic → PREFETCHT1
R8: mnemonic → PREFETCHT2
R9: mnemonic → PREFETCHNTA

Cache Invalidate:
R10: mnemonic → WBINVD
R11: mnemonic → INVD

┌────────────────────────────────────────────────────────────────┐
│ 3. قوانین Operand (2 قانون) │
└────────────────────────────────────────────────────────────────┘

R12: operand → memory_address
R13: memory_address → [ base_expr ]

┌────────────────────────────────────────────────────────────────┐
│ 4. قوانین Base Expression (3 قانون) │
└────────────────────────────────────────────────────────────────┘

R14: base_expr → REGISTER offset
(رجیستر با offset مثبت یا منفی)

R15: base_expr → REGISTER
(فقط رجیستر، بدون offset)

R16: base_expr → IDENTIFIER
(label یا identifier)

┌────────────────────────────────────────────────────────────────┐
│ 5. قوانین Offset (2 قانون) │
└────────────────────────────────────────────────────────────────┘

R17: offset → + NUMBER
(offset مثبت)

R18: offset → - NUMBER
(offset منفی)

════════════════════════════════════════════════════════════════════
📊 خلاصه:
• جمع کل: 18 قانون
• Non-terminals: 6 (instruction، mnemonic، operand، ...)
• Terminals: 16 (CLFLUSH، REGISTER، NUMBER، +، -، [، ]، ...)
• Start Symbol: instruction
════════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ 18 قانون کامل
- ✅ دسته‌بندی منطقی
- ✅ توضیحات فارسی برای هر قانون

---

### منو 8: حالت تعاملی (Interactive)

**هدف:** پارس مداوم دستورات بدون خروج از برنامه

**ورودی:**
```
➤ انتخاب شما: 8
```

**خروجی:**

```
════════════════════════════════════════════════════════════════════
حالت تعاملی Parser
════════════════════════════════════════════════════════════════════

💡 راهنما:
• دستور خود را وارد کنید
• برای خروج 'exit' یا 'quit' تایپ کنید
• برای پاک کردن صفحه 'clear' تایپ کنید

────────────────────────────────────────────────────────────────────

➤ دستور: CLFLUSH [EAX]
✅ پارس موفق! → Instruction(CLFLUSH, Memory([EAX]))

➤ دستور: PREFETCHT0 [RBX+32]
✅ پارس موفق! → Instruction(PREFETCHT0, Memory([RBX+32]))

➤ دستور: WBINVD
✅ پارس موفق! → Instruction(WBINVD, None)

➤ دستور: INVALID [EAX]
❌ خطا: دستور نامعتبر

➤ دستور: CLFLUSH
❌ خطا: CLFLUSH نیاز به operand دارد

➤ دستور: exit

✅ از حالت تعاملی خارج شدید.
آمار:
• دستورات موفق: 3
• دستورات ناموفق: 2
```

**تحلیل:**
- ✅ پارس مداوم بدون خروج
- ✅ آمار در پایان
- ✅ پیام‌های خطای دقیق

---

### منو 9: نمایش نمودار Automata

**هدف:** نمایش تصویری اتوماتای LR(0)

**ورودی:**
```
➤ انتخاب شما: 9
```

**خروجی:**

```
════════════════════════════════════════════════════════════════════
نمودار اتوماتای LR(0)
════════════════════════════════════════════════════════════════════

🔍 اطلاعات اتوماتا:
• تعداد States: 17
• Start State: 0
• Accept State: 1
• تعداد Transitions: 45+

────────────────────────────────────────────────────────────────────

نمودار متنی ساده‌شده:

[State 0]
├─ CLFLUSH ──→ [State 3]
├─ CLFLUSHOPT ──→ [State 4]
├─ CLWB ──→ [State 5]
├─ PREFETCHT0 ──→ [State 6]
├─ WBINVD ──→ [State 10]
├─ INVD ──→ [State 11]
├─ mnemonic ──→ [State 2]
└─ instruction ──→ [State 1] (ACCEPT)

[State 1]
└─ $ ──→ ACCEPT

[State 2]
├─ [ ──→ [State 6]
└─ $ ──→ REDUCE R2

[State 3]
└─ $ ──→ REDUCE R3

... (state های دیگر)

────────────────────────────────────────────────────────────────────

📁 نمودار گرافیکی:
فایل: lr0_automata.png (در صورت وجود Graphviz)

برای ایجاد نمودار گرافیکی:
1. نصب Graphviz: [https://graphviz.org/](https://graphviz.org/)
2. اجرای: python lr0_automata.py

![نمودار گرافیکی]("F:\University\7th term\Compiler\Project\Compiler Project\image.png")

════════════════════════════════════════════════════════════════════
```

**تحلیل:**
- ✅ 17 state با transition ها
- ✅ Accept state مشخص
- ✅ امکان ایجاد تصویر گرافیکی

---

### منو 10: درباره پروژه

**هدف:** اطلاعات کلی پروژه

**ورودی:**
```
➤ انتخاب شما: 10
```

**خروجی:**

```
╔══════════════════════════════════════════════════════════════════╗
║ Cache Control Instructions Parser ║
║ پروژه کامپایلر - گروه ۱۵ ║
╚══════════════════════════════════════════════════════════════════╝

📚 اطلاعات پروژه:

┌──────────────────────────────────────────────────────────────────┐
│ معرفی │
└──────────────────────────────────────────────────────────────────┘

این پروژه یک Parser کامل برای دستورات کنترل حافظه نهان
(Cache Control Instructions) در معماری x86/x64 است.

پیاده‌سازی با PLY (Python Lex-Yacc) و شامل:
• Lexer (تحلیلگر واژگانی)
• Parser (تحلیلگر نحوی)
• گرامر LR(0) با 18 قانون
• اتوماتای 17 حالته
• جدول LR کامل

┌──────────────────────────────────────────────────────────────────┐
│ مشخصات فنی │
└──────────────────────────────────────────────────────────────────┘

دستورات پشتیبانی شده: 9
• CLFLUSH، CLFLUSHOPT (Cache Flush)
• PREFETCHT0، PREFETCHT1، PREFETCHT2، PREFETCHNTA (Prefetch)
• CLWB (Write-Back)
• WBINVD، INVD (Invalidate)

رجیسترهای پشتیبانی شده: 33+
• 32-bit: EAX، EBX، ECX، ...
• 64-bit: RAX، RBX، RCX، ...
• مدرن: R8-R15، R8D-R15D

قابلیت‌ها:
✓ پارس دستورات منفرد
✓ پارس فایل Assembly
✓ خروجی JSON
✓ نمایش Parse Tree و Derivation
✓ تحلیل Shift-Reduce
✓ جدول LR و Automata
✓ تست‌های خودکار

┌──────────────────────────────────────────────────────────────────┐
│ تیم توسعه │
└──────────────────────────────────────────────────────────────────┘

دانشگاه: شهید باهنر کرمان
دانشکده: مهندسی
رشته: مهندسی کامپیوتر
درس: کامپایلر
ترم: زمستان ۱۴۰۴

گروه: 15
اعضا: سید محمد امین حسینی و سید محمد معین حسینی

┌──────────────────────────────────────────────────────────────────┐
│ آمار پروژه │
└──────────────────────────────────────────────────────────────────┘

خطوط کد: ~2500
فایل‌های Python: 8
تست‌های خودکار: 21
فایل‌های نمونه: 3
دستورات تست شده: 150+

نتیجه تست‌ها:
✓ test_quick.py: 7/7 موفق
✓ test_parser_updated.py: 8/8 موفق
✓ test_operand_requirement.py: 6/6 موفق
✓ cache_instructions.asm: 44/44 موفق
✓ advanced_test.asm: 90/90 موفق

════════════════════════════════════════════════════════════════════
</div>
