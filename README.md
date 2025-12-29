# mathviz

## Install

'''sh
sudo apt update

# Required Dependencies

sudo apt install build-essential python3-dev libcairo2-dev libpango1.0-dev ffmpeg

# Optional Dependencies

sudo apt install texlive texlive-latex-extra
poetry install
'''

## Run a scene

'poetry run python -m manim -ql scenes/<scene>.py'

## Available visualizations

| Category | Scene classes | Highlights | Example run |
| --- | --- | --- | --- |
| Intro demo | `SquareToCircle` (`scenes/quickstart.py`) | Minimal Manim example that creates a square, morphs it into a circle, then fades out—useful when validating your toolchain. | `poetry run python -m manim -ql scenes/quickstart.py SquareToCircle` |
| Prime factors & number theory | `PrimeFactorDecomposition`, `PGCD`, `GCDLCMScene` (`scenes/prime_factor_decomposition.py`) | Animates the full long-division style prime factorization of integers, highlights shared primes, then derives and explains GCD/LCM with SymPy-backed arithmetic. | `poetry run python -m manim -ql scenes/prime_factor_decomposition.py PrimeFactorDecomposition` |
| Algebra walkthroughs | `Mul1`, `Mul2`, `SimpleDistrib1`, `DoubleDistrib1`, `Add1`, `MinusParenthesis1`, `MinusParenthesis2`, `CombinedScene` (`scenes/calcullit/main.py`) | Sequence of classroom-style manipulations (grouping coefficients, distribution, combining like terms). Each scene color-codes token groups and chains MathTex transforms; `CombinedScene` plays the full set back-to-back. | `poetry run python -m manim -ql scenes/calcullit/main.py SimpleDistrib1` |
| Coordinate transformations | `Sx`, `Sy`, `So`, `Rop`, `Ron` (`scenes/isocoord/main.py`) plus refactored counterparts (`scenes/isocoord/refacto.py`) | Shows reflections across axes, central symmetry, and ±90° rotations. Every scene writes the algebraic rule, maps a concrete point, and plots the transformation on an annotated grid. The refactored versions share a base class for quicker iteration. | `poetry run python -m manim -ql scenes/isocoord/main.py Rop` |
| Vector operations | `VectorAddDiffGrid`, `VectorAddDiffNoGrid`, `VectorAddMulti` (`scenes/vectors/addition.py`) | Demonstrates head-to-tail vector addition/subtraction with and without a grid, including negative vectors and multi-vector chains, complete with labeled result arrows. | `poetry run python -m manim -ql scenes/vectors/addition.py VectorAddDiffGrid` |
| Symbolic helpers | `StepByStepScene` subclasses & `CustomScene` (`scenes/calcullit/poc.py`), `ColorSubstringExample` (`scenes/isocoord/substrings.py`) | Utility scenes for rapid prototyping: parse LaTeX with SymPy to show expansion/simplification steps or color specific substrings inside MathTex expressions when building bespoke lessons. | `poetry run python -m manim -ql scenes/calcullit/poc.py SimplificationScene1` |
