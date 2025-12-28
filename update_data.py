#!/usr/bin/env python3
"""
Update MagentaA11y data by copying content.json from the submodule.
Run this script to update the accessibility data from the MagentaA11y project.

Prerequisites:
- MagentaA11y submodule must be initialized and built
- Run from repository root: python update_data.py
"""

import shutil
from pathlib import Path

def main():
    repo_root = Path(__file__).parent
    source_json = repo_root / "data" / "magentaA11y" / "src" / "shared" / "content.json"
    dest_json = repo_root / "data" / "content.json"
    
    if not source_json.exists():
        print("❌ Source file not found:", source_json)
        print("\nPlease initialize and build the submodule first:")
        print("  git submodule update --init --remote")
        print("  cd data/magentaA11y")
        print("  npm ci && npm run build")
        return 1
    
    print(f"📋 Copying content.json from submodule...")
    dest_json.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_json, dest_json)
    
    print("✅ Data update complete!")
    print(f"   Content file: {dest_json}")
    print(f"   File size: {dest_json.stat().st_size:,} bytes")
    return 0

if __name__ == "__main__":
    exit(main())
