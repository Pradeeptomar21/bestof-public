$(document).ready(function(){


  $image_demo_edit_more_gm = $('#image_demo_edit_gm').croppie({
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


  $('#upload_file_image_thum_edit_gm').on('change', function(){

    reader = new FileReader();
    reader.onload = function (event) {
    $image_demo_edit_more_gm.croppie('bind', {
    url: event.target.result

    }).then(function(){

        console.log('jQuery bind complete');

      });

    }

    reader.readAsDataURL(this.files[0]);
   $('#uploadimage_gm').modal('show');
  
  });



  $('.crop_image_edit_gm').click(function(event){
  $('.crop_image_edit_gm').html('Image Uploading');
    $image_demo_edit_more_gm.croppie('result', {

      type: 'canvas',
      size: 'viewport'

    }).then(function(response){

      $.ajax({

        url:"image_upload_more.php",
        type: "POST",
        data:{"image": response},

        success:function(data)

        {

      $('.crop_image_edit_gm').html('Crop Image');
          $('#uploadimage_gm').modal('hide');

          $('#image_preview_gm').append(data);

          console.log(data);

        }

      });

    })

  });

 
});