#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cache Control Instructions Parser - Main Interface
رابط اصلی Parser دستورات کنترل کش
تیم 15 - پروژه کامپایلر - دانشگاه شهید باهنر کرمان
"""

# ═════════════════════════════════════════════════════════════════════
# تنظیمات اولیه - قبل از هر import دیگر
# ═════════════════════════════════════════════════════════════════════
import sys
import os

# 1️⃣ غیرفعال کردن cache برای همیشه
sys.dont_write_bytecode = True

# 2️⃣ تنظیم UTF-8 برای Windows (فارسی درست نمایش بده)
if sys.platform == 'win32':
    try:
        import codecs

        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# 3️⃣ پاک‌سازی خودکار cache در هر اجرا
import shutil
from pathlib import Path


def clear_cache():
    """پاک کردن فایل‌های cache"""
    try:
        # پاک کردن __pycache__
        if os.path.exists('__pycache__'):
            shutil.rmtree('__pycache__')

        # پاک کردن parser.out
        if os.path.exists('parser.out'):
            os.remove('parser.out')

        # پاک کردن parsetab.py
        if os.path.exists('parsetab.py'):
            os.remove('parsetab.py')

    except Exception:
        pass  # اگر خطایی بود نادیده بگیر


# پاک‌سازی خودکار در شروع
clear_cache()

# حالا import های اصلی برنامه
import json

# Import Parser Components
from cache_parser import (
    parse_instruction,
    parse_file,
    analyze_instruction,
    Instruction,
    Register,
    Identifier
)
from cache_lexer import build_lexer


# ═══════════════════════════════════════════════════════════════════
#                          Display Functions
# ═══════════════════════════════════════════════════════════════════

def clear_screen():
    """پاک کردن صفحه"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """چاپ هدر"""
    width = 80
    print("\n" + "═" * width)
    print(f"║{title.center(width - 2)}║")
    print("═" * width)


def press_enter():
    """منتظر فشردن Enter"""
    input("\n⏎ برای ادامه Enter را فشار دهید...")


def print_banner():
    """نمایش بنر اولیه"""
    clear_screen()
    print("""
╔════════════════════════════════════════════════════════════════╗
║          Cache Control Instructions Parser                     ║
║                     پروژه کامپایلر - گروه ۱۵                   ║
║                 دانشگاه شهید باهنر کرمان                       ║
╚════════════════════════════════════════════════════════════════╝

🔄 در حال بارگذاری...
""")


def print_main_menu():
    """نمایش منوی اصلی"""
    clear_screen()
    print("""
╔══════════════════════════════════════════════════════════════════╗
║      Cache Control Instructions Parser - منوی اصلی               ║
║                     پروژه کامپایلر - گروه ۱۵                     ║
║                   دانشگاه شهید باهنر کرمان                       ║
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

