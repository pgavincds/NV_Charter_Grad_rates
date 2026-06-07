from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd


PLOTLY_CDN = "https://cdn.plot.ly/plotly-2.35.2.min.js"


def _write_plotly_html(path: Path, title: str, traces: list[dict], layout: dict, note: str = "") -> None:
    payload = {
        "traces": traces,
        "layout": layout,
    }
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <script src="{PLOTLY_CDN}"></script>
  <style>
    body {{
      font-family: Georgia, "Times New Roman", serif;
      background: #f5f1e8;
      color: #1f2a2e;
      margin: 0;
      padding: 2rem;
    }}
    .wrap {{
      max-width: 1100px;
      margin: 0 auto;
    }}
    .note {{
      color: #4a5d63;
      margin: 0 0 1rem 0;
    }}
    #chart {{
      width: 100%;
      height: 720px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>{title}</h1>
    <p class="note">{note}</p>
    <div id="chart"></div>
  </div>
  <script>
    const payload = {json.dumps(payload)};
    Plotly.newPlot("chart", payload.traces, payload.layout, {{responsive: true, displayModeBar: true}});
  </script>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def _series_trace(df: pd.DataFrame, series_id: str, label: str, color: str) -> dict:
    sub = df[df["series_id"] == series_id].sort_values("year")
    return {
        "type": "scatter",
        "mode": "lines+markers",
        "name": label,
        "x": sub["year"].tolist(),
        "y": sub["weighted_acgr"].tolist(),
        "line": {"color": color, "width": 3},
        "marker": {"size": 8},
        "hovertemplate": "%{x}<br>%{y:.2f}%<extra>" + label + "</extra>",
    }


def _bar_trace(df: pd.DataFrame, xcol: str, ycol: str, name: str, color: str) -> dict:
    return {
        "type": "bar",
        "name": name,
        "x": df[xcol].tolist(),
        "y": df[ycol].tolist(),
        "marker": {"color": color},
        "hovertemplate": "%{x}<br>%{y:,}<extra>" + name + "</extra>",
    }


