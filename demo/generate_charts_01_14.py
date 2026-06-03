"""
Generate result charts 01–14 for the DR Diagnosis Dashboard.
All data from data.js constants. Output: demo/public/results/
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'public', 'results')
os.makedirs(OUT, exist_ok=True)
DPI = 200

# ─── Color Palette (from data.js C) ───
BLUE = '#378ADD'
TEAL = '#1D9E75'
CORAL = '#D85A30'
PURPLE = '#7F77DD'
AMBER = '#EF9F27'
GRAY = '#888780'
GREEN = '#639922'
RED = '#E24B4A'

# ─── Data (from data.js) ───
CONFIGS = {
    'A': {'f1': 0.724, 'f1s': 0.011, 'auc': 0.830, 'aucs': 0.014, 'k': 0.618, 'ks': 0.035, 'acc': 0.717,
          'lbl': 'A: Baseline + ResNet-50'},
    'B': {'f1': 0.776, 'f1s': 0.009, 'auc': 0.863, 'aucs': 0.011, 'k': 0.698, 'ks': 0.026, 'acc': 0.768,
          'lbl': 'B: Pipeline + ResNet-50'},
    'C': {'f1': 0.727, 'f1s': 0.033, 'auc': 0.821, 'aucs': 0.019, 'k': 0.620, 'ks': 0.067, 'acc': 0.719,
          'lbl': 'C: Baseline + EfficientNet-B3'},
    'D': {'f1': 0.780, 'f1s': 0.022, 'auc': 0.865, 'aucs': 0.015, 'k': 0.700, 'ks': 0.030, 'acc': 0.770,
          'lbl': 'D: Pipeline + EfficientNet-B3'},
}

ABL = [
    {'n': 'Baseline', 'f1': 0.727, 'auc': 0.821},
    {'n': '+Canonical flip', 'f1': 0.738, 'auc': 0.830},
    {'n': '+OD-fovea rot.', 'f1': 0.748, 'auc': 0.840},
    {'n': '+Flat-field', 'f1': 0.758, 'auc': 0.848},
    {'n': '+CLAHE', 'f1': 0.772, 'auc': 0.858},
    {'n': '+Augmentation', 'f1': 0.778, 'auc': 0.863},
    {'n': 'Full pipeline', 'f1': 0.780, 'auc': 0.865},
]

ABL_INDIV = [
    {'stage': 'Stage 0: Canonical flip', 'f1': 0.8},
    {'stage': 'Stage 1: OD-fovea rot.', 'f1': 0.7},
    {'stage': 'Stage 4: Flat-field', 'f1': 1.0},
    {'stage': 'Stage 5: CLAHE', 'f1': 1.4},
    {'stage': 'Stage 6: Augmentation', 'f1': 0.6},
]

ALO = [
    {'l': 'Microaneurysms', 'ab': 0.28, 'ap': 0.45},
    {'l': 'Hemorrhages', 'ab': 0.42, 'ap': 0.62},
    {'l': 'Hard exudates', 'ab': 0.55, 'ap': 0.72},
    {'l': 'Soft exudates', 'ab': 0.38, 'ap': 0.56},
]

IOU = [
    {'l': 'Microaneurysms', 'b': 0.12, 'p': 0.22},
    {'l': 'Hemorrhages', 'b': 0.20, 'p': 0.35},
    {'l': 'Hard exudates', 'b': 0.28, 'p': 0.42},
    {'l': 'Soft exudates', 'b': 0.18, 'p': 0.32},
]

GEN = [
    {'d': 'EyePACS (train)', 'fb': 0.727, 'fp': 0.780},
    {'d': 'APTOS 2019', 'fb': 0.596, 'fp': 0.694},
    {'d': 'IDRiD', 'fb': 0.608, 'fp': 0.690},
    {'d': 'Messidor-2', 'fb': 0.625, 'fp': 0.700},
]
GEN_AUC = [
    {'d': 'EyePACS (train)', 'b': 0.821, 'p': 0.865},
    {'d': 'APTOS 2019', 'b': 0.792, 'p': 0.842},
    {'d': 'IDRiD', 'b': 0.780, 'p': 0.830},
    {'d': 'Messidor-2', 'b': 0.790, 'p': 0.840},
]

G_RATIO = [
    {'d': 'APTOS 2019', 'Gb': 0.82, 'Gp': 0.89},
    {'d': 'IDRiD', 'Gb': 0.84, 'Gp': 0.88},
    {'d': 'Messidor-2', 'Gb': 0.86, 'Gp': 0.90},
]

DEV = [
    {'c': 'Canon CR-1\n(EyePACS)', 'fb': 0.727, 'fp': 0.780},
    {'c': 'Topcon\n(Messidor-2)', 'fb': 0.640, 'fp': 0.700},
    {'c': 'Kowa\n(IDRiD)', 'fb': 0.620, 'fp': 0.690},
    {'c': 'Canon+Topcon\n(DDR)', 'fb': 0.590, 'fp': 0.670},
    {'c': 'Canon+Zeiss\n(ODIR-5K)', 'fb': 0.560, 'fp': 0.650},
    {'c': 'Topcon+Kowa\n(RFMiD)', 'fb': 0.550, 'fp': 0.640},
]

CLIN = [
    {'m': 'Sensitivity', 'b': 0.82, 'v': 0.90},
    {'m': 'Specificity', 'b': 0.88, 'v': 0.91},
    {'m': 'PPV', 'b': 0.76, 'v': 0.82},
    {'m': 'NPV', 'b': 0.92, 'v': 0.96},
]

CLAHE1 = [[.32,.35,.37,.36,.34],[.36,.39,.41,.40,.38],[.38,.42,.44,.43,.41],[.40,.44,.47,.46,.43],[.39,.43,.45,.44,.42],[.37,.41,.43,.42,.40],[.35,.38,.40,.39,.37]]
CLAHE2 = [[.48,.51,.53,.52,.50],[.52,.55,.58,.57,.54],[.54,.58,.62,.61,.57],[.53,.57,.60,.59,.56],[.51,.55,.57,.56,.54],[.49,.53,.55,.54,.52],[.47,.50,.52,.51,.49]]


def setup_style():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Helvetica', 'Arial'],
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': False,
        'figure.facecolor': 'white',
    })

setup_style()


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  [OK] {name}")


# ─── Chart 01 ───
def chart_01():
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = ['A', 'B', 'C', 'D']
    vals = [CONFIGS[k]['f1'] for k in labels]
    errs = [CONFIGS[k]['f1s'] for k in labels]
    colors = [GRAY, BLUE, GRAY, TEAL]
    x = np.arange(len(labels))
    bars = ax.bar(x, vals, yerr=errs, capsize=4, color=colors, width=0.6, edgecolor='white', linewidth=0.5)
    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + errs[i] + 0.005,
                f'{vals[i]:.3f}\n({CONFIGS[labels[i]]["f1s"]:.3f})',
                ha='center', va='bottom', fontsize=9)
    # Threshold lines: +5pp above each baseline
    ax.axhline(y=CONFIGS['A']['f1'] + 0.05, color=RED, linestyle='--', linewidth=1, alpha=0.7)
    ax.text(3.45, CONFIGS['A']['f1'] + 0.05 + 0.003, 'EH-3: +5pp (ResNet)', fontsize=7, color=RED, ha='right')
    ax.axhline(y=CONFIGS['C']['f1'] + 0.05, color=RED, linestyle='--', linewidth=1, alpha=0.5)
    ax.text(3.45, CONFIGS['C']['f1'] + 0.05 + 0.003, 'EH-3: +5pp (EffNet)', fontsize=7, color=RED, ha='right')
    ax.set_xticks(x)
    ax.set_xticklabels([CONFIGS[k]['lbl'] for k in labels], fontsize=8, rotation=15, ha='right')
    ax.set_ylabel('Weighted F1-Score', fontsize=11)
    ax.set_ylim(0.65, 0.85)
    ax.set_title('Experiment 1: 2x2 Factorial Design -- Weighted F1', fontsize=13, fontweight='bold')
    legend_patches = [
        mpatches.Patch(color=GRAY, label='Baseline (3ch)'),
        mpatches.Patch(color=BLUE, label='Pipeline + ResNet-50'),
        mpatches.Patch(color=TEAL, label='Pipeline + EfficientNet-B3'),
    ]
    ax.legend(handles=legend_patches, fontsize=8, loc='upper left')
    save(fig, '01_exp1_factorial_f1.png')


# ─── Chart 02 ───
def chart_02():
    metrics = [('Weighted F1', 'f1', 'f1s'), ('ROC-AUC', 'auc', 'aucs'),
               ("Cohen's kappa", 'k', 'ks'), ('Accuracy', 'acc', None)]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4.5))
    fig.suptitle('Experiment 1 -- All Primary Metrics by Configuration', fontsize=14, fontweight='bold')
    labels = ['A', 'B', 'C', 'D']
    colors = [GRAY, BLUE, GRAY, TEAL]
    for idx, (title, key, std_key) in enumerate(metrics):
        ax = axes[idx]
        vals = [CONFIGS[k][key] for k in labels]
        errs = [CONFIGS[k][std_key] for k in labels] if std_key else [0]*4
        x = np.arange(4)
        bars = ax.bar(x, vals, yerr=errs if std_key else None, capsize=3, color=colors, width=0.6, edgecolor='white')
        for i, bar in enumerate(bars):
            yoff = errs[i] + 0.005 if std_key else 0.005
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + yoff,
                    f'{vals[i]:.3f}', ha='center', va='bottom', fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_title(title, fontsize=11)
        ax.set_ylim(0.55, 0.95)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    save(fig, '02_exp1_all_metrics.png')


# ─── Chart 03 ───
def chart_03():
    fig, ax = plt.subplots(figsize=(8, 5))
    metrics = ['dF1', 'dAUC', 'dk']
    metric_labels = ['$\\Delta$F1 (pp)', '$\\Delta$AUC (pp)', '$\\Delta\\kappa$ (pp)']
    resnet = [5.2, 3.3, 8.0]
    effnet = [5.3, 4.4, 8.0]
    thresholds = [5.0, 2.0, 0.0]
    x = np.arange(len(metrics))
    w = 0.3
    b1 = ax.bar(x - w/2, resnet, w, color=BLUE, label='ResNet-50 (B-A)', edgecolor='white')
    b2 = ax.bar(x + w/2, effnet, w, color=TEAL, label='EfficientNet-B3 (D-C)', edgecolor='white')
    for i, (bar, val) in enumerate(zip(b1, resnet)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'+{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLUE)
    for i, (bar, val) in enumerate(zip(b2, effnet)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'+{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=TEAL)
    # Threshold lines
    for i, t in enumerate(thresholds):
        xmin = (x[i] - 0.4) / (len(x) - 1 + 0.8) + 0.4/(len(x)-1+0.8) if len(x) > 1 else 0.1
    ax.axhline(y=5.0, color=RED, linestyle='--', linewidth=1, alpha=0.7)
    ax.text(2.55, 5.15, 'EH-3: 5pp ($\\Delta$F1)', fontsize=7, color=RED)
    ax.axhline(y=2.0, color=RED, linestyle='--', linewidth=1, alpha=0.5)
    ax.text(2.55, 2.15, 'EH-3: 2pp ($\\Delta$AUC)', fontsize=7, color=RED)
    ax.axhline(y=0.0, color=RED, linestyle='--', linewidth=1, alpha=0.3)
    ax.text(2.55, 0.15, 'EH-3: 0pp ($\\Delta\\kappa$)', fontsize=7, color=RED)
    ax.set_xticks(x)
    ax.set_xticklabels(metric_labels, fontsize=11)
    ax.set_ylabel('Improvement (percentage points)', fontsize=11)
    ax.set_ylim(-0.5, 10.5)
    ax.set_title('Preprocessing Effect: $\\Delta$ (Pipeline - Baseline)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    save(fig, '03_exp1_delta.png')


# ─── Chart 04 ───
def chart_04():
    fig, ax = plt.subplots(figsize=(10, 5))
    names = [a['n'] for a in ABL]
    vals = [a['f1'] for a in ABL]
    n = len(vals)
    colors_list = [GRAY] + [BLUE]*(n-2) + [TEAL]
    x = np.arange(n)
    bars = ax.bar(x, vals, color=colors_list, width=0.65, edgecolor='white')
    # Marginal deltas
    for i in range(1, n):
        delta = (vals[i] - vals[i-1]) * 100
        ax.annotate(f'+{delta:.1f}pp', xy=(i, vals[i] + 0.003),
                    fontsize=8, ha='center', va='bottom', color=CORAL, fontweight='bold')
    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.012,
                f'{vals[i]:.3f}', ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=8, rotation=25, ha='right')
    ax.set_ylabel('Weighted F1-Score', fontsize=11)
    ax.set_ylim(0.70, 0.82)
    ax.set_title('Experiment 2: Cumulative Ablation -- Pipeline Stages', fontsize=13, fontweight='bold')
    save(fig, '04_exp2_ablation.png')


# ─── Chart 05 ───
def chart_05():
    fig, ax = plt.subplots(figsize=(8, 5))
    stages = [a['stage'] for a in ABL_INDIV]
    vals = [a['f1'] for a in ABL_INDIV]
    # Sort by value
    sorted_pairs = sorted(zip(vals, stages), reverse=True)
    vals_s = [v for v, _ in sorted_pairs]
    stages_s = [s for _, s in sorted_pairs]
    colors_list = []
    for v in vals_s:
        if v >= 1.4:
            colors_list.append(TEAL)
        elif v >= 0.8:
            colors_list.append(BLUE)
        else:
            colors_list.append(GRAY)
    y = np.arange(len(stages_s))
    bars = ax.barh(y, vals_s, color=colors_list, height=0.6, edgecolor='white')
    for i, bar in enumerate(bars):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f'+{vals_s[i]:.1f}pp', ha='left', va='center', fontsize=10, fontweight='bold')
    ax.set_yticks(y)
    ax.set_yticklabels(stages_s, fontsize=9)
    ax.set_xlabel('Marginal $\\Delta$F1 (pp)', fontsize=11)
    ax.set_title('Per-Stage Marginal Contribution to F1', fontsize=13, fontweight='bold')
    ax.invert_yaxis()
    save(fig, '05_exp2_per_stage.png')


# ─── Chart 06 ───
def chart_06():
    fig, ax = plt.subplots(figsize=(9, 5))
    lesions = [a['l'] for a in ALO]
    base = [a['ab'] for a in ALO]
    pipe = [a['ap'] for a in ALO]
    pct_improve = ['+61%', '+48%', '+31%', '+47%']
    x = np.arange(len(lesions))
    w = 0.3
    b1 = ax.bar(x - w/2, base, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax.bar(x + w/2, pipe, w, color=TEAL, label='Pipeline', edgecolor='white')
    for i, bar in enumerate(b2):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015,
                pct_improve[i], ha='center', va='bottom', fontsize=9, fontweight='bold', color=CORAL)
    for bars, vals in [(b1, base), (b2, pipe)]:
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(lesions, fontsize=10)
    ax.set_ylabel('ALO Score', fontsize=11)
    ax.set_ylim(0, 0.9)
    ax.set_title('Attention-Lesion Overlap (ALO) by Lesion Type', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    save(fig, '06_exp4_alo.png')


# ─── Chart 07 ───
def chart_07():
    fig, ax = plt.subplots(figsize=(9, 5))
    lesions = [a['l'] for a in IOU]
    base = [a['b'] for a in IOU]
    pipe = [a['p'] for a in IOU]
    pct_improve = ['+83%', '+75%', '+50%', '+78%']
    x = np.arange(len(lesions))
    w = 0.3
    b1 = ax.bar(x - w/2, base, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax.bar(x + w/2, pipe, w, color=PURPLE, label='Pipeline', edgecolor='white')
    for i, bar in enumerate(b2):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015,
                pct_improve[i], ha='center', va='bottom', fontsize=9, fontweight='bold', color=CORAL)
    for bars, vals in [(b1, base), (b2, pipe)]:
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(lesions, fontsize=10)
    ax.set_ylabel('IoU Score', fontsize=11)
    ax.set_ylim(0, 0.6)
    ax.set_title('IoU by Lesion Type', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    save(fig, '07_exp4_iou.png')


# ─── Chart 08 ───
def chart_08():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Cross-Dataset Generalization -- F1 and AUC', fontsize=14, fontweight='bold')
    datasets = [g['d'] for g in GEN]
    x = np.arange(len(datasets))
    w = 0.3
    # Left: F1
    fb = [g['fb'] for g in GEN]
    fp = [g['fp'] for g in GEN]
    b1 = ax1.bar(x - w/2, fb, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax1.bar(x + w/2, fp, w, color=TEAL, label='Pipeline', edgecolor='white')
    for bars, vals in [(b1, fb), (b2, fp)]:
        for bar, val in zip(bars, vals):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                     f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(datasets, fontsize=9, rotation=15, ha='right')
    ax1.set_ylabel('Weighted F1', fontsize=11)
    ax1.set_ylim(0.5, 0.85)
    ax1.set_title('Weighted F1', fontsize=11)
    ax1.legend(fontsize=8)
    # Right: AUC
    ab = [g['b'] for g in GEN_AUC]
    ap = [g['p'] for g in GEN_AUC]
    b1 = ax2.bar(x - w/2, ab, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax2.bar(x + w/2, ap, w, color=TEAL, label='Pipeline', edgecolor='white')
    for bars, vals in [(b1, ab), (b2, ap)]:
        for bar, val in zip(bars, vals):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                     f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(datasets, fontsize=9, rotation=15, ha='right')
    ax2.set_ylabel('ROC-AUC', fontsize=11)
    ax2.set_ylim(0.7, 0.92)
    ax2.set_title('ROC-AUC', fontsize=11)
    ax2.legend(fontsize=8)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    save(fig, '08_exp5_generalization.png')


# ─── Chart 09 ───
def chart_09():
    fig, ax = plt.subplots(figsize=(9, 5))
    datasets = [g['d'] for g in G_RATIO]
    gb = [g['Gb'] for g in G_RATIO]
    gp = [g['Gp'] for g in G_RATIO]
    x = np.arange(len(datasets))
    w = 0.3
    b1 = ax.bar(x - w/2, gb, w, color=GRAY, label='Baseline G', edgecolor='white')
    b2 = ax.bar(x + w/2, gp, w, color=TEAL, label='Pipeline G', edgecolor='white')
    for bar, val in zip(b1, gb):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    for bar, val in zip(b2, gp):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.axhline(y=0.85, color=RED, linestyle='--', linewidth=1.5)
    ax.text(2.45, 0.853, 'H-4 threshold: G = 0.85', fontsize=8, color=RED, ha='right')
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, fontsize=10)
    ax.set_ylabel('Generalization Ratio G', fontsize=11)
    ax.set_ylim(0.75, 0.95)
    ax.set_title('Generalization Ratio G = F1_external / F1_EyePACS', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    save(fig, '09_exp5_G_ratio.png')


# ─── Chart 10 ───
def chart_10():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    cameras = [d['c'] for d in DEV]
    fb = [d['fb'] for d in DEV]
    fp = [d['fp'] for d in DEV]
    x = np.arange(len(cameras))
    w = 0.3
    b1 = ax.bar(x - w/2, fb, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax.bar(x + w/2, fp, w, color=CORAL, label='Pipeline', edgecolor='white')
    for bars, vals in [(b1, fb), (b2, fp)]:
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(cameras, fontsize=8)
    ax.set_ylabel('Weighted F1', fontsize=11)
    ax.set_ylim(0.45, 0.85)
    ax.set_title('Cross-Device Performance (H-6)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    # Variance inset
    textstr = ('Cross-device variance:\n'
               'Baseline: $\\sigma^2$ = 0.0052\n'
               'Pipeline: $\\sigma^2$ = 0.0028\n'
               'Reduction: -46%')
    props = dict(boxstyle='round,pad=0.5', facecolor='#E1F5EE', alpha=0.9, edgecolor=TEAL)
    ax.text(0.98, 0.55, textstr, transform=ax.transAxes, fontsize=9, verticalalignment='top',
            horizontalalignment='right', bbox=props)
    save(fig, '10_exp6_device_shift.png')


# ─── Chart 11 ───
def chart_11():
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    categories = ['Weighted F1', 'ROC-AUC', "Cohen's $\\kappa$", 'Generalization\n(G ratio)', 'ALO', 'Device\nRobustness']
    N = len(categories)
    # Normalize each to [0, 1] range for radar
    baseline_raw = [0.727, 0.821, 0.620, 0.84, 0.41, 0.60]  # approximate means
    pipeline_raw = [0.780, 0.865, 0.700, 0.89, 0.59, 0.73]
    # Scale to 0-1 for display (min-max per axis)
    mins = [0.5, 0.7, 0.4, 0.7, 0.2, 0.4]
    maxs = [0.9, 0.95, 0.8, 1.0, 0.8, 0.9]
    baseline = [(v - mi) / (ma - mi) for v, mi, ma in zip(baseline_raw, mins, maxs)]
    pipeline = [(v - mi) / (ma - mi) for v, mi, ma in zip(pipeline_raw, mins, maxs)]
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    baseline += baseline[:1]
    pipeline += pipeline[:1]
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)
    plt.xticks(angles[:-1], categories, fontsize=9)
    ax.fill(angles, baseline, alpha=0.15, color=GRAY)
    ax.plot(angles, baseline, 'o-', color=GRAY, linewidth=1.5, markersize=5, label='Baseline')
    ax.fill(angles, pipeline, alpha=0.15, color=TEAL)
    ax.plot(angles, pipeline, 'o-', color=TEAL, linewidth=1.5, markersize=5, label='Pipeline')
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['', '', '', ''], fontsize=7)
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), fontsize=9)
    ax.set_title('Overall Performance: Baseline vs Full Pipeline', fontsize=13, fontweight='bold', y=1.08)
    save(fig, '11_summary_radar.png')


# ─── Chart 12 ───
def chart_12():
    fig, ax = plt.subplots(figsize=(8, 5))
    metrics = ['$\\Delta$F1 (pp)', '$\\Delta$AUC (pp)', '$\\Delta\\kappa$ (pp)']
    resnet = [5.2, 3.3, 8.0]
    effnet = [5.3, 4.4, 8.0]
    x = np.arange(len(metrics))
    w = 0.3
    b1 = ax.bar(x - w/2, resnet, w, color=BLUE, label='ResNet-50', edgecolor='white')
    b2 = ax.bar(x + w/2, effnet, w, color=TEAL, label='EfficientNet-B3', edgecolor='white')
    for bar, val in zip(b1, resnet):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'+{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLUE)
    for bar, val in zip(b2, effnet):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'+{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=TEAL)
    ax.axhline(y=5.0, color=RED, linestyle='--', linewidth=1.5)
    ax.text(2.55, 5.15, 'EH-3: 5pp ($\\Delta$F1)', fontsize=8, color=RED, ha='right')
    ax.axhline(y=2.0, color=RED, linestyle='--', linewidth=1)
    ax.text(2.55, 2.15, 'EH-3: 2pp ($\\Delta$AUC)', fontsize=8, color=RED, ha='right')
    ax.axhline(y=0.0, color=RED, linestyle='--', linewidth=0.8, alpha=0.5)
    ax.text(2.55, 0.15, 'EH-3: 0pp ($\\Delta\\kappa$)', fontsize=8, color=RED, ha='right')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11)
    ax.set_ylabel('Improvement (pp)', fontsize=11)
    ax.set_ylim(-0.5, 10.5)
    ax.set_title('EH-3 Dominance Criterion Check', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    # Green check annotations
    ax.text(0, -0.3, 'PASS', ha='center', fontsize=9, fontweight='bold', color=GREEN)
    ax.text(1, -0.3, 'PASS', ha='center', fontsize=9, fontweight='bold', color=GREEN)
    ax.text(2, -0.3, 'PASS', ha='center', fontsize=9, fontweight='bold', color=GREEN)
    save(fig, '12_eh3_dominance.png')


# ─── Chart 13 ───
def chart_13():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('CLAHE Parameter Sensitivity -- DR Grade 1 vs DR Grade 2', fontsize=14, fontweight='bold')
    cf_labels = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0']
    gt_labels = ['0.01', '0.02', '0.03', '0.04', '0.05']
    data1 = np.array(CLAHE1)
    data2 = np.array(CLAHE2)
    # DR Grade 1
    im1 = ax1.imshow(data1, cmap='YlOrRd', aspect='auto', vmin=0.30, vmax=0.48)
    ax1.set_xticks(range(5))
    ax1.set_xticklabels(gt_labels, fontsize=9)
    ax1.set_yticks(range(7))
    ax1.set_yticklabels(cf_labels, fontsize=9)
    ax1.set_xlabel('global_threshold', fontsize=10)
    ax1.set_ylabel('clip_factor', fontsize=10)
    ax1.set_title('DR Grade 1 (Mild)', fontsize=11)
    for i in range(7):
        for j in range(5):
            ax1.text(j, i, f'{data1[i,j]:.2f}', ha='center', va='center', fontsize=8,
                     color='white' if data1[i,j] > 0.43 else 'black')
    # Optimum star (clip_factor=2.5=row3, threshold=0.03=col2)
    ax1.plot(2, 3, marker='*', color='white', markersize=18, markeredgecolor='black', markeredgewidth=0.5)
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    # DR Grade 2
    im2 = ax2.imshow(data2, cmap='YlGnBu', aspect='auto', vmin=0.46, vmax=0.64)
    ax2.set_xticks(range(5))
    ax2.set_xticklabels(gt_labels, fontsize=9)
    ax2.set_yticks(range(7))
    ax2.set_yticklabels(cf_labels, fontsize=9)
    ax2.set_xlabel('global_threshold', fontsize=10)
    ax2.set_ylabel('clip_factor', fontsize=10)
    ax2.set_title('DR Grade 2 (Moderate)', fontsize=11)
    for i in range(7):
        for j in range(5):
            ax2.text(j, i, f'{data2[i,j]:.2f}', ha='center', va='center', fontsize=8,
                     color='white' if data2[i,j] > 0.58 else 'black')
    # Optimum star (clip_factor=2.0=row2, threshold=0.03=col2)
    ax2.plot(2, 2, marker='*', color='white', markersize=18, markeredgecolor='black', markeredgewidth=0.5)
    plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    save(fig, '13_exp2_clahe_sensitivity.png')


# ─── Chart 14 ───
def chart_14():
    fig, ax = plt.subplots(figsize=(9, 5))
    metrics = [c['m'] for c in CLIN]
    base = [c['b'] for c in CLIN]
    pipe = [c['v'] for c in CLIN]
    x = np.arange(len(metrics))
    w = 0.3
    b1 = ax.bar(x - w/2, base, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax.bar(x + w/2, pipe, w, color=TEAL, label='Pipeline', edgecolor='white')
    for bars, vals in [(b1, base), (b2, pipe)]:
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.axhline(y=0.80, color=RED, linestyle=':', linewidth=1.5)
    ax.text(3.45, 0.805, 'WHO screening: 0.80', fontsize=8, color=RED, ha='right')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11)
    ax.set_ylabel('Score', fontsize=11)
    ax.set_ylim(0.65, 1.02)
    ax.set_title('Clinical Screening Metrics -- Referable DR (Grade >= 2)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    save(fig, '14_clinical_metrics.png')


# ─── Main ───
if __name__ == '__main__':
    print("Generating charts 01-14...")
    chart_01()
    chart_02()
    chart_03()
    chart_04()
    chart_05()
    chart_06()
    chart_07()
    chart_08()
    chart_09()
    chart_10()
    chart_11()
    chart_12()
    chart_13()
    chart_14()
    print("[OK] Charts 01-14 complete!")
