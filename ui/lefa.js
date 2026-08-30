const ids = (name) => document.getElementById(name);

function text(id, value, fallback = "—") {
  ids(id).textContent = value ?? fallback;
}

function render(view) {
  text("connectionLabel", view.connection_label, "Not connected");
  ids("connectionDot").className = view.mode === "fixture" ? "fixture" : "";
  text("observationLabel", view.observation_label, "Awaiting observation");
  text("truthAnchor", view.truth_anchor, "Unknown");
  text("executionAuthority", String(view.execution_authority).toUpperCase(), "ZERO");
  text("latestPrice", view.market.latest_price, "—");
  text(
    "provenance",
    `Source: ${view.provenance.source} · Provider: ${view.provenance.provider} · Freshness: ${view.provenance.freshness}`,
  );

  for (const stage of view.stages) {
    text(`stage-${stage.key}-status`, stage.status);
    text(`stage-${stage.key}-detail`, stage.detail);
  }
}

async function loadState() {
  try {
    const response = await fetch("/api/snapshot?symbol=SPY", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    render(await response.json());
  } catch (error) {
    text("connectionLabel", "Interface state unavailable");
    text("truthAnchor", "HOLD");
    text("provenance", `Source: unavailable · ${error.message}`);
  }
}

const dialog = ids("gateDialog");
ids("gateButton").addEventListener("click", () => dialog.showModal());

loadState();
