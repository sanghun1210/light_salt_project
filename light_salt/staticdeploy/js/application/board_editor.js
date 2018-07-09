
 	tinyMCE.init({ 
		selector: '#lightsalt',
        paste_data_images: true,
		menubar : false,
		statusbar: false,
		plugins: 'fileupload image imagetools print preview paste searchreplace autolink directionality visualblocks visualchars fullscreen link table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists textcolor contextmenu colorpicker textpattern',
		toolbar: 'undo redo  | bold italic | quicklink h2 h3 blockquote | forecolor backcolor | bullist numlist outdent indent | styleselect fontselect fontsizeselect | link image',
		language : 'ko_KR',
		content_css: [
		  '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
		  '//www.tinymce.com/css/codepen.min.css'
		], 
		
		theme_advanced_fonts: "굴림=Gulim;궁서=Gungsuh;돋움=Dotum;바탕=Batang;"+
		                      "Andale Mono=andale mono,times;"+
							  "Arial=arial,helvetica,sans-serif;"+
							  "Arial Black=arial black,avant garde;"+
							  "Book Antiqua=book antiqua,palatino;"+
							  "Comic Sans MS=comic sans ms,sans-serif;"+
							  "Courier New=courier new,courier;"+
							  "Georgia=georgia,palatino;"+
							  "Helvetica=helvetica;"+
							  "Impact=impact,chicago;"+
							  "Symbol=symbol;"+
							  "Tahoma=tahoma,arial,helvetica,sans-serif;"+
							  "Terminal=terminal,monaco;"+
							  "Times New Roman=times new roman,times;"+
							  "Trebuchet MS=trebuchet ms,geneva;"+
							  "Verdana=verdana,geneva;"+
							  "Webdings=webdings;"+
							  "Wingdings=wingdings,zapf dingbats",
        force_br_newlines: false,
		relative_urls : false,
        force_p_newlines: false,
		toolbar_items_size: 'small',
        remove_linebreaks: false,
        remove_trailing_nbsp: false,
		remove_trailing_brs: true,
		forced_root_block : false,
        paste_auto_cleanup_on_paste: false,  
        height : "450",
        paste_retain_style_properties : "all",
        paste_strip_class_attributes : "none",					
		automatic_uploads: true,
		extended_valid_elements: "+@[data-options]",
        custom_elements: "block, airnote",
        images_upload_handler: function (blobInfo, success, failure) 
		{
		  var xhr, formData;
		  
		  //확장자 체크(only image)

          xhr = new XMLHttpRequest();
          xhr.withCredentials = false;
          xhr.open('POST', imageUploadUrl, true);

          xhr.onload = function() {
            var json;

            if (xhr.status != 200) {
              failure("HTTP Error: " + xhr.status);
              return;
            }

            json = JSON.parse(xhr.responseText);
            if (!json || typeof json.location != "string") {
              failure("Invalid JSON: " + xhr.responseText);
              return;
            }
			console.log("image upload success:",json.location);
            success(json.location);
			//tinymce.activeEditor.fire('change');			
          };

          formData = new FormData();
          formData.append('file', blobInfo.blob(), blobInfo.filename());
		  formData.append('csrfmiddlewaretoken', csrf_token);

          xhr.send(formData);		          	  
        },
	    setup: function (ed) {
		  ed.on('init', function (e) {
			//e.preventDefault();
			var fileName = "";
			var MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver;
      		if (typeof MutationObserver != 'undefined')
            {   
              // select the target node
              var targets =ed.getDoc().querySelector('body');
              // create an observer instance
              var observer = new MutationObserver(function(mutations) {
				//console.log( "mutations2 :",mutations);
                mutations.forEach(function(mutation) { 
                  if ( mutation.type == 'childList' ) 
				  {	
					if( mutation.removedNodes[0] && 
					    mutation.removedNodes[0].nodeName.toLowerCase() == "img") {  //서버에서 이미지 삭제처리		
                      
					  //이미지 사이즈 변경 이면 skip
					  if( mutation.removedNodes[0].className == "mce-clonedresizable" )	
                        return;						  
					  
					  fileName = mutation.removedNodes[0].getAttribute("src");
					  if(fileName && justDeletedImg != fileName) {
					    deleteImage(fileName); 
                        console.log("mutations image deleted: "+fileName);  					
				      }
					}	
				  }  
				  
                });    
              });

              // configuration of the observer:
              var config = { subtree:true, childList: true }
              // pass in the target node, as well as the observer options
              observer.observe(targets, config);
            }
            else // fallback for older browsers
            {
              $(ed.getBody()).bind('DOMNodeRemoved', function(e) {
				  if(e.element.firstChild.nodeName.toLowerCase() == "img" ) {
					//alert( "image deleted");  
				  }
              });
            }			
		  });
		  
		  ed.on('Change', function(e) {
			var changedBlcokId = "";  
			var data = "";
		    var selectedNode = ed.selection.getNode();	  
		    var changedBlcokNode = ed.dom.getParent(selectedNode, 'block');
			
			if(changedBlcokNode ) {
              var images =changedBlcokNode.getElementsByTagName("img");
              for ( var i= 0; i < images.length; i++ ) {	
			    var img = String(images[i].getAttribute("src"));			    
                if( img.indexOf('blob:') != -1 ) {		//저장하지 않음	  
				  //console.log("image blob :",img);
                  return; 				  
                }				  
		      }
			  			  
			  changedBlcokId = changedBlcokNode.getAttribute("id");
			  prev_changed_block_id = changedBlcokId;
			  data = changedBlcokNode.innerHTML;		  
			}
            else // undo일 경우 null 발생
			{
			  changedBlcokId = prev_changed_block_id;
			  changedBlcokNode = selectedNode;
			  data = changedBlcokNode;
			}				
		  });		  
          				
		  ed.on('Undo Redo', function(e) { 
		    var selectedNode = ""; 
			var filePath = "";
	        var data = e.target.undoManager.data;
			var before_content = "";
			var target_obj = "";
			var curr_obj = "";
			var exec_type = "";
			//console.log(e.+" :" e );
			
			if( data.length  > 1 )
			{
              var current_content = e.level.content; 
			  if( e.type == "redo")
			    before_content = data[data.length-2].content;
			  else
				before_content = data[data.length-1].content;  
			
			  var parser = new DOMParser()
              var current_elm = parser.parseFromString(current_content, "text/html");
			  var before_elm = parser.parseFromString(before_content, "text/html");

			  //images find for recovery
			  var current_imgs = current_elm.getElementsByTagName("img");
			  var before_imgs = before_elm.getElementsByTagName("img");

              if( current_imgs.length > before_imgs.length )
			  {		
				curr_obj = current_imgs;
				target_obj = before_imgs;
				exec_type = "R"; // recovery
			  }	
              else if( current_imgs.length < before_imgs.length )
              {
				curr_obj = before_imgs;
				target_obj = current_imgs;
				exec_type = "D"; // recovery
			  }
  			  console.log("current images:"+current_imgs.length+",before images: "+before_imgs.length);	
			  if( current_imgs.length != before_imgs.length )
			  {			
				for(var i=0; i<curr_obj.length; i++)
				{
				  filePath = curr_obj[i].getAttribute("src");	
				  if(target_obj[i] && filePath == target_obj[i].getAttribute("src")) {
					// skip  
				  }
                  else 
				  {
					if( exec_type == "R") {	
					  recoveryFile(filePath);				
                      justDeletedImg=""; 							  
				      console.log("image re-saved: "+filePath);  
					}
					else if( exec_type == "D") {		
					  deleteImage(filePath);
					  console.log("image delete:" +filePath );
                    }                  			
				  }
				}	  
			  }			  
			}
		  }); 
		  	  
        },
			
		file_picker_types: 'image',		
		file_picker_callback: function(cb, value, meta) 
		{
		  var input = document.createElement('input');
		  input.setAttribute('type', 'file');
		  input.setAttribute('accept', 'image/*');
          			
		  input.onchange = function() {
			var file = this.files[0];
			var reader = new FileReader();
			reader.onload = function () {
			  // Note: Now we need to register the blob in TinyMCEs image blob
			  // registry. In the next release this part hopefully won't be
			  // necessary, as we are looking to handle it internally.
			  var id = 'blobid' + (new Date()).getTime();
			  var blobCache =  tinymce.activeEditor.editorUpload.blobCache;
			  var base64 = reader.result.split(',')[1];
			  var blobInfo = blobCache.create(id, file, base64);
			  blobCache.add(blobInfo);

			  // call the callback and populate the Title field with the file name
			  cb(blobInfo.blobUri(), { title: file.name });
		    };
		    reader.readAsDataURL(file);
		  };		
		  input.click();
        } 
	  });
    
	function deleteImage(imageName)
	{
  	  //alert(imageName);
	  $.ajax({
		url : deleteImageUrl,
		cache: false,
		data: { csrfmiddlewaretoken: csrf_token,
				imageName: imageName
			  },
		type: 'POST',
		error : function(){
		  console.log("image delete error") ;
		},
		success : function(result){
		  justDeletedImg = imageName;
		  console.log("image delete success") ;
		}
	  });	
	}
  	function recoveryFile(filePath)
	{
	  $.ajax({
		url : recoveryImageUrl,
		cache: false,
		data: { csrfmiddlewaretoken: csrf_token,
				filePath: filePath
			  },
		type: 'POST',
		error : function(){
		  console.log("attaches recovery error") ;
		},
		success : function(result){
		  console.log("attaches recovery success") ;
		}
	  });	  
	}
