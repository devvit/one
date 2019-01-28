//

$(function () {
  var loc = window.location, new_uri;
  if (loc.protocol === "https:") {
    new_uri = "wss:";
  } else {
    new_uri = "ws:";
  }
  new_uri += "//" + loc.host;
  new_uri += loc.pathname + "ws";

  var ws = new WebSocket(new_uri);
  var charts = [];

  for (var i=0;i<4;i++) {
    charts[i] = $('#test' + i).epoch({
      type: 'time.area',
      data: [{ label: 'foo' + i, values: [] }],
      axes: ['left', 'right', 'bottom']
    });
  }

  ws.onmessage = function(msg) {
    var current = JSON.parse(msg.data);
    for (var i=0;i<4;i++) {
      charts[i].push([current[i]]);
    }
  };
});
