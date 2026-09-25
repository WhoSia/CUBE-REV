# P15-R1 failure localization

P15's 70.949% discrepancy was an adapter failure, not a data verdict. The R0
adapter replaced any nonliteral `LETTER` with `chr(KEYCODE)`, thereby imposing
physical key identity as emitted text. That conflated Layer K with Layer L and
destroyed browser-recorded punctuation, layout-dependent output, and collector
keypress overrides. Modifiers were also counted as ambiguous edits.

Localized classes: keycode-interpreted-as-character; Shift/case and
punctuation/symbol failure; browser-event semantic mismatch; missing/nonemitting
modifier misclassification; and final-input comparison against an incorrectly
reconstructed Layer T. The raw parsing anomalies (180 target-missing streams;
three missing press/release values) are separately retained and do not explain
the high-mass discrepancy.

No hazard, timing, transport, or error-state conclusion is authorized until
the Layer-L-authoritative adapter completes its census and revalidation.
