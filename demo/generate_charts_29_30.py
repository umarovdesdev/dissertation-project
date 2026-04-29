"""
Generate result charts 29-30 for the DR Diagnosis Dashboard.
Reads metrics from JSON files in public/results/{exp3,exp7}/ and produces
matching PNG visualisations. Output: demo/public/results/{exp3,exp7}/
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'public', 'results')
DPI = 200

BLUE = '#378ADD'
TEAL = '#1D9E75'
CORAL = '#D85A30'
PURPLE = '#7F77DD'
AMBER = '#EF9F27'
GRAY = '#888780'
GREEN = '#639922'
RED = '#E24B4A'


def setup_style():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Helvetica', 'Arial'],
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': False,
        'figure.facecolor': 'white',
    })


def save(fig, subdir, name):
    out_dir = os.path.join(OUT, subdir)
    os.makedirs(out_dir, exist_ok=True)
    fig.savefig(os.path.join(out_dir, name), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  [OK] {subdir}/{name}")


def load_json(subdir, fname):
    with open(os.path.join(OUT, subdir, fname), 'r', encoding='utf-8') as f:
        return json.load(f)


# ─── Chart 29: Experiment 3 — APTOS 2019 cross-dataset transfer ───
def chart_29():
    data = load_json('exp3', 'exp3_aptos_transfer.json')
    R = data['results']
    keys = ['Config_A', 'Config_B', 'Config_C', 'Config_D']
    short = ['A', 'B', 'C', 'D']
    desc = {
        'A': 'Baseline\nResNet-50',
        'B': 'V5 Pipeline\nResNet-50',
        'C': 'Baseline\nEffNet-B3',
        'D': 'V5 Pipeline\nEffNet-B3',
    }
    colors = [GRAY, BLUE, GRAY, TEAL]

    eyepacs = [R[k]['eyepacs_f1'] for k in keys]
    aptos = [R[k]['aptos_f1'] for k in keys]
    aptos_std = [R[k]['aptos_f1_std'] for k in keys]
    G = [R[k]['G'] for k in keys]
    h4_ok = [R[k]['h4_satisfied'] for k in keys]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.2))
    fig.suptitle('Experiment 3 — APTOS 2019 Cross-Dataset Transfer (H-4)',
                 fontsize=14, fontweight='bold')

    # ── Left panel: F1 EyePACS vs APTOS, paired bars per config ──
    x = np.arange(len(short))
    w = 0.36
    b1 = ax1.bar(x - w/2, eyepacs, w, color=GRAY, label='EyePACS (train, in-domain)',
                 edgecolor='white')
    b2 = ax1.bar(x + w/2, aptos, w, yerr=aptos_std, capsize=4,
                 color=[colors[i] for i in range(len(short))],
                 label='APTOS 2019 (zero-shot)', edgecolor='white')
    for bar, val in zip(b1, eyepacs):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    for bar, val, sd in zip(b2, aptos, aptos_std):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + sd + 0.005,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    # Drop labels EyePACS → APTOS, placed below EyePACS bar tops
    for i in range(len(short)):
        drop = (aptos[i] - eyepacs[i]) * 100
        ax1.text(x[i] - w/2, eyepacs[i] - 0.025, f'{drop:+.1f}pp',
                 ha='center', va='top', fontsize=8, color=CORAL,
                 fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'{s}\n{desc[s]}' for s in short], fontsize=8.5)
    ax1.set_ylabel('Weighted F1', fontsize=11)
    ax1.set_ylim(0.5, 0.86)
    ax1.set_title('In-domain (EyePACS) vs Zero-shot (APTOS) F1', fontsize=11)
    legend_patches = [
        mpatches.Patch(color=GRAY, label='EyePACS / Baseline APTOS'),
        mpatches.Patch(color=BLUE, label='APTOS — V5+ResNet'),
        mpatches.Patch(color=TEAL, label='APTOS — V5+EffNet'),
    ]
    ax1.legend(handles=legend_patches, fontsize=8, loc='upper left')

    # ── Right panel: Generalization ratio G with H-4 threshold ──
    bars = ax2.bar(x, G, width=0.55, color=colors, edgecolor='white')
    for i, (bar, val) in enumerate(zip(bars, G)):
        mark = 'PASS' if h4_ok[i] else 'FAIL'
        mark_color = GREEN if h4_ok[i] else RED
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.004,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=10,
                 fontweight='bold')
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.018,
                 mark, ha='center', va='top', fontsize=10,
                 color='white', fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor=mark_color,
                           edgecolor='none', alpha=0.95))
    ax2.axhline(y=0.85, color=RED, linestyle='--', linewidth=1.5)
    ax2.text(3.4, 0.854, 'H-4 threshold: G >= 0.85',
             fontsize=8.5, color=RED, ha='right')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'{s}\n{desc[s]}' for s in short], fontsize=8.5)
    ax2.set_ylabel('Generalization Ratio  G = F1$_{APTOS}$ / F1$_{EyePACS}$',
                   fontsize=10.5)
    ax2.set_ylim(0.75, 0.94)
    ax2.set_title('Generalization Ratio G (H-4 criterion)', fontsize=11)

    # Stats inset
    st = data['statistical_tests']
    ci = st['bootstrap_delta_g_95ci']
    txt = (f"DeLong AUC (Config D):\n  p = {st['delong_auc_config_d']['p_value']:.3f} *\n"
           f"Bootstrap ΔG 95% CI:\n  [{ci[0]:.2f}, {ci[1]:.2f}]")
    props = dict(boxstyle='round,pad=0.45', facecolor='#E1F5EE',
                 alpha=0.9, edgecolor=TEAL)
    ax2.text(0.02, 0.98, txt, transform=ax2.transAxes, fontsize=8,
             verticalalignment='top', bbox=props)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    save(fig, 'exp3', '29_exp3_aptos_transfer.png')


# ─── Chart 30: Experiment 7 — small data clinical training ───
def chart_30():
    data = load_json('exp7', 'exp7_small_data.json')
    B = data['results']['baseline']
    P = data['results']['pipeline']
    imp = data['results']['improvement']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))
    fig.suptitle('Experiment 7 — Small-Data Clinical Training (IDRiD → Kazakh clinic)',
                 fontsize=14, fontweight='bold')

    # ── Left: F1 — IDRiD 5-fold CV and Clinical hold-out, baseline vs pipeline ──
    splits = ['IDRiD\n5-fold CV', 'Clinical\nhold-out (n=60)']
    base_f1 = [B['idrid_cv_f1'], B['clinical_test_f1']]
    base_std = [B['idrid_cv_f1_std'], B['clinical_test_f1_std']]
    pipe_f1 = [P['idrid_cv_f1'], P['clinical_test_f1']]
    pipe_std = [P['idrid_cv_f1_std'], P['clinical_test_f1_std']]
    deltas_pp = [imp['idrid_delta_f1_pp'], imp['clinical_delta_f1_pp']]

    x = np.arange(len(splits))
    w = 0.35
    b1 = ax1.bar(x - w/2, base_f1, w, yerr=base_std, capsize=4,
                 color=GRAY, label='Baseline (3ch)', edgecolor='white')
    b2 = ax1.bar(x + w/2, pipe_f1, w, yerr=pipe_std, capsize=4,
                 color=PURPLE, label='V5 Pipeline (4ch)', edgecolor='white')
    for bar, val, sd in zip(b1, base_f1, base_std):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + sd + 0.008,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=9)
    for bar, val, sd in zip(b2, pipe_f1, pipe_std):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + sd + 0.008,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=9)
    # Delta annotations centered between paired bars
    for i, d in enumerate(deltas_pp):
        ymax = max(base_f1[i] + base_std[i], pipe_f1[i] + pipe_std[i])
        ax1.annotate(f'+{d:.1f}pp', xy=(x[i], ymax + 0.05),
                     ha='center', fontsize=10, fontweight='bold', color=CORAL)
    ax1.set_xticks(x)
    ax1.set_xticklabels(splits, fontsize=10)
    ax1.set_ylabel('Weighted F1', fontsize=11)
    ax1.set_ylim(0.4, 0.78)
    ax1.set_title('Weighted F1 — IDRiD CV and Clinical hold-out', fontsize=11)
    ax1.legend(fontsize=9, loc='upper right')

    # ── Right: Clinical AUC + summary ──
    auc_b = B['clinical_test_auc']
    auc_b_sd = B['clinical_test_auc_std']
    auc_p = P['clinical_test_auc']
    auc_p_sd = P['clinical_test_auc_std']
    labels = ['Baseline (3ch)', 'V5 Pipeline (4ch)']
    vals = [auc_b, auc_p]
    stds = [auc_b_sd, auc_p_sd]
    colors2 = [GRAY, PURPLE]
    xb = np.arange(len(labels))
    bars = ax2.bar(xb, vals, yerr=stds, capsize=5, color=colors2,
                   width=0.5, edgecolor='white')
    for bar, val, sd in zip(bars, vals, stds):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + sd + 0.006,
                 f'{val:.3f} ± {sd:.3f}', ha='center', va='bottom',
                 fontsize=10, fontweight='bold')
    # Improvement arrow
    ax2.annotate('', xy=(1, auc_p - 0.005), xytext=(0, auc_b + 0.005),
                 arrowprops=dict(arrowstyle='->', color=CORAL, lw=2))
    ax2.text(0.5, (auc_b + auc_p) / 2 + 0.012,
             f"+{imp['clinical_delta_auc_pp']:.1f}pp",
             ha='center', fontsize=11, fontweight='bold', color=CORAL)
    ax2.set_xticks(xb)
    ax2.set_xticklabels(labels, fontsize=10)
    ax2.set_ylabel('ROC-AUC (Clinical hold-out)', fontsize=11)
    ax2.set_ylim(0.65, 0.88)
    ax2.set_title('Clinical ROC-AUC', fontsize=11)

    # Summary box
    summary = (f"Train: IDRiD ({data['training_dataset'].split('(')[1].rstrip(')')})\n"
               f"Test:  Clinical hold-out, n=60\n"
               f"CV: {data['cross_validation']}\n"
               f"Bootstrap resamples: {data['bootstrap_resamples']}")
    props = dict(boxstyle='round,pad=0.5', facecolor='#EFEDFA',
                 alpha=0.9, edgecolor=PURPLE)
    ax2.text(0.02, 0.98, summary, transform=ax2.transAxes, fontsize=8,
             verticalalignment='top', bbox=props)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    save(fig, 'exp7', '30_exp7_small_data.png')


if __name__ == '__main__':
    setup_style()
    print("Generating charts 29-30...")
    chart_29()
    chart_30()
    print("[OK] Charts 29-30 complete!")
