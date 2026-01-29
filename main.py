#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║        Cache Control Instructions Parser - Main Interface        ║
║                     پروژه کامپایلر - گروه ۱۵                   ║
║                   دانشگاه شهید باهنر کرمان - ۱۴۰۴               ║
╚══════════════════════════════════════════════════════════════════╝

نقطه ورود اصلی پروژه - رابط تعاملی جامع
"""

import sys
import os
import json
import shutil
from pathlib import Path
from typing import Optional


# ═══════════════════════════════════════════════════════════════════
# Import ماژول‌های پروژه
# ═══════════════════════════════════════════════════════════════════

def check_dependencies():
    """بررسی وابستگی‌ها و فایل‌های لازم"""
    try:
        import ply
    except ImportError:
        print("❌ خطا: کتابخانه PLY نصب نیست!")
        print("\n📦 لطفاً با دستور زیر نصب کنید:")
        print("   pip install ply")
        return False

    required_files = [
        'cache_lexer.py',
        'cache_parser.py',
    ]

    missing_files = [f for f in required_files if not Path(f).exists()]

    if missing_files:
        print("❌ خطا: فایل‌های زیر یافت نشد:")
        for f in missing_files:
            print(f"   • {f}")
        return False

    return True


if not check_dependencies():
    sys.exit(1)

# Import ماژول‌های اصلی پروژه
from cache_lexer import build_lexer
from cache_parser import build_parser, parse_instruction, Register


# ═══════════════════════════════════════════════════════════════════
# توابع کمکی رابط کاربری
# ═══════════════════════════════════════════════════════════════════

def print_header(title, width=80):
    """چاپ سرتیتر با فرمت زیبا"""
    print("\n" + "═" * width)
    padding = (width - len(title) - 2) // 2
    print("║" + " " * padding + title + " " * (width - padding - len(title) - 2) + "║")
    print("═" * width)


def print_separator(char="─", width=80):
    """چاپ خط جداکننده"""
    print(char * width)


def clear_screen():
    """پاک کردن صفحه"""
    os.system('cls' if os.name == 'nt' else 'clear')


def press_enter():
    """توقف برای خواندن"""
    input("\n⏎ برای ادامه Enter را فشار دهید...")


# ═══════════════════════════════════════════════════════════════════
# 1️⃣ پارس یک دستور
# ═══════════════════════════════════════════════════════════════════

def parse_single_instruction():
    """پارس یک دستور با جزئیات کامل"""
    print_header("پارس یک دستور")

    print("\n📝 مثال‌های معتبر:")
    examples = [
        ("CLFLUSH [EAX]", "دستور ساده با رجیستر"),
        ("CLFLUSHOPT [EBX+16]", "دستور با offset مثبت"),
        ("PREFETCHT0 [ECX-8]", "دستور با offset منفی"),
        ("WBINVD", "دستور بدون operand"),
        ("CLWB [cache_line]", "دستور با label"),
        ("PREFETCHNTA [RAX+128]", "رجیستر 64-bit"),
        ("CLFLUSH [R8]", "رجیستر مدرن"),
    ]

    for i, (ex, desc) in enumerate(examples, 1):
        print(f"  {i}. {ex:<30} → {desc}")

    print_separator()
    code = input("➤ دستور خود را وارد کنید (Enter برای بازگشت): ").strip()

    if not code:
        return

    print("\n🔄 در حال پارس...")

    try:
        ast = parse_instruction(code, debug=False)

        if ast:
            print("\n✅ پارس موفق!")
            print(f"\n📊 نمایش AST:")
            print(f"   {ast}")

            # ═══════════════════════════════════════════════════
            # Parse Tree ساده (AST)
            # ═══════════════════════════════════════════════════
            print("\n🌳 Parse Tree (ساده‌شده - AST):")
            for line in ast.pretty_print():
                print("  " + line)

            # ═══════════════════════════════════════════════════
            # Parse Tree کامل طبق گرامر BNF
            # ═══════════════════════════════════════════════════
            print("\n🌲 Parse Tree (کامل - طبق گرامر BNF):")
            for line in ast.full_parse_tree():
                print("  " + line)

            # ═══════════════════════════════════════════════════
            # مراحل اشتقاق (Derivation)
            # ═══════════════════════════════════════════════════
            print("\n📐 مراحل اشتقاق (Derivation):")
            for step in ast.derivation_steps():
                print(f"  {step}")

            # ═══════════════════════════════════════════════════
            # تحلیل دقیق
            # ═══════════════════════════════════════════════════
            category = ast.get_instruction_category()
            category_desc = {
                'flush': 'Cache Flush - پاک‌سازی خط کش',
                'writeback': 'Cache Write-Back - بازنویسی خط کش',
                'prefetch': 'Cache Prefetch - پیش‌خوانی داده',
                'invalidate': 'Cache Invalidate - باطل‌سازی کش',
            }

            print(f"\n🔍 تحلیل معنایی:")
            print(f"  • Mnemonic: {ast.mnemonic}")
            print(f"  • دسته: {category_desc.get(category, 'نامشخص')}")
            print(f"  • دارای Operand: {'✓' if ast.operand else '✗'}")

            if ast.operand:
                print(f"  • نوع Base: {type(ast.operand.base).__name__}")
                print(f"  • مقدار Base: {ast.operand.base}")

                if isinstance(ast.operand.base, Register):
                    print(f"  • عرض رجیستر: {ast.operand.base.bit_width}-bit")

                if ast.operand.offset:
                    print(f"  • Offset: {ast.operand.offset}")

            # ═══════════════════════════════════════════════════
            # JSON Output (اختیاری)
            # ═══════════════════════════════════════════════════
            print("\n" + "─" * 80)
            show_json = input("💡 آیا می‌خواهید JSON Output را ببینید؟ (y/n): ").lower()

            if show_json == 'y':
                print("\n📄 JSON Output:")
                json_output = ast.to_dict()
                print(json.dumps(json_output, indent=2, ensure_ascii=False))
        else:
            print("\n❌ پارس ناموفق - دستور نامعتبر است")

    except Exception as e:
        print(f"\n❌ خطا: {e}")

    press_enter()


# ═══════════════════════════════════════════════════════════════════
# 2️⃣ خروجی JSON
# ═══════════════════════════════════════════════════════════════════

def show_json_output():
    """نمایش و ذخیره خروجی JSON"""
    print_header("خروجی JSON")

    code = input("\n➤ دستور: ").strip()
    if not code:
        return

    try:
        ast = parse_instruction(code, debug=False)

        if ast:
            print("\n📄 JSON Output:")
            json_output = ast.to_dict()
            json_str = json.dumps(json_output, indent=2, ensure_ascii=False)
            print(json_str)

            # پیشنهاد ذخیره
            print_separator()
            save = input("\n💾 ذخیره در فایل؟ (y/n): ").lower()

            if save == 'y':
                filename = input("نام فایل (بدون پسوند): ").strip() or "output"
                filepath = f"{filename}.json"

                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(json_output, f, indent=2, ensure_ascii=False)

                print(f"✅ ذخیره شد: {filepath}")
        else:
            print("❌ دستور نامعتبر")

    except Exception as e:
        print(f"❌ خطا: {e}")

    press_enter()


# ═══════════════════════════════════════════════════════════════════
# 3️⃣ پارس فایل
# ═══════════════════════════════════════════════════════════════════

def parse_assembly_file():
    """پارس یک فایل کامل Assembly"""
    print_header("پارس فایل Assembly")

    filename = input("\n➤ نام فایل: ").strip()

    if not filename:
        return

    if not Path(filename).exists():
        print(f"\n❌ فایل '{filename}' پیدا نشد!")
        press_enter()
        return

    print("\n🔄 در حال پارس فایل...")

    results = []
    errors = []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
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

    except Exception as e:
        print(f"❌ خطا در خواندن فایل: {e}")

    press_enter()


# ═══════════════════════════════════════════════════════════════════
# 4️⃣ جدول LR
# ═══════════════════════════════════════════════════════════════════

def show_lr_table():
    """نمایش جدول پارس LR"""
    print_header("جدول پارس LR(0)")

    try:
        from lr_tables import generate_parsing_table
        generate_parsing_table()
    except ImportError:
        print("\n⚠️ فایل lr_tables.py پیدا نشد")
        print("این فایل شامل جداول Action و Goto است.")
    except Exception as e:
        print(f"\n❌ خطا: {e}")

    press_enter()


# ═══════════════════════════════════════════════════════════════════
# 5️⃣ تحلیل Shift-Reduce
# ═══════════════════════════════════════════════════════════════════

def show_shift_reduce():
    """نمایش تحلیل دستی Shift-Reduce"""
    print_header("تحلیل دستی Shift-Reduce")

    try:
        from shift_reduce_trace import (
            print_grammar_rules,
            example1_simple,
            example2_with_offset,
            example3_no_operand,
            example4_with_label
        )

        print("\n📋 انتخاب مثال:")
        print("  1️⃣  مثال 1: CLFLUSH [EAX] - دستور ساده")
        print("  2️⃣  مثال 2: CLFLUSHOPT [EBX+16] - با offset مثبت")
        print("  3️⃣  مثال 3: WBINVD - بدون operand")
        print("  4️⃣  مثال 4: CLWB [cache_line] - با label")
        print("  5️⃣  نمایش قوانین گرامر")
        print("  6️⃣  نمایش همه مثال‌ها")

        choice = input("\n➤ انتخاب (1-6): ").strip()

        examples = {
            '1': example1_simple,
            '2': example2_with_offset,
            '3': example3_no_operand,
            '4': example4_with_label,
            '5': print_grammar_rules,
        }

        if choice == '6':
            print_grammar_rules()
            for func in [example1_simple, example2_with_offset,
                         example3_no_operand, example4_with_label]:
                func()
        elif choice in examples:
            examples[choice]()
        else:
            print("❌ انتخاب نامعتبر")

    except ImportError:
        print("\n⚠️ فایل shift_reduce_trace.py پیدا نشد")
    except Exception as e:
        print(f"\n❌ خطا: {e}")

    press_enter()


# ═══════════════════════════════════════════════════════════════════
# 6️⃣ اجرای تست‌ها
# ═══════════════════════════════════════════════════════════════════

def run_tests():
    """اجرای تست‌های خودکار"""
    print_header("اجرای تست‌های خودکار")

    try:
        print("\n🧪 در حال اجرای تست‌ها...\n")

        # Import و اجرای quick_test
        import quick_test

        # اجرای مستقیم
        if hasattr(quick_test, 'main'):
            quick_test.main()
        else:
            # اجرای با subprocess
            import subprocess
            result = subprocess.run([sys.executable, 'quick_test.py'],
                                    capture_output=False)

    except ImportError:
        print("\n⚠️ فایل quick_test.py پیدا نشد")
    except Exception as e:
        print(f"\n❌ خطا: {e}")

    press_enter()


# ═══════════════════════════════════════════════════════════════════
# 7️⃣ نمایش گرامر
# ═══════════════════════════════════════════════════════════════════

def show_grammar():
    """نمایش قوانین گرامر BNF"""
    print_header("قوانین گرامر BNF")

    try:
        with open('grammar.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            print("\n" + content)
    except FileNotFoundError:
        print("\n⚠️ فایل grammar.txt پیدا نشد")

        # نمایش گرامر از حافظه
        print("\n📋 قوانین گرامر:")
        grammar = """
