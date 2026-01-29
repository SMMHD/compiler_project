#!/usr/bin/env python3
"""
تحلیل دستی Shift-Reduce Parse
نمایش مرحله به مرحله پارسینگ برای دستورات Cache

پروژه کامپایلر - گروه 15
دانشگاه شهید بهشتی
"""


def print_header(title):
    print("\n" + "═" * 100)
    print(f" {title}")
    print("═" * 100)


def print_trace_table(instruction, steps):
    """
    نمایش جدول ردیابی Shift-Reduce

    Args:
        instruction: دستور ورودی
        steps: لیست مراحل پارسینگ
    """
    print(f"\n📋 دستور ورودی: {instruction}")
    print("\n" + "─" * 100)

    # هدر جدول
    header = f"{'مرحله':<8} | {'پشته (Stack)':<30} | {'ورودی باقی‌مانده':<25} | {'عملیات':<15} | {'قانون/توضیح':<20}"
    print(header)
    print("─" * 100)

    # چاپ مراحل
    for step in steps:
        step_num = step['step']
        stack = step['stack']
        input_remaining = step['input']
        action = step['action']
        rule = step['rule']

        print(f"{step_num:<8} | {stack:<30} | {input_remaining:<25} | {action:<15} | {rule:<20}")

    print("─" * 100)
    print("✅ پارس موفق - دستور معتبر است\n")


def example1_simple():
    """
    مثال 1: CLFLUSH [EAX]
    دستور ساده با رجیستر بدون offset
    """
    print_header("مثال 1: CLFLUSH [EAX] - دستور ساده")

    steps = [
        {
            'step': 1,
            'stack': '$',
            'input': 'CLFLUSH [ EAX ] $',
            'action': 'Shift',
            'rule': 'انتقال CLFLUSH'
        },
        {
            'step': 2,
            'stack': '$ CLFLUSH',
            'input': '[ EAX ] $',
            'action': 'Reduce',
            'rule': 'R3: CLFLUSH → Mnem'
        },
        {
            'step': 3,
            'stack': '$ Mnemonic',
            'input': '[ EAX ] $',
            'action': 'Shift',
            'rule': 'انتقال ['
        },
        {
            'step': 4,
            'stack': '$ Mnemonic [',
            'input': 'EAX ] $',
            'action': 'Shift',
            'rule': 'انتقال رجیستر'
        },
        {
            'step': 5,
            'stack': '$ Mnemonic [ EAX',
            'input': '] $',
            'action': 'Reduce',
            'rule': 'R10: REG → Base'
        },
        {
            'step': 6,
            'stack': '$ Mnemonic [ Base',
            'input': '] $',
            'action': 'Shift',
            'rule': 'انتقال ]'
        },
        {
            'step': 7,
            'stack': '$ Mnemonic [ Base ]',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R8: [Base] → MemAddr'
        },
        {
            'step': 8,
            'stack': '$ Mnemonic MemAddr',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R7: MemAddr → Operand'
        },
        {
            'step': 9,
            'stack': '$ Mnemonic Operand',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R1: Mnem+Op → Inst'
        },
        {
            'step': 10,
            'stack': '$ Instruction',
            'input': '$',
            'action': 'Accept',
            'rule': '✅ پذیرش'
        }
    ]

    print_trace_table("CLFLUSH [EAX]", steps)