def build_visualizations(release_root: Path) -> None:
    clean_dir = release_root / "03_Clean_Data"
    viz_dir = release_root / "05_Visualizations"
    viz_dir.mkdir(parents=True, exist_ok=True)

    weighted = pd.read_csv(clean_dir / "weighted_sector_series.csv")
    audit = pd.read_csv(release_root / "04_Audit_Files" / "weighted_line_items_audit_release.csv")

    trend_traces = [
        _series_trace(weighted, "statewide_official", "Statewide Official", "#1f2a2e"),
        _series_trace(weighted, "spcsa_official", "SPCSA Official", "#b23a48"),
        _series_trace(weighted, "spcsa_adjusted_charter_only", "SPCSA Charter Only", "#0f5c63"),
        _series_trace(weighted, "spcsa_brick_mortar", "SPCSA Brick & Mortar", "#147a4b"),
        _series_trace(weighted, "spcsa_virtual", "SPCSA Virtual", "#2a6fdb"),
        _series_trace(weighted, "spcsa_alternative", "SPCSA Alternative", "#a05a00"),
    ]
    _write_plotly_html(
        viz_dir / "weighted_acgr_trend.html",
        "Weighted ACGR Trend",
        trend_traces,
        {
            "paper_bgcolor": "#f5f1e8",
            "plot_bgcolor": "#fffaf2",
            "xaxis": {"title": "Graduating Class Year"},
            "yaxis": {"title": "Weighted ACGR (%)", "range": [0, 100]},
            "legend": {"orientation": "h", "y": -0.2},
        },
        "Weighted ACGR is the primary sector measure. It reflects the average student rather than the average school.",
    )

    graduates = (
        weighted[weighted["series_id"].isin(["spcsa_adjusted_charter_only", "clark_charter_total", "washoe_charter_total"])]
        .pivot(index="year", columns="series_label", values="graduates")
        .fillna(0)
        .reset_index()
    )
    graduate_traces = [
        _bar_trace(graduates, "year", col, col, color)
        for col, color in [
            ("Clark Charter Total", "#2a6fdb"),
            ("SPCSA Charter Only", "#0f5c63"),
            ("Washoe Charter Total", "#a05a00"),
        ]
        if col in graduates.columns
    ]
    _write_plotly_html(
        viz_dir / "graduates_produced_by_year.html",
        "Graduates Produced By Year",
        graduate_traces,
        {
            "barmode": "group",
            "paper_bgcolor": "#f5f1e8",
            "plot_bgcolor": "#fffaf2",
            "xaxis": {"title": "Graduating Class Year"},
            "yaxis": {"title": "Graduates"},
        },
        "This is a core policy chart: it shows how many students actually graduated, not just whether rates rose or fell.",
    )

    composition = (
        weighted[weighted["series_id"].isin(["spcsa_brick_mortar", "spcsa_virtual", "spcsa_alternative"])]
        .pivot(index="year", columns="series_label", values="cohort")
        .fillna(0)
        .reset_index()
    )
    composition_traces = [
        {
            "type": "bar",
            "name": col,
            "x": composition["year"].tolist(),
            "y": composition[col].tolist(),
            "hovertemplate": "%{x}<br>%{y:,}<extra>" + col + "</extra>",
        }
        for col in ["SPCSA Brick & Mortar", "SPCSA Virtual", "SPCSA Alternative"]
        if col in composition.columns
    ]
    _write_plotly_html(
        viz_dir / "cohort_composition_by_model.html",
        "Cohort Composition By Model",
        composition_traces,
        {
            "barmode": "stack",
            "paper_bgcolor": "#f5f1e8",
            "plot_bgcolor": "#fffaf2",
            "xaxis": {"title": "Graduating Class Year"},
            "yaxis": {"title": "Cohort"},
        },
        "The sector changed materially over time. This chart shows how much of the graduating cohort sat in brick-and-mortar, virtual, and alternative models.",
    )

    compare = weighted[
        weighted["series_id"].isin(
            ["spcsa_adjusted_charter_only", "spcsa_brick_mortar", "spcsa_virtual", "spcsa_alternative"]
        )
    ].copy()
    compare["current_unweighted_panel_avg"] = pd.to_numeric(compare["current_unweighted_panel_avg"], errors="coerce")
    weighted_traces = []
    for sid, label, color in [
        ("spcsa_adjusted_charter_only", "SPCSA Charter Only Weighted", "#0f5c63"),
        ("spcsa_adjusted_charter_only", "SPCSA Charter Only Unweighted", "#8bbfc4"),
    ]:
        sub = compare[compare["series_id"] == "spcsa_adjusted_charter_only"].sort_values("year")
        y = sub["weighted_acgr"].tolist() if "Weighted" in label else sub["current_unweighted_panel_avg"].tolist()
        weighted_traces.append(
            {
                "type": "scatter",
                "mode": "lines+markers",
                "name": label,
                "x": sub["year"].tolist(),
                "y": y,
                "line": {"color": color, "width": 3, "dash": "solid" if "Weighted" in label else "dot"},
                "marker": {"size": 8},
            }
        )
    _write_plotly_html(
        viz_dir / "weighted_vs_unweighted.html",
        "Weighted vs Unweighted",
        weighted_traces,
        {
            "paper_bgcolor": "#f5f1e8",
            "plot_bgcolor": "#fffaf2",
            "xaxis": {"title": "Graduating Class Year"},
            "yaxis": {"title": "ACGR (%)", "range": [0, 100]},
        },
        "Weighted = average student. Unweighted = average school. The difference matters most when a few schools dominate the sector's cohort.",
    )

    top_years = ["2013-14", "2018-19", "2024-25"]
    top_parts = []
    for year in top_years:
        sub = audit[audit["class_year"] == year].copy()
        sub["graduates"] = pd.to_numeric(sub["graduates"], errors="coerce").fillna(0)
        sub["cohort"] = pd.to_numeric(sub["cohort"], errors="coerce").fillna(0)
        top = sub.sort_values(["graduates", "cohort"], ascending=False).head(10)
        top_parts.append(
            {
                "type": "bar",
                "orientation": "h",
                "name": year,
                "x": top["graduates"].tolist(),
                "y": top["matched_name"].tolist(),
                "hovertemplate": "%{y}<br>Graduates: %{x:,}<extra>" + year + "</extra>",
            }
        )
    _write_plotly_html(
        viz_dir / "top_contributors_selected_years.html",
        "Top Contributors By Year",
        top_parts,
        {
            "barmode": "group",
            "paper_bgcolor": "#f5f1e8",
            "plot_bgcolor": "#fffaf2",
            "xaxis": {"title": "Graduates"},
            "yaxis": {"title": "School"},
        },
        "These are the schools producing the largest numbers of graduates in selected years. The policy story is not only about rates; it is also about who actually produced graduating students.",
    )

    summary = {
        "generated_files": [
            "weighted_acgr_trend.html",
            "graduates_produced_by_year.html",
            "cohort_composition_by_model.html",
            "weighted_vs_unweighted.html",
            "top_contributors_selected_years.html",
        ],
        "png_generation": "not attempted because this environment does not currently include a Plotly static image engine such as kaleido",
    }
    (viz_dir / "visualization_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import sys

    build_visualizations(Path(sys.argv[1]))