═══ گرامر BNF برای دستورات کنترل کش ═══

<Instruction>     ::= <Mnemonic> <Operand> | <Mnemonic>
<Mnemonic>        ::= <CacheFlush> | <CacheWrite> | <CachePrefetch> | <CacheInvalidate>

<CacheFlush>      ::= "CLFLUSH" | "CLFLUSHOPT"
<CacheWrite>      ::= "CLWB"
<CachePrefetch>   ::= "PREFETCHT0" | "PREFETCHT1" | "PREFETCHT2" | "PREFETCHNTA"
<CacheInvalidate> ::= "WBINVD" | "INVD"

<Operand>         ::= <MemoryAddress> | ε
<MemoryAddress>   ::= "[" <BaseExpr> "]"
<BaseExpr>        ::= <Register> <Offset> | <Register> | <Label>

<Offset>          ::= "+" <Number> | "-" <Number>
<Register>        ::= "EAX" | "EBX" | ... | "RAX" | "RBX" | ... | "R8" | ... | "R15"
<Number>          ::= <Digit>+
<Label>           ::= <Identifier>
"""
        print(grammar)

    press_enter()


# ═══════════════════════════════════════════════════════════════════
# 8️⃣ حالت تعاملی
# ═══════════════════════════════════════════════════════════════════

def interactive_mode():
    """حالت تعاملی - پارس مداوم"""
    print_header("حالت تعاملی")

    print("\n🔄 حالت پارس مداوم فعال شد")
    print("دستورات خود را وارد کنید")
    print("دستورات کنترلی: 'exit', 'quit', 'help'\n")

    counter = 1

    while True:
        try:
            code = input(f"[{counter}] ➤ ").strip()

            if code.lower() in ['exit', 'quit', 'q']:
                print("👋 خروج از حالت تعاملی")
                break

            if code.lower() == 'help':
                print("  دستورات کنترلی:")
                print("    exit/quit - خروج")
                print("    help      - راهنما")
                print("    clear     - پاک کردن صفحه")
                continue

            if code.lower() == 'clear':
                clear_screen()
                continue

            if not code:
                continue

            ast = parse_instruction(code, debug=False)

            if ast:
                category = ast.get_instruction_category()
                print(f"    ✅ {ast}")
                print(f"    📂 دسته: {category}")
            else:
                print("    ❌ نامعتبر")

            counter += 1

        except KeyboardInterrupt:
            print("\n👋 خروج از حالت تعاملی (Ctrl+C)")
            break
        except Exception as e:
            print(f"    ❌ خطا: {e}")

    press_enter()


# ═══════════════════════════════════════════════════════════════════
# 9️⃣ نمایش Automata
# ═══════════════════════════════════════════════════════════════════

def show_automata():
    """نمایش نمودار Automata"""
    print_header("نمودار Automata LR(0)")

    # فایل‌های احتمالی تصویر
    possible_images = [
        'lr0_automata.jpg',
        'lr0_automata.png',
        'LR0_automata.jpg',
        'automata.jpg',
    ]

    image_found = None

    # جستجوی تصویر
    for img in possible_images:
        if Path(img).exists():
            image_found = img
            break

    # نمایش وضعیت
    if image_found:
        print(f"\n✅ تصویر Automata پیدا شد: {image_found}")

        # نمایش اطلاعات فایل
        file_size = Path(image_found).stat().st_size / 1024  # KB
        print(f"   📊 حجم: {file_size:.2f} KB")

        print("\n💡 برای مشاهده تصویر:")
        print(f"   • فایل '{image_found}' را با Image Viewer باز کنید")

        # پیشنهاد باز کردن خودکار
        open_file = input("\n🖼️  آیا می‌خواهید تصویر را باز کنید؟ (y/n): ").lower()

        if open_file == 'y':
            try:
                import platform
                import subprocess

                system = platform.system()

                if system == 'Windows':
                    os.startfile(image_found)
                    print("✅ تصویر با برنامه پیش‌فرض باز شد")
                elif system == 'Darwin':  # macOS
                    subprocess.run(['open', image_found])
                    print("✅ تصویر با برنامه پیش‌فرض باز شد")
                else:  # Linux
                    subprocess.run(['xdg-open', image_found])
                    print("✅ تصویر با برنامه پیش‌فرض باز شد")
            except Exception as e:
                print(f"⚠️ خطا در باز کردن تصویر: {e}")
                print(f"لطفاً فایل '{image_found}' را به صورت دستی باز کنید")
    else:
        print("\n⚠️ تصویر Automata پیدا نشد")

    press_enter()


# ═══════════════════════════════════════════════════════════════════
# 🔟 پاک‌سازی کش
# ═══════════════════════════════════════════════════════════════════

def clean_cache_files():
    """پاک‌سازی فایل‌های کش PLY"""
    print_header("پاک‌سازی فایل‌های کش")

    files_to_remove = ['parser.out', 'parsetab.py', 'lextab.py']
    dirs_to_remove = ['__pycache__']

    removed = 0

    print("\n🧹 در حال پاک‌سازی...\n")

    for filename in files_to_remove:
        if Path(filename).exists():
            try:
                os.remove(filename)
                print(f"✅ حذف شد: {filename}")
                removed += 1
            except Exception as e:
                print(f"❌ خطا در حذف {filename}: {e}")

    for dirname in dirs_to_remove:
        if Path(dirname).exists():
            try:
                shutil.rmtree(dirname)
                print(f"✅ حذف شد: {dirname}/")
                removed += 1
            except Exception as e:
                print(f"❌ خطا در حذف {dirname}: {e}")

    if removed == 0:
        print("✅ فایل کش‌ی یافت نشد - همه چیز تمیز است!")
    else:
        print(f"\n✅ تعداد {removed} مورد حذف شد")
        print("💡 در اجرای بعدی، فایل‌ها دوباره ساخته می‌شوند")

    press_enter()


# ═══════════════════════════════════════════════════════════════════
# 1️⃣1️⃣ درباره پروژه
# ═══════════════════════════════════════════════════════════════════

def show_about():
    """نمایش اطلاعات پروژه"""
    print_header("درباره پروژه")

    about_text = """
