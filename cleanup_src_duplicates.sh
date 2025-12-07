#!/bin/bash

echo "🗑️  Removing duplicate visualization files from src/..."

# These files are duplicates - already in src/visualization/
rm -f src/generate_figures.py
rm -f src/visualize_4d_alternatives.py
rm -f src/additional_figures.py

# Also remove old backup if exists
rm -rf src/figures_backup

echo "✅ Cleanup complete!"
echo ""
echo "📁 Remaining files in src/:"
ls -1 src/*.py

echo ""
echo "✨ All visualization scripts are now only in: src/visualization/"
