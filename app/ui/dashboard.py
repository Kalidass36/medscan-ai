import json
import tempfile
from pathlib import Path

import streamlit as st

from app.pipeline.pipeline import run_pipeline
from app.validation.validator import FLAGGED, SAFETY_NOTICE


st.set_page_config(page_title="MedScan-AI", page_icon=":material/health_and_safety:", layout="wide")


def _prepare_upload(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    data = uploaded_file.getvalue()
    if suffix not in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".pdf"}:
        raise ValueError("Unsupported file format.")

    preview = data
    if suffix == ".pdf":
        try:
            import fitz
        except ImportError as error:
            raise ValueError("PDF processing requires the PyMuPDF package.") from error
        document = fitz.open(stream=data, filetype="pdf")
        if not document.page_count:
            raise ValueError("Unable to process document.")
        preview = document[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).tobytes("png")
        suffix = ".png"

    temporary_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    temporary_file.write(preview)
    temporary_file.close()
    return Path(temporary_file.name), preview


def _render_entity(entity, minimum_confidence):
    meets_confidence = entity.get("confidence", 0) >= minimum_confidence
    validated = entity.get("validated") and meets_confidence
    status = "Validated" if validated else "Needs human review"
    icon = ":material/check_circle:" if validated else ":material/warning:"
    with st.container(border=True):
        st.markdown(f"**{entity['type']}**")
        st.subheader(entity["word"])
        st.caption(f"Confidence: {entity.get('confidence', 0):.0%}")
        st.write(f"{icon} {status}")
        st.caption("Source: OCR text")


def _render_relationship(relationship):
    with st.container(border=True):
        st.markdown(
            f"**{relationship['drug']}**  \n"
            f"↓  \n"
            f"**{relationship['dosage']}**  \n"
            f"↓  \n"
            f"**{relationship['condition']}**"
        )


st.title("MedScan-AI")
st.caption("Clinical document intelligence")
st.warning(SAFETY_NOTICE)
minimum_confidence = st.sidebar.slider("Minimum confidence", 0.0, 1.0, 0.8, 0.05)

with st.form("document_form"):
    uploaded_file = st.file_uploader(
        "Upload clinical document",
        type=["png", "jpg", "jpeg", "tif", "tiff", "pdf"],
    )
    submitted = st.form_submit_button("Process document", icon=":material/arrow_forward:")

if submitted:
    if uploaded_file is None:
        st.error("Unable to process document.")
    else:
        temporary_path = None
        try:
            temporary_path, preview = _prepare_upload(uploaded_file)
            with st.status("Processing document", expanded=True) as status:
                result = run_pipeline(temporary_path)
                status.update(label="Processing complete", state="complete")
            temporary_path.unlink(missing_ok=True)

            st.header("Original document")
            st.image(preview, caption=uploaded_file.name, width="stretch")

            st.header("AI extraction")
            if result["entities"]:
                for entity in result["entities"]:
                    _render_entity(entity, minimum_confidence)
            else:
                st.info("No medical entities detected.")

            flagged = [
                entity for entity in result["entities"]
                if not entity["validated"] or entity.get("confidence", 0) < minimum_confidence
            ]
            if flagged:
                for entity in flagged:
                    st.warning(
                        f'Drug or condition "{entity["word"]}" was not found in the configured knowledge base. '
                        "Human review required."
                    )

            st.header("Relationship")
            if result["relationships"]:
                for relationship in result["relationships"]:
                    _render_relationship(relationship)
            else:
                st.info("No complete drug-dosage-condition relationship detected.")
                if any(entity["type"] == "DRUG" for entity in result["entities"]):
                    st.warning("Dosage not detected or relationship requires human review.")

            st.header("Validation")
            validated_count = sum(
                entity["validated"] and entity.get("confidence", 0) >= minimum_confidence
                for entity in result["entities"]
            )
            total_count = len(result["entities"])
            with st.container(horizontal=True):
                st.metric("Entities detected", total_count, border=True)
                st.metric("Validated", validated_count, border=True)
                st.metric("Flagged", total_count - validated_count, border=True)
                st.metric(
                    "Validation rate",
                    f"{validated_count / total_count:.1%}" if total_count else "0.0%",
                    border=True,
                )
            st.json(result["validation"])

            st.header("FHIR output")
            if result["fhir"]:
                fhir_json = json.dumps(result["fhir"], indent=2)
                st.json(result["fhir"])
                st.download_button(
                    "Download FHIR JSON",
                    data=fhir_json,
                    file_name="medication_request.json",
                    mime="application/fhir+json",
                    icon=":material/download:",
                )
                report = {
                    "entities": result["entities"],
                    "relationships": result["relationships"],
                    "validation": result["validation"],
                    "fhir": result["fhir"],
                }
                st.download_button(
                    "Download extraction report",
                    data=json.dumps(report, indent=2),
                    file_name="medscan_report.json",
                    mime="application/json",
                    icon=":material/description:",
                )
            else:
                st.warning("FHIR output was not generated because no validated relationship was found.")
        except ValueError as error:
            st.error(str(error))
        except Exception:
            st.error("Unable to process document.")
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)