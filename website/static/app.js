(function () {
  "use strict";

  var papers = window.__PAPER_DATA__ || [];
  var taxonomy = window.__TAXONOMY_DATA__ || { axes: [], display_categories: [] };
  var project = window.__PROJECT_DATA__ || {};
  var notesAvailable = window.__NOTES_AVAILABLE__ || {};

  var searchInput = document.getElementById("search");
  var taskSelect = document.getElementById("task-filter");
  var directionSelect = document.getElementById("direction-filter");
  var themeSelect = document.getElementById("theme-filter");
  var statusSelect = document.getElementById("status-filter");
  var resetButton = document.getElementById("reset-filters");
  var resultCount = document.getElementById("result-count");
  var paperContainer = document.querySelector(".papers");
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  var hero = document.querySelector(".hero");
  var progress = document.querySelector(".reading-progress");
  var navigation = document.querySelector(".site-nav");
  var navToggle = document.querySelector(".nav-toggle");
  if (navigation && navToggle) {
    navigation.classList.add("nav-enhanced");
    function closeNavigation() {
      navigation.classList.remove("nav-open");
      navToggle.setAttribute("aria-expanded", "false");
    }
    navToggle.addEventListener("click", function () {
      var open = navigation.classList.toggle("nav-open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && navigation.classList.contains("nav-open")) {
        closeNavigation();
        navToggle.focus();
      }
    });
    document.addEventListener("pointerdown", function (event) {
      if (!navigation.contains(event.target)) closeNavigation();
    });
    window.matchMedia("(max-width: 1100px)").addEventListener("change", closeNavigation);
  }
  var revealObserver = !reducedMotion.matches && "IntersectionObserver" in window ?
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -5% 0px" }) : null;

  function observeReveals(root) {
    if (!revealObserver) {
      return;
    }
    root.querySelectorAll(".section-heading, .survey-card, .theme-card, .foundation-card, .paper-card, .method-card").forEach(function (item) {
      if (!item.classList.contains("motion-reveal")) {
        item.classList.add("motion-reveal");
        revealObserver.observe(item);
      }
    });
  }

  var progressFrame = 0;
  function updateProgress() {
    if (progressFrame) {
      return;
    }
    progressFrame = requestAnimationFrame(function () {
      var available = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = "scaleX(" + (available > 0 ? Math.min(1, window.scrollY / available) : 0) + ")";
      progressFrame = 0;
    });
  }
  window.addEventListener("scroll", updateProgress, { passive: true });
  window.addEventListener("resize", updateProgress);
  updateProgress();

  if (hero) {
    var heroFrame = 0;
    var heroPointer = null;
    hero.addEventListener("pointermove", function (event) {
      if (!finePointer.matches || reducedMotion.matches) {
        return;
      }
      heroPointer = event;
      if (heroFrame) {
        return;
      }
      heroFrame = requestAnimationFrame(function () {
        heroFrame = 0;
        if (!heroPointer) {
          return;
        }
        var rect = hero.getBoundingClientRect();
        hero.style.setProperty("--parallax-x", ((heroPointer.clientX / rect.width - 0.5) * -24).toFixed(1) + "px");
        hero.style.setProperty("--parallax-y", ((heroPointer.clientY / rect.height - 0.5) * -16).toFixed(1) + "px");
      });
    });
    hero.addEventListener("pointerleave", function () {
      heroPointer = null;
      hero.style.removeProperty("--parallax-x");
      hero.style.removeProperty("--parallax-y");
    });
  }

  reducedMotion.addEventListener("change", function () {
    if (reducedMotion.matches) {
      document.querySelectorAll(".motion-reveal").forEach(function (item) {
        item.classList.add("is-visible");
      });
    }
  });

  document.querySelectorAll(".glass-surface").forEach(function (surface) {
    surface.addEventListener("pointermove", function (event) {
      if (reducedMotion.matches) {
        return;
      }
      var rect = surface.getBoundingClientRect();
      surface.style.setProperty("--glint-x", ((event.clientX - rect.left) / rect.width * 100) + "%");
      surface.style.setProperty("--glint-y", ((event.clientY - rect.top) / rect.height * 100) + "%");
    });
    surface.addEventListener("pointerleave", function () {
      surface.style.removeProperty("--glint-x");
      surface.style.removeProperty("--glint-y");
    });
  });

  function axisTags(axisId) {
    var axis = (taxonomy.axes || []).filter(function (item) {
      return item && item.id === axisId;
    })[0];
    return (axis && axis.tags || []).map(function (tag) {
      return tag && tag.id;
    }).filter(Boolean);
  }

  function displayCategories() {
    return (taxonomy.display_categories || []).slice().sort(function (a, b) {
      return (a.display_order || 0) - (b.display_order || 0);
    });
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

  function populateThemeSelect(select, categories) {
    categories.forEach(function (category) {
      var option = document.createElement("option");
      option.value = category.id;
      option.textContent = category.name;
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

  function categoryName(categoryId) {
    var match = displayCategories().filter(function (category) {
      return category.id === categoryId;
    })[0];
    return match ? match.name : categoryId;
  }

  function categoryText(paper) {
    var primary = paper.primary_category || "";
    var secondary = paper.secondary_categories || [];
    var names = [];
    if (primary) {
      names.push(categoryName(primary));
    }
    secondary.forEach(function (categoryId) {
      if (categoryId !== primary) {
        names.push(categoryName(categoryId));
      }
    });
    return names.join(", ") || "\u2014";
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

    var theme = themeSelect.value;
    if (theme) {
      var primary = paper.primary_category || "";
      var secondary = paper.secondary_categories || [];
      if (primary !== theme && secondary.indexOf(theme) === -1) {
        return false;
      }
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
      return '<a class="pill-link" href="' + escapeHtml(url) + '" rel="noopener noreferrer">' +
        escapeHtml(label.join(": ")) + "</a>";
    }).filter(Boolean);
    return links.join(" ");
  }

  function noteLink(paper) {
    if (!notesAvailable[paper.id] || !project.github_url) {
      return "";
    }
    var url = project.github_url + "/blob/master/notes/papers/" + paper.id + ".md";
    return '<a class="pill-link" href="' + escapeHtml(url) + '" rel="noopener noreferrer">note</a>';
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

  function paperRow(paper) {
    var canonical = safeUrl(paper.canonical_url);
    var code = safeUrl(paper.code_url);
    var title = canonical ? '<a href="' + escapeHtml(canonical) + '" rel="noopener noreferrer">' + escapeHtml(paper.title) + '</a>' : escapeHtml(paper.title);
    var codeLink = code ? '<a href="' + escapeHtml(code) + '" rel="noopener noreferrer">GitHub</a>' : '—';
    return '<tr class="paper-row"><td>' + title + '</td><td>' + escapeHtml(paper.listing_type) +
      '</td><td>' + escapeHtml(paper.listing_publication) + '</td><td>' + codeLink + '</td></tr>';
  }

  function renderCards() {
    var visible = papers.filter(matches);
    resultCount.textContent = "Showing " + visible.length + " of " + papers.length + " papers.";
    if (revealObserver) {
      paperContainer.querySelectorAll(".motion-reveal").forEach(function (item) {
        revealObserver.unobserve(item);
      });
    }
    if (!visible.length) {
      paperContainer.innerHTML = '<p class="status-note">No papers match the current filters.</p>';
      return;
    }
    paperContainer.innerHTML = '<div class="table-wrap" tabindex="0" role="region" aria-label="Paper list"><table class="literature-table"><thead><tr><th scope="col">Title</th><th scope="col">Type</th><th scope="col">Publication</th><th scope="col">Code</th></tr></thead><tbody>' +
      visible.map(paperRow).join("") + "</tbody></table></div>";
    observeReveals(paperContainer);
  }

  if (paperContainer) {
    populateSelect(taskSelect, axisTags("uav_task"));
    populateSelect(directionSelect, axisTags("integration_direction"));
    populateThemeSelect(themeSelect, displayCategories());
    populateSelect(statusSelect, unique(papers.map(function (paper) {
      return paper.screening_status || "";
    }).filter(Boolean)));

    searchInput.addEventListener("input", renderCards);
    taskSelect.addEventListener("change", renderCards);
    directionSelect.addEventListener("change", renderCards);
    themeSelect.addEventListener("change", renderCards);
    statusSelect.addEventListener("change", renderCards);
    resetButton.addEventListener("click", function () {
      searchInput.value = "";
      taskSelect.value = "";
      directionSelect.value = "";
      themeSelect.value = "";
      statusSelect.value = "";
      renderCards();
    });
  }

  document.querySelectorAll(".theme-card[data-theme]").forEach(function (card) {
    card.addEventListener("pointermove", function (event) {
      if (!finePointer.matches || reducedMotion.matches) {
        return;
      }
      var rect = card.getBoundingClientRect();
      var x = (event.clientX - rect.left) / rect.width;
      var y = (event.clientY - rect.top) / rect.height;
      card.style.setProperty("--tilt-x", ((0.5 - y) * 7).toFixed(2) + "deg");
      card.style.setProperty("--tilt-y", ((x - 0.5) * 7).toFixed(2) + "deg");
      card.style.setProperty("--image-x", ((0.5 - x) * 8).toFixed(1) + "px");
      card.style.setProperty("--image-y", ((0.5 - y) * 8).toFixed(1) + "px");
      card.style.setProperty("--spot-x", (x * 100).toFixed(1) + "%");
      card.style.setProperty("--spot-y", (y * 100).toFixed(1) + "%");
    });
    card.addEventListener("pointerleave", function () {
      ["--tilt-x", "--tilt-y", "--image-x", "--image-y", "--spot-x", "--spot-y"].forEach(function (property) {
        card.style.removeProperty(property);
      });
    });
  });

  observeReveals(document.querySelector("main"));
  if (paperContainer) renderCards();
}());
