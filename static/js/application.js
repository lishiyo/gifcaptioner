$(function() {
  // Support TLS-specific URLs, when appropriate.
  if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
  } else {
    var ws_scheme = "ws://"
  };

  var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/receive");
  var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/submit");

  inbox.onmessage = function(message) {
    // console.log("INBOX ++ onMessage!", message.data);
    // var data = JSON.parse(message.data);
    // $("#chat-text").append("<div class='panel panel-default'><div class='panel-heading'>" + $('<span/>').text(data.handle).html() + "</div><div class='panel-body'>" + $('<span/>').text(data.text).html() + "</div></div>");
    // $("#chat-text").stop().animate({
    //   scrollTop: $('#chat-text')[0].scrollHeight
    // }, 800);
  };

  inbox.onclose = function(){
      console.log('inbox closed');
      this.inbox = new WebSocket(inbox.url);
  };

  outbox.onmessage = function(message) {
    // console.log("OUTBOX ++ onMessage!", message.data);
  }

  outbox.onclose = function(){
      console.log('outbox closed');
      this.outbox = new WebSocket(outbox.url);
  };

  $("#input-form").submit(function(event) {
    event.preventDefault();
    console.log("input form hit!");
    var handle = $("#input-handle")[0].value;
    var text   = $("#input-text")[0].value;
    // hits the outbox
    outbox.send(JSON.stringify({ handle: handle, text: text }));
    $("#input-text")[0].value = "";
    return false;
  });

  $("#caption-form").submit(event => {
    event.preventDefault();
    console.log("hit submit!");
    let text = $("#gif-text").val();
    let search = $("#gif-search").val();
    let url = $("#gif-url").val();
    let formData = { };
    if (text.length > 0) {
      formData['text'] = text;
    }
    if (search.length > 0) {
      formData['search'] = search
    }
    if (url.length > 0) {
      formData['gif'] = search
    }
    console.log("sending=== ",  JSON.stringify(formData));
    $.ajax({
      type        : 'POST', 
      contentType: 'application/json',
      url         : '/',
      data        : JSON.stringify(formData), 
      //dataType    : 'image/gif', 
    }).done((data, textStatus, jqXHR) => {
      console.log("done!");
      // create an image
      let outputImg = $("#result");
      let b64Response = btoa(data);

      outputImg.src = 'data:image/gif;base64,' + data;
    }).fail( (jqXHR, textStatus, errorThrown) => {
      console.log("fail", jqXHR, errorThrown, textStatus);
    }).always( (dataOrjqXHR, textStatus, jqXHOrErorThrown) => {
      console.log("always", dataOrjqXHR, textStatus, jqXHOrErorThrown);
    })
    
    return false;
  });

  // $("#caption").on("click", event => {
  //   event.preventDefault();
  //   let data = $("#caption-input").val();
  //   let json = JSON.stringify(data);

  //   console.log("submit!", data, json);
  //   // open up webserver connection
  //   // outbox.send(json);

  //   // make the request
  //   $.ajax({
  // 		url: '/',
  // 		data: data,
  // 		type: 'POST',
  // 		success: function(response){
  // 			console.log("SUCCESS", response);
  // 		},
  // 		error: function(error){
  // 			console.log("ERROR", error);
  // 		}
  //   });
    
  // })
})
