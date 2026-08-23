"""Canonical index audit for prime-selector experiments.

An array position is not a physically meaningful index. Degenerate
eigenspaces make prime membership representation-dependent.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class CanonicalIndexAudit:
    indexed_object: str
    dimensionless: bool
    reproducible_convention: bool
    basis_dependent: bool
    ordering_arbitrary: bool
    degeneracies: list[tuple[float, int]]
    degenerate: bool
    selector_acts_on: str
    symmetry_preserved: bool | None
    index_is_object_invariant: bool
    valid_for_physical_prime_test: bool
    allowed_as_encoding_experiment: bool
    answers: dict[str, str]
    warnings: list[str] = field(default_factory=list)


def audit_canonical_index(
    eigenvalues: np.ndarray,
    *,
    indexed_object: str = "eigenmode label",
    dimensionless: bool = True,
    convention: str = "sort_by_eigenvalue_then_first_nonzero_component",
    basis_vectors: np.ndarray | None = None,
    selector_acts_on: str = "individual_basis_vectors",
    symmetry_preserved: bool | None = None,
    atol: float = 1e-8,
) -> CanonicalIndexAudit:
    values = np.asarray(eigenvalues, dtype=float)
    degeneracies: list[tuple[float, int]] = []
    used = np.zeros(values.size, dtype=bool)
    for i, val in enumerate(values):
        if used[i]:
            continue
        group = np.where(np.abs(values - val) <= atol)[0]
        if group.size > 1:
            degeneracies.append((float(val), int(group.size)))
            used[group] = True
    degenerate = bool(degeneracies)
    basis_dependent = degenerate and selector_acts_on == "individual_basis_vectors"
    ordering_arbitrary = degenerate
    valid = (
        dimensionless
        and not basis_dependent
        and selector_acts_on == "invariant_eigenspaces"
        and not ordering_arbitrary
    )
    # A nondegenerate spectrum with a declared convention can be confirmatory.
    if dimensionless and not degenerate and convention:
        valid = True
    warnings: list[str] = []
    if degenerate:
        warnings.append(
            "Degenerate eigenvalues are present. Any orthogonal mixture of "
            "an eigenspace may be assigned different integer labels. Prime "
            "membership of those labels is therefore basis- and order-"
            "dependent. The index is not an invariant of the object."
        )
    if basis_dependent:
        warnings.append(
            "The selector acts on individual basis vectors rather than "
            "invariant eigenspaces. Equivalent representations can change "
            "which modes are labeled prime."
        )
    if not dimensionless:
        warnings.append(
            "The index is not dimensionless. Unit-dependent labels such as "
            "'5 Hz' must not be treated as prime."
        )
    answers = {
        "What mathematical object is being indexed?": indexed_object,
        "Is the index dimensionless?": "yes" if dimensionless else "no",
        "Is the indexing convention reproducible?": convention or "unspecified",
        "Does changing basis alter the index?": "yes" if basis_dependent else "not established",
        "Does mode ordering depend on arbitrary numerical choices?": (
            "yes" if ordering_arbitrary else "not for the declared convention"
        ),
        "Are there degeneracies?": "yes" if degenerate else "no",
        "How are degenerate eigenspaces treated?": (
            "not invariant; labels attach to basis vectors"
            if basis_dependent
            else "no degeneracy or selector declared on eigenspaces"
        ),
        "Does the selector act on individual basis vectors or invariant eigenspaces?": selector_acts_on,
        "Is the index preserved under relevant symmetries?": (
            "unknown" if symmetry_preserved is None else str(symmetry_preserved)
        ),
    }
    return CanonicalIndexAudit(
        indexed_object=indexed_object,
        dimensionless=dimensionless,
        reproducible_convention=bool(convention),
        basis_dependent=basis_dependent,
        ordering_arbitrary=ordering_arbitrary,
        degeneracies=degeneracies,
        degenerate=degenerate,
        selector_acts_on=selector_acts_on,
        symmetry_preserved=symmetry_preserved,
        index_is_object_invariant=valid and not degenerate,
        valid_for_physical_prime_test=valid and not degenerate,
        allowed_as_encoding_experiment=True,
        answers=answers,
        warnings=warnings,
    )
