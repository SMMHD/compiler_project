# Cache Control Instructions Parser

<div align="center">

![Parser](https://img.shields.io/badge/Parser-LR(0)-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Status](https://img.shields.io/badge/Status-Complete-success)
![Grade](https://img.shields.io/badge/Grade-90.5%2F100-brightgreen)

**تحلیلگر نحوی دستورات کنترل کش x86 با استفاده از LR(0) Parser**

[مستندات](#-مستندات) •
[نصب](#-نصب) •
[استفاده](#-استفاده) •
[مثال‌ها](#-مثال‌ها) •
[گرامر](#-گرامر) •
[تیم](#-تیم)

</div>

---

## 📋 درباره پروژه

این پروژه یک **تحلیلگر نحوی (Parser) کامل** برای دستورات کنترل کش پردازنده‌های x86/x64 است که با استفاده از تکنیک **LR(0) Bottom-Up Parsing** پیاده‌سازی شده است.

### ✨ ویژگی‌های کلیدی

- ✅ پارسر کامل LR(0) با 17 State
- ✅ گرامر 18 قانونی استاندارد
- ✅ پشتیبانی از 9 دستور کنترل کش (CLFLUSH, CLFLUSHOPT, CLWB, PREFETCH*, WBINVD, INVD)
- ✅ پشتیبانی از آدرس‌دهی پیچیده: `[REGISTER±OFFSET]` و `[IDENTIFIER]`
- ✅ تولید Abstract Syntax Tree (AST) کامل
- ✅ تحلیل shift-reduce با trace دقیق
- ✅ رابط تعاملی (Interactive CLI) با 10 منوی کامل
- ✅ تست‌های خودکار و نمونه‌های کاربردی
- ✅ مستندات کامل و دیاگرام‌های دقیق

---

## 🏗️ معماری پروژه

```
┌─────────────────────────────────────────────────────────────┐
│                       Cache Instructions                    │
│          (CLFLUSH [EAX], PREFETCHT0 [RBX+16], ...)         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
            ┌─────────────────┐
            │  Lexical        │
            │  Analyzer       │  ← cache_lexer.py
            │  (PLY Lex)      │
            └────────┬─────────┘
                     │ Tokens
                     ▼
            ┌─────────────────┐
            │  Syntax         │
            │  Analyzer       │  ← cache_parser.py
            │  (LR Parser)    │
            └────────┬─────────┘
                     │ AST
                     ▼
            ┌─────────────────┐
            │  Semantic       │
            │  Analyzer       │  ← analyze_instruction()
            └────────┬─────────┘
                     │ Analysis
                     ▼
            ┌─────────────────┐
            │  Output         │
            │  (JSON/Tree)    │
            └─────────────────┘
```

---

## 📂 ساختار پروژه

```
cache-control-parser/
├── 📄 main.py                          # رابط اصلی (10 منو)
├── 📄 cache_lexer.py                   # Lexical Analyzer
├── 📄 cache_parser.py                  # Syntax Analyzer (LR Parser)
├── 📄 lr_tables.py                     # جداول LR(0)
├── 📄 shift_reduce_trace.py            # تحلیل Shift-Reduce
│
├── 📁 docs/                            # مستندات
│   ├── grammar.txt                     # گرامر 18 قانونی
│   ├── SHIFT_REDUCE_ANALYSIS.txt       # مثال‌های trace
│   ├── LR_PARSING_TABLE_ASCII.txt      # جدول LR کامل
│   ├── LR_TABLE_COMPACT.txt            # جدول فشرده
│   ├── LR0_AUTOMATA_DETAILS.txt        # توضیحات اتوماتا
│   ├── lr0_automata                    # فایل DOT اتوماتا
│   ├── lr0_automata.png                # دیاگرام اتوماتا
│   └── document.docx                   # گزارش نهایی
│
├── 📁 examples/                        # نمونه‌های JSON
│   ├── CLFLUSHOPT-RBX-16.json
│   ├── PREFETCHNTA-RAX.json
│   ├── prefetch.json
│   └── WBINVD.json
│
├── 📁 tests/                           # تست‌ها
│   ├── quick_test.py
│   └── test_parser_demo.py
│
├── 📄 requirements.txt                 # وابستگی‌ها
├── 📄 README.md                        # این فایل
└── 📄 LICENSE                          # مجوز MIT
```

---

## 🚀 نصب

### پیش‌نیازها

- Python 3.8 یا بالاتر
- pip (مدیر بسته‌های Python)

### مراحل نصب

```bash
# 1. کلون کردن repository
git clone https://github.com/YOUR_USERNAME/cache-control-parser.git
cd cache-control-parser

# 2. نصب وابستگی‌ها
pip install -r requirements.txt

# 3. اجرای تست (اختیاری)
python tests/quick_test.py

# 4. اجرای برنامه اصلی
python main.py
```

### نصب Graphviz (برای نمایش اتوماتا - اختیاری)

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Windows:**
دانلود از [graphviz.org](https://graphviz.org/download/)

---

## 💻 استفاده

### رابط تعاملی (Interactive Mode)

```bash
python main.py
```

منوهای موجود:
1. **پارس یک دستور** - پارس دستور با Parse Tree کامل
2. **نمایش خروجی JSON** - تبدیل به JSON
3. **پارس فایل Assembly** - پارس چندین دستور
4. **نمایش جدول LR(0)** - نمایش جدول پارسینگ
5. **تحلیل دستی Shift-Reduce** - trace گام‌به‌گام
6. **اجرای تست‌های خودکار** - تست کیس‌های آماده
7. **نمایش قوانین گرامر** - گرامر 18 قانونی
8. **حالت تعاملی** - ورودی آزاد
9. **نمایش نمودار Automata** - دیاگرام LR(0)
10. **درباره پروژه** - اطلاعات تیم

### استفاده به صورت کتابخانه

```python
from cache_parser import parse_instruction, analyze_instruction

# پارس یک دستور
ast = parse_instruction("CLFLUSHOPT [EBX+16]")

# نمایش AST
print(ast)  # Instruction(CLFLUSHOPT, Memory([EBX+16]))

# تحلیل دستور
analysis = analyze_instruction(ast)
print(analysis['category'])  # 'flush'
print(analysis['has_operand'])  # True
```

---

## 📝 مثال‌ها

### مثال 1: دستور ساده با رجیستر

```python
>>> parse_instruction("CLFLUSH [EAX]")

✅ پارس موفق!

Parse Tree:
Instruction: CLFLUSH
├─ Operand:
   └─ MemoryOperand:
      ├─ Base: Register(EAX, 32-bit)
      └─ Offset: None
```

### مثال 2: دستور با Offset مثبت

```python
>>> parse_instruction("CLFLUSHOPT [EBX+16]")

✅ پارس موفق!

Derivation:
Instruction
→ mnemonic operand
→ CLFLUSHOPT operand
→ CLFLUSHOPT memory_address
→ CLFLUSHOPT [ base_expr ]
→ CLFLUSHOPT [ REGISTER offset ]
→ CLFLUSHOPT [ EBX + 16 ]
```

### مثال 3: دستور با شناسه (Label)

```python
>>> parse_instruction("CLWB [cache_line]")

✅ پارس موفق!

JSON Output:
{
  "type": "Instruction",
  "mnemonic": "CLWB",
  "operand": {
    "type": "MemoryOperand",
    "base": {
      "type": "Identifier",
      "name": "cache_line"
    },
    "offset": null
  }
}
```

### مثال 4: دستور بدون Operand

```python
>>> parse_instruction("WBINVD")

✅ پارس موفق!

Analysis:
دستور: WBINVD
دسته: Cache Invalidate - باطلسازی کش
دارای Operand: ✗
```

---

## 📜 گرامر

### قوانین تولید (18 قانون)

```
R1:  instruction → mnemonic operand
R2:  instruction → mnemonic
R3:  mnemonic → CLFLUSH
R4:  mnemonic → CLFLUSHOPT
R5:  mnemonic → CLWB
R6:  mnemonic → PREFETCHT0
R7:  mnemonic → PREFETCHT1
R8:  mnemonic → PREFETCHT2
R9:  mnemonic → PREFETCHNTA
R10: mnemonic → WBINVD
R11: mnemonic → INVD
R12: operand → memory_address
R13: memory_address → [ base_expr ]
R14: base_expr → REGISTER offset
R15: base_expr → REGISTER
R16: base_expr → IDENTIFIER
R17: offset → + NUMBER
R18: offset → - NUMBER
```

### دستورات پشتیبانی شده

| دسته | دستورات | توضیح |
|------|---------|-------|
| **Cache Flush** | CLFLUSH, CLFLUSHOPT | پاکسازی خط کش |
| **Cache Write-Back** | CLWB | نوشتن به حافظه اصلی |
| **Cache Prefetch** | PREFETCHT0, PREFETCHT1, PREFETCHT2, PREFETCHNTA | پیشخوانی داده |
| **Cache Invalidate** | WBINVD, INVD | باطلسازی کش |

### فرمت‌های آدرس‌دهی

- `[REGISTER]` - آدرس‌دهی مستقیم: `CLFLUSH [EAX]`
- `[REGISTER+NUMBER]` - با offset مثبت: `CLFLUSHOPT [EBX+16]`
- `[REGISTER-NUMBER]` - با offset منفی: `PREFETCHT0 [ECX-8]`
- `[IDENTIFIER]` - با لیبل: `CLWB [cache_line]`

---

## 🔬 LR(0) Automata

اتوماتای LR(0) این پارسر شامل **17 state** است:

![LR(0) Automata](docs/lr0_automata.png)

### State های کلیدی

- **State 0**: حالت اولیه
- **State 1**: Accept state
- **State 2**: بعد از mnemonic (تصمیم‌گیری با/بدون operand)
- **State 8**: بعد از REGISTER (تصمیم‌گیری با/بدون offset)
- **State 14-16**: پردازش offset های مثبت/منفی

جزئیات کامل در [LR0_AUTOMATA_DETAILS.txt](docs/LR0_AUTOMATA_DETAILS.txt)

---

## 📊 جدول LR(0)

جدول پارسینگ LR(0) شامل:
- **ACTION table**: 17 state × terminal symbols
- **GOTO table**: 17 state × non-terminal symbols

مشاهده جدول کامل: [LR_PARSING_TABLE_ASCII.txt](docs/LR_PARSING_TABLE_ASCII.txt)

---

## 🧪 تست‌ها

### اجرای تست‌های سریع

```bash
python tests/quick_test.py
```

نتیجه:
```
✅ تست 1: CLFLUSH [EAX] - موفق
✅ تست 2: CLFLUSHOPT [EBX+16] - موفق
✅ تست 3: PREFETCHT0 [ECX-8] - موفق
✅ تست 4: WBINVD - موفق
✅ تست 5: CLWB [cache_line] - موفق
✅ تست 6: PREFETCHNTA [RAX+128] - موفق

6/6 تست موفق ✅
```

### اجرای تست‌های دمو

```bash
python tests/test_parser_demo.py
```

---

## 📚 مستندات

### فایل‌های مستندات

- 📄 [grammar.txt](docs/grammar.txt) - گرامر کامل 18 قانونی
- 📄 [SHIFT_REDUCE_ANALYSIS.txt](docs/SHIFT_REDUCE_ANALYSIS.txt) - 6 مثال trace کامل
- 📄 [LR_PARSING_TABLE_ASCII.txt](docs/LR_PARSING_TABLE_ASCII.txt) - جدول LR کامل
- 📄 [LR0_AUTOMATA_DETAILS.txt](docs/LR0_AUTOMATA_DETAILS.txt) - توضیحات هر state
- 📄 [document.docx](docs/document.docx) - گزارش نهایی پروژه

---

## 🛠️ تکنولوژی‌ها

- **Python 3.8+** - زبان برنامه‌نویسی اصلی
- **PLY (Python Lex-Yacc)** - ابزار lexer و parser
- **Graphviz** - تولید دیاگرام اتوماتا
- **JSON** - فرمت خروجی

---

## 👥 تیم

**تیم 15 - پروژه کامپایلر**

دانشگاه شهید باهنر کرمان  
دانشکده مهندسی کامپیوتر  
زمستان ۱۴۰۴ - بهار ۱۴۰۵

---

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر [LICENSE](LICENSE) را مشاهده کنید.

---

## 🌟 ستاره بدهید!

اگر این پروژه برای شما مفید بود، لطفاً یک ⭐ به آن بدهید!

---

## 📞 تماس

سوالات یا پیشنهادات؟

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/cache-control-parser/issues)

---

<div align="center">

**ساخته شده با ❤️ توسط تیم 15**

[⬆ بازگشت به بالا](#cache-control-instructions-parser)

</div>