─────────────────────────────────────────────────────────────────
""")


# ═══════════════════════════════════════════════════════════════════
#                          Menu Options
# ═══════════════════════════════════════════════════════════════════

def option_parse_single():
    """گزینه 1: پارس یک دستور"""
    print_header("پارس یک دستور")

    code = input("\n➤ دستور: ").strip()

    if not code:
        return

    print("\n🔄 در حال پارس...")

    ast = parse_instruction(code, debug=False)

    if ast:
        print("\n✅ پارس موفق!\n")
        print(f"AST: {ast}\n")

        # Parse Tree ساده (AST)
        print("🌳 Parse Tree (ساده‌شده - AST):")
        for line in ast.pretty_print():
            print("  " + line)

        # Parse Tree کامل طبق گرامر
        print("\n🌲 Parse Tree (کامل - طبق گرامر BNF):")
        for line in ast.full_parse_tree():
            print("  " + line)

        # مراحل اشتقاق
        print("\n📐 مراحل اشتقاق (Derivation):")
        for step in ast.derivation_steps():
            print(f"  {step}")

        # تحلیل
        analysis = analyze_instruction(ast)
        print("\n" + "═" * 70)
        print(f"  دستور: {analysis['mnemonic']}")
        print("═" * 70)
        print(f"  دسته: {analysis['description']}")
        print(f"  دارای Operand: {'✓' if analysis['has_operand'] else '✗'}")

        if analysis['has_operand']:
            op = analysis['operand']
            print(f"  نوع Base: {op['base_type']}")
            print(f"  مقدار Base: {op['base_value']}")
            if 'register_width' in op:
                print(f"  عرض رجیستر: {op['register_width']}-bit")
            if op['has_offset']:
                print(f"  Offset: {op['offset_value']}")

        print("═" * 70)
    else:
        print("\n❌ پارس ناموفق!")

    press_enter()


def option_json_output():
    """گزینه 2: نمایش JSON"""
    print_header("نمایش خروجی JSON")

    code = input("\n➤ دستور: ").strip()

    if not code:
        return

    print("\n🔄 در حال پارس...")

    ast = parse_instruction(code, debug=False)

    if ast:
        print("\n📄 JSON Output:")
        json_str = json.dumps(ast.to_dict(), indent=2, ensure_ascii=False)
        print(json_str)

        # پرسش برای ذخیره
        save = input("\n💾 ذخیره در فایل؟ (y/n): ").strip().lower()
        if save == 'y':
            filename = input("نام فایل (بدون پسوند): ").strip()
            if filename:
                filepath = f"{filename}.json"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(json_str)
                print(f"\n✅ ذخیره شد: {filepath}")
    else:
        print("\n❌ پارس ناموفق!")

    press_enter()


def option_parse_file():
    """گزینه 3: پارس فایل Assembly"""
    print_header("پارس فایل Assembly")

    filename = input("\n➤ نام فایل: ").strip()

    if not filename:
        return

    # ─────────────────────────────────────────────────────────────
    # جستجوی هوشمند فایل
    # ─────────────────────────────────────────────────────────────

    file_path = None

    # حالت 1: فایل با مسیر کامل داده شده
    if Path(filename).exists():
        file_path = filename

    # حالت 2: جستجو در پوشه examples/
    elif Path(f"examples/{filename}").exists():
        file_path = f"examples/{filename}"

    # حالت 3: اگر پسوند نداشت، .asm اضافه کن و دوباره جستجو کن
    elif not filename.endswith('.asm'):
        # جستجو در پوشه اصلی با پسوند
        if Path(f"{filename}.asm").exists():
            file_path = f"{filename}.asm"
        # جستجو در examples با پسوند
        elif Path(f"examples/{filename}.asm").exists():
            file_path = f"examples/{filename}.asm"

    # اگر فایل پیدا نشد
    if not file_path:
        print(f"\n❌ فایل '{filename}' پیدا نشد!")
        print("\n💡 مکان‌های جستجو شده:")
        print(f"   • {filename}")
        print(f"   • examples/{filename}")
        if not filename.endswith('.asm'):
            print(f"   • {filename}.asm")
            print(f"   • examples/{filename}.asm")
        press_enter()
        return

    print(f"\n📁 فایل یافت شد: {file_path}")
    print("\n🔄 در حال پارس فایل...")

    results = []
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            code = line.strip()

            # رد کردن خطوط خالی و کامنت
            if not code or code.startswith(';'):
                continue

            # حذف کامنت انتهای خط
            if ';' in code:
                code = code.split(';')[0].strip()

            try:
                ast = parse_instruction(code, debug=False)
                if ast:
                    results.append((line_num, code, ast))
                else:
                    errors.append((line_num, code, "پارس ناموفق"))
            except Exception as e:
                errors.append((line_num, code, str(e)))

        # نمایش نتایج
        print(f"\n📊 نتیجه:")
        print(f"  ✓ موفق: {len(results)} دستور")
        print(f"  ✗ خطا: {len(errors)} دستور")

        if results:
            print("\n✅ دستورات معتبر:")
            for line_num, code, ast in results[:15]:
                category = ast.get_instruction_category()
                print(f"  خط {line_num:3d}: {code:35s} → {category}")

            if len(results) > 15:
                print(f"  ... و {len(results) - 15} دستور دیگر")

        if errors:
            print("\n❌ خطاها:")
            for line_num, code, error in errors[:5]:
                print(f"  خط {line_num:3d}: {code}")
                print(f"         → {error}")

            if len(errors) > 5:
                print(f"  ... و {len(errors) - 5} خطای دیگر")

    except Exception as e:
        print(f"❌ خطا در خواندن فایل: {e}")

    press_enter()


def option_lr_table():
    """گزینه 4: نمایش جدول LR"""
    print_header("جدول LR(0)")

    try:
        from lr_tables import LR_PARSING_TABLE, GRAMMAR_RULES

        # نمایش جدول
        print("\n" + "═" * 100)
        print(" " * 35 + "جدول پارسینگ LR(0)")
        print("═" * 100)

        for state in sorted(LR_PARSING_TABLE.keys()):
            actions = LR_PARSING_TABLE[state]
            print(f"\n🔹 State {state}:")

            for symbol in sorted(actions.keys()):
                action = actions[symbol]
                if isinstance(action, int):
                    print(f"  {symbol:<20} → goto {action}")
                else:
                    print(f"  {symbol:<20} → {action}")

        print("\n" + "═" * 100)
        print("📜 قوانین گرامر")
        print("═" * 100)

        for rule_num in sorted(GRAMMAR_RULES.keys()):
            print(f"  R{rule_num:<2}: {GRAMMAR_RULES[rule_num]}")

        print("═" * 100)

    except ImportError as e:
        print(f"\n❌ خطا در import: {e}")
        print("💡 لطفاً فایل lr_tables.py را بررسی کنید")
    except AttributeError as e:
        print(f"\n❌ خطا: {e}")
        print("💡 متغیرهای LR_PARSING_TABLE یا GRAMMAR_RULES یافت نشدند")
    except Exception as e:
        print(f"\n❌ خطا: {e}")

    press_enter()


def option_shift_reduce():
    """گزینه 5: تحلیل Shift-Reduce"""
    print_header("تحلیل دستی Shift-Reduce")

    code = input("\n➤ دستور: ").strip()

    if not code:
        return

    try:
        from shift_reduce_trace import trace_shift_reduce
        trace_shift_reduce(code)
    except ImportError as e:
        print(f"\n❌ خطا در import: {e}")
        print("💡 لطفاً فایل shift_reduce_trace.py را بررسی کنید")
    except Exception as e:
        print(f"\n❌ خطا: {e}")

    press_enter()


def option_run_tests():
    """گزینه 6: اجرای تست‌ها"""
    print_header("اجرای تست‌های خودکار")

    print("\n🧪 در حال اجرای تست‌ها...\n")

    test_cases = [
        ("CLFLUSH [EAX]", "دستور ساده"),
        ("CLFLUSHOPT [EBX+16]", "با offset مثبت"),
        ("PREFETCHT0 [ECX-8]", "با offset منفی"),
        ("WBINVD", "بدون operand"),
        ("CLWB [cache_line]", "با شناسه"),
        ("PREFETCHNTA [RAX+128]", "رجیستر 64-bit"),
        ("CLFLUSHOPT", "خطا - بدون operand"),
    ]

    success = 0
    failed = 0

    for i, (code, desc) in enumerate(test_cases, 1):
        print(f"تست {i}/{len(test_cases)}: {desc}")
        print(f"  کد: {code}")

        ast = parse_instruction(code, debug=False)

        if ast:
            print(f"  ✅ موفق - {ast.mnemonic}")
            success += 1
        else:
            print(f"  ❌ ناموفق")
            failed += 1
        print()

    print("─" * 70)
    print(f"نتیجه: {success} موفق، {failed} ناموفق")
    print("─" * 70)

    press_enter()


def option_show_grammar():
    """گزینه 7: نمایش گرامر"""
    print_header("قوانین گرامر")

    grammar = """
