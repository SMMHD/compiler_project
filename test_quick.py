#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست سریع پروژه Cache Control Parser
Quick Test - 30 ثانیه
"""

def test_quick():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 25 + "تست سریع پروژه" + " " * 36 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    passed = 0
    failed = 0

    # تست 1: Import کردن parser
    print("🔄 تست 1: Import کردن parser...")
    try:
        from cache_parser import parse_instruction
        print("✅ Parser قابل import است")
        passed += 1
    except Exception as e:
        print(f"❌ خطا در import: {e}")
        failed += 1
        return

    # تست 2: پارس دستورات مختلف
    print("\n🔄 تست 2: پارس دستورات...")

    test_cases = [
        "CLFLUSH [EAX]",
        "CLFLUSHOPT [EBX+16]",
        "PREFETCHT0 [ECX-8]",
        "WBINVD",
        "CLWB [cache_line]",
        "PREFETCHNTA [RAX+128]"
    ]

    for i, instruction in enumerate(test_cases, 1):
        try:
            result = parse_instruction(instruction)
            if result:
                print(f"✅ تست {i}/6: {instruction}")
                passed += 1
            else:
                print(f"❌ تست {i}/6: {instruction} - نتیجه None")
                failed += 1
        except Exception as e:
            print(f"❌ تست {i}/6: {instruction} - خطا: {e}")
            failed += 1

    # خلاصه
    print("\n" + "─" * 80)
    print(f"\n📊 نتیجه: {passed} موفق، {failed} ناموفق")

    if failed == 0:
        print("\n🎉 عالی! همه تست‌ها موفق بود. پارسر درست کار می‌کند!")
    else:
        print(f"\n⚠️  {failed} تست ناموفق بود. کد را بررسی کنید.")

    print("\n💡 برای تست جامع‌تر: python test_comprehensive.py")
    print()

if __name__ == "__main__":
    try:
        test_quick()
    except KeyboardInterrupt:
        print("\n\n👋 تست متوقف شد")
    except Exception as e:
        print(f"\n❌ خطا: {e}")
