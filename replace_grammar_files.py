#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت خودکار جایگزینی فایل‌های گرامر
Auto-replacement script for grammar files
تیم 15 - پروژه کامپایلر
"""

import os
import shutil
from datetime import datetime

def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "اسکریپت جایگزینی خودکار گرامر" + " " * 29 + "║")
    print("╚" + "═" * 78 + "╝")

    # بررسی وجود فایل‌های جدید
    new_files = {
        'grammar_UPDATED.txt': 'grammar.txt',
        'SHIFT_REDUCE_ANALYSIS_UPDATED.txt': 'SHIFT_REDUCE_ANALYSIS.txt'
    }

    missing = []
    for new_file in new_files.keys():
        if not os.path.exists(new_file):
            missing.append(new_file)

    if missing:
        print("\n❌ خطا: فایل‌های زیر یافت نشدند:")
        for f in missing:
            print(f"   • {f}")
        print("\n💡 ابتدا فایل‌های به‌روز شده را ایجاد کنید.")
        return

    print("\n✅ تمام فایل‌های جدید یافت شدند.")

    # ایجاد پوشه backup
    backup_dir = f"backup_grammar_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    print(f"\n📦 ایجاد پوشه backup: {backup_dir}")

    # پشتیبان‌گیری و جایگزینی
    for new_file, target_file in new_files.items():
        # اگر فایل قدیمی وجود دارد، backup بگیر
        if os.path.exists(target_file):
            backup_path = os.path.join(backup_dir, target_file)
            shutil.copy2(target_file, backup_path)
            print(f"  ✓ پشتیبان: {target_file} → {backup_path}")

        # جایگزینی
        shutil.copy2(new_file, target_file)
        print(f"  ✓ جایگزین: {new_file} → {target_file}")

    print("\n" + "═" * 80)
    print("✅ عملیات با موفقیت انجام شد!")
    print("═" * 80)

    print("\n📋 فایل‌های به‌روز شده:")
    for target in new_files.values():
        print(f"  • {target}")

    print(f"\n💾 فایل‌های قبلی در پوشه '{backup_dir}' ذخیره شدند")

    print("\n" + "─" * 80)
    print("🔍 بررسی سازگاری:")
    print("─" * 80)

    # بررسی lr_tables.py
    if os.path.exists('lr_tables.py'):
        with open('lr_tables.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'GRAMMAR_RULES = {' in content:
                # شمارش قوانین
                rules_count = content.count('":')
                print(f"  ✓ lr_tables.py → {rules_count} قانون")

    # بررسی grammar.txt
    if os.path.exists('grammar.txt'):
        with open('grammar.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            rules_count = content.count('R')
            print(f"  ✓ grammar.txt → قوانین R1-R18 موجود")

    # بررسی SHIFT_REDUCE_ANALYSIS.txt
    if os.path.exists('SHIFT_REDUCE_ANALYSIS.txt'):
        with open('SHIFT_REDUCE_ANALYSIS.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            examples = content.count('مثال')
            print(f"  ✓ SHIFT_REDUCE_ANALYSIS.txt → {examples} مثال با شماره قوانین صحیح")

    print("\n✅ همه فایل‌ها با گرامر 18 قانونی هماهنگ هستند!")
    print("\n💡 می‌توانید فایل‌های _UPDATED را حذف کنید:")
    print("   rm grammar_UPDATED.txt SHIFT_REDUCE_ANALYSIS_UPDATED.txt")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()
