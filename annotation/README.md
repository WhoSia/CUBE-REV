# CUBE-REV 0.7.12 two-pass annotation

Pass A contains the event trace but removes participant linkage, experimental
condition, history visibility, and probe answers. Annotators mark episode
boundaries, one label, confidence, and notes.

Pass B is opened only after Pass A is complete and hashed. It adds the assigned
condition, visibility-gated history facts, probe arm, and response context.
Pass B never overwrites Pass A.

Labels are `REPLAY`, `GEODESIC_PLANNING`, `ALGORITHMIC_CHUNK`, `LOCAL_SEARCH`,
`FRAME_REPAIR`, `INPUT_RECOVERY`, `PERIODIC_POLICY`, `DISENGAGEMENT`, and
`OTHER_OR_MIXED`.

Three independent annotators are required by governance before prospective
activation. This repository does not contain annotator identities or raw human
records.
