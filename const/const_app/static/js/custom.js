$(function() {

  function login() {
    console.log("login is working!") // sanity check
    $.ajax({
        url : "",
        type : "POST",
        data : { username: $('#username-field').val(),
                 password: $('#password-field').val()},
        success : function(json) {
            if (json.redirect) {
            // data.redirect contains the string URL to redirect to
              window.location.href = json.redirect;
            }
            else {
              $('#password-field').val('');
              console.log(json); // log the returned json to the console
              $("#failed-notice").html("<div id='failed-div-top' class='failed-login mdl-card mdl-shadow--2dp'> Login incorrecto </div>");
              setTimeout(function() {
                  $("#failed-div-top").fadeOut().empty();
                }, 3000);
              console.log("success"); // another sanity check
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
  }

  $('#login-button').on('click', function(event){
      event.preventDefault();
      console.log("form submitted!")  // sanity check
      login();
  });

  $('#refresh-prof').on('click', function(event){
      event.preventDefault();
      var data = $('#refresh-prof').data('userid');
      console.log(data)
      window.location.href = "/profile/user/" + data;
  });

  $('#make-comment').on('click', function(event){
      event.preventDefault();
      console.log("form submitted!")  // sanity check
      create_comment();
  });

  $('#make-post').on('click', function(event){
      event.preventDefault();
      console.log("form submitted!")  // sanity check
      create_post();
  });

  $('.delete-but').on('click', function(event){
      event.preventDefault();
      console.log("form submitted!")  // sanity check
      delete_post();
  });

  function create_comment() {
    var post_id = $('#post-header').data('postid');
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "/create_comment/",
        type : "POST",
        data : { content: $('#comment-box').val(), pid: post_id},
        success : function(json) {
            $('#text_area_post').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            $("#comments").append('\
              <div class="section__circle-container mdl-cell mdl-cell--1-col mdl-cell--1-col-phone"> \
              <div class="section__circle-container__circle"> \
                <img class="comment-image profile-image" src="' + json.userImage + '" alt="Mountain View"> </img> \
              </div>\
            </div>\
            <div class="comment section__text mdl-cell mdl-cell--11-col-desktop mdl-cell--6-col-tablet mdl-cell--3-col-phone"> \
              ' + json.cont + ' \
            </div> \
            ');
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
  }

  function create_post() {
    var user_id = $('#createpost-header').data('userid');
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "/create_post/",
        type : "POST",
        data : { content: $('#post-box').val(),
                title:  $('#post-box-title').val()},
        success : function(json) {
            $('#text_area_post').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            window.location.href = "/candidate/user/" + user_id;
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
  }

  function delete_post() {
    event.preventDefault();
    var $this = $(this);
    var post_id = $this.data('postid');
    var user_id = $('#createpost-header').data('userid');
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "/delete_post/",
        type : "POST",
        data : { post_id: post_id,
               },
        success : function(json) {
            console.log(json); // log the returned json to the console
            window.location.href = "/candidate/user/" + user_id;
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
  }

  // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});