╔══════════════════════════════════════════════════════════════════╗
║                  Grammar Rules (BNF) - 18 Rules                  ║
║                   قوانین گرامر - 18 قانون                        ║
╚══════════════════════════════════════════════════════════════════╝

📜 قوانین اصلی (2 قانون):

  R1:  instruction → mnemonic operand
  R2:  instruction → mnemonic

🔖 Mnemonic (9 قانون):

  R3:  mnemonic → CLFLUSH
  R4:  mnemonic → CLFLUSHOPT
  R5:  mnemonic → CLWB
  R6:  mnemonic → PREFETCHT0
  R7:  mnemonic → PREFETCHT1
  R8:  mnemonic → PREFETCHT2
  R9:  mnemonic → PREFETCHNTA
  R10: mnemonic → WBINVD
  R11: mnemonic → INVD

🎯 Operand و Memory Address (2 قانون):

  R12: operand → memory_address
  R13: memory_address → [ base_expr ]

🏷️  Base Expression (3 قانون):

  R14: base_expr → REGISTER offset
  R15: base_expr → REGISTER
  R16: base_expr → IDENTIFIER

🔢 Offset (2 قانون):

  R17: offset → + NUMBER
  R18: offset → - NUMBER

═══════════════════════════════════════════════════════════════════

