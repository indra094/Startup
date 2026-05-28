const form = document.getElementById("planner-form");
const results = document.getElementById("results");
const statusNode = document.getElementById("status");
const summaryGrid = document.getElementById("summary-grid");
const orgGrid = document.getElementById("org-grid");
const financialTable = document.getElementById("financial-table");
const employeeTable = document.getElementById("employee-table");
const yearSelect = document.getElementById("year-select");
const departmentPills = document.getElementById("department-pills");

let latestPlan = null;

const usdFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function getLocalFormatter(plan) {
  return new Intl.NumberFormat(plan.matched_profiles.currency_locale || undefined, {
    style: "currency",
    currency: plan.matched_profiles.currency_code,
    maximumFractionDigits: 0,
  });
}

function formatUsd(value) {
  return usdFormatter.format(value);
}

function formatLocal(value, plan) {
  return getLocalFormatter(plan).format(value);
}

function renderMoneyPair(localValue, usdValue, plan) {
  return `
    <div class="money-stack">
      <strong>${escapeHtml(formatLocal(localValue, plan))}</strong>
      <span>${escapeHtml(formatUsd(usdValue))} USD equivalent</span>
    </div>
  `;
}

function setStatus(message, isError = false) {
  statusNode.textContent = message;
  statusNode.dataset.error = isError ? "true" : "false";
}

function renderSummary(plan) {
  const finalYear = plan.yearly_plan.at(-1);
  const totalFundingUsd = plan.yearly_plan.reduce(
    (sum, year) => sum + year.funding_required_usd,
    0,
  );
  const totalFundingLocal = plan.yearly_plan.reduce(
    (sum, year) => sum + year.funding_required_local,
    0,
  );

  const cards = [
    {
      label: "Profile Match",
      value: `${plan.matched_profiles.industry_name} in ${plan.matched_profiles.country_name}`,
      meta: `${plan.matched_profiles.leanness_name} operating model.`,
    },
    {
      label: "Year 5 Revenue",
      value: formatLocal(finalYear.revenue_local, plan),
      meta: `${formatUsd(finalYear.revenue_usd)} USD equivalent by the fifth year.`,
    },
    {
      label: "Year 5 Operating Costs",
      value: formatLocal(finalYear.operating_costs_local, plan),
      meta: `${formatUsd(finalYear.operating_costs_usd)} USD equivalent annual cost base.`,
    },
    {
      label: "Total Funding Need",
      value: formatLocal(totalFundingLocal, plan),
      meta: `${formatUsd(totalFundingUsd)} USD equivalent across the first five years.`,
    },
  ];

  summaryGrid.innerHTML = cards
    .map(
      (card) => `
        <article class="summary-card">
          <p class="summary-label">${escapeHtml(card.label)}</p>
          <h2>${escapeHtml(card.value)}</h2>
          <p class="summary-meta">${escapeHtml(card.meta)}</p>
        </article>
      `,
    )
    .join("");

  const takeawayMarkup = plan.key_takeaways
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join("");
  const assumptionMarkup = plan.assumptions
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join("");

  summaryGrid.insertAdjacentHTML(
    "beforeend",
    `
      <article class="summary-card wide">
        <p class="summary-label">Planner Notes</p>
        <div class="dual-list">
          <div>
            <h3>Key takeaways</h3>
            <ul>${takeawayMarkup}</ul>
          </div>
          <div>
            <h3>Assumptions</h3>
            <ul>${assumptionMarkup}</ul>
          </div>
        </div>
      </article>
    `,
  );
}

function renderOrg(plan) {
  const finalYear = plan.yearly_plan.at(-1);
  orgGrid.innerHTML = finalYear.org_structure
    .map(
      (node) => `
        <article class="org-card">
          <p class="org-dept">${escapeHtml(node.department)}</p>
          <h3>${escapeHtml(node.leader)}${node.count > 1 ? ` x${node.count}` : ""}</h3>
          <p class="org-caption">Direct reports</p>
          <ul>
            ${node.reports.length ? node.reports.map((item) => `<li>${escapeHtml(item)}</li>`).join("") : "<li>No direct reports in this model</li>"}
          </ul>
        </article>
      `,
    )
    .join("");
}

function renderFinancials(plan) {
  financialTable.innerHTML = plan.yearly_plan
    .map(
      (year) => `
        <tr>
          <td>Year ${year.year}</td>
          <td>${year.headcount}</td>
          <td>${renderMoneyPair(year.revenue_local, year.revenue_usd, plan)}</td>
          <td>${renderMoneyPair(year.gross_profit_local, year.gross_profit_usd, plan)}</td>
          <td>${renderMoneyPair(year.operating_costs_local, year.operating_costs_usd, plan)}</td>
          <td>${renderMoneyPair(year.funding_required_local, year.funding_required_usd, plan)}</td>
          <td>${renderMoneyPair(year.cumulative_funding_local, year.cumulative_funding_usd, plan)}</td>
        </tr>
      `,
    )
    .join("");
}

function renderYearOptions(plan) {
  yearSelect.innerHTML = plan.yearly_plan
    .map((year) => `<option value="${year.year}">Year ${year.year}</option>`)
    .join("");
}

function renderEmployeeTable(plan, selectedYear) {
  const year = plan.yearly_plan.find((entry) => entry.year === selectedYear) ?? plan.yearly_plan[0];
  const departmentEntries = Object.entries(year.headcount_by_department);
  departmentPills.innerHTML = departmentEntries
    .map(
      ([department, count]) => `
        <span class="pill">${escapeHtml(department)}: ${count}</span>
      `,
    )
    .join("");

  employeeTable.innerHTML = year.employees
    .map(
      (employee) => `
        <tr>
          <td>${escapeHtml(employee.name)}</td>
          <td>${escapeHtml(employee.title)}</td>
          <td>${escapeHtml(employee.department)}</td>
          <td>${escapeHtml(employee.reports_to)}</td>
          <td>${renderMoneyPair(employee.salary_local, employee.salary_usd, plan)}</td>
          <td class="reason-cell">${escapeHtml(employee.salary_reason)}</td>
        </tr>
      `,
    )
    .join("");
}

function renderPlan(plan) {
  latestPlan = plan;
  results.classList.remove("hidden");
  renderSummary(plan);
  renderOrg(plan);
  renderFinancials(plan);
  renderYearOptions(plan);
  renderEmployeeTable(plan, 1);
}

yearSelect.addEventListener("change", () => {
  if (!latestPlan) {
    return;
  }
  renderEmployeeTable(latestPlan, Number(yearSelect.value));
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const industry = document.getElementById("industry").value.trim();
  const country = document.getElementById("country").value.trim();
  const leanness = document.getElementById("leanness").value.trim();

  setStatus("Generating your startup blueprint...");

  try {
    const response = await fetch("/api/plan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ industry, country, leanness }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Unable to generate a plan.");
    }

    renderPlan(data);
    setStatus("Blueprint ready.");
  } catch (error) {
    setStatus(error.message || "Something went wrong.", true);
  }
});
