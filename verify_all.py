# -*- coding: utf-8 -*-
"""
verify_all.py - Full verification script for Online Retail project.
Checks: encoding cleanliness, imports, predictions, Flask syntax, Streamlit syntax.
"""
import sys
import os
import subprocess

PASS = 0
FAIL = 0

def ok(msg):
    global PASS
    PASS += 1
    print("[PASS] " + msg)

def fail(msg):
    global FAIL
    FAIL += 1
    print("[FAIL] " + msg)

# ── 1. Check all source files are pure ASCII or UTF-8 safe for cp1252 print paths ──
files_to_check = [
    "train_models.py",
    "backend/app.py",
    "backend/ml_model.py",
    "backend/data_processor.py",
    "frontend/streamlit_app.py",
]

ALLOWED_NON_ASCII = {
    # Streamlit renders these in a browser, cp1252 stdout is never called with them
    "frontend/streamlit_app.py": True,
}

print("=" * 60)
print("  STEP 1: Encoding checks")
print("=" * 60)

for fpath in files_to_check:
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        # Check UTF-8 header
        if content.startswith("# -*- coding: utf-8 -*-"):
            ok("%s has UTF-8 coding header" % fpath)
        else:
            fail("%s missing UTF-8 coding header" % fpath)

        # For non-frontend files, no non-ASCII should appear in print() calls
        if fpath not in ALLOWED_NON_ASCII:
            lines_with_print_unicode = []
            for i, line in enumerate(content.splitlines(), 1):
                if "print(" in line:
                    bad_chars = [c for c in line if ord(c) > 127]
                    if bad_chars:
                        lines_with_print_unicode.append((i, bad_chars))
            if lines_with_print_unicode:
                fail("%s has non-ASCII in print() at lines: %s" % (
                    fpath, [l for l, _ in lines_with_print_unicode]))
            else:
                ok("%s print() calls are ASCII-safe" % fpath)
    except UnicodeDecodeError as e:
        fail("%s is not valid UTF-8: %s" % (fpath, e))
    except FileNotFoundError:
        fail("%s not found" % fpath)

# ── 2. Import checks ──────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 2: Import + prediction checks")
print("=" * 60)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

try:
    from data_processor import load_data, clean_data, engineer_features
    ok("data_processor imports OK")
except Exception as e:
    fail("data_processor import: " + str(e))

try:
    from ml_model import predict_revenue, predict_segment, get_feature_importance
    ok("ml_model imports OK")
except Exception as e:
    fail("ml_model import: " + str(e))

try:
    rev = predict_revenue(30, 8, 200, 120, 25)
    ok("predict_revenue = %.2f" % rev)
except Exception as e:
    fail("predict_revenue: " + str(e))

try:
    seg, conf = predict_segment(30, 8, 200, 120, 25)
    ok("predict_segment = %s (%.1f%%)" % (seg, conf))
except Exception as e:
    fail("predict_segment: " + str(e))

try:
    fi = get_feature_importance()
    ok("feature_importance = %s" % str(list(fi.keys())[:3]))
except Exception as e:
    fail("feature_importance: " + str(e))

# ── 3. Python syntax check all files ─────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 3: Python syntax check (py_compile)")
print("=" * 60)

import py_compile

for fpath in files_to_check:
    try:
        py_compile.compile(fpath, doraise=True)
        ok("%s syntax OK" % fpath)
    except py_compile.PyCompileError as e:
        fail("%s syntax ERROR: %s" % (fpath, e))

# ── 4. Final summary ──────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  RESULTS: %d passed, %d failed" % (PASS, FAIL))
print("=" * 60)
if FAIL == 0:
    print("[ALL CLEAR] No errors found. Project is ready to run.")
    print("\n  python train_models.py")
    print("  python backend/app.py")
    print("  streamlit run frontend/streamlit_app.py")
else:
    print("[ACTION NEEDED] Fix the %d failed checks above." % FAIL)

sys.exit(0 if FAIL == 0 else 1)
