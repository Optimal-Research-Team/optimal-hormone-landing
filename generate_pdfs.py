#!/usr/bin/env python3
"""Generate Optimal Hormone PDF — landscape, one section per page."""

from playwright.sync_api import sync_playwright

BASE = "/Users/peterphua/Claude Code/optimal-hormone-landing"
IMG  = f"file://{BASE}/images"

# ─── Shared CSS tokens ───────────────────────────────────────────────────────
TOKENS = """
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=Inter:wght@300;400;500;600;700&display=swap');
  *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
  :root {
    --g900:#1a2e1a; --g800:#243524; --g700:#2d4a2d; --g600:#3d6b3d;
    --g500:#4a7c4a; --g400:#6b9e6b; --g100:#e8f0e8;
    --cream:#f7f3ed; --creamy:#efe9e0; --sage:#c5d5b5; --sagel:#dde8d3;
    --td:#1a2e1a; --tb:#3a4a3a; --tm:#6b7b6b; --bdr:#d4cdc2;
    --serif:'Cormorant Garamond',Georgia,serif;
    --sans:'Inter',-apple-system,sans-serif;
  }
  body { font-family:var(--sans); -webkit-print-color-adjust:exact; print-color-adjust:exact; }

  /* atoms */
  .lbl  { font-size:8.5px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; color:var(--g600); margin-bottom:8px; }
  .h1   { font-family:var(--serif); font-weight:600; line-height:1.12; color:var(--td); }
  .h1 em{ font-style:italic; color:var(--g600); }
  .sub  { font-size:10.5px; color:var(--tm); line-height:1.7; }
  .body-text { font-size:10.5px; color:var(--tb); line-height:1.78; }

  .green-bar { height:5px; background:linear-gradient(to right,var(--g700),var(--g400)); flex-shrink:0; }

  .callout { padding:14px 18px; background:var(--sagel); border:1.5px solid #b8ccaa; border-radius:10px; margin-top:12px; }
  .callout p { font-family:var(--serif); font-size:13px; color:var(--td); line-height:1.6; }
  .callout em { color:var(--g600); font-style:italic; font-weight:700; }

  .sx-card { background:var(--sagel); padding:10px 12px; border-radius:8px; }
  .sx-card h5 { font-family:var(--serif); font-size:11.5px; font-weight:600; color:var(--td); margin-bottom:2px; }
  .sx-card p  { font-size:8.5px; color:var(--tb); line-height:1.5; }

  .step-card { background:white; border:1px solid var(--bdr); border-radius:10px; padding:16px 18px; }
  .step-num  { width:28px;height:28px;border-radius:50%;background:var(--cream);border:1.5px solid var(--g400);
               display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:700;
               letter-spacing:.06em;color:var(--g600);margin-bottom:9px; }
  .step-tag  { font-size:7px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--g500);margin-bottom:2px; }
  .step-card h4 { font-family:var(--serif);font-size:13.5px;font-weight:600;color:var(--td);margin-bottom:4px;line-height:1.3; }
  .step-card p  { font-size:9px;color:var(--tm);line-height:1.55; }

  .inc-card { padding:14px 16px; border:1px solid var(--bdr); border-radius:10px; background:white; }
  .inc-card h5 { font-family:var(--serif);font-size:13px;font-weight:600;color:var(--td);margin-bottom:4px; }
  .inc-card p  { font-size:9px;color:var(--tm);line-height:1.55; }

  .check svg { width:12px;height:12px;stroke:var(--g600);fill:none;stroke-width:2.5;flex-shrink:0; }
  .check { display:flex;align-items:center;gap:7px;font-size:9px;color:var(--tb);padding:6px 10px;background:var(--cream);border-radius:6px; }

  .price-badge { display:inline-block;padding:4px 12px;border-radius:50px;background:var(--sagel);border:1px solid #b8ccaa;color:var(--g700);font-size:7.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase; }
  .vstack li { display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid var(--bdr);font-size:9px;color:var(--tb); }
  .vstack li:last-child { border-bottom:none; }
  .vstack .free { color:var(--g600);font-size:8px;font-weight:600; }
  .price-big { font-family:var(--serif);font-size:44px;font-weight:700;color:var(--g800);line-height:1;margin:10px 0 4px; }
  .price-big span { font-size:16px;font-weight:400;color:var(--tm); }
  .scarcity { padding:8px 14px;background:var(--sagel);border:1px solid #b8ccaa;border-radius:8px;font-size:9px;color:var(--g700);text-align:center;margin:10px 0; }
  .btn-green { display:block;width:100%;padding:12px;background:var(--g700);color:white;border-radius:50px;font-size:10.5px;font-weight:600;text-align:center;text-decoration:none;margin-top:8px; }
  .btn-white { display:inline-block;padding:12px 24px;background:white;color:var(--g800);border-radius:50px;font-size:10.5px;font-weight:700;text-decoration:none; }

  .benefit-card { background:var(--cream);border-radius:12px;padding:18px 16px; }
  .benefit-icon { width:38px;height:38px;border-radius:50%;background:var(--g100);display:flex;align-items:center;justify-content:center;margin-bottom:10px; }
  .benefit-icon svg { width:19px;height:19px;stroke:var(--g700);fill:none;stroke-width:1.5; }
  .benefit-card h4 { font-family:var(--serif);font-size:12.5px;font-weight:600;color:var(--td);margin-bottom:4px; }
  .benefit-card p  { font-size:8.5px;color:var(--tm);line-height:1.6; }

  /* comparison table */
  .ctbl { width:100%;border-collapse:separate;border-spacing:0;border-radius:12px;overflow:hidden;border:1px solid var(--bdr);font-size:9px; }
  .ctbl thead th { padding:11px 14px;text-align:left;font-size:8.5px;font-weight:600;background:var(--creamy);border-bottom:1px solid var(--bdr); }
  .ctbl thead th.hi { background:var(--g700);color:white; }
  .ctbl td { padding:9.5px 14px;border-bottom:1px solid var(--bdr);color:var(--tb);background:white;vertical-align:top; }
  .ctbl td:first-child { font-weight:500;color:var(--td);background:var(--cream);width:160px; }
  .ctbl td.hi { background:var(--g100); }
  .ctbl tr:last-child td { border-bottom:none; }
  .ck  { color:var(--g600);font-weight:700; }
  .cx  { color:#c0392b;font-weight:700; }
  .det { display:block;font-size:7.5px;color:var(--tm);margin-top:2px;font-weight:400; }

  /* hormone map */
  .hmap { background:#2d4a2d;border-radius:12px;padding:22px 28px;margin-top:14px;flex:1; }
  .hmap-row { display:flex;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.06); }
  .hmap-row:last-child { border-bottom:none; }
  .hmap-sx { flex:1;font-size:10.5px;color:#f0ece4; }
  .hmap-sx .sub-sx { font-size:8px;color:#b0c8b0;display:block;margin-top:1px; }
  .hmap-line { width:100px;display:flex;align-items:center;padding:0 10px; }
  .hmap-line-inner { flex:1;height:1.5px;border-radius:1px;opacity:.65; }
  .hmap-hormone { flex:1;text-align:right; }
  .hmap-hormone .name { font-size:10.5px;font-weight:600; }
  .hmap-hormone .desc { font-size:8px;color:#a0c0a8;display:block;margin-top:1px; }

  /* page shell */
  @page { size:A4 landscape; margin:0; }
  .page { width:297mm; height:210mm; page-break-after:always; position:relative; overflow:hidden; display:flex; flex-direction:column; }
  .page:last-child { page-break-after:avoid; }

  .two-col { display:flex; flex:1; overflow:hidden; }
  .lcol,.rcol { padding:32px 40px; display:flex; flex-direction:column; overflow:hidden; }
  .lcol { width:50%; }
  .rcol { width:50%; }
  .dvider { width:1px; background:var(--bdr); flex-shrink:0; }
  .full { padding:32px 50px; display:flex; flex-direction:column; flex:1; overflow:hidden; }

  .two-up   { display:grid; grid-template-columns:1fr 1fr; gap:11px; margin-top:11px; }
  .three-up { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-top:10px; }
  .sx-grid  { display:grid; grid-template-columns:1fr 1fr; gap:7px; margin-top:10px; }
  .steps-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:11px; margin-top:11px; flex:1; }
  .ben-grid   { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-top:10px; flex:1; }
  .four-up    { display:grid; grid-template-columns:repeat(4,1fr); gap:7px; margin-top:9px; }
"""

