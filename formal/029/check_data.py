"""Run the pinned data checks and reject deliberately malformed certificates."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent
DAG_SHA = "dc9841db1f84819e140a02e9d468a7bbaf062e974beff440fed5db3bcf1bd8ce"
POLICY_SHA = "80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227"
ODD_ROOT = "DL,BL,FL,UL,DB,DF,UB,UF,DR,BR,FR,UR:------------:1:0:18"


def commands(args, *, check=True):
    return subprocess.run(["lake", *args], cwd=ROOT, text=True, capture_output=True, check=check)


def require_hash(raw, expected):
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected:
        raise ValueError(f"Expected {expected}, got {digest}")
    print(f"SHA-256 {digest}", flush=True)


def reject(data, name, verifier):
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / f"{name}.json"
        path.write_text(json.dumps(data, separators=(",", ":")))
        failure = commands(["env", "lean", "--run", f"./{verifier}.lean", str(path)], check=False)
        if failure.returncode != 1 or failure.stdout:
            raise RuntimeError(f"Unexpected result for {name}: {failure}")
        print(f"REJECTED {name}: {failure.stderr.strip()}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dag", type=Path)
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    raw_dag = args.dag.read_bytes()
    if raw_dag[:2] == bytes((31, 139)):
        raw_dag = gzip.decompress(raw_dag)
    raw_policy = args.policy.read_bytes()
    require_hash(raw_dag, DAG_SHA)
    require_hash(raw_policy, POLICY_SHA)
    (ROOT / "EIGHTEEN_QUERY_DAG.json").write_bytes(raw_dag)
    (ROOT / "upper-policy-certificate.json").write_bytes(raw_policy)

    print(commands(["build"]).stdout, flush=True)
    for word, data in (("Eighteen", "EIGHTEEN_QUERY_DAG.json"),
                       ("Nineteen", "upper-policy-certificate.json")):
        print(commands(["env", "lean", "--run", f"./Verify{word}.lean", data]).stdout, flush=True)
        print(commands(["env", "lean", f"./{word}DataReceipt.lean"]).stdout, flush=True)

    print(commands(["env", "lean", "--run", "./VerifySemantic.lean",
                    "EIGHTEEN_QUERY_DAG.json"]).stdout, flush=True)
    print(commands(["env", "lean", "./EighteenCertified.lean"]).stdout, flush=True)
    print(commands(["env", "lean", "--run", "./SemanticControls.lean",
                    "EIGHTEEN_QUERY_DAG.json"]).stdout, flush=True)

    dag = json.loads(raw_dag)
    missing = dag.pop(ODD_ROOT)
    reject(dag, "missing_odd_root", "VerifyEighteen")
    dag[ODD_ROOT] = missing
    dag[ODD_ROOT][0] = "X"
    reject(dag, "wrong_color", "VerifyEighteen")
    dag = json.loads(raw_dag)
    leaf = next(row for key, row in dag.items() if key.endswith(":0"))
    leaf[1] = leaf[0]
    reject(dag, "duplicate_leaf_witness", "VerifyEighteen")

    policy = json.loads(raw_policy)
    root = next(row for row in policy["representatives"][0]["nodes"] if row[0] == "read")
    root[2].pop(next(iter(root[2])))
    reject(policy, "missing_upper_color_branch", "VerifyNineteen")


if __name__ == "__main__":
    main()
