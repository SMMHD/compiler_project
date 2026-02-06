#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cache Control Instructions Parser
Parser دستورات کنترل کش
تیم 15 - پروژه کامپایلر - دانشگاه شهید باهنر کرمان

ویژگی‌ها:
- گرامر 18 قانونی استاندارد (R1-R18)
- Abstract Syntax Tree (AST)
- Bottom-Up Parsing با LR(0)
- پشتیبانی از 9 دستور کنترل کش
- Parse Tree کامل طبق گرامر BNF
"""

import ply.yacc as yacc
from cache_lexer import tokens, build_lexer
import json


# ═══════════════════════════════════════════════════════════════════
#                          AST Node Classes
# ═══════════════════════════════════════════════════════════════════

class ASTNode:
    """Base class for all Abstract Syntax Tree nodes"""

    def to_dict(self):
        """تبدیل به JSON"""
        raise NotImplementedError

    def pretty_print(self, indent=0):
        """چاپ زیبای درخت"""
        raise NotImplementedError


class Instruction(ASTNode):
    """
    نود ریشه AST - نمایانگر یک دستور کامل

    Args:
        mnemonic: نام دستور (مثل CLFLUSH)
        operand: عملوند (None برای دستوراتی مثل WBINVD)
    """

    def __init__(self, mnemonic, operand=None):
        self.mnemonic = mnemonic
        self.operand = operand
        self.type = "Instruction"

    def __repr__(self):
        if self.operand:
            return f"Instruction({self.mnemonic}, {self.operand})"
        return f"Instruction({self.mnemonic})"

    def to_dict(self):
        return {
            'type': 'Instruction',
            'mnemonic': self.mnemonic,
            'operand': self.operand.to_dict() if self.operand else None,
            'has_operand': self.operand is not None
        }

    def pretty_print(self, indent=0):
        """Parse Tree ساده (AST)"""
        prefix = "  " * indent
        lines = []
        lines.append(f"{prefix}Instruction: {self.mnemonic}")

        if self.operand:
            lines.append(f"{prefix}├─ Operand:")
            lines.extend(self.operand.pretty_print(indent + 1))
        else:
            lines.append(f"{prefix}└─ No Operand")

        return lines

    def full_parse_tree(self):
        """
        Parse Tree کامل طبق گرامر BNF (18 قانون)
        بدون non-terminal های واسطه
        """
        lines = []
        indent = "  "

        lines.append("Instruction")

        if self.operand:
            # R1: instruction → mnemonic operand
            lines.append(f"{indent}├── mnemonic")
            lines.append(f"{indent}│   └── {self.mnemonic} (terminal)")
            lines.append(f"{indent}└── operand")
            lines.append(f"{indent}    └── memory_address")
            lines.append(f"{indent}        ├── [ (terminal)")
            lines.append(f"{indent}        ├── base_expr")

            # Base Expression
            if isinstance(self.operand.base, Register):
                lines.append(f"{indent}        │   └── REGISTER")
                lines.append(f"{indent}        │       └── {self.operand.base.name} (terminal)")

                # Offset (اگر دارد)
                if self.operand.offset:
                    sign = '+' if self.operand.offset > 0 else '-'
                    num = abs(self.operand.offset)
                    lines.append(f"{indent}        │   └── offset")
                    lines.append(f"{indent}        │       ├── {sign} (terminal)")
                    lines.append(f"{indent}        │       └── {num} (terminal)")
                else:
                    lines.append(f"{indent}        │   └── ε (no offset)")

            elif isinstance(self.operand.base, Identifier):
                lines.append(f"{indent}        │   └── IDENTIFIER")
                lines.append(f"{indent}        │       └── {self.operand.base.name} (terminal)")

            lines.append(f"{indent}        └── ] (terminal)")

        else:
            # R2: instruction → mnemonic
            lines.append(f"{indent}└── mnemonic")
            lines.append(f"{indent}    └── {self.mnemonic} (terminal)")

        return lines

    def derivation_steps(self):
        """
        مراحل اشتقاق طبق گرامر 18 قانونی
        """
        steps = []
        steps.append("Instruction")

        if self.operand:
            # R1: instruction → mnemonic operand
            steps.append("→ mnemonic operand")

            # R3-R11: mnemonic → TERMINAL
            steps.append(f"→ {self.mnemonic} operand")

            # R12: operand → memory_address
            steps.append(f"→ {self.mnemonic} memory_address")

            # R13: memory_address → [ base_expr ]
            steps.append(f"→ {self.mnemonic} [ base_expr ]")

            # Base Expression
            if isinstance(self.operand.base, Register):
                if self.operand.offset:
                    # R14: base_expr → REGISTER offset
                    steps.append(f"→ {self.mnemonic} [ REGISTER offset ]")
                    steps.append(f"→ {self.mnemonic} [ {self.operand.base.name} offset ]")

                    # R17 یا R18: offset → + NUMBER یا - NUMBER
                    sign = '+' if self.operand.offset > 0 else '-'
                    num = abs(self.operand.offset)
                    steps.append(f"→ {self.mnemonic} [ {self.operand.base.name} {sign} {num} ]")
                else:
                    # R15: base_expr → REGISTER
                    steps.append(f"→ {self.mnemonic} [ REGISTER ]")
                    steps.append(f"→ {self.mnemonic} [ {self.operand.base.name} ]")

            else:
                # R16: base_expr → IDENTIFIER
                steps.append(f"→ {self.mnemonic} [ IDENTIFIER ]")
                steps.append(f"→ {self.mnemonic} [ {self.operand.base.name} ]")

        else:
            # R2: instruction → mnemonic
            steps.append("→ mnemonic")

            # R10 یا R11: mnemonic → WBINVD یا INVD
            steps.append(f"→ {self.mnemonic}")

        return steps

    def get_instruction_category(self):
        """دریافت دسته دستور"""
        categories = {
            'flush': ['CLFLUSH', 'CLFLUSHOPT'],
            'writeback': ['CLWB'],
            'prefetch': ['PREFETCHT0', 'PREFETCHT1', 'PREFETCHT2', 'PREFETCHNTA'],
            'invalidate': ['WBINVD', 'INVD']
        }

        for category, mnemonics in categories.items():
            if self.mnemonic in mnemonics:
                return category

        return 'unknown'


class MemoryOperand(ASTNode):
    """
    نمایانگر یک عملوند حافظه

    Args:
        base: پایه (Register یا Identifier)
        offset: جابجایی (اختیاری)
    """

    def __init__(self, base, offset=None):
        self.base = base
        self.offset = offset
        self.type = "MemoryOperand"

    def __repr__(self):
        if self.offset:
            return f"Memory([{self.base}{self.offset:+d}])"
        return f"Memory([{self.base}])"

    def to_dict(self):
        return {
            'type': 'MemoryOperand',
            'base': self.base.to_dict() if hasattr(self.base, 'to_dict') else str(self.base),
            'offset': self.offset,
            'has_offset': self.offset is not None
        }

    def pretty_print(self, indent=0):
        prefix = "  " * indent
        lines = []
        lines.append(f"{prefix}  MemoryOperand:")
        lines.append(f"{prefix}  ├─ Base: {self.base}")

        if self.offset:
            lines.append(f"{prefix}  └─ Offset: {self.offset:+d}")
        else:
            lines.append(f"{prefix}  └─ Offset: None")

        return lines


class Register(ASTNode):
    """
    نمایانگر یک رجیستر CPU

    Args:
        name: نام رجیستر (مثل EAX, RBX)
    """

    def __init__(self, name):
        self.name = name
        self.type = "Register"
        self.bit_width = 64 if name.startswith('R') else 32

    def __repr__(self):
        return f"Register({self.name})"

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'type': 'Register',
            'name': self.name,
            'bit_width': self.bit_width
        }

    def pretty_print(self, indent=0):
        prefix = "  " * indent
        return [f"{prefix}Register({self.name}, {self.bit_width}-bit)"]


class Identifier(ASTNode):
    """
    نمایانگر یک شناسه (label)

    Args:
        name: نام شناسه (مثل cache_line, data_ptr)
    """

    def __init__(self, name):
        self.name = name
        self.type = "Identifier"

    def __repr__(self):
        return f"Identifier({self.name})"

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'type': 'Identifier',
            'name': self.name
        }

    def pretty_print(self, indent=0):
        prefix = "  " * indent
        return [f"{prefix}Identifier({self.name})"]


# ═══════════════════════════════════════════════════════════════════
#                   Grammar Rules - 18 قانون
# ═══════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────
# قوانین اصلی (2 قانون)
# ─────────────────────────────────────────────────────────────────

def p_instruction_with_operand(p):
    """instruction : mnemonic operand"""
    # R1: instruction → mnemonic operand
    p[0] = Instruction(p[1], p[2])
    if parser_debug:
        print(f"REDUCE: mnemonic operand → Instruction (R1)")


def p_instruction_no_operand(p):
    """instruction : mnemonic"""
    # R2: instruction → mnemonic
    p[0] = Instruction(p[1])
    if parser_debug:
        print(f"REDUCE: mnemonic → Instruction (R2)")


# ─────────────────────────────────────────────────────────────────
# Mnemonic (9 قانون)
# ─────────────────────────────────────────────────────────────────

def p_mnemonic_clflush(p):
    """mnemonic : CLFLUSH"""
    # R3: mnemonic → CLFLUSH
    p[0] = p[1]
    if parser_debug:
        print(f"REDUCE: CLFLUSH → mnemonic (R3)")


def p_mnemonic_clflushopt(p):
    """mnemonic : CLFLUSHOPT"""
    # R4: mnemonic → CLFLUSHOPT
    p[0] = p[1]
    if parser_debug:
        print(f"REDUCE: CLFLUSHOPT → mnemonic (R4)")


def p_mnemonic_clwb(p):
    """mnemonic : CLWB"""
    # R5: mnemonic → CLWB
    p[0] = p[1]
    if parser_debug:
        print(f"REDUCE: CLWB → mnemonic (R5)")


def p_mnemonic_prefetcht0(p):
    """mnemonic : PREFETCHT0"""
    # R6: mnemonic → PREFETCHT0
    p[0] = p[1]
    if parser_debug:
        print(f"REDUCE: PREFETCHT0 → mnemonic (R6)")


def p_mnemonic_prefetcht1(p):
    """mnemonic : PREFETCHT1"""
    # R7: mnemonic → PREFETCHT1
    p[0] = p[1]
    if parser_debug:
        print(f"REDUCE: PREFETCHT1 → mnemonic (R7)")


def p_mnemonic_prefetcht2(p):
    """mnemonic : PREFETCHT2"""
    # R8: mnemonic → PREFETCHT2
    p[0] = p[1]
    if parser_debug:
        print(f"REDUCE: PREFETCHT2 → mnemonic (R8)")


def p_mnemonic_prefetchnta(p):
    """mnemonic : PREFETCHNTA"""
    # R9: mnemonic → PREFETCHNTA
    p[0] = p[1]
    if parser_debug:
        print(f"REDUCE: PREFETCHNTA → mnemonic (R9)")


def p_mnemonic_wbinvd(p):
    """mnemonic : WBINVD"""
    # R10: mnemonic → WBINVD
    p[0] = p[1]
    if parser_debug:
        print(f"REDUCE: WBINVD → mnemonic (R10)")


def p_mnemonic_invd(p):
    """mnemonic : INVD"""
    # R11: mnemonic → INVD
    p[0] = p[1]
    if parser_debug:
        print(f"REDUCE: INVD → mnemonic (R11)")


# ─────────────────────────────────────────────────────────────────
# Operand و Memory Address (2 قانون)
# ─────────────────────────────────────────────────────────────────

def p_operand(p):
    """operand : memory_address"""
    # R12: operand → memory_address
    p[0] = p[1]
    if parser_debug:
        print(f"REDUCE: memory_address → operand (R12)")


def p_memory_address(p):
    """memory_address : LBRACKET base_expr RBRACKET"""
    # R13: memory_address → [ base_expr ]
    p[0] = p[2]
    if parser_debug:
        print(f"REDUCE: [ base_expr ] → memory_address (R13)")


# ─────────────────────────────────────────────────────────────────
# Base Expression (3 قانون)
# ─────────────────────────────────────────────────────────────────

def p_base_expr_register_offset(p):
    """base_expr : REGISTER offset"""
    # R14: base_expr → REGISTER offset
    p[0] = MemoryOperand(Register(p[1]), p[2])
    if parser_debug:
        print(f"REDUCE: REGISTER offset → base_expr (R14)")


def p_base_expr_register(p):
    """base_expr : REGISTER"""
    # R15: base_expr → REGISTER
    p[0] = MemoryOperand(Register(p[1]))
    if parser_debug:
        print(f"REDUCE: REGISTER → base_expr (R15)")


def p_base_expr_identifier(p):
    """base_expr : IDENTIFIER"""
    # R16: base_expr → IDENTIFIER
    p[0] = MemoryOperand(Identifier(p[1]))
    if parser_debug:
        print(f"REDUCE: IDENTIFIER → base_expr (R16)")


# ─────────────────────────────────────────────────────────────────
# Offset (2 قانون)
# ─────────────────────────────────────────────────────────────────

def p_offset_plus(p):
    """offset : PLUS NUMBER"""
    # R17: offset → + NUMBER
    p[0] = +p[2]
    if parser_debug:
        print(f"REDUCE: + NUMBER → offset (R17)")


def p_offset_minus(p):
    """offset : MINUS NUMBER"""
    # R18: offset → - NUMBER
    p[0] = -p[2]
    if parser_debug:
        print(f"REDUCE: - NUMBER → offset (R18)")


# ─────────────────────────────────────────────────────────────────
# Error Handling
# ─────────────────────────────────────────────────────────────────

def p_error(p):
    if p:
        error_msg = f"❌ SYNTAX ERROR at '{p.value}' (type: {p.type}, line: {p.lineno})"
        error_msg += "\n\n💡 راهنما:"
        error_msg += "\n  • دستورات معتبر: CLFLUSH، CLFLUSHOPT، CLWB، PREFETCH*، WBINVD، INVD"
        error_msg += "\n  • فرمت: MNEMONIC [REGISTER] یا MNEMONIC [REGISTER±NUMBER]"
        error_msg += "\n  • یا: MNEMONIC [IDENTIFIER]"
        error_msg += "\n  • WBINVD و INVD بدون operand"
        print(error_msg)

        # پیام خطای خاص‌تر
        if p.type == 'REGISTER':
            print("\n⚠️  رجیستر بدون '[' و ']'؟")
        elif p.type == 'NUMBER':
            print("\n⚠️  عدد بدون '+' یا '-'؟")
        elif p.type in ['CLFLUSH', 'CLFLUSHOPT', 'CLWB', 'PREFETCHT0', 'PREFETCHT1', 'PREFETCHT2', 'PREFETCHNTA']:
            print(f"\n⚠️  {p.type} نیاز به operand دارد: {p.type} [REGISTER]")
        else:
            print("\n⚠️  SYNTAX ERROR - فرمت دستور را بررسی کنید")
    else:
        print("❌ SYNTAX ERROR - پایان غیرمنتظره ورودی")


# ═══════════════════════════════════════════════════════════════════
#                   Parser Builder & Interface
# ═══════════════════════════════════════════════════════════════════

parser_debug = False


def build_parser(debug=False):
    """
    ساخت parser

    Args:
        debug: فعال‌سازی حالت debug

    Returns:
        parser object
    """
    global parser_debug
    parser_debug = debug
    return yacc.yacc(debug=debug, write_tables=False)


def parse_instruction(code, debug=False):
    """
    پارس یک دستور assembly

    Args:
        code: رشته دستور assembly
        debug: فعال‌سازی حالت debug

    Returns:
        AST node یا None در صورت خطا
    """
    lexer = build_lexer()
    parser = build_parser(debug=debug)

    try:
        result = parser.parse(code, lexer=lexer)
        return result
    except Exception as e:
        print(f"❌ خطا: {e}")
        return None


def parse_file(filename, debug=False):
    """
    پارس یک فایل assembly

    Args:
        filename: نام فایل
        debug: فعال‌سازی حالت debug

    Returns:
        tuple: (لیست AST های موفق، لیست خطاها)
    """
    lexer = build_lexer()
    parser = build_parser(debug=debug)

    results = []
    errors = []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # رد کردن خطوط خالی و کامنت
            if not line or line.startswith(';'):
                continue

            # حذف کامنت انتهای خط
            if ';' in line:
                line = line.split(';')[0].strip()

            try:
                ast = parser.parse(line, lexer=lexer)
                if ast:
                    results.append((line_num, line, ast))
            except Exception as e:
                errors.append((line_num, line, str(e)))

    except FileNotFoundError:
        print(f"❌ فایل '{filename}' یافت نشد!")
        return None

    return results, errors


def analyze_instruction(ast):
    """
    تحلیل یک دستور پارس شده

    Args:
        ast: Instruction object

    Returns:
        dict حاوی اطلاعات تحلیل
    """
    category = ast.get_instruction_category()

    category_desc = {
        'flush': 'Cache Flush - پاک‌سازی خط کش',
        'writeback': 'Cache Write-Back - نوشتن کش در حافظه',
        'prefetch': 'Cache Prefetch - پیش‌بارگذاری در کش',
        'invalidate': 'Cache Invalidate - نامعتبرسازی کش'
    }

    analysis = {
        'mnemonic': ast.mnemonic,
        'category': category,
        'description': category_desc.get(category, ''),
        'has_operand': ast.operand is not None,
    }

    if ast.operand:
        mem = ast.operand
        analysis['operand'] = {
            'base_type': mem.base.type,
            'base_value': str(mem.base),
            'has_offset': mem.offset is not None,
            'offset_value': mem.offset
        }

        if isinstance(mem.base, Register):
            analysis['operand']['register_width'] = mem.base.bit_width

    return analysis


def print_analysis(analysis):
    """چاپ تحلیل"""
    print("═" * 70)
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
            print(f"  Offset: {op['offset_value']:+d}")

    print("═" * 70)


# ═══════════════════════════════════════════════════════════════════
#                          Test Main
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 70)
    print(" " * 20 + "Cache Parser تست")
    print(" " * 15 + "تیم 15 - پروژه کامپایلر")
    print("═" * 70)

    test_cases = [
        ("CLFLUSH [EAX]", "رجیستر ساده"),
        ("CLFLUSHOPT [EBX+16]", "با offset مثبت"),
        ("PREFETCHT0 [ECX-8]", "با offset منفی"),
        ("WBINVD", "بدون operand"),
        ("CLWB [cache_line]", "با شناسه"),
        ("PREFETCHNTA [RAX+128]", "رجیستر 64-bit"),
        ("CLFLUSHOPT", "❌ خطا - بدون operand"),
    ]

    print(f"\n🧪 اجرای {len(test_cases)} تست:\n")

    success_count = 0
    error_count = 0

    for i, (code, description) in enumerate(test_cases, 1):
        print("─" * 70)
        print(f"تست {i}/{len(test_cases)}: {description}")
        print(f"دستور: {code}")
        print("─" * 70)

        ast = parse_instruction(code, debug=False)

        if ast:
            print("✅ پارس موفق!")
            print(f"AST: {ast}")

            print("\n🌳 Parse Tree (ساده - AST):")
            for line in ast.pretty_print():
                print(line)

            print("\n🌲 Parse Tree (کامل - گرامر 18 قانونی):")
            for line in ast.full_parse_tree():
                print(line)

            print("\n📐 مراحل اشتقاق:")
            for step in ast.derivation_steps():
                print(f"  {step}")

            print("\n📊 تحلیل:")
            analysis = analyze_instruction(ast)
            print_analysis(analysis)

            print("\n📄 JSON Output:")
            print(json.dumps(ast.to_dict(), indent=2, ensure_ascii=False))

            success_count += 1
        else:
            print("❌ پارس ناموفق!")
            error_count += 1

        print()

    print("═" * 70)
    print(f"نتیجه: {success_count} موفق، {error_count} ناموفق")
    print("═" * 70)
