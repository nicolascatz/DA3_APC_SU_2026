# CLAUDE.md

Guide for AI assistants working in this repository.

## Project overview

`DA3_APC_SU_2026` (author: Nicolas, v0.1.0) is a data-science project analysing **single-unit (SU) electrophysiology recordings** from rats (`RAT57-*`), exploring neuronal spiking responses to sensory stimuli (whisker/air-puff stimulation, left/right conditions, CS + PUFF combinations). The reference paper is `documents/CaronGuyon et al_CerebralCortex 2020.pdf`.

The repo is at an early stage: one exploratory notebook, a placeholder helper module, and the raw data. The README is minimal.

The user codes mainly in **Python**, is learning data-science techniques, and writes comments/notes in **French**. Prefer clear, didactic code and explanations; answer in the language the user uses.

## Repository structure

```
.
├── README.md                 # Title, author, version only
├── pyproject.toml            # Project metadata + dependencies (uv)
├── uv.lock                   # Locked dependencies (do not edit by hand)
├── .gitignore                # .venv/, __pycache__/, *.pyc, .ipynb_checkpoints/, Scripts_hidden/
├── data/                     # ~170 MATLAB .mat files, one per sorted unit
├── documents/                # Reference paper (PDF, ~13 MB)
├── functions/                # Reusable helper package (has __init__.py)
│   └── function_test.py      # mean(X), median(X) — pure-Python placeholders
└── Scripts/
    └── APC_SU_Open_and_start.ipynb   # Exploration notebook (raster plots)
```

`Scripts_hidden/` is git-ignored: use it for private/scratch scripts that must not be committed.

## Data

Files in `data/` are named `RAT57-<session>-01_unit_<channel><letter>.mat` (e.g. `RAT57-012-01_unit_11b.mat`): rat 57, recording session `<session>`, electrode/unit number, and a letter distinguishing multiple sorted units on the same channel (a, b, c).

Each `.mat` file is loaded with `scipy.io.loadmat` and contains (at least):

| Key | Meaning |
|---|---|
| `single_unit_aligned_sorted` | 2-D array `(n_trials, n_timepoints)`; binary spike raster at 1 ms resolution, trials sorted by condition. Stimulus onset is at **t = 200 ms** (column 200). |
| `list_trial_name` | Condition names, in the same order as the sorted trials. |
| `N_cond` | Row indices delimiting each condition: trials `N_cond[k]:N_cond[k+1]` belong to condition `list_trial_name[k]`. |

Conditions of interest (others can be dropped):
`GR_Left_CS_10`, `GR_Left_CS_10_PUFF_12`, `GR_Left_CS_10_PUFF_34`, `GR_Right_CS_10`, `GR_Right_CS_10_PUFF_12`, `GR_Right_CS_10_PUFF_34`, `PUFF_12`, `PUFF_34`.

Notes:
- `loadmat` returns nested arrays; `list_trial_name` entries and `N_cond` often need flattening (`data['N_cond'].tolist()[0]`) and string conversion before comparisons — check shapes/dtypes interactively.
- Treat `data/*.mat` as **read-only raw data**. Never modify or regenerate these files; write derived outputs elsewhere (e.g. a new `outputs/` folder) and don't commit large artefacts without asking.

## Development workflow

- **Python ≥ 3.12**, managed with [uv](https://docs.astral.sh/uv/).
  - Set up: `uv sync` (creates `.venv/` from `uv.lock`).
  - Add a dependency: `uv add <package>` (updates `pyproject.toml` and `uv.lock`).
  - Run: `uv run python <script>` or `uv run jupyter lab` / select the `.venv` kernel in the IDE.
- Declared dependencies: `ipykernel`, `numpy`, `pandas`, `scikit-learn`, `scipy`, `seaborn`, `statsmodels`.
  - **`matplotlib` is imported by the notebook but not declared** explicitly (it comes in transitively via `seaborn`). If you rely on it in new code, consider `uv add matplotlib`.
- No test suite, linter, formatter, or CI is configured. If you add tests, use `pytest` (`uv add --dev pytest`) and place them in a `tests/` folder.

### Notebook conventions

- The notebook lives in `Scripts/` but paths are relative to the repo root; the first cell does `os.chdir('..')` when the cwd ends with `Scripts`. Keep this pattern so `data/...` paths work whether it runs from the root or from `Scripts/`.
- Raster plots use `ax.spy(su[:, :700], markersize=0.5, aspect='auto', ...)` with a dashed vertical line at t = 200 (stimulus onset) and dashed horizontal lines at condition boundaries from `N_cond`.
- The notebook is large (~390 KB, embedded figure outputs). Prefer small, targeted edits; clear outputs before committing new notebooks if size grows (`jupyter nbconvert --clear-output`).
- Notebook comments and markdown are in French; keep that style.

## Code conventions

- Reusable logic goes in `functions/` (a package: `from functions.function_test import mean`); keep notebooks for exploration and plotting. Run notebooks/scripts from the repo root so the `functions` package is importable.
- Use descriptive names and docstrings for new functions; type hints welcome. The existing helpers are minimal pure-Python functions (no numpy) with no docstrings — match the surrounding style unless improving it is requested.
- Prefer vectorised numpy/pandas over Python loops for spike-train analysis (PSTH, firing rates, trial averaging).
- Use `pathlib`/relative paths from the repo root; never hard-code absolute paths.
- Label plots (title, axes with units — time in ms, trials) and keep the 200 ms stimulus-onset convention explicit.

## Git workflow

- Develop on the branch designated for the task (currently `claude/claude-md-documentation-encaok`); do not push elsewhere.
- Commit history so far uses short, informal messages; for new commits prefer clear, descriptive messages.
- Do not open pull requests unless explicitly asked.
- Do not commit `.venv/`, caches, or checkpoints (already git-ignored).

## Preferences when producing deliverables

- **PowerPoint (.ppt/.pptx)**: use the user's **AMU template**; if it isn't available, ask the user to provide it.
- **PPT/PPTX/PDF**: if the language (English or French) is not specified, ask which one to use.

## Things to be careful about

- Don't load all ~170 `.mat` files into memory at once without need; iterate and keep only extracted features (the notebook loops over a slice of `os.listdir('data')`, which is unordered — use `sorted(...)` for reproducibility).
- `uv.lock` is large and generated; never edit manually.
- The PDF in `documents/` is the scientific context; consult it for experimental design/terminology (conditions, stimulus timing) before making assumptions.
