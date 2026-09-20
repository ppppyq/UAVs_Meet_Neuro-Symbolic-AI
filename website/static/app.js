(function () {
  "use strict";

  var papers = window.__PAPER_DATA__ || [];
  var taxonomy = window.__TAXONOMY_DATA__ || { axes: [] };
  var project = window.__PROJECT_DATA__ || {};
  var notesAvailable = window.__NOTES_AVAILABLE__ || {};

  var searchInput = document.getElementById("search");
  var taskSelect = document.getElementById("task-filter");
  var directionSelect = document.getElementById("direction-filter");
  var statusSelect = document.getElementById("status-filter");
  var resetButton = document.getElementById("reset-filters");
  var resultCount = document.getElementById("result-count");
  var tableContainer = document.querySelector(".papers");

  function axisTags(axisId) {
    var axis = (taxonomy.axes || []).filter(function (item) {
      return item && item.id === axisId;
    })[0];
    return (axis && axis.tags || []).map(function (tag) {
      return tag && tag.id;
    }).filter(Boolean);
  }

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

  function tagValues(paper, axisId) {
    var tags = paper.taxonomy_tags || {};
    return Array.isArray(tags[axisId]) ? tags[axisId] : [];
  }

  function allTags(paper) {
    var tags = paper.taxonomy_tags || {};
    return Object.keys(tags).reduce(function (out, axis) {
      return out.concat((tags[axis] || []).map(function (tag) {
        return axis + ":" + tag;
      }));
    }, []);
  }

  function textOf(paper) {
    return [
      paper.title || "",
      (paper.authors || []).join(" "),
      allTags(paper).join(" "),
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
    if (task && tagValues(paper, "uav_task").indexOf(task) === -1) {
      return false;
    }

    var direction = directionSelect.value;
    if (direction && tagValues(paper, "integration_direction").indexOf(direction) === -1) {
      return false;
    }

    var status = statusSelect.value;
    if (status && paper.screening_status !== status) {
      return false;
    }

    return true;
  }

  function evidenceLinks(paper) {
    var links = (paper.evidence_items || []).map(function (item) {
      var url = safeUrl(item.source_url);
      if (!url) {
        return "";
      }
      var label = [item.source_kind || "evidence"];
      if (item.locator) {
        label.push(item.locator);
      }
      return '<a href="' + escapeHtml(url) + '" rel="noopener noreferrer">' +
        escapeHtml(label.join(": ")) + "</a>";
    }).filter(Boolean);
    return links.join(" ") || "\u2014";
  }

  function noteLink(paper) {
    if (!notesAvailable[paper.id] || !project.github_url) {
      return "";
    }
    var url = project.github_url + "/blob/master/notes/papers/" + paper.id + ".md";
    return '<a href="' + escapeHtml(url) + '" rel="noopener noreferrer">note</a>';
  }

  function versionConflictHint(paper) {
    var parts = [];
    var conflicts = paper.metadata_conflict_scope || [];
    if (conflicts.length) {
      parts.push("conflict:" + conflicts.join(","));
    }
    (paper.related_versions || []).forEach(function (rel) {
      if (rel && rel.relation && rel.id) {
        parts.push(rel.relation + ":" + rel.id);
      }
    });
    if (paper.publication_status === "withdrawn") {
      parts.push("withdrawn");
    }
    return parts.join("; ");
  }

  function renderTable() {
    var visible = papers.filter(matches);
    resultCount.textContent = "Showing " + visible.length + " of " + papers.length + " records.";

    if (!visible.length) {
      tableContainer.innerHTML = "<p>No matching records.</p>";
      return;
    }

    var rows = visible.map(function (paper) {
      var canonical = safeUrl(paper.canonical_url);
      var code = safeUrl(paper.code_url);
      var original = canonical
        ? '<a href="' + escapeHtml(canonical) + '" rel="noopener noreferrer">original</a>'
        : "\u2014";
      var codeLink = code
        ? '<a href="' + escapeHtml(code) + '" rel="noopener noreferrer">code</a>'
        : "\u2014";
      var tags = allTags(paper).map(function (tag) {
        return '<span class="tag">' + escapeHtml(tag) + "</span>";
      }).join("");
      var evidenceNotes = [evidenceLinks(paper), noteLink(paper)].filter(Boolean).join(" ");

      return [
        "<tr>",
        "<td>" + escapeHtml(paper.title) + "<br><span class=\"tag-list\">" + tags + "</span></td>",
        "<td>" + escapeHtml((paper.authors || []).join(", ")) + "</td>",
        "<td>" + escapeHtml(paper.year) + "</td>",
        "<td>" + escapeHtml(paper.record_type || "") + "</td>",
        "<td><span class=\"status " + escapeHtml(paper.screening_status || "") + "\">" + escapeHtml(paper.screening_status || "") + "</span></td>",
        "<td><span class=\"status " + escapeHtml(paper.metadata_status || "") + "\">" + escapeHtml(paper.metadata_status || "") + "</span></td>",
        "<td>" + escapeHtml(paper.reading_status || "") + "</td>",
        "<td>" + escapeHtml(paper.relevance || "") + "</td>",
        "<td>" + escapeHtml(versionConflictHint(paper)) + "</td>",
        "<td>" + escapeHtml((paper.uav_evidence || []).join(", ")) + "</td>",
        "<td>" + (evidenceNotes || "\u2014") + "</td>",
        "<td>" + original + " \u00b7 " + codeLink + "</td>",
        "</tr>"
      ].join("");
    }).join("");

    tableContainer.innerHTML = [
      '<div class="table-wrap"><table>',
      "<thead><tr>",
      "<th>Title and tags</th><th>Authors</th><th>Year</th><th>Type</th>",
      "<th>Screening</th><th>Metadata</th><th>Reading</th><th>Relevance</th>",
      "<th>Version/conflict</th><th>Evidence</th><th>Evidence and notes</th><th>Links</th>",
      "</tr></thead><tbody>",
      rows,
      "</tbody></table></div>"
    ].join("");
  }

  populateSelect(taskSelect, axisTags("uav_task"));
  populateSelect(directionSelect, axisTags("integration_direction"));
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
