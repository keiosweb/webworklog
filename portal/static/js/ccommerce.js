var ccommerce = {
    animateSpeed: 700,

showPreview: function () {
     $('body').one('click', function (e) {
        $('#categorylist').removeClass('col-md-12').addClass('col-md-7');
        $('#categorypage').addClass('categorypage-open');
    } 
},
hidePreview: function () {
    $('body').one('click', function (e) {
        if ($(e.target).closest('#categorypage').length === 0 && $(e.target).closest('.categorypage-open').length === 0) {
            ccommerce.performHidePreview();
        } else {
            ccommerce.hidePreview();
        }
    });
},
performHidePreview: function () {
    $('#categorylist').removeClass('col-md-7').addClass('col-md-12');
    $('#categorypage').removeClass('categorypage-open');
    ccommerce.preview = false;
}
}



var UploadManager = {
    animateSpeed: 700,
    extensions: {
        'img.png': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tga', 'tiff'],
        'pdf.png': ['pdf'],
        'doc.png': ['doc', 'docx'],
        'zip.png': ['zip', 'rar', 'gzip', 'tar.gzip'],
        'xls.png': ['xlsx', 'xls'],
        'ppt.png': ['pptx', 'ppt'],
        'mp3.png': ['wav', 'mp3', 'ogg'],
        'mov.png': ['mp4', 'mpg', 'avi', 'mkv', 'vid']
    },
    getFileIcon: function (ext) {
        var extension = ext ? ext.toLowerCase() : null;
        for (var icoName in UploadManager.extensions) {
            for (var i = 0; i < UploadManager.extensions[icoName].length; i++) {
                if (UploadManager.extensions[icoName][i] === extension) return icoName;
            }
        }
        return 'default.png';
    },
    renderFileBox: function (fileObj, index) {
        switch (fileObj.type) {
            case 'dir':
                $('<div class="UM-dir col-xlg-1 col-lg-2 col-md-2 col-xs-3 file-container-col">' +
                    '<a href="' + UploadManager.baseUrl + '?path=' + (UploadManager.currentPath ? UploadManager.currentPath + '/' : '') + fileObj.basename + '">' +
                    '<div class="file-container">' +
                    '<div class="file-icon-container">' +
                    '<img class="img-responsive center-block" src="/plugins/voipdeploy/uploadmanager/assets/ico/dir.png">' +
                    '</div>' +
                    '<div class="UM-file-label">' + fileObj.basename + '</div>' +
                    '<div class="UM-checkbox-container">' +
                    '<input id="dir-box-' + index + '" type="checkbox" class="file-selector css-checkbox" value="' + fileObj.basename + '">' +
                    '<label for="dir-box-' + index + '" class="css-label"></label>' +
                    '</div>' +
                    '</div>' +
                    '</a>' +
                    '</div>').appendTo('.UM-control-grid').data('fileObj', fileObj).hide().css('z-index', index);
                break;
            case 'file':
                $('<div class="UM-file col-xlg-1 col-lg-2 col-md-2 col-xs-3 file-container-col">' +
                    '<a href="#">' +
                    '<div class="file-container">' +
                    '<div class="file-icon-container">' +
                    '<img class="img-responsive center-block" src="/plugins/voipdeploy/uploadmanager/assets/ico/' + UploadManager.getFileIcon(fileObj.extension) + '">' +
                    '</div>' +
                    '<div class="UM-file-label">' + fileObj.basename + '</div>' +
                    '<div class="UM-checkbox-container">' +
                    '<input id="file-box-' + index + '" type="checkbox" class="file-selector css-checkbox" value="' + fileObj.basename + '">' +
                    '<label for="file-box-' + index + '" class="css-label"></label>' +
                    '</div>' +
                    '</div>' +
                    '</a>' +
                    '</div>').appendTo('.UM-control-grid').data('fileObj', fileObj).on('click',function (e) {
                    UploadManager.showPreview($(this).data('fileObj'), $(this));
                }).hide().css('z-index', index);
                break;
        }
    },
    animateFileBoxes: function () {
        var $bawkses = $('.file-container-col');
        $bawkses.each(function (i) {
            $(this).delay((i) * UploadManager.animateSpeed / $bawkses.length).queue(function () {
                $(this).addClass('animated zoomIn').dequeue().show();
            });
        })
    },
    showPreview: function (fileObj, handle) {
        UploadManager.setFileActive(handle);
        if (!UploadManager.preview) {
            UploadManager.preview = true;
            $('.UM-grid-container').removeClass('col-md-12').addClass('col-md-7');
            $('.UM-preview-panel').addClass('UM-preview-panel-open');
            UploadManager.renderPreview(fileObj);
            setTimeout(UploadManager.hidePreview, 50);
        } else {
            UploadManager.renderPreview(fileObj);
        }
    },
    hidePreview: function () {
        $('body').one('click', function (e) {
            if ($(e.target).closest('.UM-preview-panel').length === 0 && $(e.target).closest('.file-container-col').length === 0) {
                UploadManager.performHidePreview();
            } else {
                UploadManager.hidePreview();
            }
        });
    },
    performHidePreview: function () {
        $('.UM-grid-container').removeClass('col-md-7').addClass('col-md-12');
        $('.UM-preview-panel').removeClass('UM-preview-panel-open');
        UploadManager.preview = false;
        UploadManager.removeActiveFile();
    },
    renderPreview: function (fileObj) {
        var preview = $('.UM-preview');
        var spinner = $('<div class="spinner"></div>');
        var notPreviewable = $('<div class="UM-file-info-box center-block"><div class="UM-file-info">Sorry, this file cannot be previewed. Please take a look at its data below.</div></div>');
        preview.empty();
        preview.append(spinner);
        if (!fileObj.hasOwnProperty('extension')) {
            preview.empty();
            notPreviewable.appendTo(preview);
        } else {
            switch (fileObj.extension.toLowerCase()) {
                case 'pdf':
                    preview.empty();
                    $('<object data="' + fileObj.path + '#view=FitV" type="application/pdf" width="100%" height="700">' +
                        '<p>PDF plugin is not installed in your browser. Use download link below.</p>' +
                        '</object>').appendTo(preview);
                    break;
                case 'png':
                case 'jpg':
                case 'jpeg':
                case 'gif':
                case 'tiff':
                case 'bmp':
                case 'tga':
                    var img = new Image();
                    img.onload = function () {
                        preview.empty();
                        $('<img class="img-responsive animated zoomIn center-block">').attr('src', this.src).appendTo(preview);
                    };
                    img.src = window.location.origin + '/' + fileObj.path;
                    break;
                default:
                    preview.empty();
                    notPreviewable.appendTo(preview);
                    break;
            }
        }
        UploadManager.renderFileData(fileObj);
    },
    renderFileData: function (fileObj) {
        var dataContainer = $('.UM-data');
        dataContainer.empty();
        console.log(fileObj)
        var fileDataTemplate = $('<div class="UM-file-info-box center-block">' +
            '<h2 class="UM-file-info-header">' + fileObj.basename + '</h2>' +
            '<span class="UM-file-info">Full URL: <input type="text" class="form-control" value="' + window.location.origin + encodeURI(fileObj.path) + '"></span>' +
            '<span class="UM-file-info">Description: <textarea class="UM-file-desc form-control">' + fileObj.description + '</textarea></span>' +
            '<a class="btn btn-primary oc-icon-save center-block UM-download-btn UM-save-description">Save description</a>' +
            '<a class="btn btn-primary oc-icon-download center-block UM-download-btn" href="' + window.location.origin + encodeURI(fileObj.path) + '" target="_blank" download>Download this file</a>' +
            '</div>');
        fileDataTemplate.appendTo(dataContainer);
        $('.UM-save-description').one('click', function () {
            $.request('onSaveDesc', {
                data: {
                    path: UploadManager.currentPath,
                    file: fileObj.basename,
                    desc: $('.UM-file-desc').val()
                },
                success: function (data, textStatus, jqXHR) {
                    this.success(data, textStatus, jqXHR);
                    UploadManager.performHidePreview();
                    UploadManager.refresh(data);
                }
            });
        });
    },
    setFileActive: function (handle) {
        UploadManager.removeActiveFile();
        UploadManager.activeFile = handle;
        handle.addClass('UM-active-file')
    },
    removeActiveFile: function () {
        if (UploadManager.activeFile) UploadManager.activeFile.removeClass('UM-active-file');
    },
    activeFile: false,
    preview: false,
    baseUrl: null,
    currentPath: null,
    refresh: function (data) {
        UploadManager.baseUrl = data.URL;
        UploadManager.currentPath = data.currentPath;
        if (data.fileListUpdate.length === 0) {
            $('.UM-control-grid').empty().append('No directories created yet!');
        } else {
            var folders = data.fileListUpdate.filter(function (fileObj) {
                if (fileObj.type === 'dir') return fileObj;
            });
            var files = data.fileListUpdate.filter(function (fileObj) {
                if (fileObj.type === 'file') return fileObj;
            });
            folders.sort(UploadManager.sortAlpha);
            files.sort(UploadManager.sortAlpha);
            $('.UM-control-grid').empty();
            folders.forEach(function (dir, index) {
                UploadManager.renderFileBox(dir, index);
            });
            files.forEach(function (file, index) {
                UploadManager.renderFileBox(file, index);
            });
            UploadManager.addMoveHandlers();
            UploadManager.animateFileBoxes();
        }
    },
    addMoveHandlers: function () {
        var droppables = $('.UM-dir');
        var draggables = $('.UM-file');
        droppables.droppable({
            hoverClass: "ui-state-hover",
            drop: function (event, ui) {
                var dir = $(this).data('fileObj');
                var file = ui.draggable.data('fileObj');
                ui.draggable.removeClass('zoomIn').addClass('zoomOut');
                $.request('onMove', {
                    data: {
                        path: UploadManager.currentPath,
                        dir: dir.basename,
                        file: file.basename
                    },
                    success: function (data, textStatus, jqXHR) {
                        this.success(data, textStatus, jqXHR);
                        UploadManager.performHidePreview();
                        UploadManager.refresh(data);
                    }
                });
            }
        });
        draggables.draggable({
            revert: "invalid",
            zIndex: 9999,
            start: function (event, ui) {
                droppables.append($('<div class="arrow bounce UM-drop-arrow"></div>'));
            },
            stop: function (event, ui) {
                $('.UM-drop-arrow').remove();
            }
        });
    },
    sortAlpha: function (a, b) {
        if (a.basename < b.basename) return -1;
        if (a.basename > b.basename) return 1;
        return 0;
    }
};
$(document).on('UploadManagerReady', function (e, data) {
    if (!window.location.origin)
        window.location.origin = window.location.protocol + "//" + window.location.host;
    UploadManager.refresh(data);
});