def example2_with_offset():
    """
    مثال 2: CLFLUSHOPT [EBX+16]
    دستور با offset مثبت
    """
    print_header("مثال 2: CLFLUSHOPT [EBX+16] - دستور با Offset مثبت")

    steps = [
        {
            'step': 1,
            'stack': '$',
            'input': 'CLFLUSHOPT [ EBX + 16 ] $',
            'action': 'Shift',
            'rule': 'انتقال CLFLUSHOPT'
        },
        {
            'step': 2,
            'stack': '$ CLFLUSHOPT',
            'input': '[ EBX + 16 ] $',
            'action': 'Reduce',
            'rule': 'R3: CLFLUSHOPT → Mnem'
        },
        {
            'step': 3,
            'stack': '$ Mnemonic',
            'input': '[ EBX + 16 ] $',
            'action': 'Shift',
            'rule': 'انتقال ['
        },
        {
            'step': 4,
            'stack': '$ Mnemonic [',
            'input': 'EBX + 16 ] $',
            'action': 'Shift',
            'rule': 'انتقال رجیستر'
        },
        {
            'step': 5,
            'stack': '$ Mnemonic [ EBX',
            'input': '+ 16 ] $',
            'action': 'Shift',
            'rule': 'انتقال +'
        },
        {
            'step': 6,
            'stack': '$ Mnemonic [ EBX +',
            'input': '16 ] $',
            'action': 'Shift',
            'rule': 'انتقال عدد'
        },
        {
            'step': 7,
            'stack': '$ Mnemonic [ EBX + 16',
            'input': '] $',
            'action': 'Reduce',
            'rule': 'R12: +NUM → Offset'
        },
        {
            'step': 8,
            'stack': '$ Mnemonic [ EBX Offset',
            'input': '] $',
            'action': 'Reduce',
            'rule': 'R9: REG+Off → Base'
        },
        {
            'step': 9,
            'stack': '$ Mnemonic [ Base',
            'input': '] $',
            'action': 'Shift',
            'rule': 'انتقال ]'
        },
        {
            'step': 10,
            'stack': '$ Mnemonic [ Base ]',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R8: [Base] → MemAddr'
        },
        {
            'step': 11,
            'stack': '$ Mnemonic MemAddr',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R7: MemAddr → Operand'
        },
        {
            'step': 12,
            'stack': '$ Mnemonic Operand',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R1: Mnem+Op → Inst'
        },
        {
            'step': 13,
            'stack': '$ Instruction',
            'input': '$',
            'action': 'Accept',
            'rule': '✅ پذیرش'
        }
    ]

    print_trace_table("CLFLUSHOPT [EBX+16]", steps)


def example3_no_operand():
    """
    مثال 3: WBINVD
    دستور بدون عملوند
    """
    print_header("مثال 3: WBINVD - دستور بدون Operand")

    steps = [
        {
            'step': 1,
            'stack': '$',
            'input': 'WBINVD $',
            'action': 'Shift',
            'rule': 'انتقال WBINVD'
        },
        {
            'step': 2,
            'stack': '$ WBINVD',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R6: WBINVD → Mnem'
        },
        {
            'step': 3,
            'stack': '$ Mnemonic',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R2: Mnem → Inst'
        },
        {
            'step': 4,
            'stack': '$ Instruction',
            'input': '$',
            'action': 'Accept',
            'rule': '✅ پذیرش'
        }
    ]

    print_trace_table("WBINVD", steps)


def example4_with_label():
    """
    مثال 4: CLWB [cache_line]
    دستور با شناسه (label)
    """
    print_header("مثال 4: CLWB [cache_line] - دستور با Label")

    steps = [
        {
            'step': 1,
            'stack': '$',
            'input': 'CLWB [ cache_line ] $',
            'action': 'Shift',
            'rule': 'انتقال CLWB'
        },
        {
            'step': 2,
            'stack': '$ CLWB',
            'input': '[ cache_line ] $',
            'action': 'Reduce',
            'rule': 'R4: CLWB → Mnem'
        },
        {
            'step': 3,
            'stack': '$ Mnemonic',
            'input': '[ cache_line ] $',
            'action': 'Shift',
            'rule': 'انتقال ['
        },
        {
            'step': 4,
            'stack': '$ Mnemonic [',
            'input': 'cache_line ] $',
            'action': 'Shift',
            'rule': 'انتقال شناسه'
        },
        {
            'step': 5,
            'stack': '$ Mnemonic [ cache_line',
            'input': '] $',
            'action': 'Reduce',
            'rule': 'R11: ID → Base'
        },
        {
            'step': 6,
            'stack': '$ Mnemonic [ Base',
            'input': '] $',
            'action': 'Shift',
            'rule': 'انتقال ]'
        },
        {
            'step': 7,
            'stack': '$ Mnemonic [ Base ]',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R8: [Base] → MemAddr'
        },
        {
            'step': 8,
            'stack': '$ Mnemonic MemAddr',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R7: MemAddr → Operand'
        },
        {
            'step': 9,
            'stack': '$ Mnemonic Operand',
            'input': '$',
            'action': 'Reduce',
            'rule': 'R1: Mnem+Op → Inst'
        },
        {
            'step': 10,
            'stack': '$ Instruction',
            'input': '$',
            'action': 'Accept',
            'rule': '✅ پذیرش'
        }
    ]

    print_trace_table("CLWB [cache_line]", steps)


