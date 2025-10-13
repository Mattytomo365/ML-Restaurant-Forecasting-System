import json
'''
Handles model manifests
'''

def validate(manifest):
    if manifest.kind not in {"ridge","rf","xgb"}:
        raise ValueError(f"Unsupported kind: {manifest.kind}")
    if manifest.target not in {"sales","covers"}:
        raise ValueError(f"Unsupported target: {manifest.target}")
    if not manifest.features:
        raise ValueError("features must be non-empty")
    # ensure metrics contain MAE/MAPE
    for k in ("MAE","MAPE"):
        if k not in manifest.metrics:
            raise KeyError(f"metrics missing '{k}'")

def save_manifest(model_id, target, features, best_params, metrics, t, out): # Writes model manifest JSON (Human-readable model metadata for frontend use)
    manifest = {
        "model_id": model_id,
        "kind": metrics["kind"],
        "target": target,
        "features": features,
        "params": best_params,
        "metrics": {metrics["MAE"], metrics["MAPE"], metrics["RMSE"], metrics["R2"]},
        "created_at": t
    }
    validate(manifest)
    (out / "manifest.json").write_text(json.dumps(manifest))
    return str(out)

def read_manifest(model_id: str):

    return

def list_models():
    return

def set_active(): # Write ACTIVE.txt
    return

def get_active(): # Read ACTIVE.txt
    return