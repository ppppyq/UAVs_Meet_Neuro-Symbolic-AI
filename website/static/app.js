(function () {
  "use strict";

  var papers = window.__PAPER_DATA__ || [];
  var searchInput = document.getElementById("search");
  var taskSelect = document.getElementById("task-filter");
  var directionSelect = document.getElementById("direction-filter");
  var statusSelect = document.getElementById("status-filter");
  var resetButton = document.getElementById("reset-filters");
  var resultCount = document.getElementById("result-count");
  var tableContainer = document.querySelector(".papers");

  var TASK_TAGS = [
    "navigation",
    "mission_planning",
    "search_and_exploration",
    "landing",
    "inspection",
    "aerial_manipulation",
    "multi_uav_coordination",
    "communication_and_networking",
    "other"
  ];

  var DIRECTION_TAGS = [
    "neural_to_symbolic",
    "symbolic_to_neural",
    "bidirectional",
    "other",
    "unknown"
  ];

  function unique(values) {
    return Array.from(new Set(values)).sort();
  }

  function populateSelect(select, values) {
    values.forEach(function (value) {
      var option = document.createElement("option");
      option.value = value;
      option.textContent = value.replace(/_/g, " ");
      select.appendChild(option);
    });
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function safeUrl(value) {
    if (!value) {
      return null;
    }
    try {
      var url = new URL(value, window.location.href);
      if (url.protocol === "http:" || url.protocol === "https:") {
        return url.href;
      }
    } catch (error) {
      return null;
    }
    return null;
  }

  function textOf(paper) {
    return [
      paper.title || "",
      (paper.authors || []).join(" "),
      (paper.taxonomy_tags || []).join(" "),
      paper.summary || "",
      paper.limitations || ""
    ].join(" ").toLowerCase();
  }

  function matches(paper) {
    var query = searchInput.value.trim().toLowerCase();
    if (query && textOf(paper).indexOf(query) === -1) {
      return false;
    }

    var task = taskSelect.value;
    if (task && (paper.taxonomy_tags || []).indexOf(task) === -1) {
      return false;
    }

    var direction = directionSelect.value;
    if (direction && (paper.taxonomy_tags || []).indexOf(direction) === -1) {
      return false;
    }

    var status = statusSelect.value;
    if (status && paper.screening_status !== status) {
      return false;
    }

    return true;
  }

  function renderTable() {
    var visible = papers.filter(matches);
    resultCount.textContent = "Showing " + visible.length + " of " + papers.length + " records.";

    if (!visible.length) {
      tableContainer.innerHTML = '<p>No matching records.</p>';
      return;
    }

    var rows = visible.map(function (paper) {
      var canonical = safeUrl(paper.canonical_url);
      var code = safeUrl(paper.code_url);
      var original = canonical
        ? '<a href="' + escapeHtml(canonical) + '" rel="noopener noreferrer">original</a>'
        : "—";
      var codeLink = code
        ? '<a href="' + escapeHtml(code) + '" rel="noopener noreferrer">code</a>'
        : "—";
      var tags = (paper.taxonomy_tags || []).map(function (tag) {
        return '<span class="tag">' + escapeHtml(tag) + "</span>";
      }).join("");

      return [
        "<tr>",
        "<td>" + escapeHtml(paper.title) + "<br><span class=\"tag-list\">" + tags + "</span></td>",
        "<td>" + escapeHtml((paper.authors || []).join(", ")) + "</td>",
        "<td>" + escapeHtml(paper.year) + "</td>",
        "<td>" + escapeHtml(paper.record_type || "") + "</td>",
        "<td><span class=\"status " + escapeHtml(paper.screening_status || "") + "\">" + escapeHtml(paper.screening_status || "") + "</span></td>",
        "<td>" + escapeHtml((paper.uav_evidence || []).join(", ")) + "</td>",
        "<td>" + original + " · " + codeLink + "</td>",
        "</tr>"
      ].join("");
    }).join("");

    tableContainer.innerHTML = [
      '<div class="table-wrap"><table>',
      "<thead><tr>",
      "<th>Title and tags</th><th>Authors</th><th>Year</th><th>Type</th><th>Status</th><th>Evidence</th><th>Links</th>",
      "</tr></thead><tbody>",
      rows,
      "</tbody></table></div>"
    ].join("");
  }

  populateSelect(taskSelect, TASK_TAGS);
  populateSelect(directionSelect, DIRECTION_TAGS);
  populateSelect(statusSelect, unique(papers.map(function (paper) {
    return paper.screening_status || "";
  }).filter(Boolean)));

  searchInput.addEventListener("input", renderTable);
  taskSelect.addEventListener("change", renderTable);
  directionSelect.addEventListener("change", renderTable);
  statusSelect.addEventListener("change", renderTable);
  resetButton.addEventListener("click", function () {
    searchInput.value = "";
    taskSelect.value = "";
    directionSelect.value = "";
    statusSelect.value = "";
    renderTable();
  });

  renderTable();
}());
