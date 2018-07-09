 
 $(function () {
	'use strict';

	$('#fileupload').fileupload({
		url: $('#uploadForm').attr('action'),
		dataType: 'json',
		done: function (e, data) {
			$.each(data.result.files, function (index, file) {
				var uuid = top.guid();
				top.tinymce.EditorManager.activeEditor.insertContent('<a name="airnote_attache_file" id="'+ uuid+ '" href="'+file.url+'">'+file.name+'</a>');
				top.tinymce.EditorManager.activeEditor.insertContent('('+file.size+')');
				//top.airnoteAddEvent(uuid, file.url);
			});
			top.tinymce.EditorManager.activeEditor.windowManager.close(window);
		},
		progressall: function (e, data) {
			var progress = parseInt(data.loaded / data.total * 100, 10);
			$('#progress .progress-bar').css(
				'width',
				progress + '%'
			);
		}
	}).prop('disabled', !$.support.fileInput)
	.parent().addClass($.support.fileInput ? undefined : 'disabled');
});
