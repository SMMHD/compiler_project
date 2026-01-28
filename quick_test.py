#!/usr/bin/env python3
"""
تست سریع 30 ثانیه‌ای Parser
فقط اجرا کنید و نتیجه را ببینید!
"""

def quick_test():
    print("\n" + "🚀 " * 30)
    print(" " * 25 + "تست سریع PARSER")
    print("🚀 " * 30 + "\n")

    tests_passed = 0
    tests_total = 0

    # تست 1: Import
    print("1️⃣  Import کردن ماژول‌ها...", end=" ")
    tests_total += 1
    try:
        from cache_parser import parse_instruction
        print("✅")
        tests_passed += 1
    except Exception as e:
        print(f"❌ ({e})")
        return

    # تست 2: پارس ساده
    print("2️⃣  پارس دستور ساده...", end=" ")
    tests_total += 1
    try:
        ast = parse_instruction("CLFLUSH [EAX]")
        assert ast is not None
        assert ast.mnemonic == "CLFLUSH"
        print("✅")
        tests_passed += 1
    except Exception as e:
        print(f"❌ ({e})")

    # تست 3: پارس با offset
    print("3️⃣  پارس دستور با offset...", end=" ")
    tests_total += 1
    try:
        ast = parse_instruction("CLFLUSHOPT [EBX+16]")
        assert ast is not None
        assert ast.operand.offset == "+16"
        print("✅")
        tests_passed += 1
    except Exception as e:
        print(f"❌ ({e})")

    # تست 4: بدون operand
    print("4️⃣  پارس دستور بدون operand...", end=" ")
    tests_total += 1
    try:
        ast = parse_instruction("WBINVD")
        assert ast is not None
        assert ast.operand is None
        print("✅")
        tests_passed += 1
    except Exception as e:
        print(f"❌ ({e})")

    # تست 5: Parse Tree
    print("5️⃣  ساخت Parse Tree...", end=" ")
    tests_total += 1
    try:
        ast = parse_instruction("CLWB [cache_line]")
        lines = ast.pretty_print()
        assert len(lines) > 0
        print("✅")
        tests_passed += 1
    except Exception as e:
        print(f"❌ ({e})")

    # تست 6: JSON
    print("6️⃣  تولید JSON...", end=" ")
    tests_total += 1
    try:
        ast = parse_instruction("PREFETCHT0 [ECX]")
        json_dict = ast.to_dict()
        assert 'mnemonic' in json_dict
        print("✅")
        tests_passed += 1
    except Exception as e:
        print(f"❌ ({e})")

    # نتیجه
    print("\n" + "─" * 80)
    print(f"\n📊 نتیجه: {tests_passed}/{tests_total} تست موفق")

    if tests_passed == tests_total:
        print("\n🎉 عالی! Parser کاملا درست کار می‌کند!")
        print("\n💡 حالا می‌توانید:")
        print("   • از Parser در پروژه استفاده کنید")
        print("   • فایل‌های assembly را پارس کنید")
        print("   • Parse Tree و JSON تولید کنید")
    elif tests_passed > tests_total / 2:
        print("\n⚠️  Parser تا حدودی کار می‌کند ولی مشکلاتی دارد")
        print("   بررسی کنید که cache_parser.py درست نوشته شده باشد")
    else:
        print("\n❌ Parser کار نمی‌کند!")
        print("   بررسی کنید:")
        print("   • آیا cache_lexer.py و cache_parser.py موجود هستند؟")
        print("   • آیا PLY نصب شده؟ (pip install ply)")

    print("\n" + "─" * 80)

if __name__ == "__main__":
    try:
        quick_test()
    except KeyboardInterrupt:
        print("\n\n⚠️  تست متوقف شد")
    except Exception as e:
        print(f"\n\n❌ خطای غیرمنتظره: {e}")
        import traceback
        traceback.print_exc()
