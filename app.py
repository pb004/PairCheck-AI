import html
import re
import streamlit as st
import backend as B
from explain import type_meaning, ai_summary

SEV_T, TYPE_T = B.thresholds()
DISCLAIMER = ("Research and educational prototype. This does not confirm that an interaction "
              "will occur in any individual. Please consult a pharmacist or physician.")
e = html.escape

st.set_page_config(page_title="PairCheck AI", layout="centered")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }
.block-container { max-width: 860px; padding-top: 1rem; padding-bottom: 5rem; }
.brand { font-size: 1.35rem; font-weight: 500; color: #12283F; padding-top: .35rem; }
.plus { font-size: 1.4rem; color: #5F5E5A; text-align: center; padding-bottom: .35rem; }
.pair { font-size: 1.35rem; font-weight: 500; margin: 1.2rem 0 .7rem; color: #1F2937; }
.sevrow { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.sevlbl { font-size: 1.15rem; color: #5F5E5A; }
.tag { display: inline-flex; align-items: center; gap: 10px; padding: 8px 18px; border-radius: 12px;
       font-size: 1.5rem; font-weight: 500; }
.glyph { width: 26px; height: 26px; border: 2px solid; border-radius: 50%; display: inline-flex;
         align-items: center; justify-content: center; font-size: .95rem; }
.status { margin: .7rem 0 .15rem; font-size: 1.05rem; font-weight: 500; }
.sub { font-size: .9rem; color: #5F5E5A; margin-bottom: 1rem; }
.diagram { display: flex; justify-content: center; align-items: center; gap: 10px; flex-wrap: wrap;
           margin-bottom: 1rem; }
.pill { padding: 5px 14px; border: .5px solid #B4B2A9; border-radius: 20px; background: #F5F7FA; }
.panel { border: .5px solid #D3D1C7; border-radius: 12px; padding: 14px 16px; background: #fff;
         height: 100%; margin-bottom: .6rem; }
.ph { font-size: .85rem; color: #5F5E5A; margin-bottom: 6px; }
.ai { margin-top: 10px; padding-top: 10px; border-top: .5px solid #D3D1C7; }
.chip { font-size: .72rem; padding: 2px 8px; border-radius: 6px; background: #E6F1FB; color: #0C447C; }
.brow { display: flex; align-items: center; gap: 10px; margin-top: 6px; font-size: .85rem; }
.bn { width: 120px; } .bp { width: 36px; text-align: right; }
.bt { flex: 1; height: 8px; background: #EEF0F3; border-radius: 4px; }
.bt div { height: 8px; background: #185FA5; border-radius: 4px; }
mark { background: #FAEEDA; color: #633806; padding: 0 2px; border-radius: 3px; }
.empty { border: .5px dashed #B4B2A9; border-radius: 12px; padding: 1.4rem; color: #5F5E5A; }
.foot { position: fixed; left: 0; right: 0; bottom: 0; background: #12283F; color: #EEF2F7;
        font-size: .8rem; padding: .5rem 1rem; text-align: center; z-index: 99; }
</style>""", unsafe_allow_html=True)

STYLE = {"Major": ("#FCEBEB", "#791F1F", "#A32D2D", "!"),
         "Moderate": ("#FAEEDA", "#633806", "#BA7517", "!"),
         "Minor": ("#E6F1FB", "#0C447C", "#378ADD", "i"),
         None: ("#F1EFE8", "#444441", "#888780", "?")}


def tag(sev, predicted):
    bg, fg, bd, g = STYLE.get(sev, STYLE[None])
    fill, line = ("transparent", "dashed") if predicted else (bg, "solid")
    return (f'<div class="sevrow"><span class="sevlbl">Severity:</span>'
            f'<span class="tag" style="background:{fill};color:{fg};border:2px {line} {bd}">'
            f'<span class="glyph" style="border-color:{fg}">{g}</span>'
            f'{e(sev or "Not enough information")}</span></div>')


def build(a, b):
    rec = B.lookup_pair(a, b)
    if rec:
        return dict(kind="rec", sev=rec["severity"], type=rec["type"], types=rec["types"], ids=rec.get("ids", ""),
                    status="Recorded in source databases",
                    sub="Looked up, not predicted. Severity from DDInter.")
    p = B.predict_pair(a, b)
    sev_ok, type_ok = p["sev_p"] >= SEV_T, p["types"][0][1] >= TYPE_T
    if not (sev_ok or type_ok):
        return dict(kind="none", sev=None, status="No record found, and no reliable estimate is available",
                    sub="This does not mean the pair is safe.")
    return dict(kind="pred", sev=p["severity"] if sev_ok else None,
                type=p["types"][0][0] if type_ok else None, types=p["types"] if type_ok else [],
                status="Predicted. Treat as low confidence",
                sub="Not recorded in the source databases. Applies only if an interaction exists.")


def panel(head, body):
    return f'<div class="panel"><div class="ph">{e(head)}</div>{body}</div>'


def highlight(text, partner):
    return re.sub(f"({re.escape(e(partner))})", r"<mark>\1</mark>", e(text), flags=re.I)


def show(a, b):
    if a == b:
        st.markdown('<div class="empty">Choose two different drugs.</div>', unsafe_allow_html=True)
        return
    s = build(a, b)
    na, nb = a.title(), b.title()
    top = (f'<div class="pair">{e(na)} + {e(nb)}</div>'
           f'{tag(s["sev"], s["kind"] == "pred" and s["sev"] is not None)}'
           f'<div class="status">{e(s["status"])}</div><div class="sub">{e(s["sub"])}</div>')
    if s.get("type"):
        arrow = '<span style="color:#5F5E5A;font-size:1.2rem">&#8596;</span>'
        top += (f'<div class="diagram"><span class="pill">{e(na)}</span>{arrow}'
                f'<span class="pill">{e(s["type"])}</span>{arrow}<span class="pill">{e(nb)}</span></div>')
    st.markdown(top, unsafe_allow_html=True)

    sent = B.get_label_sentence(a, b) if s["kind"] == "rec" else None
    ma, mb = B.get_mechanism(a), B.get_mechanism(b)
    if s["kind"] == "rec":
        body = f'<div>{e(" ".join(type_meaning(t) for t in s["types"]))}</div>'
        if s["ids"]:
            body += f'<div class="ph" style="margin-top:10px">Record IDs: {e(s["ids"])}</div>'
        if sent:
            with st.spinner("Writing summary"):
                ai = ai_summary(na, nb, s["type"], s["sev"], sent["sentence"], sent["cite"],
                                ma and ma["text"], mb and mb["text"])
            if ai:
                body += (f'<div class="ai"><span class="chip">AI-written from the source text below</span>'
                         f'<div style="margin-top:6px">{e(ai)}</div></div>')
    elif s["kind"] == "pred":
        body = ('<div>This estimate comes from chemical structure only, so there is no explanation '
                'of how the two drugs interact.</div>')
        if s["types"]:
            body += '<div class="ph" style="margin-top:12px">Top three types, if an interaction exists</div>'
            for n, p in s["types"]:
                body += (f'<div class="brow"><span class="bn">{e(n)}</span><div class="bt">'
                         f'<div style="width:{p * 100:.0f}%"></div></div><span class="bp">{p:.0%}</span></div>')
    else:
        body = "<div>No estimate is shown. Ask a pharmacist or physician about this combination.</div>"
    st.markdown(panel("What this means", body), unsafe_allow_html=True)

    if sent:
        with st.expander("Source text"):
            st.markdown(f'<div>{highlight(sent["sentence"], sent["partner"])}</div>'
                        f'<div class="ph" style="margin-top:6px">{e(sent["cite"])}</div>',
                        unsafe_allow_html=True)

    if s["kind"] != "none":
        for col, d, m in zip(st.columns(2), (na, nb), (ma, mb)):
            txt = (f'<div>{e(m["text"])}</div><div class="ph" style="margin-top:6px">Source: '
                   f'{e(m["source"])}</div>') if m else '<div class="ph">Not available</div>'
            col.markdown(panel(d, txt), unsafe_allow_html=True)


c1, c2, c3 = st.columns([6, 1.7, 2], vertical_alignment="center")
c1.markdown('<div class="brand">PairCheck AI</div>', unsafe_allow_html=True)
with c2.popover("How it works"):
    st.markdown("**Recorded pairs are looked up.** You see the stored severity and interaction type. "
                "No model is used.\n\n**Unrecorded pairs get a marked estimate.** A model uses each "
                "drug's chemical structure and the result reads *Predicted. Treat as low confidence*.\n\n"
                "**Explanations stay close to the source.** A short summary appears only when a label "
                "sentence names both drugs, and the source sentence is shown next to it.")
with c3.popover("Data and limits"):
    st.markdown("- The app never says a pair is safe. A missing record can mean the pair was never studied.\n"
                "- The model learns only from recorded interactions, so it estimates *if* an interaction exists.\n"
                "- It covers drugs with a known chemical structure and checks two drugs at a time.\n"
                "- It gives no dosing or personal advice and is not for clinical use.")

if B.DEMO_MODE:
    st.warning("Demo mode: results are placeholders. Connect your project in backend.py.")

opts = B.drug_options()
p1, p2, p3, p4 = st.columns([5, 0.6, 5, 2.3], vertical_alignment="bottom")
la = p1.selectbox("First drug", list(opts), index=None, placeholder="Search a drug")
p2.markdown('<div class="plus">+</div>', unsafe_allow_html=True)
lb = p3.selectbox("Second drug", list(opts), index=None, placeholder="Search a drug")
if p4.button("Check pair", type="primary", use_container_width=True):
    st.session_state.checked = (la, lb) if la and lb else "missing"

ck = st.session_state.get("checked")
if ck == "missing":
    st.markdown('<div class="empty">Choose both drugs, then select Check pair.</div>', unsafe_allow_html=True)
elif ck:
    show(opts[ck[0]], opts[ck[1]])
else:
    st.markdown('<div class="empty"><b>Pick two drugs to begin</b><br>You will see whether the pair is '
                'recorded, or a clearly marked estimate if it is not.</div>', unsafe_allow_html=True)

st.markdown(f'<div class="foot">{e(DISCLAIMER)}</div>', unsafe_allow_html=True)