💡 توضیحات:

  • CLFLUSH, CLFLUSHOPT, CLWB, PREFETCH* نیاز به operand دارند (R1)
  • WBINVD و INVD می‌توانند بدون operand باشند (R2)
  • Operand می‌تواند رجیستر (REGISTER) یا شناسه (IDENTIFIER) باشد
  • Offset اختیاری است و می‌تواند مثبت (+) یا منفی (-) باشد

📊 آمار:

  • مجموع قوانین: 18
  • Terminal ها: 14 (CLFLUSH, CLFLUSHOPT, ..., [, ], +, -, NUMBER)
  • Non-terminal ها: 5 (instruction, mnemonic, operand, memory_address, 
                        base_expr, offset)

═══════════════════════════════════════════════════════════════════

📝 مثال‌ها:

  CLFLUSHOPT [EBX+16]
  ├─ R4: mnemonic → CLFLUSHOPT
  ├─ R12: operand → memory_address
  ├─ R13: memory_address → [ base_expr ]
  ├─ R14: base_expr → REGISTER offset
  ├─ REGISTER → EBX
  ├─ R17: offset → + NUMBER
  └─ R1: instruction → mnemonic operand

  WBINVD
  ├─ R10: mnemonic → WBINVD
  └─ R2: instruction → mnemonic

═══════════════════════════════════════════════════════════════════
"""

    print(grammar)
    press_enter()


def option_interactive():
    """گزینه 8: حالت تعاملی"""
    print_header("حالت تعاملی (Interactive)")

    print("""
💡 در این حالت می‌توانید دستورات مختلف را به‌صورت پشت‌سر‌هم تست کنید
   برای خروج 'exit' یا 'q' را وارد کنید
