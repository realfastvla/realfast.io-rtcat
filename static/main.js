var catalog;
$(document).ready(setup);

function setup() {
	$.ajax({
		url: "/gen_catalog",
		success: setHTML
	});
}

function check_version() {
	check_atnf();
	check_rratalog();
	check_parallaxes();
	check_gcpsr();
	check_frbcat();
}

function setHTML(result) {
	catalog = JSON.parse(result);
	catalog.entries_per_page = 10;
	catalog.pages = Math.ceil(catalog.entries.length / catalog.entries_per_page);
	catalog.curr_page = 1;

	check_version();
	$("#search").keyup(filter);
	$("#ATNF").change(filter);
	$("#RRATalog").change(filter);
	$("#Parallaxes").change(filter);
	$("#GCpsr").change(filter);
	$("#frbcat").change(filter);
	$("#next").click(next);
	$("#prev").click(prev);

	filter();
}

function filter() {
	var prestring = $("#search").val();
	var numVisible = 0;
	for (var i = 0; i < catalog.entries.length; i++) {
		var curr = catalog.entries[i];
		var smaller = Math.min(prestring.length, curr.Name.length);
		if (curr.Name.slice(0, smaller) == prestring.slice(0, smaller)) {
			curr.visible = true;
		} else {
			curr.visible = false;
		}
		var sourceNames = [];
		for (source of curr.sources) {
			sourceNames.push(source.Name);
		}
		if ($("#ATNF").is(":checked") && curr.visible) {
			if ($.inArray("ATNF", sourceNames) == -1) {
				curr.visible = false;
			}
		}
		if ($("#RRATalog").is(":checked")) {
			if ($.inArray("RRATalog", sourceNames) == -1) {
				curr.visible = false;
			}
		}
		if ($("#Parallaxes").is(":checked")) {
			if ($.inArray("Parallaxes", sourceNames) == -1) {
				curr.visible = false;
			}
		}
		if ($("#GCpsr").is(":checked")) {
			if ($.inArray("GCpsr", sourceNames) == -1) {
				curr.visible = false;
			}
		}
		if ($("#frbcat").is(":checked")) {
			if ($.inArray("frbcat", sourceNames) == -1) {
				curr.visible = false;
			}
		}
		if (curr.visible) {
			numVisible += 1;
		}
	}
	if (numVisible === 0) {
		numVisible = 1;
	}
	catalog.pages = Math.ceil(numVisible / catalog.entries_per_page);
	catalog.curr_page = 1;
	render(catalog);
}

function next() {
	if (catalog.curr_page != catalog.pages) {
		catalog.curr_page += 1;
		render(catalog);
	}
}

function prev() {
	if (catalog.curr_page != 1) {
		catalog.curr_page -= 1;
		render(catalog);
	}
}

function render(catalog) {
    var table = '<tr><th>Name</th><th>RA</th><th>DEC</th><th>Sources</th></tr>';
	var start_buffer = (catalog.curr_page - 1) * catalog.entries_per_page;
	var entries_left = catalog.entries_per_page;
	var i = 0;
	var curr;
	while (start_buffer > 0 && i < catalog.entries.length) {
		curr = catalog.entries[i];
		if (curr.visible) {
			start_buffer -= 1;
		}
		i += 1;
	}
	while (entries_left > 0 && i < catalog.entries.length) {
		curr = catalog.entries[i];
		if (curr.visible) {
			var sourceNames = [];
			for (var source of curr.sources) {
				sourceNames.push(source.Name);
			}
			var classString;
			if (entries_left % 2 == 0) {
				classString = "light-grey-row"
			} else {
				classString = "light-blue-row"
			}
			table += "<tr class=\"" + classString + "\"><td><a target=\"_blank\" href=/entries/" + curr.Name.replace("/", "-") + ">" + curr.Name + "</a></td><td>" + curr.RA + "</td><td>" + curr.DEC + "</td><td>" + sourceNames.join() + "</td></tr>";
			entries_left -= 1;
		}
		i += 1;
	}
	$("#table").html(table);
	$("#pageinfo").html(catalog.curr_page.toString() + " of " + catalog.pages.toString());
}

