# Lecture notes build.
#
# Sources live here in src/; the single compiled document, all_sessions.pdf, is
# published one level up, in lecture_notes/, which is where the README links point.

MAIN = all_sessions

SESSIONS = classical_magnetism quantum_magnetism many_body_fermions \
           mps_spin_chains mps_fermionic

OUT = ..

.PHONY: all clean

all: $(OUT)/$(MAIN).pdf

# The combined document pulls the sessions in as subfiles, so it goes stale
# whenever any of them changes.
$(OUT)/$(MAIN).pdf: $(MAIN).tex $(addsuffix .tex,$(SESSIONS)) notes.sty
	latexmk -pdf -interaction=nonstopmode $(MAIN).tex
	mv $(MAIN).pdf $(OUT)/

clean:
	latexmk -C $(addsuffix .tex,$(MAIN) $(SESSIONS))
