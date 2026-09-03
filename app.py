import streamlit as st
import os
import tempfile
from datetime import datetime

from agent import extract_pdf_text, summarize_paper


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Research Digest — Paper Summarizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------------------------------------------------------------------
# Design tokens / custom styling
# ---------------------------------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Sora:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --bg: #F6F3EA;
    --panel: #FFFFFF;
    --panel-2: #FCFAF3;
    --ink: #171B22;
    --ink-soft: #5B6472;
    --coral: #E4572E;
    --coral-deep: #B8431F;
    --teal: #1E8A73;
    --teal-deep: #146552;
    --gold: #B9821F;
    --line: rgba(23,27,34,0.12);
    --line-soft: rgba(23,27,34,0.07);
}

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    color: var(--ink);
}

.stApp {
    background:
        radial-gradient(circle at 10% -8%, rgba(30,138,115,0.08), transparent 40%),
        radial-gradient(circle at 90% 0%, rgba(228,87,46,0.07), transparent 38%),
        var(--bg);
    color: var(--ink);
}

section[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    max-width: 1580px;
    padding: 2rem 3.2rem 4rem;
}

@media (max-width: 900px) {
    .block-container {
        padding: 1.4rem 1.2rem 3rem;
    }
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}


/* ---------- Hero ---------- */

.hero {
    animation: fadeUp 0.4s ease both;
    margin-bottom: 2.2rem;
}

.hero-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 3rem;
    line-height: 1.1;
    color: var(--ink);
    margin: 0 0 0.8rem;
    max-width: 760px;
}

.hero-title em {
    color: var(--coral);
    font-style: normal;
}

.hero-dek {
    font-size: 1.05rem;
    line-height: 1.6;
    color: var(--ink-soft);
    max-width: 600px;
    margin-bottom: 1.2rem;
}

.pill-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
}

.pill {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.35rem 0.75rem;
    border-radius: 100px;
    border: 1px solid var(--line);
    color: var(--ink-soft);
    background: var(--panel);
}

.pill.coral {
    border-color: rgba(228,87,46,0.4);
    color: var(--coral-deep);
    background: rgba(228,87,46,0.08);
}

.pill.teal {
    border-color: rgba(30,138,115,0.4);
    color: var(--teal-deep);
    background: rgba(30,138,115,0.08);
}

.pill.gold {
    border-color: rgba(185,130,31,0.4);
    color: var(--gold);
    background: rgba(185,130,31,0.08);
}


/* ---------- Rail ---------- */

.rail-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 1.5rem 1.4rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 3px 14px rgba(23,27,34,0.05);
    animation: fadeUp 0.5s ease both;
}

.rail-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--coral-deep);
    margin-bottom: 1rem;
}

.rail-step {
    display: flex;
    gap: 0.7rem;
    margin-bottom: 0.9rem;
}

.rail-step:last-child {
    margin-bottom: 0;
}

.rail-badge {
    flex-shrink: 0;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 1px solid rgba(228,87,46,0.4);
    color: var(--coral-deep);
    background: rgba(228,87,46,0.06);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.rail-step p {
    margin: 0;
    font-size: 0.9rem;
    line-height: 1.45;
    color: var(--ink);
}

.rail-guide {
    display: flex;
    gap: 0.55rem;
    margin-bottom: 0.65rem;
    font-size: 0.86rem;
    color: var(--ink-soft);
}

.rail-guide:last-child {
    margin-bottom: 0;
}

.rail-guide .tick {
    color: var(--teal);
    flex-shrink: 0;
}

.rail-footer {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--ink-soft);
    letter-spacing: 0.03em;
    padding: 0 0.2rem;
}


/* ---------- Section labels ---------- */

.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--coral-deep);
    margin: 0 0 1rem;
}


/* ---------- Upload widget ---------- */

