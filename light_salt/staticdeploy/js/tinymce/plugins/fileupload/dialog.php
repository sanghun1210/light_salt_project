<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>Upload an image</title>
		<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
		<link href="css/dialog.css" rel="stylesheet" type="text/css">
	</head>
<body>

	<form id="uploadForm" action="../../../../action/files_upload.php" method="POST" enctype="multipart/form-data" data-ng-app="demo">
        <input type="hidden" name="project" value="<?=$project?>">
		<input type="hidden" name="note" value="<?=$note?>">
		<p>
			<span class="btn btn-success fileinput-button">
				<i class="glyphicon glyphicon-plus"></i>
				<span>Select files...</span>
				<input id="fileupload" type="file" name="files" multiple>
			</span>
		</p>

		<div id="progress" class="progress">
			<div class="progress-bar progress-bar-primary"></div>
		</div>

		<div id="files" class="files"></div>

	</form>

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
	<script src="js/vendor/jquery.ui.widget.js"></script>
	<script src="js/vendor/jquery.iframe-transport.js"></script>
	<script src="js/vendor/jquery.fileupload.js"></script>
	<script src="js/dialog.js"></script>
</body>
</html>