function check_atnf() {
	$.ajax({
		url: "/versioning",
		data: {
			catalog: "ATNF"
		},
		success: function(response) {
			localVersion = Number(catalog.versions.ATNF);
			remoteVersion = Number(response);
			if (localVersion < remoteVersion) {
				$.ajax({
					url: "/render-version-box",
					data: {
						isCurrent: false,
						catalog: "ATNF"
					},
					success: function(response) { $("#ATNF_v").html(response) }
				});
			} else {
				$.ajax({
					url: "/render-version-box",
					data: {
						isCurrent: true,
						catalog: "ATNF"
					},
					success: function(response) { $("#ATNF_v").html(response) }
				});
			}
		}
	});
}

function check_rratalog() {
	$.ajax({
		url: "/versioning",
		data: {
			catalog: "RRATalog"
		},
		success: function(response) {
			localVersion = Date.parse(catalog.versions.RRATalog);
			remoteVersion = Date.parse(response);
			if (localVersion < remoteVersion) {
				$.ajax({
					url: "/render-version-box",
					data: {
						isCurrent: false,
						catalog: "RRATalog"
					},
					success: function(response) { $("#RRATalog_v").html(response) }
				});
			} else {
				$.ajax({
					url: "/render-version-box",
					data: {
						isCurrent: true,
						catalog: "RRATalog"
					},
					success: function(response) { $("#RRATalog_v").html(response) }
				});
			}
		}
	});
}

function check_parallaxes() {
	$.ajax({
		url: "/versioning",
		data: {
			catalog: "Parallaxes"
		},
		success: function(response) {
			var month = catalog.versions.Parallaxes.slice(4, 6);
			var day = catalog.versions.Parallaxes.slice(6, 8);
			var year = catalog.versions.Parallaxes.slice(0, 5);
			localVersion = Date.parse(month + "-" + day + "-" + year);
			remoteVersion = Date.parse(response);
			if (localVersion < remoteVersion) {
				$.ajax({
					url: "/render-version-box",
					data: {
						isCurrent: false,
						catalog: "Parallaxes"
					},
					success: function(response) { $("#Parallaxes_v").html(response) }
				});
			} else {
				$.ajax({
					url: "/render-version-box",
					data: {
						isCurrent: true,
						catalog: "Parallaxes"
					},
					success: function(response) { $("#Parallaxes_v").html(response) }
				});
			}
		}
	});
}

function check_gcpsr() {
	$.ajax({
		url: "/versioning",
		data: {
			catalog: "GCpsr"
		},
		success: function(response) {
			localVersion = Date.parse(catalog.versions.GCpsr);
			remoteVersion = Date.parse(response);
			if (localVersion < remoteVersion) {
				$.ajax({
					url: "/render-version-box",
					data: {
						isCurrent: false,
						catalog: "GCpsr"
					},
					success: function(response) { $("#GCpsr_v").html(response) }
				});
			} else {
				$.ajax({
					url: "/render-version-box",
					data: {
						isCurrent: true,
						catalog: "GCpsr"
					},
					success: function(response) { $("#GCpsr_v").html(response) }
				});
			}
		}
	});
}

function check_frbcat() {
	$.ajax({
		url: "/versioning",
		data: {
			catalog: "frbcat"
		},
		success: function(response) {
			localVersion = parseFloat(catalog.versions.GCpsr);
			remoteVersion = parseFloat(response);
			if (localVersion < remoteVersion) {
				$.ajax({
					url: "/render-version-box",
					data: {
						isCurrent: false,
						catalog: "frbcat"
					},
					success: function(response) { $("#frbcat_v").html(response) }
				});
			} else {
				$.ajax({
					url: "/render-version-box",
					data: {
						isCurrent: true,
						catalog: "frbcat"
					},
					success: function(response) { $("#frbcat_v").html(response) }
				});
			}
		}
	});
}
