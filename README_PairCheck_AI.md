# PairCheck AI

**A lookup-first drug--drug interaction (DDI) checker with a
machine-learning fallback**

PairCheck AI is an educational/research prototype designed to help users
explore potential interactions between medicines. It checks available
interaction records first and may use machine-learning predictions when
a suitable recorded interaction is unavailable and the model meets its
configured confidence criteria.

> **Medical disclaimer:** PairCheck AI is not a medical device and must
> not be used to make treatment decisions. It does not replace advice
> from a qualified doctor or pharmacist. Do not start, stop, or change
> medication based on this application. Consult a healthcare
> professional about possible drug interactions.

## Main features

-   **Drug-pair checking:** Check a pair of medicines against the
    configured interaction data.
-   **Recorded interactions:** Display matching interaction information
    found in the reference data.
-   **Machine-learning fallback:** For eligible pairs without a complete
    recorded result, the application may provide a prediction when it
    meets the configured confidence threshold.
-   **Uncertainty handling:** Return **"Not enough information"** when
    evidence is insufficient, rather than presenting an uncertain
    prediction as confirmed.
-   **Multi-drug checking:** Check up to five medicines by evaluating
    their unique pairs. Five medicines produce up to ten pairwise
    checks. Results are pair-level; they are not a clinical assessment
    of the entire combination.
-   **Print sheet:** Generate a printable summary using the browser's
    print function.
-   **Evidence display:** Depending on available data, results may
    include severity, interaction type, explanation, source text, or
    record identifiers.

Feature availability depends on the files and configuration in the
deployed version.

## Understanding result categories

  -----------------------------------------------------------------------
  Result                              Meaning
  ----------------------------------- -----------------------------------
  Recorded interaction                The configured reference data
                                      contains a matching interaction
                                      record.

  Predicted interaction               A machine-learning model produced a
                                      prediction for a pair without a
                                      complete recorded result, and it
                                      met the configured confidence
                                      criteria.

  Not enough information              The available record or model
                                      evidence was insufficient to return
                                      a result under the application's
                                      rules.
  -----------------------------------------------------------------------

**A missing interaction record or "Not enough information" does not mean
that a medicine combination is safe.** A predicted interaction is a
model output, not a clinically confirmed interaction.

## Technology

The project has been described as using the technologies below. Confirm
the actual imports and installed packages in the final source code and
`requirements.txt`.

-   Python
-   Streamlit
-   pandas and NumPy
-   RDKit
-   scikit-learn
-   XGBoost
-   joblib

## Repository structure

The exact structure depends on the version uploaded to GitHub. A typical
layout may look like:

``` text
PairCheck-AI/
├── app.py                  # Pairwise app entrypoint, if used
├── app_multi.py            # Multi-drug app entrypoint, if used
├── backend.py              # Backend logic, if present
├── explain.py              # Explanation utilities, if present
├── requirements.txt        # Python dependencies
├── models/                 # Saved models, if required
├── data/                   # Reference data, if required
└── README.md
```

This is an illustrative structure, not a claim about the exact files in
your repository. Keep the real filenames and folders required by your
code, and update this section to match the final repository.

## Run locally

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR-USERNAME/PairCheck-AI.git
cd PairCheck-AI
```

Replace `YOUR-USERNAME` with the GitHub account that owns the
repository.

### 2. Create and activate a virtual environment (recommended)

**Windows:**

``` bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Run the application

If `app_multi.py` is the intended entrypoint for the multi-drug version:

``` bash
streamlit run app_multi.py
```

For a pairwise-only version, if `app.py` is the intended entrypoint:

``` bash
streamlit run app.py
```

Use the entrypoint that matches the version you intend to run. Streamlit
will print a local URL, commonly `http://localhost:8501`.

## Deploy on Streamlit Community Cloud

1.  Push the complete project to a GitHub repository.
2.  Confirm that the repository contains the correct Streamlit
    entrypoint, `requirements.txt`, and all required model and data
    files.
3.  Sign in to [Streamlit Community Cloud](https://share.streamlit.io/)
    using GitHub.
4.  Select **Create app**, then choose your repository and branch.
5.  Set **Main file path** to the actual entrypoint (for example,
    `app_multi.py` if appropriate).
6.  Add required credentials through Streamlit's **Secrets** settings.
    Never commit private keys or passwords to GitHub.
7.  Deploy and inspect the app logs if deployment fails.

Streamlit assigns the deployed URL. Add the real URL here after
deployment:

**Live application:** `ADD_YOUR_STREAMLIT_APP_URL_HERE`

Official documentation: - [Streamlit Community
Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud) -
[Streamlit deployment documentation](https://docs.streamlit.io/deploy)

## Data, models, and methodology

The project report describes a lookup-first design supported by
machine-learning models. It describes molecular representations and
descriptors being used to construct pair-level features, followed by
classification models for interaction severity and interaction type.

The report also describes evaluation using different data-splitting
strategies, including test settings where one or both drugs in a pair
are unseen during training.

**Reproducibility note:** Dataset counts, model metrics, thresholds, and
source coverage are reported project results and have not been
independently reproduced for this README. Verify them against the final
code, saved model artefacts, data versions, and experiment outputs
before presenting them as validated results.

Before publishing, document: - Exact dataset versions, sources, and
licences. - The source and version of each saved model. - Training and
evaluation scripts or reproducible commands. - Configured confidence
thresholds. - Preprocessing and filtering steps.

## Limitations

-   Interaction databases and medicine labels may be incomplete or out
    of date.
-   Database results are limited by the coverage and quality of the
    configured sources.
-   Machine-learning predictions are not clinical confirmation.
-   Performance may be lower for drugs or combinations not represented
    in training data.
-   Multi-drug mode evaluates individual pairs; it does not model every
    possible higher-order effect of a complete regimen.
-   The application does not necessarily account for patient-specific
    factors such as age, pregnancy, allergies, organ function, dose,
    route, or treatment history.
-   The print sheet records application output; it is not a prescription
    or clinical clearance.
-   Any optional AI-generated explanation is supplementary and should
    not replace underlying evidence.

## Responsible use

Use this application for academic demonstration and research exploration
only. Verify important information against reliable clinical references
and consult a qualified healthcare professional before making medication
decisions. Do not enter identifiable patient information.

## Project information

-   **Project:** PairCheck AI
-   **Student:** Prameet Basu Ray Chaudhury
-   **Programme:** B.Tech Biotechnology, Third Year
-   **Institution:** Amity University Kolkata
-   **Project organisation:** IDEAS -- Institute of Data Engineering,
    Analytics and Science Foundation, ISI Kolkata
-   **Project period:** 21 September 2026 -- 30 November 2026

Add the project mentor, official project title, repository URL, and
contact details if required by your final submission format.

## Acknowledgements and references

Add the exact bibliographic references, dataset documentation, model
references, and software versions used in the final project report. Cite
the sources and licences for all drug-interaction records, molecular
data, drug labels, and model-training data included in the repository.