# ─── Full lander HTML ────────────────────────────────────────────────────────
FULL_HTML = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{TOKENS}
/* Cover */
.cover {{ background:var(--g800); flex-direction:row; }}
.cover-photo {{ position:absolute;right:0;top:0;bottom:0;width:48%; }}
.cover-photo img {{ width:100%;height:100%;object-fit:cover;object-position:center 15%;display:block; }}
.cover-photo::before {{ content:'';position:absolute;inset:0;background:linear-gradient(to right,var(--g800) 0%,transparent 60%);z-index:1; }}
.cover-inner {{ position:relative;z-index:2;padding:36px 52px;display:flex;flex-direction:column;justify-content:space-between;height:100%;max-width:57%; }}
.nav-logo {{ display:flex;align-items:center;gap:10px; }}
.nav-logo svg {{ width:24px;height:24px; }}
.nav-logo span {{ font-size:9.5px;color:rgba(255,255,255,.65);letter-spacing:.04em; }}
.pill {{ padding:4px 11px;border-radius:50px;font-size:8px;font-weight:600;letter-spacing:.06em;text-transform:uppercase; }}
.pill-a {{ background:rgba(255,255,255,.15);color:white;border:1px solid rgba(255,255,255,.3); }}
.pill-b {{ background:rgba(255,255,255,.1);color:rgba(255,255,255,.9);border:1px solid rgba(255,255,255,.2); }}
.cover-h1 {{ font-family:var(--serif);font-size:44px;font-weight:600;line-height:1.1;color:white;margin-bottom:14px; }}
.cover-h1 em {{ font-style:italic;color:#a8cfa8; }}
.cover-p {{ font-size:11.5px;color:rgba(255,255,255,.8);line-height:1.65;max-width:320px;margin-bottom:16px; }}
.gdot {{ width:7px;height:7px;border-radius:50%;background:#6bdb6b;flex-shrink:0; }}
.cover-proof {{ display:flex;align-items:center;gap:8px; }}
.cover-proof span {{ font-size:9px;color:rgba(255,255,255,.55); }}
.cover-foot {{ border-top:1px solid rgba(255,255,255,.1);padding-top:12px;display:flex;justify-content:space-between;align-items:center; }}
.cover-foot p {{ font-size:9px;color:rgba(255,255,255,.38); }}
.cover-foot .url {{ font-size:9px;color:rgba(255,255,255,.58);font-weight:500; }}
/* Pricing page */
.pricing-box {{ background:white;border:1px solid var(--bdr);border-radius:16px;padding:28px 32px;box-shadow:0 6px 28px rgba(0,0,0,.06); }}
/* CTA panel */
.cta-panel h2 {{ font-family:var(--serif);font-size:27px;font-weight:600;color:white;line-height:1.2;margin-bottom:12px; }}
.cta-panel h2 em {{ font-style:italic;color:#a8cfa8; }}
.cta-panel .sub {{ color:rgba(255,255,255,.72);margin-bottom:22px; }}
.contact {{ margin-top:16px;padding-top:14px;border-top:1px solid rgba(255,255,255,.12); }}
.contact p {{ font-size:9px;color:rgba(255,255,255,.48);margin-bottom:3px; }}
.contact strong {{ color:white;font-size:10.5px; }}
</style></head><body>

<!-- ══════════════════════════════════════════════════ -->
<!-- PAGE 1 — COVER                                     -->
<!-- ══════════════════════════════════════════════════ -->
<div class="page cover">
  <div class="cover-photo">
    <img src="{IMG}/woman-field.jpg" alt="">
  </div>
  <div class="cover-inner">
    <div class="nav-logo">
      <svg viewBox="0 0 28 28" fill="none">
        <circle cx="8" cy="8" r="4" fill="white"/>
        <circle cx="20" cy="8" r="4" fill="white"/>
        <circle cx="8" cy="20" r="4" fill="white"/>
        <circle cx="20" cy="20" r="4" fill="white" opacity="0.4"/>
      </svg>
      <span>Optimal Family Health &nbsp;·&nbsp; Enhanced Care</span>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:14px 0;">
      <div style="display:flex;gap:7px;margin-bottom:16px;">
        <span class="pill pill-a">Now Enrolling</span>
        <span class="pill pill-b">Barrie, Ontario</span>
      </div>
      <div class="cover-h1">Finally feel like <em>yourself</em> again.</div>
      <p class="cover-p">A 6-step clinical protocol for women in perimenopause and menopause — led by a dedicated Nurse Practitioner who will listen, test thoroughly, and build a plan that actually works.</p>
      <div class="cover-proof">
        <div class="gdot"></div>
        <span>No family doctor required &nbsp;·&nbsp; OHIP-covered bloodwork &nbsp;·&nbsp; Founding rate: $695 + HST</span>
      </div>
    </div>
    <div class="cover-foot">
      <p>Women's Hormone Optimization Protocol &nbsp;·&nbsp; 2026</p>
      <span class="url">beoptimal.ca &nbsp;·&nbsp; (437) 370-0291</span>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- PAGE 2 — THE CHALLENGE + SOUND FAMILIAR            -->
<!-- ══════════════════════════════════════════════════ -->
<div class="page" style="background:var(--cream);">
  <div class="green-bar"></div>
  <div class="two-col">
    <div class="lcol" style="background:var(--cream);">
      <div class="lbl">The Challenge</div>
      <div class="h1" style="font-size:25px;max-width:340px;">Your body is changing, but you can still <em>feel optimal.</em></div>
      <div style="flex:1;margin-top:14px;display:flex;flex-direction:column;justify-content:space-between;">
        <p class="body-text">Most family physicians have <strong>10 minutes per visit</strong> and received fewer than a handful of hours of menopause-specific training in medical school. It's not that they don't care — it's that the system wasn't built for this. We're here to fill that gap.</p>
        <div class="callout">
          <p><em>It doesn't have to be this way.</em> The right assessment, with a clinician who specializes in hormone health, can change the trajectory of this entire chapter of your life.</p>
        </div>
        <div style="padding:14px 18px;background:var(--sagel);border-radius:10px;border:1px solid #b8ccaa;">
          <p style="font-size:9px;color:var(--g700);margin-bottom:5px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;">Why the Optimal Protocol?</p>
          <p style="font-size:9.5px;color:var(--tb);line-height:1.65;">60-minute appointments &nbsp;·&nbsp; Same NP every visit &nbsp;·&nbsp; OHIP bloodwork &nbsp;·&nbsp; InBody scans &nbsp;·&nbsp; Structured 6-step protocol</p>
        </div>
      </div>
    </div>
    <div class="dvider"></div>
    <div class="rcol" style="background:var(--creamy);">
      <div class="lbl">Sound Familiar?</div>
      <div class="h1" style="font-size:22px;">You don't need a diagnosis <em>to start</em></div>
      <p class="sub" style="margin-top:7px;font-size:9.5px;">Many women aren't sure if what they're experiencing is perimenopause, menopause, or thyroid — that's exactly what the assessment is for.</p>
      <div class="sx-grid" style="flex:1;align-content:start;">
        <div class="sx-card"><h5>Brain fog &amp; fatigue</h5><p>Can't focus. Exhausted by 2pm no matter how much you slept.</p></div>
        <div class="sx-card"><h5>Hot flashes &amp; night sweats</h5><p>Disrupting your day and destroying your sleep.</p></div>
        <div class="sx-card"><h5>Mood changes &amp; anxiety</h5><p>Irritability or anxiety that came out of nowhere.</p></div>
        <div class="sx-card"><h5>Sleep disruption</h5><p>Falling asleep is fine. Staying asleep? That ended.</p></div>
        <div class="sx-card"><h5>Weight &amp; body changes</h5><p>Your metabolism shifted. Nothing is working the way it used to.</p></div>
        <div class="sx-card"><h5>Low libido &amp; dryness</h5><p>Changes you don't feel comfortable raising in 10 minutes.</p></div>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- PAGE 3 — HORMONE MAP                               -->
<!-- ══════════════════════════════════════════════════ -->
<div class="page" style="background:white;">
  <div class="green-bar"></div>
  <div class="full">
    <div style="text-align:center;">
      <div class="lbl" style="text-align:center;">Your Body Is Changing</div>
      <div class="h1" style="font-size:26px;margin-bottom:6px;">The biology <em>behind your symptoms</em></div>
      <p class="sub" style="max-width:560px;margin:0 auto;font-size:9.5px;">Your hormones work in concert. When one or more shift — as they naturally do through perimenopause — the effects ripple across your whole wellbeing.</p>
    </div>
    <div class="hmap">
      <div style="display:flex;margin-bottom:12px;">
        <div style="flex:1;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#5db882;">Symptoms</div>
        <div style="width:100px;"></div>
        <div style="flex:1;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#5db882;text-align:right;">Hormonal Driver</div>
      </div>
      <div class="hmap-row">
        <div class="hmap-sx">Hot flashes <span class="sub-sx">night sweats</span></div>
        <div class="hmap-line"><div class="hmap-line-inner" style="background:#5db882;"></div></div>
        <div class="hmap-hormone"><span class="name" style="color:#5db882;">Estrogen ↓</span><span class="desc">Declining through perimenopause</span></div>
      </div>
      <div class="hmap-row">
        <div class="hmap-sx">Brain fog <span class="sub-sx">poor memory</span></div>
        <div class="hmap-line"><div class="hmap-line-inner" style="background:#5db882;"></div></div>
        <div class="hmap-hormone"><span class="name" style="color:#5db882;">Estrogen ↓</span><span class="desc">Impacts hippocampal function</span></div>
      </div>
      <div class="hmap-row">
        <div class="hmap-sx">Mood shifts <span class="sub-sx">anxiety</span></div>
        <div class="hmap-line"><div class="hmap-line-inner" style="background:#70b8b0;"></div></div>
        <div class="hmap-hormone"><span class="name" style="color:#70b8b0;">Progesterone ↓</span><span class="desc">Often the first hormone to drop</span></div>
      </div>
      <div class="hmap-row">
        <div class="hmap-sx">Sleep disruption</div>
        <div class="hmap-line"><div class="hmap-line-inner" style="background:#70b8b0;"></div></div>
        <div class="hmap-hormone"><span class="name" style="color:#70b8b0;">Progesterone ↓</span><span class="desc">Natural sedative effect lost</span></div>
      </div>
      <div class="hmap-row">
        <div class="hmap-sx">Low libido <span class="sub-sx">vaginal dryness</span></div>
        <div class="hmap-line"><div class="hmap-line-inner" style="background:#c8a840;"></div></div>
        <div class="hmap-hormone"><span class="name" style="color:#c8a840;">Testosterone ↓</span><span class="desc">Declines with age &amp; stress</span></div>
      </div>
      <div class="hmap-row">
        <div class="hmap-sx">Weight changes <span class="sub-sx">slowed metabolism</span></div>
        <div class="hmap-line"><div class="hmap-line-inner" style="background:#c88040;"></div></div>
        <div class="hmap-hormone"><span class="name" style="color:#c88040;">Thyroid (T3/T4)</span><span class="desc">Often missed on standard panels</span></div>
      </div>
      <div class="hmap-row">
        <div class="hmap-sx">Fatigue <span class="sub-sx">muscle loss</span></div>
        <div class="hmap-line"><div class="hmap-line-inner" style="background:#c06060;"></div></div>
        <div class="hmap-hormone"><span class="name" style="color:#c06060;">Cortisol ↑</span><span class="desc">Elevated by chronic stress</span></div>
      </div>
    </div>
    <p style="text-align:center;font-size:7.5px;color:var(--tm);font-style:italic;margin-top:10px;">Sources: NAMS 2022 Hormone Therapy Position Statement · Endocrine Society Clinical Practice Guidelines · ACOG Practice Bulletin on Menopausal HT</p>
  </div>
</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- PAGE 4 — 6-STEP PROTOCOL                           -->
<!-- ══════════════════════════════════════════════════ -->
<div class="page" style="background:var(--cream);">
  <div class="green-bar"></div>
  <div class="full">
    <div style="text-align:center;">
      <div class="lbl" style="text-align:center;">How It Works</div>
      <div class="h1" style="font-size:27px;margin-bottom:6px;">A 6-step <em>protocol.</em> Not a single appointment.</div>
      <p class="sub" style="max-width:520px;margin:0 auto;font-size:9.5px;">A structured clinical program with a dedicated care team — so nothing falls through the cracks.</p>
    </div>
    <div class="steps-grid">
      <div class="step-card"><div class="step-num">01</div><div class="step-tag">Step 01</div><h4>Initial Phone Call</h4><p>Care coordinator reviews your history and confirms you're a good candidate for the protocol.</p></div>
      <div class="step-card"><div class="step-num">02</div><div class="step-tag">Step 02</div><h4>Onboarding Visit</h4><p>Protocol orientation, InBody body composition scan, and OHIP bloodwork requisition provided.</p></div>
      <div class="step-card"><div class="step-num">03</div><div class="step-tag">Step 03</div><h4>Bloodwork</h4><p>Comprehensive hormone panel at LifeLabs or Dynacare — fully OHIP covered.</p></div>
      <div class="step-card"><div class="step-num">04</div><div class="step-tag">Step 04</div><h4>60-Min NP Consultation</h4><p>Deep results review, personalized treatment plan, and prescriptions as appropriate.</p></div>
      <div class="step-card"><div class="step-num">05</div><div class="step-tag">Step 05</div><h4>Follow-Up #1</h4><p>Symptom check, dose review, adjustments as needed. Virtual or in-person, 30 min.</p></div>
      <div class="step-card"><div class="step-num">06</div><div class="step-tag">Step 06</div><h4>Follow-Up #2</h4><p>InBody repeat, treatment review, 1-year Rx renewal, and annual care plan established.</p></div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- PAGE 5 — WHAT'S INCLUDED                           -->
<!-- ══════════════════════════════════════════════════ -->
<div class="page" style="background:white;">
  <div class="green-bar"></div>
  <div class="full">
    <div>
      <div class="lbl">Everything Included</div>
      <div class="h1" style="font-size:27px;">Your <em>Optimal</em> protocol</div>
      <p class="sub" style="margin-top:6px;font-size:9.5px;">One fee. No surprise bills. Everything below is covered by your single protocol fee.</p>
    </div>
    <div class="two-up" style="flex:1;align-content:start;">
      <div class="inc-card"><h5>60-Min NP Consultation</h5><p>A deep-dive assessment with your dedicated Nurse Practitioner. Not a rushed visit — a real conversation about your history, symptoms, and goals.</p></div>
      <div class="inc-card"><h5>OHIP-Covered Bloodwork</h5><p>A comprehensive hormone and metabolic panel — estradiol, testosterone, progesterone, FSH, thyroid, cortisol, DHEA — covered by your health card.</p></div>
      <div class="inc-card"><h5>Body Composition Analysis × 2</h5><p>InBody scan at intake and follow-up. Real data on muscle mass, metabolic rate, and body fat — not just a number on a scale.</p></div>
      <div class="inc-card"><h5>Two NP Follow-Up Appointments</h5><p>Review progress, adjust dosing, and manage side effects. Virtual or in-person options available for your convenience.</p></div>
    </div>
    <div class="four-up">
      <div class="check"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Written treatment plan</div>
      <div class="check"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Dedicated care coordinator</div>
      <div class="check"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Secure patient portal</div>
      <div class="check"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>GP coordination &amp; reports</div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- PAGE 6 — COMPARISON TABLE                          -->
<!-- ══════════════════════════════════════════════════ -->
<div class="page" style="background:var(--cream);">
  <div class="green-bar"></div>
  <div class="full">
    <div>
      <div class="lbl">How We Compare</div>
      <div class="h1" style="font-size:27px;margin-bottom:7px;">Not all hormone care is <em>the same</em></div>
      <p class="sub" style="font-size:9.5px;margin-bottom:14px;">We built this protocol to fill the gaps left by alternatives available in Barrie and across Ontario.</p>
    </div>
    <table class="ctbl">
      <thead><tr>
        <th></th>
        <th class="hi">Optimal Hormone Protocol</th>
        <th>Family Doctor / Walk-in</th>
        <th>Med Spa / Pellet Clinic</th>
      </tr></thead>
      <tbody>
        <tr><td>Consultation length</td><td class="hi"><span class="ck">✓</span> 60 minutes<span class="det">Thorough, unhurried</span></td><td><span class="cx">✗</span> 10 minutes<span class="det">Rushed visits</span></td><td><span class="ck">✓</span> 30–45 min</td></tr>
        <tr><td>Same clinician every visit</td><td class="hi"><span class="ck">✓</span> Yes<span class="det">Your NP from start to finish</span></td><td><span class="cx">✗</span> Often no<span class="det">Rotating providers</span></td><td><span class="ck">✓</span> Usually</td></tr>
        <tr><td>Comprehensive bloodwork</td><td class="hi"><span class="ck">✓</span> Full panel<span class="det">OHIP-covered</span></td><td><span class="ck">✓</span> Basic<span class="det">OHIP-covered</span></td><td><span class="cx">✗</span> Limited<span class="det">Often out-of-pocket</span></td></tr>
        <tr><td>Body composition testing</td><td class="hi"><span class="ck">✓</span> InBody × 2<span class="det">Baseline + follow-up</span></td><td><span class="cx">✗</span> No</td><td><span class="cx">✗</span> Rarely</td></tr>
        <tr><td>Structured follow-up</td><td class="hi"><span class="ck">✓</span> 2 NP visits<span class="det">6-step protocol</span></td><td><span class="cx">✗</span> If you rebook</td><td><span class="ck">✓</span> Insertion visits<span class="det">Every 3–6 months</span></td></tr>
        <tr><td>Treatment options</td><td class="hi"><span class="ck">✓</span> Wider HRT range<span class="det">More options available</span></td><td><span class="ck">✓</span> Standard HRT</td><td><span class="cx">✗</span> Pellets only<span class="det">Not Health Canada-approved</span></td></tr>
        <tr><td>Year-one cost</td><td class="hi"><span class="ck">✓</span> $695<span class="det">All-in, introductory rate</span></td><td><span class="ck">✓</span> $0 OHIP<span class="det">If you can get an appointment</span></td><td><span class="cx">✗</span> $1,800–$2,200+<span class="det">Pellet insertions + consults</span></td></tr>
      </tbody>
    </table>
    <p style="text-align:center;font-size:8px;color:var(--tm);font-style:italic;margin-top:12px;">Introductory rate of $695 + HST. Standard rate will be $895 + HST.</p>
  </div>
</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- PAGE 7 — POTENTIAL BENEFITS                        -->
<!-- ══════════════════════════════════════════════════ -->
<div class="page" style="background:white;">
  <div class="green-bar"></div>
  <div class="full">
    <div style="text-align:center;">
      <div class="lbl" style="text-align:center;">Potential Benefits</div>
      <div class="h1" style="font-size:27px;margin-bottom:6px;">Real relief. <em>Real results.</em></div>
      <p class="sub" style="max-width:520px;margin:0 auto;font-size:9.5px;">Women in hormone optimization protocols often report meaningful improvement within the first 8–12 weeks.</p>
    </div>
    <div class="ben-grid">
      <div class="benefit-card"><div class="benefit-icon"><svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 0 0 9.79 9.79z"/></svg></div><h4>Sleep through the night</h4><p>Night sweats and insomnia are among the first symptoms to improve with proper hormone support.</p></div>
      <div class="benefit-card"><div class="benefit-icon"><svg viewBox="0 0 24 24"><path d="M12 2a5 5 0 0 1 5 5v3a5 5 0 0 1-10 0V7a5 5 0 0 1 5-5z"/><path d="M3 18c0-3 4-5 9-5s9 2 9 5v2H3v-2z"/></svg></div><h4>Think clearly again</h4><p>Brain fog and mental fatigue often resolve once hormone levels are properly addressed.</p></div>
      <div class="benefit-card"><div class="benefit-icon"><svg viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div><h4>Stable energy all day</h4><p>No more crashing by mid-afternoon. Balanced hormones support sustained energy.</p></div>
      <div class="benefit-card"><div class="benefit-icon"><svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg></div><h4>Mood you recognize</h4><p>Anxiety and low mood often improve significantly when the hormonal picture is corrected.</p></div>
      <div class="benefit-card"><div class="benefit-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><path d="M9 9h.01M15 9h.01"/></svg></div><h4>Feel like yourself</h4><p>Libido, comfort, and confidence — the things that slipped away — can come back.</p></div>
      <div class="benefit-card"><div class="benefit-icon"><svg viewBox="0 0 24 24"><path d="M18 20V10M12 20V4M6 20v-6"/></svg></div><h4>Measurable progress</h4><p>Body composition scans give you data — not just a feeling — that things are changing.</p></div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- PAGE 8 — PRICING                                   -->
<!-- ══════════════════════════════════════════════════ -->
<div class="page">
  <div class="green-bar"></div>
  <div class="two-col">
    <div class="lcol" style="background:var(--g100);justify-content:center;">
      <div class="lbl">Pricing</div>
      <div class="h1" style="font-size:26px;margin-bottom:4px;">Simple, <em>transparent</em> pricing</div>
      <p class="sub" style="font-size:9.5px;margin-bottom:16px;">One protocol fee covers everything. No hidden costs. No surprise bills.</p>
      <div class="pricing-box">
        <div style="text-align:center;margin-bottom:14px;"><span class="price-badge">Founding Patient Rate</span></div>
        <ul class="vstack" style="list-style:none;margin-bottom:14px;">
          <li>60-min NP consultation + treatment plan <span class="free">Included</span></li>
          <li>Comprehensive hormone bloodwork panel <span class="free">Included</span></li>
          <li>InBody body composition scan × 2 <span class="free">Included</span></li>
          <li>Onboarding &amp; orientation appointment <span class="free">Included</span></li>
          <li>Two NP follow-up appointments <span class="free">Included</span></li>
          <li>Care coordinator &amp; patient portal <span class="free">Included</span></li>
          <li>Reports to your family doctor <span class="free">Included</span></li>
        </ul>
        <div style="text-align:center;"><div class="price-big">$695 <span>+ HST</span></div></div>
        <p style="text-align:center;font-size:8.5px;color:var(--tm);margin-bottom:8px;">Standard rate will be $895 + HST</p>
        <div class="scarcity">First 50 patients only at this introductory rate</div>
        <div class="btn-green">Book a free intro call &nbsp;·&nbsp; book.beoptimal.ca</div>
        <p style="text-align:center;font-size:8px;color:var(--tm);margin-top:10px;line-height:1.5;">NP receipts may be submittable to extended health plans. May qualify as a medical expense on your taxes.</p>
      </div>
    </div>
    <div class="dvider"></div>
    <div class="rcol" style="background:var(--g800);justify-content:center;gap:18px;">
      <div style="padding:20px 24px;background:rgba(255,255,255,.06);border-radius:14px;border:1px solid rgba(255,255,255,.1);">
        <p style="font-size:8.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#a8cfa8;margin-bottom:6px;">NP receipts</p>
        <p style="font-size:10px;color:rgba(255,255,255,.75);line-height:1.65;">Many extended health benefit plans will accept receipts from Nurse Practitioners. Check with your insurer — this may be partially or fully reimbursable.</p>
      </div>
      <div style="padding:20px 24px;background:rgba(255,255,255,.06);border-radius:14px;border:1px solid rgba(255,255,255,.1);">
        <p style="font-size:8.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#a8cfa8;margin-bottom:6px;">Tax deductible</p>
        <p style="font-size:10px;color:rgba(255,255,255,.75);line-height:1.65;">Protocol fees may qualify as a medical expense on your personal income tax return under CRA guidelines.</p>
      </div>
      <div style="padding:20px 24px;background:rgba(255,255,255,.06);border-radius:14px;border:1px solid rgba(255,255,255,.1);">
        <p style="font-size:8.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#a8cfa8;margin-bottom:6px;">OHIP bloodwork</p>
        <p style="font-size:10px;color:rgba(255,255,255,.75);line-height:1.65;">Your comprehensive hormone panel is ordered under OHIP and processed at LifeLabs or Dynacare — at zero additional cost to you.</p>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- PAGE 9 — YOUR CLINICIAN + CTA                      -->
<!-- ══════════════════════════════════════════════════ -->
<div class="page">
  <div class="green-bar"></div>
  <div class="two-col">
    <div class="lcol" style="background:var(--cream);">
      <div class="lbl">Your Clinician</div>
      <div style="display:flex;gap:20px;margin-top:12px;flex:1;">
        <div style="width:120px;border-radius:12px;overflow:hidden;aspect-ratio:3/4;flex-shrink:0;">
          <img src="{IMG}/np-chantelle.png" style="width:100%;height:100%;object-fit:cover;object-position:center top;display:block;" alt="Chantelle Oostwoud, MN PHC-NP">
        </div>
        <div style="flex:1;">
          <div style="font-family:var(--serif);font-size:21px;font-weight:600;color:var(--td);margin-bottom:3px;">Chantelle Oostwoud</div>
          <div style="font-size:8px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--g600);margin-bottom:12px;">MN, PHC-NP &nbsp;·&nbsp; Nurse Practitioner</div>
          <p style="font-size:10px;color:var(--tb);line-height:1.8;">Chantelle Oostwoud, MN, PHC-NP is the dedicated clinician for the Women's Hormone Health Protocol at Optimal Family Health. A Nurse Practitioner with a Master of Nursing from Athabasca University, she brings nearly a decade of frontline experience across emergency medicine, critical care, and remote community health to her work in Optimal's Enhanced Care program — where she works with a small panel of patients who want more time, more thoroughness, and more answers than the standard system typically allows.</p>
        </div>
      </div>
    </div>
    <div class="dvider"></div>
    <div class="rcol" style="background:var(--g800);justify-content:center;">
      <div class="cta-panel">
        <h2>Start your journey to <em>feeling like yourself</em> again.</h2>
        <p class="sub" style="font-size:10.5px;">A free intro call with our care coordinator takes fifteen minutes. No commitment. No pressure. Just a conversation about what you're going through and whether the protocol is right for you.</p>
        <div class="btn-white">Book a free intro call</div>
        <div class="contact">
          <p>Phone / text &nbsp;<strong>(437) 370-0291</strong></p>
          <p>Email &nbsp;<strong>care@beoptimal.ca</strong></p>
          <p>Book online &nbsp;<strong>book.beoptimal.ca</strong></p>
          <p style="margin-top:12px;color:rgba(255,255,255,.32);font-size:8.5px;">Optimal Family Health &nbsp;·&nbsp; Barrie, Ontario</p>
        </div>
      </div>
    </div>
  </div>
</div>

</body></html>"""


def generate():
    out = f"{BASE}/Optimal Clinic - Women's Hormone Optimization Protocol brochure - March 22, 2026 version.pdf"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.set_content(FULL_HTML, wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.pdf(
            path=out,
            format="A4",
            landscape=True,
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()
    print(f"✓  {out}")


if __name__ == "__main__":
    generate()
