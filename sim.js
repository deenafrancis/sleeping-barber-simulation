

function display(data) {

    if(data.length == 0) { return; }
    if(data[0].length == 0 ) { return; }
    var barber = data[0][0];
    var numseats = data[0].length - 1;
    var actions = data[1];

    var html = "<table>"
    html += "<tr>";
    for( var ii=0; ii<numseats+1; ii++ ) {
	html += "<td>";
	if (ii==0) {
	    html += "Barber is " + barber["state"];
	    if(barber["state"] == "busy") {
		html += "<br>" + barber["customer"] + " is getting a haircut";
	    }
	} else {
	    if(data[0][ii]["name"] == "none") {
		html += "Empty";
	    } else {
		html += data[0][ii]["name"];
	    }
	}
	html += "</td>";
    }
    html += "</tr><tr>";

    for( var ii=0; ii<numseats+1; ii++ ) {
	html += "<td>";
	if (ii==0) {
	    if(barber["state"] == "busy") {
		html += "<img src='images/cutting.jpg'>";
	    } else {
		html += "<img src='images/sleeping.jpg'>";
	    }

	} else {
	    if(data[0][ii]["name"] == "none") {
		html += "<img src='images/empty.jpg'>";
	    } else {
		html += "<img src='images/waiting.jpg'>";
	    }
	}
	html += "</td>";
    }    
    html += "</tr>";
    html += "</table>";

    $("#bshop").html(html);

    html = "<p>";
    for(var ii=actions.length-1; ii>=0; ii--) {
	html += actions[ii] + "<br>";
    }
    html += "</p>";
    $("#talk").html(html);
}


function get_json() {
//    $.getJSON("bshop.json", function(data) { display(data); })
    $.ajax({
	cache: false,
	url: "bshop.json",
	dataType: "json",
	success: function(data) {
	    display(data);
	}
    });
}


window.setInterval(get_json, 1000);