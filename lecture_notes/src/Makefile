# Lecture notes build.
#
# Sources live here in src/; the compiled PDFs are published one level up, in
# lecture_notes/, which is where the README links point.

DOCS = all_sessions classical_magnetism quantum_magnetism many_body_fermions \
       mps_spin_chains mps_fermionic

OUT = ..

PDFS = $(addprefix $(OUT)/,$(addsuffix .pdf,$(DOCS)))

.PHONY: all clean

all: $(PDFS)

$(OUT)/%.pdf: %.tex notes.sty
	latexmk -pdf -interaction=nonstopmode $<
	mv $*.pdf $(OUT)/

# The combined document pulls the sessions in as subfiles, so it goes stale
# whenever any of them changes.
$(OUT)/all_sessions.pdf: $(addsuffix .tex,$(DOCS))

clean:
	latexmk -C $(addsuffix .tex,$(DOCS))