""")

    while True:
        code = input("\n➤ دستور: ").strip()

        if code.lower() in ['exit', 'q', 'quit']:
            print("👋 خروج از حالت تعاملی")
            break

        if not code:
            continue

        ast = parse_instruction(code, debug=False)

        if ast:
            print(f"✅ {ast.mnemonic} - دسته: {ast.get_instruction_category()}")
            if ast.operand:
                print(f"   Operand: {ast.operand}")
        else:
            print("❌ پارس ناموفق")

    press_enter()


def option_show_automata():
    """گزینه 9: نمایش Automata"""
    print_header("نمودار Automata")

    print("\n🔍 اطلاعات اتوماتا LR(0):")
    print("  • تعداد States: 22")
    print("  • Start State: 0")
    print("  • Accept State: 1")
    print("  • قوانین پوشش داده شده: R1-R18")
    print()

    automata_files = [
        "lr0_automata_COMPLETE.pdf",    # اولویت اول
        "lr0_automata.jpg",
        "lr0_automata.png",
        "lr0_automata.pdf",
        "lr0_automata"
    ]

    found = False
    for filename in automata_files:
        if Path(filename).exists():
            print(f"✅ فایل پیدا شد: {filename}")
            print(f"📍 مسیر کامل: {Path(filename).absolute()}")

            try:
                if os.name == 'nt':  # Windows
                    os.startfile(filename)
                elif sys.platform == 'darwin':  # macOS
                    os.system(f'open "{filename}"')
                else:  # Linux
                    os.system(f'xdg-open "{filename}"')
                print("🎨 PDF/تصویر در برنامه پیش‌فرض باز شد!")
            except Exception as e:
                print(f"⚠️ خطا در باز کردن: {e}")
                print(f"💡 دستی باز کنید: {filename}")

            found = True
            break

    if not found:
        print("\n❌ فایل نمودار پیدا نشد!")
        print("\n💡 راهنما:")
        print("   1. lr0_automata_COMPLETE.pdf رو در پوشه پروژه کپی کن")
        print("   2. یا lr0_automata.jpg/png/pdf")
        print("\n📋 فایل‌های قابل قبول:")
        for f in automata_files:
            print(f"   • {f}")

    print("\n" + "="*60)
    press_enter()



def option_about():
    """گزینه 10: درباره"""
    print_header("درباره پروژه")

    about = """
╔══════════════════════════════════════════════════════════════════╗
║         Cache Control Instructions Parser                        ║
║                   تحلیل‌گر دستورات کنترل کش                       ║
╚══════════════════════════════════════════════════════════════════╝

📚 پروژه: کامپایلر
🎓 دانشگاه: شهید باهنر کرمان
👥 گروه: 15
📅 ترم: زمستان ۱۴۰۴

═══════════════════════════════════════════════════════════════════

🎯 هدف پروژه:

  طراحی و پیاده‌سازی یک Parser کامل برای دستورات کنترل کش در
  معماری x86/x64 با استفاده از تکنیک‌های Bottom-Up Parsing

═══════════════════════════════════════════════════════════════════

⚙️  ویژگی‌ها:

  ✓ پشتیبانی از 9 دستور کنترل کش
  ✓ گرامر 18 قانونی استاندارد
  ✓ LR(0) Parser با 22 State
  ✓ جدول Action و Goto کامل
  ✓ تحلیل Shift-Reduce گام‌به‌گام
  ✓ ساخت Abstract Syntax Tree (AST)
  ✓ خروجی JSON
  ✓ مدیریت خطاهای نحوی
  ✓ پشتیبانی از رجیسترهای 32 و 64 بیتی
  ✓ پشتیبانی از offset های مثبت و منفی

═══════════════════════════════════════════════════════════════════

🛠️  تکنولوژی‌ها:

  • زبان: Python 3.8+
  • ابزار Lexer: PLY (Python Lex-Yacc)
  • ابزار Parser: PLY Yacc
  • روش: LR(0) Bottom-Up Parsing
  • States: 22 حالت
  • Grammar Rules: 18 قانون

═══════════════════════════════════════════════════════════════════

📦 دستورات پشتیبانی شده:

  Cache Flush:     CLFLUSH, CLFLUSHOPT
  Cache WriteBack: CLWB
  Cache Prefetch:  PREFETCHT0, PREFETCHT1, PREFETCHT2, PREFETCHNTA
  Cache Invalid:   WBINVD, INVD