╔══════════════════════════════════════════════════════════════════╗
║          Cache Control Instructions Parser & Compiler            ║
╚══════════════════════════════════════════════════════════════════╝

📚 پروژه: تحلیل و کامپایل دستورات کنترل حافظه نهان (Cache)
🎓 درس: کامپایلر (Compiler Design)
👥 گروه: ۱۵
🏛️  دانشگاه: شهید باهنر کرمان (Shahid Bahonar University of Kerman)
📅 ترم: زمستان ۱۴۰۴ (Winter 2026)

─────────────────────────────────────────────────────────────────

✨ ویژگی‌ها:
  • پشتیبانی از 9 دستور Cache Control x86/x64
  • تحلیلگر واژگانی (Lexer) با PLY
  • تحلیلگر نحوی (Parser) - LALR(1)
  • درخت نحوی انتزاعی (AST) - 4 کلاس
  • Parse Tree کامل طبق گرامر BNF
  • مراحل اشتقاق (Derivation)
  • خروجی JSON برای یکپارچگی
  • جدول LR(0) کامل - 14 State
  • نمودار Automata با Graphviz
  • تحلیل Shift-Reduce دستی - 4 مثال
  • تست خودکار - Coverage 100%
  • مستندات کامل فارسی/انگلیسی

─────────────────────────────────────────────────────────────────

