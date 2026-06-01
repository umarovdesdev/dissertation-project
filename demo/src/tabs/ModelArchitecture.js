import { C } from '../data';
import { Sec, DataTable, Note, DiagramViewer } from '../components';
import { useLang } from '../i18n';

export default function ModelArchitecture() {
  const { t } = useLang();
  return (
    <div>
      <Sec title={t('arch.title')}>
        <DiagramViewer
          src={process.env.PUBLIC_URL + '/diagrams/02_system_architecture.svg'}
          alt="DR Diagnosis System Architecture"
          caption="Full system architecture: fundus image input → 8-stage preprocessing pipeline → CNN backbone → 5-class DR grade output."
          tooltip="tooltip.arch_diagram"
        />
      </Sec>

      <Sec title={t('arch.equation')}>
        <div style={{ background: 'var(--color-background-secondary,#f7f7f5)', borderRadius: 8, padding: '14px 16px', fontFamily: 'monospace', fontSize: 13, lineHeight: 2 }}>
          <div><strong>Image-level:</strong> ŷ = f(CNN(P(I)))</div>
          <div><strong>Batch:</strong> ŷ<sub>i</sub> = f(CNN(P(I<sub>i</sub>))) for each image I<sub>i</sub> independently</div>
        </div>
        <Note>
          P(·) — 8-stage preprocessing pipeline. CNN — backbone (ResNet-50 or EfficientNet-B3).
          g — classification head (FC + softmax).
          The pipeline P is an integral component of the model, not a data preparation step.
        </Note>
      </Sec>

      <Sec title={t('arch.cnnSpecs')}>
        <DataTable
          headers={['Arm', 'Backbone', 'Parameters', 'Pretrain source', 'Input', 'Used in']}
          rows={[
            ['Baseline', 'ResNet-50', '25.6M', 'ImageNet (torchvision)', '3 ch, 512×512', 'Exp 1 (Config A)'],
            ['Baseline', 'EfficientNet-B3', '12.2M', 'ImageNet (timm)', '3 ch, 512×512', 'Exp 1 (Config C), Exp 4 (Grad-CAM/ALO)'],
            ['V5 (proposed)', 'ResNet-50 / EfficientNet-B3', '25.6M / 12.2M', 'Ophthalmology-specific SSL (in-house fundus pretrain)', '4 ch, 512×512 (RGB + FOV mask)', 'Exp 1 (Config B / D)'],
          ]}
        />
        <Note>
          Baseline arm: ImageNet-pretrained weights (cross-domain transfer from natural images).
          V5 arm: the same CNN backbones (ResNet-50 / EfficientNet-B3) initialized from ophthalmology-specific self-supervised pretraining — a CNN-compatible domain-adaptive SSL protocol (DINO / BYOL / SimCLR / MoCo family) pretrained on an unlabeled retinal fundus corpus, then fine-tuned for DR classification. This keeps the CNN architecture identical across arms, isolating the architecture factor.
          Per CFC-2.8, observed differences are attributable only to the integrated (preprocessing × pretrain) pair, not to either factor in isolation.
          All models trained with patient-level 5-fold cross-validation.
          Mixed precision disabled for EfficientNet models; batch size 16 (EfficientNet) / 32 (ResNet-50).
          Hardware: NVIDIA RTX 3060 12GB, WSL2 Ubuntu, PyTorch 2.5.
        </Note>
      </Sec>

      <Sec title={t('arch.operatingModes')}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {[
            { mode: 'Image-level', desc: 'Single fundus image → 5-class DR grade. Standard mode for Exp 1–3.', color: C.blue },
            { mode: 'Image-level (single-eye)', desc: 'Each fundus image classified independently. Standard mode for all Exp 1–7 configurations (A–D).', color: C.teal },
            { mode: 'Explainability', desc: 'EfficientNet-B3 + Grad-CAM overlay. ALO/IoU metrics computed against IDRiD lesion masks. Exp 4 only.', color: C.purple },
          ].map((m, i) => (
            <div key={i} style={{ display: 'flex', gap: 10, padding: '10px 12px', background: 'var(--color-background-secondary,#f7f7f5)', borderRadius: 7 }}>
              <div style={{ minWidth: 130, fontWeight: 600, fontSize: 12, color: m.color }}>{m.mode}</div>
              <div style={{ fontSize: 12, color: 'var(--color-text-primary,#333)', lineHeight: 1.5 }}>{m.desc}</div>
            </div>
          ))}
        </div>
      </Sec>
    </div>
  );
}
