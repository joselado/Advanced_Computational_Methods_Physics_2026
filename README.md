# Advanced Computational Methods in Physics 2026: Quantum many body and tensor networks
Teaching material for the course PHYS-E0510, Advanced Computational Methods in Physics D:
Quantum many body and tensor networks, at Aalto University (2026).

Each of the five sessions comes with a set of lecture slides, a short set of lecture notes, and a
Jupyter notebook reproducing the calculations discussed in the lecture. The notebooks also have
questions that require you to modify the examples in order to answer them.

## Installation
The Jupyter notebooks require that you install the following two libraries

- [pyqula](https://github.com/joselado/pyqula): Session 1
- [dmrgpy](https://github.com/joselado/dmrgpy): Sessions 2, 3, 4, 5

Check the link of each library to know how to install it

## Lecture slides
- [Session 1: Many-body interactions and classical symmetry broken magnetism](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/slides/classical_magnetism.pdf)
- [Session 2: Many-body quantum magnets](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/slides/quantum_magnetism.pdf)
- [Session 3: Many-body correlated fermionic systems](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/slides/many_body_fermions.pdf)
- [Session 4: Tensor networks for many-body quantum magnets](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/slides/mps_spin_chains.pdf)
- [Session 5: Tensor networks for many-body correlated fermionic systems](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/slides/mps_fermionic.pdf)
- [Machine learning for quantum states](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/slides/machine_learning_quantum.pdf) (slides only, no notebook or lecture notes)

## Lecture notes
Short lecture notes for each session, plus a single combined document covering all five

- [All sessions (combined)](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/lecture_notes/all_sessions.pdf)
- [Session 1: Many-body interactions and classical symmetry broken magnetism](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/lecture_notes/classical_magnetism.pdf)
- [Session 2: Many-body quantum magnets](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/lecture_notes/quantum_magnetism.pdf)
- [Session 3: Many-body correlated fermionic systems](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/lecture_notes/many_body_fermions.pdf)
- [Session 4: Tensor networks for many-body quantum magnets](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/lecture_notes/mps_spin_chains.pdf)
- [Session 5: Tensor networks for many-body correlated fermionic systems](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/lecture_notes/mps_fermionic.pdf)

The notes are written in LaTeX; each session's source sits next to its PDF in `lecture_notes`, and
the combined document pulls them in as subfiles. Build any of them with

```bash
cd lecture_notes && latexmk -pdf all_sessions.tex
```

## Jupyter notebooks
- [Session 1: Many-body interactions and classical symmetry broken magnetism](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/jupyter-notebooks/classical_magnetism.ipynb)
- [Session 2: Many-body quantum magnets](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/jupyter-notebooks/quantum_magnetism.ipynb)
- [Session 3: Many-body correlated fermionic systems](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/jupyter-notebooks/quantum_interacting_fermions.ipynb)
- [Session 4: Tensor networks for many-body quantum magnets](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/jupyter-notebooks/mps_quantum_magnets.ipynb)
- [Session 5: Tensor networks for many-body correlated fermionic systems](https://github.com/joselado/Advanced_Computational_Methods_Physics_2026/blob/main/jupyter-notebooks/mps_many_body_fermionic.ipynb)

## Lecture recordings
Recordings of the video lectures, from the previous edition of the course
- [Session 1: Many-body interactions and classical symmetry broken magnetism](https://youtu.be/yzWwW8gNXYE)
- [Session 2: Many-body quantum magnets](https://youtu.be/QI3EhsFmkAs)
- [Session 3: Many-body correlated fermionic systems](https://youtu.be/e-v1kEi91jg)
- [Session 4: Tensor networks for many-body quantum magnets](https://youtu.be/VGZlR3KEIgE)
- [Session 5: Tensor networks for many-body correlated fermionic systems](https://youtu.be/pp5-t_dCtg0)
