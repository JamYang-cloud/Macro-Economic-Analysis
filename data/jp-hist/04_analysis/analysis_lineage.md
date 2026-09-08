# H4 analysis lineage (2026-09-06 v0.3 gate)

所有 H4 v0.3 产物共享 method/calibration/coverage/metric ID 体系。历史产物按状态归档于 archive/。

## ID 体系
- method_id: H4-SIM-2026-09 (fixed-lag + nearest-state + coverage-gated module-mean)
- calibration_id: JPZ-1970-2025 / CNZ-2000-2025 (robust-z full-sample within-country)
- coverage_rule_id: CR-2026-09 (total>=70% eligible modules, module>=50% pairs, >=4 modules)
- metric_id: RANKSTATE / MANHATTAN / EUCLID / PERCENTILE / WASSDIST
- source_feature_version: H3-FEAT-20260906-v01 + CNPANEL-2000-2025 + JPPANEL-1970-2025

## 状态记录
- h4_hyp2_c0_jp2025.csv = CURRENT (calibration JPZ-1970-2025, method H4-SIM-2026-09 exploratory variant, coverage>=1pair)
- archive/*.csv = SUPERSEDED (JP window 1970-2000 truncation or v0.1 calibration)
