#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست Parser به‌روز شده - گرامر 18 قانونی
Test Updated Parser - 18-Rule Grammar
"""

print("=" * 80)
print(" " * 25 + "تست Parser به‌روز شده")
print(" " * 20 + "Test Updated Parser (18 Rules)")
print("=" * 80)

# تست import
print("\n1️⃣ تست Import...")
try:
    from cache_parser import (
        parse_instruction, 
        Instruction, 
        MemoryOperand, 
        Register, 
        Identifier
    )
    print("   ✅ Import موفق")
except ImportError as e:
    print(f"   ❌ خطا در import: {e}")
    print("   💡 مطمئن شو cache_parser.py در همان پوشه است")
    exit(1)

# تست‌های پارسر
print("\n2️⃣ تست پارس دستورات...")

test_cases = [
    {
        'code': 'CLFLUSH [EAX]',
        'desc': 'Flush با رجیستر 32-bit',
        'should_pass': True,
        'checks': {
            'mnemonic': 'CLFLUSH',
            'has_operand': True,
            'base_type': 'Register',
            'base_name': 'EAX',
            'has_offset': False
        }
    },
    {
        'code': 'CLFLUSHOPT [EBX+16]',
        'desc': 'Flush با offset مثبت',
        'should_pass': True,
        'checks': {
            'mnemonic': 'CLFLUSHOPT',
            'has_operand': True,
            'base_type': 'Register',
            'base_name': 'EBX',
            'has_offset': True,
            'offset': 16
        }
    },
    {
        'code': 'PREFETCHT0 [ECX-8]',
        'desc': 'Prefetch با offset منفی',
        'should_pass': True,
        'checks': {
            'mnemonic': 'PREFETCHT0',
            'has_operand': True,
            'base_type': 'Register',
            'base_name': 'ECX',
            'has_offset': True,
            'offset': -8
        }
    },
    {
        'code': 'WBINVD',
        'desc': 'Invalidate بدون operand',
        'should_pass': True,
        'checks': {
            'mnemonic': 'WBINVD',
            'has_operand': False
        }
    },
    {
        'code': 'CLWB [cache_line]',
        'desc': 'WriteBack با identifier',
        'should_pass': True,
        'checks': {
            'mnemonic': 'CLWB',
            'has_operand': True,
            'base_type': 'Identifier',
            'base_name': 'cache_line',
            'has_offset': False
        }
    },
    {
        'code': 'PREFETCHNTA [RAX+128]',
        'desc': 'Prefetch با رجیستر 64-bit',
        'should_pass': True,
        'checks': {
            'mnemonic': 'PREFETCHNTA',
            'has_operand': True,
            'base_type': 'Register',
            'base_name': 'RAX',
            'has_offset': True,
            'offset': 128
        }
    },
]

success = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    print(f"\n   تست {i}/{len(test_cases)}: {test['desc']}")
    print(f"   دستور: {test['code']}")

    ast = parse_instruction(test['code'], debug=False)

    if test['should_pass']:
        if ast:
            print("   ✅ پارس موفق")

            # بررسی checks
            checks_passed = True

            if ast.mnemonic != test['checks']['mnemonic']:
                print(f"   ⚠️  mnemonic: انتظار {test['checks']['mnemonic']}, دریافت {ast.mnemonic}")
                checks_passed = False

            if (ast.operand is not None) != test['checks']['has_operand']:
                print(f"   ⚠️  has_operand: انتظار {test['checks']['has_operand']}, دریافت {ast.operand is not None}")
                checks_passed = False

            if ast.operand and 'base_type' in test['checks']:
                if ast.operand.base.type != test['checks']['base_type']:
                    print(f"   ⚠️  base_type: انتظار {test['checks']['base_type']}, دریافت {ast.operand.base.type}")
                    checks_passed = False

                if str(ast.operand.base) != test['checks']['base_name']:
                    print(f"   ⚠️  base_name: انتظار {test['checks']['base_name']}, دریافت {str(ast.operand.base)}")
                    checks_passed = False

                if (ast.operand.offset is not None) != test['checks']['has_offset']:
                    print(f"   ⚠️  has_offset: انتظار {test['checks']['has_offset']}, دریافت {ast.operand.offset is not None}")
                    checks_passed = False

                if 'offset' in test['checks'] and ast.operand.offset != test['checks']['offset']:
                    print(f"   ⚠️  offset: انتظار {test['checks']['offset']}, دریافت {ast.operand.offset}")
                    checks_passed = False

            if checks_passed:
                print("   ✅ همه بررسی‌ها موفق")
                success += 1
            else:
                print("   ⚠️  برخی بررسی‌ها ناموفق")
                failed += 1
        else:
            print("   ❌ پارس ناموفق (انتظار موفق بود)")
            failed += 1
    else:
        if not ast:
            print("   ✅ پارس ناموفق (انتظار ناموفق بود)")
            success += 1
        else:
            print("   ❌ پارس موفق (انتظار ناموفق بود)")
            failed += 1

# تست Parse Tree
print("\n3️⃣ تست Parse Tree (بدون لایه واسطه)...")

ast = parse_instruction('CLFLUSH [EAX]')
if ast:
    tree_lines = ast.full_parse_tree()
    tree_text = '\n'.join(tree_lines)

    # بررسی که non-terminal های واسطه نباشند
    bad_terms = ['CacheFlush', 'PrefetchType', 'WriteBackMnemonic', 'CacheWrite', 'CachePrefetch']
    found_bad = False

    for bad_term in bad_terms:
        if bad_term in tree_text:
            print(f"   ❌ یافت شد: {bad_term} (این نباید باشد!)")
            found_bad = True
            failed += 1

    if not found_bad:
        print("   ✅ Parse Tree بدون non-terminal واسطه")

        # بررسی که mnemonic مستقیم به CLFLUSH برود
        if 'mnemonic' in tree_text and 'CLFLUSH (terminal)' in tree_text:
            print("   ✅ mnemonic مستقیم به terminal می‌رود")
            success += 1
        else:
            print("   ⚠️  ساختار mnemonic مشکوک است")
            failed += 1
else:
    print("   ❌ پارس ناموفق")
    failed += 1

# تست Derivation Steps
print("\n4️⃣ تست Derivation Steps (طبق R1-R18)...")

ast = parse_instruction('CLFLUSHOPT [EBX+16]')
if ast:
    steps = ast.derivation_steps()
    steps_text = '\n'.join(steps)

    # بررسی که non-terminal های واسطه نباشند
    bad_terms = ['CacheFlush', 'PrefetchType', 'WriteBackMnemonic']
    found_bad = False

    for bad_term in bad_terms:
        if bad_term in steps_text:
            print(f"   ❌ یافت شد: {bad_term} (این نباید باشد!)")
            found_bad = True
            failed += 1

    if not found_bad:
        print("   ✅ Derivation بدون لایه واسطه")

        # بررسی مراحل اصلی
        if '→ mnemonic operand' in steps_text:
            print("   ✅ مرحله R1: instruction → mnemonic operand")

        if '→ CLFLUSHOPT operand' in steps_text:
            print("   ✅ مرحله R4: mnemonic → CLFLUSHOPT")

        if '→ CLFLUSHOPT memory_address' in steps_text:
            print("   ✅ مرحله R12: operand → memory_address")

        success += 1
else:
    print("   ❌ پارس ناموفق")
    failed += 1

# نتیجه نهایی
print("\n" + "=" * 80)
print(" " * 30 + "نتیجه نهایی")
print("=" * 80)

total = success + failed
percentage = (success / total * 100) if total > 0 else 0

print(f"\n   ✅ موفق: {success}")
print(f"   ❌ ناموفق: {failed}")
print(f"   📊 درصد موفقیت: {percentage:.1f}%")

if failed == 0:
    print("\n   🎉 عالی! همه تست‌ها موفق بود!")
    print("   ✅ cache_parser.py به‌درستی به‌روز شد")
    print("   ✅ گرامر 18 قانونی کاملاً هماهنگ است")
    print("\n" + "=" * 80)
    exit(0)
else:
    print("\n   ⚠️  برخی تست‌ها ناموفق بود!")
    print("   💡 راهنما:")
    print("      1. مطمئن شو cache_parser_UPDATED.py را به cache_parser.py کپی کردی")
    print("      2. __pycache__ و parser.out را پاک کن")
    print("      3. دوباره تست کن")
    print("\n" + "=" * 80)
    exit(1)
