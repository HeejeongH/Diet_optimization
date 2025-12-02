# GitHub Repository Cleanup Plan

## 🗑️ Files to Remove

### 1. Setup/Config Files (Streamlit Cloud specific)
- `GITHUB_TOKEN_SETUP.md` - GitHub token setup guide (not needed in public repo)
- `STREAMLIT_CLOUD_SETUP.md` - Streamlit deployment guide (optional)
- `config/github_token.txt` - Sensitive file (should never be in repo)

### 2. Temporary/Test Files
- `data/File_A.xlsx` - Unclear purpose
- `data/File_B.xlsx` - Unclear purpose

### 3. DevContainer Files
- `.devcontainer/` - Development container config (optional, depends on usage)

## 📁 Directories to Organize

### Create New Structure:
```
diet_optimization/
├── src/                    # Core source code (keep as is)
├── data/                   # Data files (clean up)
│   └── sarang_DB/         # Main database (keep)
├── visualization/          # Visualization tools (keep)
│   ├── figures/           # Generated figures (keep)
│   └── generate_figures.py (keep)
├── docs/                   # Documentation (NEW)
│   └── paper/             # Paper-related files (NEW)
├── .gitignore             # Git ignore (update)
├── README.md              # Main documentation (keep)
└── requirements.txt       # Dependencies (keep)
```

## ✅ Actions

1. Remove sensitive/unnecessary files
2. Update .gitignore
3. Create better documentation structure
4. Keep only essential data files
5. Commit and push cleanup
