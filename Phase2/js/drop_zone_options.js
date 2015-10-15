/**
 * Created by lixianshu on 10/9/15.
 */
//Dropzone.autoDiscover = false;
$(document).ready(function () {
    //Dropzone.autoDiscover = false;
    Dropzone.options.myDropZone = { // The camelized version of the ID of the form element
        // The configuration we've talked about above
        //url:"{{blobstore_url}}",
        //previewsContainer: ".dropzone-previews",
        init: function () {
            var $self = this;
            $self.on("processing", function (file) {
                $.ajax({
                    url: '/getUploadUrl',
                    type: 'POST',
                    dataType: "json",
                    success: function (data) {
                        $self.options.url = data;
                    }
                });
            });
            $("button#clear-dropzone").on("click", function () {
                // Using "_this" here, because "this" doesn't point to the dropzone anymore
                $self.removeAllFiles();
                // If you want to cancel uploads as well, you
                // could also call _this.removeAllFiles(true);
            });

            var submitButton = $("#submit-all");

            submitButton.on("click", function () {
                $self.processQueue(); // Tell Dropzone to process all queued files.
            });

            // You might want to show the submit button only when
            // files are dropped here:
            this.on("addedfile", function () {
                // Show submit button here and/or inform user to click it.
            });
        },
        autoProcessQueue: false,
        parallelUploads: 100,
        maxFiles: 100,
        uploadMultiple: true,
        addRemoveLinks: true,
        //dictRemoveFile: "Cancel Upload",
        //dictCancelUpload: "Remove Preview",
    }
});