[data-testid="stFileUploader"] {
    background-color: var(--panel);
    border: 1.5px dashed rgba(228,87,46,0.45);
    border-radius: 10px;
    padding: 1.2rem;
    transition: border-color 0.2s ease, background-color 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--coral);
    background-color: rgba(228,87,46,0.03);
}

[data-testid="stFileUploaderDropzone"] {
    background-color: transparent;
}

[data-testid="stFileUploader"] section {
    background-color: transparent;
}

[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: var(--ink) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: var(--ink-soft) !important;
}

[data-testid="stFileUploader"] button {
    background-color: var(--panel) !important;
    color: var(--ink) !important;
    border: 1px solid var(--line) !important;
}

[data-testid="stFileUploaderFile"] {
    color: var(--ink);
}

[data-testid="stFileUploaderFile"] small {
    color: var(--ink-soft) !important;
}


/* ---------- Buttons ---------- */

.stButton button {
    background: linear-gradient(
        135deg,
        var(--coral) 0%,
        var(--coral-deep) 100%
    );
    color: #FFF8F0;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.4rem;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.01em;
    width: 100%;
    box-shadow: 0 4px 14px rgba(228,87,46,0.24);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(228,87,46,0.34);
    color: #FFF8F0;
}

.stButton button p {
    color: #FFF8F0 !important;
}


/* ---------- Ticket ---------- */

.ticket {
    display: flex;
    gap: 1.8rem;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    background: var(--panel);
    border-radius: 8px;
    border-left: 4px solid var(--coral);
    padding: 0.9rem 1.3rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.83rem;
    color: var(--ink-soft);
    margin: 1rem 0 1.4rem;
    box-shadow: 0 3px 14px rgba(23,27,34,0.06);
    animation: fadeUp 0.35s ease both;
}

.ticket.teal {
    border-left-color: var(--teal);
}

.ticket b {
    color: var(--ink);
    font-weight: 600;
}

.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--coral);
    margin-right: 6px;
}

.ticket.teal .status-dot {
    background: var(--teal);
}


/* ---------- Stepper ---------- */

.stepper {
    display: flex;
    justify-content: space-between;
    margin: 1.7rem 0 1.3rem;
    position: relative;
}

.stepper::before {
    content: "";
    position: absolute;
    top: 10px;
    left: 5%;
    right: 5%;
    height: 2px;
    background-color: var(--line);
    z-index: 0;
}

.step {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    flex: 1;
}

.step-dot {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: var(--panel);
    border: 2px solid var(--line);
    transition: all 0.3s ease;
}

.step.done .step-dot {
    background-color: var(--teal);
    border-color: var(--teal);
}

.step.active .step-dot {
    background-color: var(--coral);
    border-color: var(--coral);
    box-shadow: 0 0 0 5px rgba(228,87,46,0.18);
    animation: pulse 1.4s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% {
        box-shadow: 0 0 0 5px rgba(228,87,46,0.18);
    }

    50% {
        box-shadow: 0 0 0 9px rgba(228,87,46,0.08);
    }
}

.step-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--ink-soft);
}

.step.done .step-label,
.step.active .step-label {
    color: var(--ink);
}


/* ---------- Result box ---------- */

.typeset {
    background: var(--panel);
    border-radius: 10px;
    border-top: 3px solid var(--gold);
    padding: 2.1rem 2.3rem;
    margin-top: 0.5rem;
    box-shadow: 0 6px 24px rgba(23,27,34,0.08);
    animation: fadeUp 0.4s ease both;
}

.typeset-eyebrow {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--coral-deep);
    margin-bottom: 1rem;
}

.stamp {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    color: var(--teal-deep);
    border: 1.5px solid var(--teal);
    border-radius: 4px;
    padding: 0.15rem 0.5rem;
    transform: rotate(-3deg);
    animation: stampIn 0.4s cubic-bezier(.2,1.6,.4,1) both;
    animation-delay: 0.2s;
}

