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

  function register() {
    var formdata = new FormData();
    var file = $("#picture-field")[0].files[0];
    console.log(file);
    formdata.append("picture", file);
    formdata.append("username", $('#username-field').val());
    formdata.append("password", $('#password-field').val());
    formdata.append("cpassword", $('#cpassword-field').val());
    formdata.append("about", $('#about-field').val());
    console.log(formdata);
    $.ajax({
        url : "",
        type : "POST",
        data : formdata,
        processData: false,
        contentType: false,
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

  $('#register-button').on('click', function(event){
      event.preventDefault();
      console.log("form submitted!")  // sanity check
      register();
  });

  $('#refresh-prof').on('click', function(event){
      event.preventDefault();
      var data = $('#refresh-prof').data('userid');
      console.log(data)
      window.location.href = "/profile/user/" + data;
  });

  $('#back-prof').on('click', function(event){
      event.preventDefault();
      var data = $('#back-prof').data('uid');
      console.log(data)
      window.location.href = "/candidate/user/" + data;
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

  $('.create-post-red').on('click', function(event){
      event.preventDefault();
      window.location.href = "/create_post_page";
  });


  $(document).on('click', '.delete-but', delete_post);
  $(document).on('click', '.delete-comment-button', delete_comment);

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
              <br> \
              <button data-commentid="' + json.cid + '" class="delete-comment-button mdl-button mdl-js-button mdl-button--icon mdl-button--colored"> \
                <i class="fa fa-trash"></i> \
              </button> \
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
    var user_id = $('#candidate-header').data('userid');
    console.log(user_id)
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

  function delete_comment() {
    event.preventDefault();
    var $this = $(this);
    var comment_id = $this.data('commentid');
    var post_id = $('#post-header').data('postid');
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "/delete_comment/",
        type : "POST",
        data : { comment_id: comment_id,
               },
        success : function(json) {
            console.log(json); // log the returned json to the console
            window.location.href = "/post/" + post_id;
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

$(document).ready(function(){
  $("#wordcloud").awesomeCloud({
    "size" : {
      "grid" : 0.005, // word spacing; smaller is more tightly packed but takes longer
      "factor" : 0, // font resizing factor; default "0" means automatically fill the container
      "normalize" : true // reduces outlier weights for a more attractive output
    },
    "color" : {
      "background" : "rgb(104,119,125, 1)", // background color, transparent by default
      "start" : "rgb(107,182,208)", // color of the smallest font, if options.color = "gradient""
      "end" : "rgb(29,142,181)" // color of the largest font, if options.color = "gradient"
    },
    "options" : {
      "color" : "gradient", // random-light, random-dark, gradient
      "rotationRatio" : 0.35, // 0 is all horizontal, 1 is all vertical
      "printMultiplier" : 2, // set to 3 for nice printer output; higher numbers take longer
      "sort" : "highest" // highest, lowest or random
    },
    "font" : "Roboto', sans-serif", //  the CSS font-family string
    "shape" : "circle" // one of "circle", "square", "diamond", "triangle", "triangle-forward", "x", "pentagon" or "star"; this can also be a function with the following prototype - function( theta ) {}
  });
});