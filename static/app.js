//

$(function () {
  var loc = window.location, new_uri;
  if (loc.protocol === "https:") {
    new_uri = "wss:";
  } else {
    new_uri = "ws:";
  }
  new_uri += "//" + loc.host;
  new_uri += loc.pathname + "test";

  var ws = new WebSocket(new_uri);
  var charts = [];
  var charts_count = 4;

  for (var i=0;i<charts_count;i++) {
    charts[i] = $('#test' + i).epoch({
      type: 'time.area',
      data: [{ label: 'foo' + i, values: [] }],
      axes: ['left', 'right', 'bottom']
    });
  }

  ws.onmessage = function(msg) {
    var current = JSON.parse(msg.data);
    for (var i=0;i<charts_count;i++) {
      charts[i].push([current[i]]);
    }
  };
});