@keyframes stampIn {
    from {
        opacity: 0;
        transform: scale(2) rotate(-3deg);
    }

    to {
        opacity: 1;
        transform: scale(1) rotate(-3deg);
    }
}

.typeset h1,
.typeset h2,
.typeset h3 {
    font-family: 'Fraunces', serif;
    color: var(--ink);
}

.typeset p,
.typeset li {
    line-height: 1.68;
    color: var(--ink);
}


/* ---------- Callout ---------- */

.callout {
    border-left: 4px solid var(--coral);
    background-color: rgba(228,87,46,0.06);
    border-radius: 6px;
    padding: 1rem 1.2rem;
    font-size: 0.92rem;
    color: var(--ink);
    margin: 1rem 0;
}

.callout b {
    color: var(--ink);
}


/* ---------- Guidance grid ---------- */

.guide-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.3rem;
    margin-top: 0.4rem;
}

.guide-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-top: 3px solid var(--coral);
    border-radius: 10px;
    padding: 1.4rem 1.3rem;
    box-shadow: 0 3px 14px rgba(23,27,34,0.05);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.guide-card:nth-child(2) {
    border-top-color: var(--teal);
}

.guide-card:nth-child(3) {
    border-top-color: var(--gold);
}

.guide-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 26px rgba(23,27,34,0.12);
}

.guide-card .icon {
    font-size: 1.4rem;
    margin-bottom: 0.6rem;
    display: block;
}

.guide-card h4 {
    font-family: 'Fraunces', serif;
    font-size: 1.1rem;
    margin: 0 0 0.5rem;
    color: var(--ink);
}

