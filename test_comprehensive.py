#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت تست جامع پروژه Cache Control Parser
Comprehensive Test Suite
تیم 15 - پروژه کامپایلر
"""

import os
import sys

# رنگ‌ها برای خروجی (ANSI codes)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """چاپ هدر با رنگ"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 80}{Colors.RESET}\n")

def print_section(text):
    """چاپ عنوان بخش"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─' * 80}{Colors.RESET}")

def print_success(text):
    """چاپ پیام موفقیت"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """چاپ پیام خطا"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    """چاپ هشدار"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    """چاپ اطلاعات"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.RESET}")


class TestResults:
    """ذخیره نتایج تست‌ها"""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.details = []

    def add_pass(self, test_name):
        self.total += 1
        self.passed += 1
        self.details.append(('PASS', test_name))

    def add_fail(self, test_name, reason=""):
        self.total += 1
        self.failed += 1
        self.details.append(('FAIL', test_name, reason))

    def add_warning(self, test_name, reason=""):
        self.warnings += 1
        self.details.append(('WARN', test_name, reason))

    def print_summary(self):
        """چاپ خلاصه نتایج"""
        print_header("خلاصه نتایج تست‌ها")

        print(f"تعداد کل تست‌ها: {Colors.BOLD}{self.total}{Colors.RESET}")
        print(f"موفق: {Colors.GREEN}{Colors.BOLD}{self.passed}{Colors.RESET}")
        print(f"ناموفق: {Colors.RED}{Colors.BOLD}{self.failed}{Colors.RESET}")
        print(f"هشدارها: {Colors.YELLOW}{Colors.BOLD}{self.warnings}{Colors.RESET}")

        if self.failed == 0 and self.warnings == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 همه چیز عالیه! پروژه آماده تحویل است.{Colors.RESET}")
        elif self.failed == 0:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}✓ تست‌ها موفق اما چند هشدار وجود دارد.{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠ برخی تست‌ها ناموفق بودند!{Colors.RESET}")

        # محاسبه نمره
        if self.total > 0:
            score = (self.passed / self.total) * 100
            if score == 100:
                color = Colors.GREEN
            elif score >= 80:
                color = Colors.YELLOW
            else:
                color = Colors.RED
            print(f"\nنمره کلی: {color}{Colors.BOLD}{score:.1f}/100{Colors.RESET}")


def test_file_existence():
    """تست 1: بررسی وجود فایل‌های ضروری"""
    print_section("تست 1: بررسی وجود فایل‌های ضروری")

    results = TestResults()

    # فایل‌های اصلی
    essential_files = {
        'main.py': 'فایل اصلی برنامه',
        'cache_lexer.py': 'Lexical Analyzer',
        'cache_parser.py': 'Syntax Parser',
        'lr_tables.py': 'جداول LR(0)',
    }

    for filename, description in essential_files.items():
        if os.path.exists(filename):
            print_success(f"{filename} - {description}")
            results.add_pass(filename)
        else:
            print_error(f"{filename} - {description} یافت نشد!")
            results.add_fail(filename, "فایل وجود ندارد")

    # فایل‌های مستندات
    doc_files = {
        'grammar.txt': 'گرامر',
        'SHIFT_REDUCE_ANALYSIS.txt': 'تحلیل shift-reduce',
        'lr0_automata': 'فایل اتوماتا',
        'LR_PARSING_TABLE_ASCII.txt': 'جدول LR',
        'README.md': 'مستندات GitHub',
        '.gitignore': 'Git ignore',
        'LICENSE': 'مجوز'
    }

    for filename, description in doc_files.items():
        if os.path.exists(filename):
            print_success(f"{filename} - {description}")
            results.add_pass(filename)
        else:
            print_warning(f"{filename} - {description} یافت نشد")
            results.add_warning(filename, "فایل مستندات موجود نیست")

    return results


def test_imports():
    """تست 2: بررسی import های پروژه"""
    print_section("تست 2: بررسی Import های پایتون")

    results = TestResults()

    # تست import کتابخانه‌های ضروری
    try:
        import ply
        print_success("PLY (Python Lex-Yacc) نصب شده است")
        results.add_pass("PLY import")
    except ImportError:
        print_error("PLY نصب نیست! نصب کنید: pip install ply")
        results.add_fail("PLY import", "کتابخانه نصب نیست")

    # تست import ماژول‌های پروژه
    modules = [
        ('cache_lexer', 'Lexer'),
        ('cache_parser', 'Parser'),
        ('lr_tables', 'LR Tables')
    ]

    for module_name, description in modules:
        try:
            __import__(module_name)
            print_success(f"{module_name}.py - {description} قابل import است")
            results.add_pass(f"{module_name} import")
        except Exception as e:
            print_error(f"{module_name}.py - خطا: {e}")
            results.add_fail(f"{module_name} import", str(e))

    return results


def test_parser_functionality():
    """تست 3: تست عملکرد پارسر"""
    print_section("تست 3: تست عملکرد Parser")

    results = TestResults()

    try:
        from cache_parser import parse_instruction

        # تست کیس‌های مختلف
        test_cases = [
            ("CLFLUSH [EAX]", "دستور با رجیستر ساده"),
            ("CLFLUSHOPT [EBX+16]", "دستور با offset مثبت"),
            ("PREFETCHT0 [ECX-8]", "دستور با offset منفی"),
            ("WBINVD", "دستور بدون operand"),
            ("CLWB [cache_line]", "دستور با شناسه"),
            ("PREFETCHNTA [RAX+128]", "دستور با offset بزرگ"),
        ]

        print()
        for instruction, description in test_cases:
            try:
                result = parse_instruction(instruction)
                if result is not None:
                    print_success(f'"{instruction}" - {description}')
                    results.add_pass(f"Parse: {instruction}")
                else:
                    print_error(f'"{instruction}" - {description} - نتیجه None')
                    results.add_fail(f"Parse: {instruction}", "نتیجه None")
            except Exception as e:
                print_error(f'"{instruction}" - {description} - خطا: {e}')
                results.add_fail(f"Parse: {instruction}", str(e))

    except ImportError as e:
        print_error(f"نمی‌توان cache_parser را import کرد: {e}")
        results.add_fail("Parser import", str(e))

    return results


def test_lr_tables():
    """تست 4: بررسی جداول LR"""
    print_section("تست 4: بررسی جداول LR(0)")

    results = TestResults()

    try:
        from lr_tables import LR_PARSING_TABLE, GRAMMAR_RULES

        # بررسی تعداد state ها
        num_states = len(LR_PARSING_TABLE)
        if num_states == 17:
            print_success(f"تعداد state ها: {num_states} (صحیح)")
            results.add_pass("تعداد state ها")
        else:
            print_warning(f"تعداد state ها: {num_states} (انتظار: 17)")
            results.add_warning("تعداد state ها", f"تعداد {num_states} است نه 17")

        # بررسی تعداد قوانین
        num_rules = len(GRAMMAR_RULES)
        if num_rules == 18:
            print_success(f"تعداد قوانین گرامر: {num_rules} (صحیح)")
            results.add_pass("تعداد قوانین")
        else:
            print_warning(f"تعداد قوانین: {num_rules} (انتظار: 18)")
            results.add_warning("تعداد قوانین", f"تعداد {num_rules} است نه 18")

        # بررسی state 0
        if 0 in LR_PARSING_TABLE:
            print_success("State 0 (حالت اولیه) موجود است")
            results.add_pass("State 0")
        else:
            print_error("State 0 موجود نیست!")
            results.add_fail("State 0", "وجود ندارد")

        # بررسی accept
        has_accept = False
        for state, actions in LR_PARSING_TABLE.items():
            if 'accept' in actions.values() or 'acc' in str(actions).lower():
                has_accept = True
                break

        if has_accept:
            print_success("جدول دارای state accept است")
            results.add_pass("Accept state")
        else:
            print_warning("state accept یافت نشد")
            results.add_warning("Accept state", "یافت نشد")

    except ImportError as e:
        print_error(f"نمی‌توان lr_tables را import کرد: {e}")
        results.add_fail("LR Tables import", str(e))

    return results


def test_grammar_consistency():
    """تست 5: بررسی سازگاری گرامر"""
    print_section("تست 5: بررسی سازگاری فایل‌های گرامر")

    results = TestResults()

    # بررسی فایل grammar.txt
    if os.path.exists('grammar.txt'):
        with open('grammar.txt', 'r', encoding='utf-8') as f:
            content = f.read()

            # شمارش قوانین
            rule_count = content.count('→') + content.count('->')

            if rule_count >= 18:
                print_success(f"grammar.txt دارای {rule_count} قانون است")
                results.add_pass("grammar.txt")
            else:
                print_warning(f"grammar.txt دارای {rule_count} قانون است (انتظار: 18)")
                results.add_warning("grammar.txt", f"فقط {rule_count} قانون")

            # بررسی وجود قوانین کلیدی
            key_rules = ['instruction', 'mnemonic', 'operand', 'memory_address', 'base_expr', 'offset']
            for rule in key_rules:
                if rule in content:
                    results.add_pass(f"قانون {rule}")
                else:
                    print_warning(f"قانون {rule} در گرامر یافت نشد")
                    results.add_warning(f"قانون {rule}", "یافت نشد")
    else:
        print_warning("grammar.txt یافت نشد")
        results.add_warning("grammar.txt", "فایل موجود نیست")

    return results


def test_documentation():
    """تست 6: بررسی مستندات"""
    print_section("تست 6: بررسی کیفیت مستندات")

    results = TestResults()

    # بررسی README.md
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()

            # بررسی بخش‌های کلیدی
            sections = [
                ('# Cache Control', 'عنوان اصلی'),
                ('## ', 'هدرهای بخش'),
                ('```', 'بلوک‌های کد'),
                ('https://', 'لینک‌ها'),
            ]

            for pattern, description in sections:
                if pattern in readme:
                    print_success(f"README دارای {description} است")
                    results.add_pass(f"README: {description}")
                else:
                    print_warning(f"README فاقد {description} است")
                    results.add_warning(f"README: {description}", "یافت نشد")

            # بررسی طول README
            lines = len(readme.splitlines())
            if lines > 200:
                print_success(f"README.md دارای {lines} خط است (جامع)")
                results.add_pass("README length")
            else:
                print_warning(f"README.md دارای {lines} خط است (کوتاه)")
                results.add_warning("README length", "خیلی کوتاه است")
    else:
        print_warning("README.md یافت نشد")
        results.add_warning("README.md", "فایل موجود نیست")

    return results


def test_examples():
    """تست 7: بررسی فایل‌های مثال"""
    print_section("تست 7: بررسی فایل‌های مثال JSON")

    results = TestResults()

    example_files = [
        'CLFLUSHOPT-RBX-16.json',
        'PREFETCHNTA-RAX.json',
        'WBINVD.json'
    ]

    for filename in example_files:
        if os.path.exists(filename):
            try:
                import json
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print_success(f"{filename} - فرمت JSON صحیح است")
                results.add_pass(filename)
            except json.JSONDecodeError:
                print_error(f"{filename} - فرمت JSON نامعتبر!")
                results.add_fail(filename, "JSON نامعتبر")
        else:
            print_warning(f"{filename} - یافت نشد")
            results.add_warning(filename, "فایل موجود نیست")

    return results


def test_automata():
    """تست 8: بررسی فایل اتوماتا"""
    print_section("تست 8: بررسی فایل‌های اتوماتا")

    results = TestResults()

    # بررسی فایل DOT
    if os.path.exists('lr0_automata'):
        with open('lr0_automata', 'r', encoding='utf-8') as f:
            content = f.read()

            # شمارش state ها
            state_count = content.count('[label="State')

            if state_count == 17:
                print_success(f"lr0_automata دارای {state_count} state است (صحیح)")
                results.add_pass("Automata states")
            else:
                print_warning(f"lr0_automata دارای {state_count} state است (انتظار: 17)")
                results.add_warning("Automata states", f"{state_count} state")

            # بررسی فرمت DOT
            if 'digraph' in content:
                print_success("فایل اتوماتا فرمت DOT صحیح دارد")
                results.add_pass("DOT format")
            else:
                print_error("فرمت فایل اتوماتا صحیح نیست")
                results.add_fail("DOT format", "نامعتبر")
    else:
        print_warning("lr0_automata یافت نشد")
        results.add_warning("lr0_automata", "فایل موجود نیست")

    # بررسی تصویر
    image_files = ['lr0_automata.png', 'lr0_automata.jpg', 'lr0_automata.pdf']
    has_image = False
    for img in image_files:
        if os.path.exists(img):
            print_success(f"{img} موجود است")
            results.add_pass(f"Image: {img}")
            has_image = True

    if not has_image:
        print_warning("تصویر اتوماتا یافت نشد (.png, .jpg, .pdf)")
        results.add_warning("Automata image", "تصویر موجود نیست")

    return results


def main():
    """اجرای همه تست‌ها"""
    print_header("🧪 تست جامع پروژه Cache Control Parser")
    print_info("این اسکریپت تمام بخش‌های پروژه را تست می‌کند")
    print_info("تیم 15 - پروژه کامپایلر - دانشگاه شهید باهنر کرمان")

    # جمع‌آوری نتایج همه تست‌ها
    all_results = TestResults()

    # اجرای تست‌ها
    test_functions = [
        test_file_existence,
        test_imports,
        test_parser_functionality,
        test_lr_tables,
        test_grammar_consistency,
        test_documentation,
        test_examples,
        test_automata
    ]

    for test_func in test_functions:
        try:
            result = test_func()
            all_results.total += result.total
            all_results.passed += result.passed
            all_results.failed += result.failed
            all_results.warnings += result.warnings
        except Exception as e:
            print_error(f"خطا در اجرای {test_func.__name__}: {e}")
            all_results.add_fail(test_func.__name__, str(e))

    # نمایش خلاصه
    all_results.print_summary()

    # پیشنهادات
    if all_results.failed > 0 or all_results.warnings > 0:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}💡 پیشنهادات:{Colors.RESET}")
        if all_results.failed > 0:
            print("  • تست‌های ناموفق را بررسی کنید")
            print("  • از وجود همه فایل‌های ضروری اطمینان حاصل کنید")
            print("  • کتابخانه‌های مورد نیاز را نصب کنید: pip install -r requirements.txt")
        if all_results.warnings > 0:
            print("  • هشدارها را بررسی کنید (اختیاری اما توصیه می‌شود)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}👋 تست متوقف شد{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ خطای غیرمنتظره: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