🎯 دستورات پشتیبانی شده:
  Cache Flush      → CLFLUSH, CLFLUSHOPT
  Cache Write-Back → CLWB
  Cache Prefetch   → PREFETCHT0, PREFETCHT1, PREFETCHT2, PREFETCHNTA
  Cache Invalidate → WBINVD, INVD

─────────────────────────────────────────────────────────────────

🔧 تکنولوژی‌ها:
  • Python 3.8+
  • PLY (Python Lex-Yacc) 3.11
  • Graphviz (برای نمودارها)

─────────────────────────────────────────────────────────────────

📖 مستندات:
  • README.md - راهنمای اصلی
  • PARSER_USAGE_GUIDE.txt - راهنمای استفاده
  • PARSER_SUMMARY.txt - خلاصه پروژه
  • SHIFT_REDUCE_ANALYSIS.txt - تحلیل دستی
  • document.docx - گزارش نهایی

─────────────────────────────────────────────────────────────────

📊 آمار پروژه:
  • خطوط کد: ~3,500+
  • فایل‌های Python: 7
  • تست‌ها: 6 (همه موفق)
  • مستندات: 5 فایل

─────────────────────────────────────────────────────────────────

© ۱۴۰۴ - گروه ۱۵ - دانشگاه شهید باهنر کرمان
Developed with ❤️ for Compiler Course
"""
    print(about_text)
    press_enter()


# ═══════════════════════════════════════════════════════════════════
# منوی اصلی
# ═══════════════════════════════════════════════════════════════════

def show_menu():
    """نمایش منوی اصلی"""
    menu = """
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

