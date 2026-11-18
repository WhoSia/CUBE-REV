# CUBE-REV 0.29 S — Independent check of the 18-read certificate

The integrated manuscript retains the 21/19 paired-frame optima, the 22/20 edge-color-only optima, and the independently replayable 19-frame upper policy. Two separate R manuscript lines are cited in the S editorial record.

The lower-bound checker derives the child by lifting a reference arrangement and measuring its parity offsets. It then lifts a checked pair from every child into the parent. Both signs pass at the root. The audit covers 6,274 nodes, 43,870 query–reply arcs, 1,418 leaves and 87,740 individual lifted assignments. Six certificate corruptions are rejected.

The original certificate is pinned at `974c931f136fe63f41269805c21152a859961b6d:data/0.29/EIGHTEEN_QUERY_DAG.json.gz`. Its uncompressed SHA-256 is `dc9841db1f84819e140a02e9d468a7bbaf062e974beff440fed5db3bcf1bd8ce`.

```bash
python3 scripts/cuberev-observation/verify_18_lifted_dag.py data/0.29/EIGHTEEN_QUERY_DAG.json.gz
python3 scripts/cuberev-observation/test_18_lifted_dag_mutations.py data/0.29/EIGHTEEN_QUERY_DAG.json.gz
```

- [Independent checker](https://github.com/WhoSia/CUBE-REV/commit/15a01ca53b33e246e74086423473ecadecee4e68)
- [Damaged-certificate checks](https://github.com/WhoSia/CUBE-REV/commit/a87f29ad507d700e7940e99802b089450b63ee31)
- [Upper checker refuses disabled assertions](https://github.com/WhoSia/CUBE-REV/commit/3f0c0cb1cd49e918d4ed76b4d95c9c1f8fa5c856)
- [Integrated S manuscript, figures, certificates and receipts](https://drive.google.com/file/d/1g5NCo2vqcjaiHGaSUEiL_OZoy3naY4SV/view?usp=drivesdk)

The verified DAG assumes the cubie legality and residual coordinate transformations in the manuscript. The physical replay remains a worked case, and the accompanying Lean formalization covers auxiliary results.
