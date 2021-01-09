
$(document).ready(function(){


   $image_demo_edit_more = $('#image_demo_edit_more').croppie({
   enableExif: true,
   viewport: {
   width:490,
   height:532,
   type:'square' //circle

    },

    boundary:{
     width:600,
     height:600

    }

  });


  $('.add_image_crope_data_dsp').on('change', function(){
  var image_array="";

 $("#get_id_or_color_row").val($(this).data("id"));
 $('#image_preview1').html("");
 $('#add_all_image').html("");
 $("#current_image_set").text('1');
 $("#all_image_set").text(this.files.length);
var j=0;
// console.log(this.files.length);
    for(var i=0; i<this.files.length; i++)
{
   
    reader = new FileReader();
    reader.onload = function (event) {
      

// console.log(event.currentTarget["result"]);
$("#add_all_image").append('<input type="hidden" class="all_image_name" value="'+event.target.result+'" >');
    

    if(j==0)
    {
      $image_demo_edit_more.croppie('bind', {
    url: event.target.result

   }).then(function(){

        console.log('jQuery bind complete');

      });
    
    }   
    
     j=j+1;

    }

  reader.readAsDataURL(this.files[i]);
  reader="";
}
    
   $('#uploadimageModal_edit_more').modal('show');
 

   

  });



  $('.crop_image_edit_more').click(function(event){

var row_id=$("#get_id_or_color_row").val();

console.log("set_row_id");
console.log(row_id);
  $('.crop_image_edit_more').html('Image Uploading <img src="images/tenor1.gif" style="width:50px; height:30px; padding:10px;">');
  $('.crop_image_edit_more').attr('disabled',true);
    $image_demo_edit_more.croppie('result', {

      type: 'canvas',
      size: 'viewport'

    }).then(function(response){

      $.ajax({

        url:"image_upload_more.php",
        type: "POST",
        data:{"image": response,"row_id":row_id},

        success:function(data)

        {

$("#uploadimageModal_edit_more").modal('hide');
var count_image=$("#all_image_set").text();
            image_array="";
             image_array=[];
            $(".all_image_name").each(function(i){
                
                 image_array[i]=$(this).val();                
            });
            var courent_image=$("#current_image_set").text();
            // console.log(count_image);
            // console.log(courent_image);
            // console.log(image_array);
            if(parseInt(courent_image)!=parseInt(count_image))
               {
                  
                   
                   // console.log(parseInt(courent_image));
                  
                  $image_demo_edit_more.croppie('bind', {
                    url: image_array[parseInt(courent_image)]

                   }).then(function(){

                        console.log('jQuery bind complete');

                      });

                   // $("#uploadimageModal_edit_more #image_demo_edit_more").attr('src',);
                   $("#uploadimageModal_edit_more #current_image_set").text(parseInt(courent_image)+1);
                   $("#uploadimageModal_edit_more").modal('show');

                   image_array="";
               }

      $('.crop_image_edit_more').html('Crop Image');
      $('.crop_image_edit_more').attr('disabled',false);
          // $('#uploadimageModal_edit_more').modal('hide');

          $('#image_preview_'+row_id).append(data);

          console.log(data);

        }

      });

    })

  });



});