─────────────────────────────────────────────────────────────────
"""
    print(menu)


def show_help():
    """نمایش راهنما"""
    print_header("راهنمای استفاده")

    help_text = """
📘 راهنمای سریع:

🔹 پارس یک دستور:
   مثال: CLFLUSH [EAX]

🔹 فرمت‌های معتبر:
   • MNEMONIC [REGISTER]
   • MNEMONIC [REGISTER+NUMBER]
   • MNEMONIC [REGISTER-NUMBER]
   • MNEMONIC [IDENTIFIER]
   • MNEMONIC (برای WBINVD و INVD)

🔹 رجیسترهای پشتیبانی شده:
   • 32-bit: EAX, EBX, ECX, EDX, ESI, EDI, EBP, ESP
   • 64-bit: RAX, RBX, RCX, RDX, RSI, RDI, RBP, RSP
   • مدرن: R8-R15 (با پسوندهای B/W/D/L)

🔹 دستورات:
   • CLFLUSH, CLFLUSHOPT - پاک‌سازی کش
   • CLWB - بازنویسی کش
   • PREFETCHT0/T1/T2/NTA - پیش‌خوانی
   • WBINVD, INVD - باطل‌سازی کش

🔹 نکات:
   • کامنت‌ها با ; شروع می‌شوند
   • فاصله (space) بین tokens الزامی نیست
   • حروف بزرگ/کوچک مهم است (case-sensitive)
