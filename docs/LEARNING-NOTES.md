# How to read the learning visuals

These illustrations were created as educational material for this portfolio. They are separate from the completed cosmology and materials projects. The small examples are intended to be read, reproduced, and understood.

[Back to the profile](../README.md) · [Editable generator](../scripts/build_profile_assets.py)

## Quantum gates

A one-qubit state has two amplitudes:

$$|\psi\rangle = a|0\rangle+b|1\rangle,\qquad |a|^2+|b|^2=1.$$

The bars show the computational-basis probabilities $P(0)=|a|^2$ and $P(1)=|b|^2$. They describe what a measurement would return at that stage, over many independently prepared copies of the state. They are not simulated shot counts.

The ideal gates are

$$H=\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad X=\begin{pmatrix}0&1\\1&0\end{pmatrix}.$$

| Stage | Operation applied | State | P(0) | P(1) |
| --- | --- | --- | ---: | ---: |
| 0 | Prepare zero | $\lvert0\rangle$ | 1 | 0 |
| 1 | H | $\lvert+\rangle=(\lvert0\rangle+\lvert1\rangle)/\sqrt{2}$ | 1/2 | 1/2 |
| 2 | H again | $\lvert0\rangle$ | 1 | 0 |
| 3 | X | $\lvert1\rangle$ | 0 | 1 |

There is **no measurement between the gates**. Applying H twice gives the identity: the amplitudes for zero add, and those for one cancel. If we measured after the first H, that would be a different experiment; a subsequent H would not deterministically restore zero. X exchanges the two basis amplitudes.

The animation changes only at the four discrete circuit stages. It does not model the physical time evolution of a hardware pulse, noise, decoherence, or an experiment on a quantum processor. Highlighted gates have already been applied; the bars and state label refer to the same stage.

**Try explaining:** Why do equal measurement probabilities after H not mean the qubit has already collapsed to an unknown classical bit?

Existing practice: [qubits and measurement](https://github.com/asp123-cyber/Quantum_Computing_basic/blob/main/01_qubits_and_measurement.ipynb) · [single-qubit gate examples](https://github.com/asp123-cyber/Quantum_Computing_basic/blob/main/single_qubit_gates.py).

## Machine learning and vision

The two panels illustrate different operations. The left model learns coefficients from labeled examples. The right image filter has fixed, explicitly chosen coefficients.

### Fitting a decision boundary

The left panel uses logistic regression:

$$p(y=1\mid x)=\sigma(w_1x_1+w_2x_2+b),\qquad\sigma(z)=\frac{1}{1+e^{-z}}.$$

The plotted line is the decision boundary $w_1x_1+w_2x_2+b=0$, corresponding to a predicted probability of one half. Dot colors indicate the supplied class labels, not the model's predictions. Each coordinate is an abstract synthetic feature, not a measurement from a research dataset.

The generator makes 32 samples: 16 per class, using Python's `random.Random(218)`. Each coordinate is Gaussian with standard deviation 0.78, centered at −0.72 for class zero and +0.72 for class one, then clipped to [−2.5, 2.5]. The overlap makes this a deliberately imperfect classification problem.

Weights and bias start at zero. Full-batch gradient descent minimizes mean binary cross-entropy, using learning rate 0.15 and no regularization. Frames show steps 0, 20, 100, and 400. Initially every prediction is 0.5, so there is no unique boundary to draw. The later boundaries are computed from the actual fitted weights.

This is a **training illustration**. There is no held-out evaluation or claim of predictive performance. The decreasing training loss is a numerical check, not evidence that a model generalizes.

**Try explaining:** Why can a visually attractive boundary still fail on new data?

Existing work: [ML foundations](https://github.com/asp123-cyber/machine-learning-foundations) · [housing-price exercise and existing diagnostic figures](https://github.com/asp123-cyber/machine-learning-foundations/tree/main/09_project_housing_price_prediction). The new synthetic illustration is not a reproduction of those housing results. The housing script supports both a real-data download and a labeled synthetic fallback; no housing benchmark numbers are asserted in this profile.

### Revealing an edge

The right panel starts with a 5×5 binary image. Every row is `[0, 0, 0, 1, 1]`, giving a vertical edge. It uses the horizontal-gradient Sobel kernel

$$K=\begin{pmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{pmatrix}.$$

The implementation performs **true convolution**: it flips the kernel, uses stride one, and keeps only the valid region, without padding. A 5×5 image and 3×3 kernel therefore produce a 3×3 result. The signed output has the row `[0, −4, −4]` repeated three times. The display shows its absolute value, `[0, 4, 4]`, to emphasize edge magnitude.

For example, the first patch is all zero and gives zero. In the next patch, the rightmost image column contains ones. It is multiplied by the flipped kernel's rightmost column, `[-1, −2, −1]`, giving −4. The displayed magnitude is 4. A constant patch gives zero because the kernel coefficients sum to zero.

The highlighted input window and output cell correspond to each other. The complete output is shown throughout; the animation moves the inspection window across selected positions, rather than claiming to show a full raster scan.

This fixed filter is **image processing, not a trained neural network**. It shows how local structure can be extracted from an image. A learned convolutional layer can optimize its coefficients from data, which is a separate concept.

**Try explaining:** Why does a constant-intensity patch have no response, while an intensity change does?

## Reproduce and inspect

From the repository root:

```bash
python3 scripts/build_profile_assets.py
```

The script uses Python's standard library. It regenerates all light/dark, desktop/compact, animated/still assets and checks:

- State normalization, the four expected probability pairs, H² = I, and X² = I.
- The logistic-regression gradient against independent finite differences.
- Decreasing training loss and the equation of every plotted decision boundary.
- The convolution's signed result, a constant image's zero response, and reversal of the edge direction.
- Well-formed SVGs without scripts.

The animation lasts ten seconds and plays once. Its final frame remains visible. CSS reduced-motion preferences show the final frame immediately; standalone still images are also available in both themes and sizes.

## Additional educational simulation

The existing [One qubit, two classes lab](https://asp123-cyber.github.io/asp123-cyber/lab/) remains available with its [method and source](../lab/README.md). It explores a one-qubit fidelity kernel and an equivalent classical feature representation. It is supplementary learning material, not evidence of an original quantum-ML research result or a quantum advantage.