.guide-card p {
    font-size: 0.9rem;
    color: var(--ink-soft);
    line-height: 1.55;
    margin: 0;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Stepper
# ---------------------------------------------------------------------------

def render_stepper(current: int, placeholder):
    """
    current:
        0 = received
        1 = extracted
        2 = reviewed
        3 = typeset
        -1 = nothing active
    """
    labels = ["Received", "Extracted", "Reviewed", "Typeset"]

    html = '<div class="stepper">'
    for i, label in enumerate(labels):
        state = "done" if i < current else ("active" if i == current else "")
        html += (
            f'<div class="step {state}">'
            f'<div class="step-dot"></div>'
            f'<div class="step-label">{label}</div>'
            f'</div>'
        )
    html += "</div>"

    placeholder.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">
        The manuscript desk for <em>faster</em> reading.
    </div>
    <div class="hero-dek">
        Submit a paper and receive a typeset summary of its methodology,
        findings, and contributions — reviewed in minutes rather than an afternoon.
    </div>
    <div class="pill-row">
        <span class="pill coral">Text-based PDF</span>
        <span class="pill teal">Full extraction</span>
        <span class="pill gold">Typeset abstract</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Two-pane layout
# ---------------------------------------------------------------------------

rail_col, main_col = st.columns([1, 2.15], gap="large")


# ---------------------------------------------------------------------------
# Left rail
# ---------------------------------------------------------------------------

with rail_col:
    steps = [
        "Submit a manuscript as a text-based PDF.",
        "The desk extracts and reads the full text.",
        "The paper is reviewed for structure and findings.",
        "A typeset abstract is returned for your records.",
    ]

    steps_html = "".join(
        f'<div class="rail-step">'
        f'<div class="rail-badge">{i + 1}</div>'
        f'<p>{step}</p>'
        f'</div>'
        for i, step in enumerate(steps)
    )

    st.markdown(
        f'<div class="rail-card">'
        f'<div class="rail-eyebrow">Submission process</div>'
        f'{steps_html}'
        f'</div>',
        unsafe_allow_html=True
    )

    guidelines = [
        "Use a text-based PDF, not a scanned image.",
        "Unprotected files only — no password locks.",
        "Papers under 50 pages return the cleanest reviews.",
    ]

    guide_html = "".join(
        f'<div class="rail-guide">'
        f'<span class="tick">✓</span>'
        f'<span>{guideline}</span>'
        f'</div>'
        for guideline in guidelines
    )

    st.markdown(
        f'<div class="rail-card">'
        f'<div class="rail-eyebrow">Submission guidelines</div>'
        f'{guide_html}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="rail-footer">'
        'Papers are processed locally and never stored after review.'
        '</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------------------------------
# Main workspace
# ---------------------------------------------------------------------------

with main_col:
    st.markdown(
        '<div class="section-label">Manuscript submission</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload a PDF for review",
        type=["pdf"],
        help="Text-based PDF only. Scanned images and password-protected files will not extract cleanly."
    )

    if uploaded_file:
        file_size = uploaded_file.size / (1024 * 1024)

        st.markdown(
            f'<div class="ticket">'
            f'<span><span class="status-dot"></span>'
            f'FILE &nbsp;<b>{uploaded_file.name}</b></span>'
            f'<span>SIZE &nbsp;<b>{file_size:.2f} MB</b></span>'
            f'<span>STATUS &nbsp;<b>received</b></span>'
            f'</div>',
            unsafe_allow_html=True
        )

        submit = st.button(
            "Review manuscript",
            use_container_width=True
        )

        if submit:
            stepper_slot = st.empty()
            render_stepper(0, stepper_slot)

            # Use NamedTemporaryFile to avoid file collisions on Streamlit Cloud
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                temp_path = tmp_file.name

            try:
                with st.spinner("Extracting text..."):
                    text = extract_pdf_text(temp_path)

                if not text:
                    render_stepper(-1, stepper_slot)
                    stepper_slot.empty()
                    
                    st.markdown(
                        '<div class="callout">'
                        '<b>Extraction failed.</b><br>'
                        'This usually means the PDF is scanned rather than text-based, '
                        'is password protected, or has an unsupported text encoding. '
                        'Try a different file.'
                        '</div>',
                        unsafe_allow_html=True
                    )
                else:
                    render_stepper(1, stepper_slot)
                    word_count = len(text.split())

                    st.markdown(
                        f'<div class="ticket teal">'
                        f'<span><span class="status-dot"></span>'
                        f'WORDS EXTRACTED &nbsp;<b>{word_count:,}</b></span>'
                        f'<span>STATUS &nbsp;<b>extracted</b></span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    render_stepper(2, stepper_slot)

                    with st.spinner("Reviewing content..."):
                        output = summarize_paper(text)

                    if isinstance(output, dict) and "error" in output:
                        render_stepper(-1, stepper_slot)
                        stepper_slot.empty()
                        st.markdown(
                            f'<div class="callout">'
                            f'<b>Review could not be completed.</b><br>'
                            f'{output["error"]}'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        render_stepper(3, stepper_slot)
                        result_text = output["result"] if isinstance(output, dict) and "result" in output else str(output)

                        st.markdown(
                            '<div class="section-label">Typeset summary</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f'<div class="typeset">'
                            f'<div class="typeset-eyebrow">'
                            f'Abstract &amp; review notes '
                            f'<span class="stamp">REVIEWED</span>'
                            f'</div>'
                            f'{result_text}'
                            f'</div>',
                            unsafe_allow_html=True
                        )
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    else:
        st.markdown(
            '<div class="section-label">Who this desk serves</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="guide-grid">
            <div class="guide-card">
                <span class="icon">📚</span>
                <h4>Students</h4>
                <p>
                    Move through literature reviews and assigned readings
                    without losing the paper's core argument.
                </p>
            </div>
            <div class="guide-card">
                <span class="icon">🔬</span>
                <h4>Researchers</h4>
                <p>
                    Triage new publications quickly and identify which papers
                    merit a closer read.
                </p>
            </div>
            <div class="guide-card">
                <span class="icon">🎓</span>
                <h4>Academics</h4>
                <p>
                    Prepare talking points for lectures, seminars, and committee
                    meetings ahead of time.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)