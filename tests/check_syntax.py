#!/usr/bin/env python3
import sys
import ast

def check_syntax(filename):
    """Check if a Python file has valid syntax"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Try to parse the AST
        ast.parse(source)
        print(f"✅ {filename}: Syntax OK")
        return True
    except SyntaxError as e:
        print(f"❌ {filename}: Syntax Error at line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ {filename}: Error - {e}")
        return False

if __name__ == "__main__":
    files_to_check = [
        "src/main.py",
        "src/server.py", 
        "src/database.py"
    ]
    
    all_good = True
    for filename in files_to_check:
        if not check_syntax(filename):
            all_good = False
    
    if all_good:
        print("\n🎉 All Python files have valid syntax!")
        sys.exit(0)
    else:
        print("\n💥 Some files have syntax errors!")
        sys.exit(1)