"""
    print(help_text)
    press_enter()


# ═══════════════════════════════════════════════════════════════════
# تابع اصلی
# ═══════════════════════════════════════════════════════════════════

def main():
    """تابع اصلی برنامه"""

    # بنر خوش‌آمدگویی
    clear_screen()
    print("\n" + "╔" + "═" * 64 + "╗")
    print("║" + " " * 10 + "Cache Control Instructions Parser" + " " * 20 + "║")
    print("║" + " " * 20 + "پروژه کامپایلر - گروه ۱۵" + " " * 19 + "║")
    print("║" + " " * 16 + "دانشگاه شهید باهنر کرمان" + " " * 23 + "║")
    print("╚" + "═" * 64 + "╝\n")

    print("🔄 در حال بارگذاری...\n")

    # ساخت Lexer و Parser
    try:
        lexer = build_lexer()
        parser = build_parser()
        print("✅ Parser آماده است!")
    except Exception as e:
        print(f"❌ خطا در بارگذاری: {e}")
        sys.exit(1)

    input("\n⏎ برای شروع Enter را فشار دهید...")

    # حلقه اصلی برنامه
    while True:
        clear_screen()
        show_menu()

        choice = input("➤ انتخاب شما: ").strip().lower()

        try:
            if choice == '1':
                parse_single_instruction()
            elif choice == '2':
                show_json_output()
            elif choice == '3':
                parse_assembly_file()
            elif choice == '4':
                show_lr_table()
            elif choice == '5':
                show_shift_reduce()
            elif choice == '6':
                run_tests()
            elif choice == '7':
                show_grammar()
            elif choice == '8':
                interactive_mode()
            elif choice == '9':
                show_automata()
            elif choice in ['10', '0']:
                show_about()
            elif choice == 'c':
                clean_cache_files()
            elif choice == 'h':
                show_help()
            elif choice == 'q':
                print("\n" + "═" * 80)
                print("👋 خروج از برنامه - موفق باشید!")
                print("📍 دانشگاه شهید باهنر کرمان")
                print("═" * 80 + "\n")
                sys.exit(0)
            else:
                print("\n❌ انتخاب نامعتبر! لطفاً یک گزینه معتبر وارد کنید.")
                press_enter()

        except KeyboardInterrupt:
            print("\n\n⚠️  عملیات لغو شد (Ctrl+C)")
            press_enter()
        except Exception as e:
            print(f"\n❌ خطای غیرمنتظره: {e}")
            import traceback
            traceback.print_exc()
            press_enter()


# ═══════════════════════════════════════════════════════════════════
# نقطه ورود برنامه
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  برنامه توسط کاربر متوقف شد (Ctrl+C)")
        print("👋 خداحافظ!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطای کلی: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
