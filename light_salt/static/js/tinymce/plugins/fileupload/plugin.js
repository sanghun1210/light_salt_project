tinymce.PluginManager.add('fileupload', function(editor, url) {
	
	function showDialog() {
		editor.windowManager.open({
			title: 'Upload an file',
			url: url + '/dialog.htm',
			width: 350,
			height: 135,
			buttons: [{
				text: 'Close',
				onclick: 'close'
			}]
		});
	}
	
	// Add a button that opens a window
	editor.addButton('fileupload', {
		tooltip: 'Upload an file',
		icon: 'upload',
		onclick: showDialog
	});

	// Adds a menu item to the tools menu
	editor.addMenuItem('fileupload', {
		text: 'Upload file',
		icon : 'upload',
		context: 'insert',
		onclick: showDialog
	});
});
