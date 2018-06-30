$(document).on('click','.sideoption',function(){
  var OpValue=$(this).text().trim();
  console.log(OpValue);
  var html_text_user="<li id='user_box' class='right clearfix'>"+ OpValue +"</li>";
  $('.chat').append(html_text_user);
  $.ajax({
          url:'/bot/response',
          data:{
            'text':OpValue,
            'source':'button'
          },
          type:'POST',
          success:function(data){
                console.log(data.response);
                $('#sideMenu').html("");
                $('#sideMenu').append(data.response_sideMenu)
                $('.chat').append(data.response_box)
                var wtf    = $('.panel-body');
                var height = wtf[0].scrollHeight;
                wtf.scrollTop(height);
              },
            });
});


$(document).ready(function(){
    $('.chat').append("<li id='bot_box' class='left clearfix'>Hello, I'm IT helpdesk virtual assistant</li>");
    $('#btn-input').keypress(function (e) {
      if (e.which == 13) { $('#btn-chat').trigger("click");}
    });
    $('#btn-chat').click(function(){
       var input_text= $('#btn-input').val().trim();
       if(input_text.length > 0){
         var html_text_user="<li id='user_box' class='right clearfix'>"+ input_text +"</li>";
         $('.chat').append(html_text_user);
         $("#btn-input").val("");
         $.ajax({
         	url:'/bot/response',
         	data:{
         		'text':input_text,
            'source':'textField'
         	},
          type:'POST',
          success:function(data){
                $('#sideMenu').html("");
                $('#sideMenu').append(data.response_sideMenu)
                $('.chat').append(data.response_box)
                var wtf    = $('.panel-body');
                var height = wtf[0].scrollHeight;
                wtf.scrollTop(height);
              },
            });
       }
     });
});