═══════════════════════════════════════════════════════════════════
"""

    print(about)
    press_enter()


def option_clean_cache():
    """پاک‌سازی کش"""
    print_header("پاک‌سازی فایل‌های کش")

    print("\n🧹 در حال پاک‌سازی...\n")

    cache_items = ['__pycache__', 'parser.out', 'parsetab.py']
    removed = 0

    for item in cache_items:
        path = Path(item)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
                print(f"✅ حذف شد: {item}/")
            else:
                path.unlink()
                print(f"✅ حذف شد: {item}")
            removed += 1

    if removed == 0:
        print("💡 فایل کشی برای پاک‌سازی یافت نشد")
    else:
        print(f"\n✅ تعداد {removed} مورد حذف شد")
        print("💡 در اجرای بعدی، فایل‌ها دوباره ساخته می‌شوند")

    press_enter()


def option_help():
    """راهنما"""
    print_header("راهنما")

    help_text = """
📖 راهنمای استفاده:

1️⃣  پارس یک دستور:
   - یک دستور assembly وارد کنید
   - Parse Tree و تحلیل کامل نمایش داده می‌شود

2️⃣  نمایش JSON:
   - خروجی JSON برای یک دستور
   - امکان ذخیره در فایل

3️⃣  پارس فایل:
   - نام فایل assembly را وارد کنید
   - فایل باید در پوشه examples/ باشد
   - یا مسیر کامل را وارد کنید

4️⃣  جدول LR:
   - نمایش جدول Action و Goto
   - مشاهده حالات Automata (17 State)

5️⃣  تحلیل Shift-Reduce:
   - مشاهده مراحل پارسینگ گام‌به‌گام
   - Stack و Input در هر مرحله

═══════════════════════════════════════════════════════════════════

💡 نکات:

  • فایل‌های assembly باید پسوند .asm داشته باشند
  • کامنت‌ها با ; شروع می‌شوند
  • فرمت دستورات باید دقیق باشد
  • گرامر شامل 18 قانون است
  • Parser دارای 17 state است

═══════════════════════════════════════════════════════════════════
"""

    print(help_text)
    press_enter()


# ═══════════════════════════════════════════════════════════════════
#                          Main Loop
# ═══════════════════════════════════════════════════════════════════

def main():
    """حلقه اصلی برنامه"""

    # نمایش بنر
    print_banner()

    # تست اولیه parser
    try:
        test_ast = parse_instruction("CLFLUSH [EAX]", debug=False)
        if test_ast:
            print("✅ Parser آماده است!")
        else:
            print("⚠️  Parser ساخته شد اما تست اولیه ناموفق بود")
    except Exception as e:
        print(f"❌ خطا در بارگذاری Parser: {e}")
        sys.exit(1)

    press_enter()

    # حلقه اصلی
    while True:
        print_main_menu()

        choice = input("➤ انتخاب شما: ").strip().lower()

        if choice == '1':
            option_parse_single()
        elif choice == '2':
            option_json_output()
        elif choice == '3':
            option_parse_file()
        elif choice == '4':
            option_lr_table()
        elif choice == '5':
            option_shift_reduce()
        elif choice == '6':
            option_run_tests()
        elif choice == '7':
            option_show_grammar()
        elif choice == '8':
            option_interactive()
        elif choice == '9':
            option_show_automata()
        elif choice == '10':
            option_about()
        elif choice == 'c':
            option_clean_cache()
        elif choice == 'h':
            option_help()
        elif choice in ['q', 'quit', 'exit']:
            clear_screen()
            print("""
╔══════════════════════════════════════════════════════════════════╗
║                         خروج از برنامه                           ║
╚══════════════════════════════════════════════════════════════════╝

            👋 با تشکر از استفاده شما

            دانشگاه شهید باهنر کرمان
            تیم 15 - پروژه کامپایلر

╔══════════════════════════════════════════════════════════════════╗
""")
            sys.exit(0)
        else:
            print("\n❌ گزینه نامعتبر! لطفاً دوباره تلاش کنید.")
            press_enter()


# ═══════════════════════════════════════════════════════════════════
#                          Entry Point
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 خروج با Ctrl+C")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
