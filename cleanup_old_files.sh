#!/bin/bash

echo "🗑️  Cleaning up old/duplicate files..."

# Remove old visualization scripts from wrong locations
rm -f visualize_metric_comparison.py
rm -f docs/paper/visualize_metrics.py

# Remove old figures directory (already moved to results/figures)
rm -rf src/figures

# Remove docs/paper/metric_examples (already moved)
rm -rf docs/paper/metric_examples

# Remove reorganization scripts
rm -f src/reorganize_figures.py
rm -f reorganize_project.py

echo "✅ Cleanup complete!"
