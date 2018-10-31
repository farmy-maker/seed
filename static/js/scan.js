$(document).ready(function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('qr_code', function(data) {
      console.log(data);
      $("#qr-img").attr("src", "/qrcode.jpg?random=" + new Date().getTime());
    });
});
