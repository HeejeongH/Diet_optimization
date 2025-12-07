#!/usr/bin/env python3
"""
METOR Project - Master Visualization Script
============================================

This script generates ALL figures for the METOR paper.

Usage:
    python src/visualization/generate_all_figures.py

Output:
    - results/figures/figure1-8.png/pdf  (Main figures)
    - results/figures/table1.png/pdf     (Performance table)
    - results/figures/4d_visualization/  (Alternative 4D methods)
    - results/figures/metric_examples/   (Metric explanations)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import subprocess
import time

def run_script(script_path, description):
    """Run a visualization script and report status."""
    print(f"\n{'='*60}")
    print(f"🎨 {description}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ['python', script_path],
            cwd=os.path.dirname(os.path.dirname(script_path)) or '.',
            capture_output=True,
            text=True,
            timeout=300
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Success ({elapsed:.1f}s)")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Failed ({elapsed:.1f}s)")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  Timeout after 300s")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Generate all figures for the METOR paper."""
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  METOR Project - Figure Generation Pipeline              ║
    ║  Multi-objective Enhanced Tool for Optimal meal Rec.     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    scripts = [
        ('src/visualization/generate_figures.py', 
         'Main Figures (Figure 1-8, Table 1)'),
        
        ('src/visualization/visualize_4d_alternatives.py',
         '4D Visualization Alternatives'),
        
        ('src/visualization/visualize_metric_comparison.py',
         'Performance Metrics Comparison'),
    ]
    
    results = []
    total_start = time.time()
    
    for script_path, description in scripts:
        if os.path.exists(script_path):
            success = run_script(script_path, description)
            results.append((description, success))
        else:
            print(f"\n⚠️  Script not found: {script_path}")
            results.append((description, False))
    
    total_elapsed = time.time() - total_start
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 GENERATION SUMMARY")
    print(f"{'='*60}")
    
    for desc, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {desc}")
    
    success_count = sum(1 for _, s in results if s)
    total_count = len(results)
    
    print(f"\n✨ Completed: {success_count}/{total_count} ({total_elapsed:.1f}s)")
    print(f"📁 Output directory: results/figures/")
    
    if success_count == total_count:
        print("\n🎉 All figures generated successfully!")
        return 0
    else:
        print("\n⚠️  Some figures failed to generate.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
