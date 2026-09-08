"""Source-bound CP04 regression, with separate exact-rational contractions.

The second contraction shares immutable observations and published gate
invariants, but neither the exporter coefficients nor its estimator code.
It is not an independent physical simulator or uncertainty calculation.
"""
from collections import defaultdict
import csv
from fractions import Fraction as F
import gzip
import hashlib
import importlib.util
import io
from pathlib import Path
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("supporting_export", ROOT / "scripts/analysis/reproduce_supporting_records.py")
EXPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORTER)
CURRENT = ROOT / "studies/checkpoint_04/results"


def read_csv(path):
    return list(csv.DictReader(path.open()))


@pytest.fixture(scope="module")
def generated(tmp_path_factory):
    output = tmp_path_factory.mktemp("supporting_exports")
    EXPORTER.export(ROOT / "entanglement-data.zip", output)
    return output


def test_complete_active_exports_reproduce_byte_for_byte(generated):
    EXPORTER.check_canonical(generated)
    assert len(read_csv(generated / "intervention_cross_architecture.csv")) == 30
    assert len(read_csv(generated / "response_stencil_decomposition.csv")) == 15


def test_every_endpoint_matches_separate_rational_stencil_and_audit():
    # Compute each row's four contributions first using exact decimal-rational
    # observations, then cell means, then equal-cell contrasts. This is not the
    # exporter's floating-point average-of-purity-shifts implementation.
    invariants = {"haar_or_clifford_2design": (F(3, 5), F(1, 2)),
                  "cartan_xy_pi8": (F(1, 2), F(1, 3)), "cartan_xx_pi4": (F(2, 3), F(1, 3))}
    actual = {(r["run"], r["family"], r["probe"]): r
              for r in read_csv(CURRENT / "intervention_cross_architecture.csv")}
    audit = {(r["run"], r["family"], r["probe"]): r for r in
             read_csv(ROOT / "audits/full-sanity-01/results/figure1_extension_points.csv")}
    decomposition = {(r["family"], r["probe"]): r for r in
                     read_csv(CURRENT / "response_stencil_decomposition.csv")}
    checked = 0
    with zipfile.ZipFile(ROOT / "entanglement-data.zip") as archive:
        for run in ("primary_rank4", "independent_seed_rank4"):
            member = f"checkpoint_04/data/intervention/{run}/state_response_rows.csv.gz"
            original = list(csv.DictReader(io.StringIO(gzip.decompress(archive.read(member)).decode())))
            for probe, (ep, gt) in invariants.items():
                by_cell = defaultdict(list)
                for row in original:
                    p = F(row["p_measure"])
                    if row["split"] != "confirmatory" or row["variant"] != "equalized_rank4" or p not in (F(2, 25), F(6, 25)):
                        continue
                    d = 2 ** (int(row["n"]) // 2)
                    norm = F(d, d - 1)
                    terms = (norm * (gt + F(5, 6) * ep) * F(row["P_A"]),
                             -norm * F(2, 3) * ep * F(row["P_L"]),
                             -norm * (gt - F(5, 6) * ep) * F(row["P_Lb"]),
                             -norm * F(2, 3) * ep * F(row["P_R"]))
                    by_cell[(row["family"], int(row["n"]), F(row["tau"]), p)].append(terms)
                for family in sorted({key[0] for key in by_cell}):
                    paired = sorted({(n, t) for f, n, t, p in by_cell if f == family and
                                     (f, n, t, F(2, 25)) in by_cell and (f, n, t, F(6, 25)) in by_cell})
                    component_means = []
                    for j in range(4):
                        differences = []
                        for n, t in paired:
                            high, low = by_cell[(family, n, t, F(6, 25))], by_cell[(family, n, t, F(2, 25))]
                            differences.append(sum(x[j] for x in high) / len(high) - sum(x[j] for x in low) / len(low))
                        component_means.append(sum(differences) / len(differences))
                    point = float(sum(component_means))
                    record = actual[(run, family, probe)]
                    assert point == pytest.approx(float(record["estimate"]), abs=2e-12, rel=0)
                    audit_run = "independent_rank4" if run == "independent_seed_rank4" else run
                    assert point == pytest.approx(float(audit[(audit_run, family, probe)]["direct"]), abs=2e-12, rel=0)
                    if run == "primary_rank4":
                        expected = decomposition[(family, probe)]
                        for value, name in zip(component_means, ("central_spectrum_contribution", "neighbor_P_L_contribution",
                                                                 "boundary_cross_P_Lb_contribution", "neighbor_P_R_contribution")):
                            assert float(value) == pytest.approx(float(expected[name]), abs=2e-12, rel=0)
                    checked += 1
    assert checked == 30


def test_all_stencil_totals_and_weighted_shift_columns():
    for row in read_csv(CURRENT / "response_stencil_decomposition.csv"):
        terms = [float(row[name]) for name in ("central_spectrum_contribution", "neighbor_P_L_contribution",
                                              "boundary_cross_P_Lb_contribution", "neighbor_P_R_contribution")]
        assert sum(terms) == pytest.approx(float(row["reconstruction"]), abs=2e-12, rel=0)
        assert float(row["reconstruction"]) == pytest.approx(float(row["observed_response_contrast"]), abs=2e-12, rel=0)
        assert abs(float(row["D_weighted_delta_P_A"])) < 2e-12


def test_mismatched_active_table_is_rejected(generated, tmp_path):
    for name in EXPORTER.FILES:
        (tmp_path / name).write_bytes((generated / name).read_bytes())
    path = tmp_path / "response_stencil_decomposition.csv"
    path.write_text(path.read_text().replace("reconstruction", "corrupt_reconstruction", 1))
    with pytest.raises(ValueError, match="Canonical supporting export differs"):
        EXPORTER.check_canonical(generated, tmp_path)


def test_changed_scientific_coefficient_is_rejected(monkeypatch):
    monkeypatch.setitem(EXPORTER.COEFFICIENTS, "cartan_xy_pi8", (F(1, 3), F(1, 4), F(1, 12), F(1, 3)))
    with pytest.raises(ValueError, match="Rowwise stencil"):
        EXPORTER.reconstruct(ROOT / "entanglement-data.zip")


def test_changed_original_member_is_rejected(tmp_path):
    with zipfile.ZipFile(tmp_path / "modified.zip", "w") as target:
        for member in EXPORTER.SOURCE_SHA256:
            target.writestr(member, b"altered")
    with pytest.raises(ValueError, match="Source-member identity mismatch"):
        EXPORTER.reconstruct(tmp_path / "modified.zip")


def test_original_defective_exports_remain_exactly_preserved():
    expected = {"intervention_cross_architecture.csv": "17e6a77e168d8bc2f0d7e10868dc3c63b74ad515c99bc40fb4468e3959936ca8",
                "response_stencil_decomposition.csv": "d699f444fe1e6af2e6b2185c40245011cefad1268178e8f21a1a3cf30ad57e19"}
    for name, digest in expected.items():
        content = (CURRENT / "historical/pre_full_sanity_01" / name).read_bytes()
        assert hashlib.sha256(content).hexdigest() == digest


def test_archived_intervals_are_explicitly_distinct_from_current_figure1():
    for row in read_csv(CURRENT / "intervention_cross_architecture.csv"):
        assert "ci_low" not in row and "ci_high" not in row
        assert row["interval_status"] == "archived_variable_support_not_regenerated"
        assert int(row["archived_bootstrap_reps"]) == 4000


def test_published_probe_coefficients_match_gate_invariants():
    invariants = {"haar_or_clifford_2design": (F(3, 5), F(1, 2)),
                  "cartan_xy_pi8": (F(1, 2), F(1, 3)), "cartan_xx_pi4": (F(2, 3), F(1, 3))}
    for row in read_csv(CURRENT / "probe_response_coefficients.csv"):
        ep, gt = invariants[row["probe"]]
        values = (F(2, 3) * ep, 1 - gt - F(5, 6) * ep, gt - F(5, 6) * ep, F(2, 3) * ep)
        for column, expected in zip(("c_I", "c_Fa", "c_Fb", "c_Fab"), values):
            assert float(row[column]) == pytest.approx(float(expected), abs=2e-15, rel=0)
