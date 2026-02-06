#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تست سریع برای بررسی operand requirement"""

from cache_parser import parse_instruction

print("="*80)
print("تست operand requirement")
print("="*80)

test_cases = [
    ("WBINVD", True, "باید موفق باشد (بدون operand مجاز است)"),
    ("INVD", True, "باید موفق باشد (بدون operand مجاز است)"),
    ("CLFLUSHOPT", False, "باید ناموفق باشد (نیاز به operand دارد)"),
    ("CLFLUSH", False, "باید ناموفق باشد (نیاز به operand دارد)"),
    ("CLWB", False, "باید ناموفق باشد (نیاز به operand دارد)"),
    ("PREFETCHT0", False, "باید ناموفق باشد (نیاز به operand دارد)"),
]

print()
success = 0
failed = 0

for code, should_succeed, desc in test_cases:
    print(f"تست: {code}")
    print(f"  انتظار: {desc}")

    try:
        ast = parse_instruction(code, debug=False)
        if ast:
            if should_succeed:
                print(f"  ✅ نتیجه: موفق (درست)")
                success += 1
            else:
                print(f"  ❌ نتیجه: موفق (اشتباه! باید خطا می‌داد)")
                failed += 1
        else:
            if not should_succeed:
                print(f"  ✅ نتیجه: ناموفق (درست)")
                success += 1
            else:
                print(f"  ❌ نتیجه: ناموفق (اشتباه! باید موفق می‌شد)")
                failed += 1
    except Exception as e:
        if not should_succeed:
            print(f"  ✅ نتیجه: خطا گرفت (درست)")
            success += 1
        else:
            print(f"  ❌ نتیجه: خطا گرفت (اشتباه! باید موفق می‌شد)")
            print(f"     خطا: {e}")
            failed += 1

    print()

print("="*80)
print(f"نتیجه: {success} موفق، {failed} ناموفق")
print("="*80)

if failed == 0:
    print("🎉 عالی! همه تست‌ها موفق بود!")
else:
    print("⚠️ برخی تست‌ها ناموفق بود!")
