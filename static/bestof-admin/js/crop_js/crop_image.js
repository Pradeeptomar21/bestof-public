$(document).ready(function(){


  $image_crop = $('#image_demo_edit').croppie({

    enableExif: true,

    viewport: {

      width:200,

      height:50,


      type:'square' 

    },

    boundary:{

      // width:400,

      height:400

    }

  });


  $('#project_map_value').on('change', function(){

      var reader = new FileReader();
      reader.onload = function (event) {
      $image_crop.croppie('bind', {

        url: event.target.result

      }).then(function(){

        console.log('jQuery bind complete');

      });

    }
     reader.readAsDataURL(this.files[0]);

    $('#uploadimageModal_edit').modal('show');

  });



  $('.crop_image_edit').click(function(event){

$('.crop_image_edit').html('Image Uploading <img src="http://18.219.135.43/static/dist/img/tenor1.gif" style="width:50px; height:30px; padding:10px;">');
$('.crop_image_edit').attr('disabled',true);
var partner_id = $('#partner_id').val();
// alert(partner_id);
    $image_crop.croppie('result', {

      type: 'canvas',

      size: 'viewport'

    }).then(function(response){

      // console.log("dsp_patel");
      // console.log(response);

      $.ajax({

        method:"POST",
        url:"/admin/manage-delivery-partner/crop-image?partner-id="+partner_id,
        data:{"image":response},
        dataType:"json",
        
        success:function(data)
        {

          console.log("jhygsdfvhvfv");
          console.log(data);

          $('.crop_image_edit').html('Crop Image');
          $('.crop_image_edit').attr('disabled',false);

          $('#uploadimageModal_edit').modal('hide');

          $('.image_preview').empty();
          $('.image_preview').html(data);
          window.location.href = "/admin/manage-delivery-partner";

          console.log(data);
           // window.location.href = "http://18.219.135.43/project_info/";


        }

      });

    })

  });



});