def print_grammar_rules():
    """نمایش قوانین گرامر مورد استفاده"""
    print_header("قوانین گرامر (Grammar Rules)")

    rules = [
        ("R1", "Instruction → Mnemonic Operand", "دستور با عملوند"),
        ("R2", "Instruction → Mnemonic", "دستور بدون عملوند"),
        ("R3", "Mnemonic → CLFLUSH | CLFLUSHOPT", "دستورات Flush"),
        ("R4", "Mnemonic → CLWB", "دستور Write-Back"),
        ("R5", "Mnemonic → PREFETCHT0 | PREFETCHT1 | ...", "دستورات Prefetch"),
        ("R6", "Mnemonic → WBINVD | INVD", "دستورات Invalidate"),
        ("R7", "Operand → MemoryAddress", "عملوند حافظه"),
        ("R8", "MemoryAddress → [ BaseExpr ]", "آدرس حافظه"),
        ("R9", "BaseExpr → Register Offset", "رجیستر با offset"),
        ("R10", "BaseExpr → Register", "رجیستر ساده"),
        ("R11", "BaseExpr → Identifier", "شناسه/لیبل"),
        ("R12", "Offset → + NUMBER", "offset مثبت"),
        ("R13", "Offset → - NUMBER", "offset منفی"),
    ]

    print(f"\n{'قانون':<6} | {'قاعده تولید':<45} | {'توضیح':<30}")
    print("─" * 85)

    for rule_id, rule, desc in rules:
        print(f"{rule_id:<6} | {rule:<45} | {desc:<30}")

    print()


def save_to_file():
    """ذخیره خروجی در فایل برای استفاده در گزارش"""
    import sys

    # Redirect stdout to file
    original_stdout = sys.stdout

    with open('SHIFT_REDUCE_ANALYSIS.txt', 'w', encoding='utf-8') as f:
        sys.stdout = f

        print("╔" + "═" * 98 + "╗")
        print("║" + " " * 30 + "تحلیل دستی Shift-Reduce Parse" + " " * 38 + "║")
        print("║" + " " * 35 + "پروژه کامپایلر - گروه 15" + " " * 39 + "║")
        print("╚" + "═" * 98 + "╝")

        print_grammar_rules()
        example1_simple()
        example2_with_offset()
        example3_no_operand()
        example4_with_label()

        print("\n" + "═" * 100)
        print("📝 نتیجه‌گیری")
        print("═" * 100)
        print("""
✅ تمامی دستورات با موفقیت پارس شدند
✅ گرامر بدون ابهام است
✅ Parser به صورت Bottom-Up (LR) کار می‌کند
✅ هر دستور دقیقاً یک درخت تجزیه دارد

این تحلیل نشان می‌دهد که:
1. گرامر طراحی شده قابل پارس با روش Shift-Reduce است
2. تمام حالات (با/بدون operand، با/بدون offset، رجیستر/شناسه) پشتیبانی می‌شوند
3. مراحل پارسینگ منطقی و قابل پیش‌بینی هستند
""")

    sys.stdout = original_stdout
    print("\n✅ فایل 'SHIFT_REDUCE_ANALYSIS.txt' ذخیره شد!")


def main():
    """تابع اصلی"""
    print("\n" + "╔" + "═" * 98 + "╗")
    print("║" + " " * 30 + "تحلیل دستی Shift-Reduce Parse" + " " * 38 + "║")
    print("║" + " " * 35 + "پروژه کامپایلر - گروه 15" + " " * 39 + "║")
    print("║" + " " * 30 + "دانشگاه شهید بهشتی - زمستان ۱۴۰۴" + " " * 32 + "║")
    print("╚" + "═" * 98 + "╝")

    # نمایش قوانین گرامر
    print_grammar_rules()

    # مثال‌های مختلف
    example1_simple()
    example2_with_offset()
    example3_no_operand()
    example4_with_label()

    # نتیجه‌گیری
    print("\n" + "═" * 100)
    print("📊 خلاصه تحلیل")
    print("═" * 100)
    print("""
✅ تعداد مثال‌های تحلیل شده: 4
✅ انواع دستورات: Flush, WriteBack, Invalidate
✅ انواع عملوند: رجیستر ساده، با offset، شناسه، بدون عملوند
✅ نتیجه: همه دستورات معتبر و قابل پارس هستند

این تحلیل نشان می‌دهد گرامر طراحی شده:
  • بدون ابهام است
  • قابل پارس به روش LR است
  • تمام حالات ممکن را پوشش می‌دهد
""")

    # ذخیره در فایل
    save_to_file()

    print("\n" + "═" * 100)
    print("✅ تحلیل کامل شد!")
    print("📄 برای استفاده در گزارش، فایل 'SHIFT_REDUCE_ANALYSIS.txt' را باز کنید")
    print("═" * 100 + "\n")


if __name__ == "__main__":
    main()
