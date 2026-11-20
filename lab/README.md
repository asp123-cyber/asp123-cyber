# One qubit, two classes

An interactive, noiseless simulation of a fidelity kernel classifier on angles. Change the winding and compare held-out predictions against a raw-angle linear model and an independently fitted, analytically equivalent classical Fourier model.

[Open the live experiment ↗](https://asp123-cyber.github.io/asp123-cyber/lab/) · [Read the source](index.html) · [Download the standalone HTML](https://raw.githubusercontent.com/asp123-cyber/asp123-cyber/main/lab/index.html)

## Encoding and model

For an angle $x$ in radians and a winding $m$ in $\{1,2,3\}$, the feature state is

$$
|\psi_m(x)\rangle = R_y(mx)|0\rangle =
\cos(mx/2)|0\rangle + \sin(mx/2)|1\rangle.
$$

The squared overlap gives a positive semidefinite kernel with a three-dimensional real feature representation:

$$
K_m(x,z)=|\langle\psi_m(x)|\psi_m(z)\rangle|^2
=\frac{1+\cos(m(x-z))}{2}
=\phi_m(x)^\mathsf{T}\phi_m(z), \qquad
\phi_m(x)=\frac{(1,\cos(mx),\sin(mx))}{\sqrt{2}}.
$$

All three models use the same ridge penalty $\lambda=0.35$ and a zero decision threshold. The quantum model evaluates real statevectors and solves $(K+\lambda I)\alpha=y$. The Fourier control solves the corresponding primal problem from its explicit features. The linear baseline uses $(1,x/\pi)$. The two equivalent models can be checked against each other numerically without sharing fitted weights.

## Reference run

The class label is the sign of $\cos(2x)$. Training and test inputs come from two separately jittered uniform grids on $[-\pi,\pi)$, with 64 training samples (seed 31415) and 48 held-out samples (seed 27182).

| Encoding | Fidelity kernel | Matched Fourier | Raw-angle linear |
|---|---:|---:|---:|
| 1× | 24 / 48 | 24 / 48 | 24 / 48 |
| 2× | 48 / 48 | 48 / 48 | 24 / 48 |
| 3× | 24 / 48 | 24 / 48 | 24 / 48 |

The target is constructed to have frequency two. Matching that frequency supplies the feature the readout needs. The agreement between the statevector and Fourier models illustrates classical equivalence for this encoding. The counts describe one synthetic dataset.

## Run locally

Download `index.html` and open it in a modern browser. Everything needed to reproduce the experiment, including its data generator, model, graphics and display fonts, is inside this one file. Use the winding controls to refit the models and the probe slider to inspect the state and decision score at any angle.

## Reference

Havlíček et al. (2019), *Supervised learning with quantum-enhanced feature spaces*, [Nature 567, 209–212](https://doi.org/10.1038/s41586-019-0980-2). This demonstration uses a simpler one-qubit feature map.
