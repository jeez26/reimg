function initComparisons() {
    var x, i;
    x = document.getElementsByClassName("img-comp-overlay");
    for (i = 0; i < x.length; i++) {
        compareImages(x[i]);
    }

    function compareImages(img) {
        var slider, img, clicked = 0,
            w, h, line;
        w = img.offsetWidth;
        h = img.offsetHeight;
        img.style.width = 59. + "%";
        slider = document.getElementsByClassName("img-comp-slider")[0];
        line = document.getElementsByClassName("img-comp-line")[0];

        img.parentElement.insertBefore(slider, img);
        slider.style.top = 27 + "%";
        slider.style.left = 53.4 + "%";
        line.style.left = 59 + "%";
        slider.addEventListener("mousedown", slideReady);
        window.addEventListener("mouseup", slideFinish);
        slider.addEventListener("touchstart", slideReady);
        window.addEventListener("touchend", slideFinish);

        function slideReady(e) {
            e.preventDefault();
            clicked = 1;
            window.addEventListener("mousemove", slideMove);
            window.addEventListener("touchmove", slideMove);
        }

        function slideFinish() {
            clicked = 0;
        }

        function slideMove(e) {
            var pos;
            if (clicked == 0) return false;
            pos = getCursorPos(e)
            if (pos < 0) pos = 0;
            if (pos > w) pos = w;
            if (pos > 1035 && pos < 1600) slide(pos);
        }

        function getCursorPos(e) {
            var a, x = 0;
            e = (e.changedTouches) ? e.changedTouches[0] : e;
            a = img.getBoundingClientRect();
            x = e.pageX - a.left;
            x = x - window.pageXOffset;
            return x;
        }

        function slide(x) {
            img.style.width = x + "px";
            line.style.left = img.offsetWidth - (line.offsetWidth / 2) + "px";
            slider.style.left = img.offsetWidth - (slider.offsetWidth / 2) + "px";
        }
    }
}

function uploadFile() {
    var file = $("#file").prop('files');
    console.log(file);
    var formdata = new FormData();
    formdata.append("scale", $('.input_number').val());
    formdata.append("alghoritm", String($('.choose_alghoritm_form').serialize()).split('=')[1]);
    formdata.append("file", document.getElementById('file').files[0]);

    $.ajax({
        type: "POST",
        url: "/load-file",
        headers: { "X-CSRFToken": $('.csrf_token').val() },
        data: formdata,
        contentType: false,
        processData: false,
        success: function(data) {
            if (data['result'] === 'error') {
                alert(data['data']);
            } else {
                var a = document.createElement("a"); //Create <a>
                a.href = "data:image/jpg;base64," + data['image']; //Image Base64 Goes here
                a.download = "Image.jpg"; //File name Here
                a.click(); //Downloaded file
                window.location.href = "/thanks";
            }
        },
        error: function(data) {
            alert('error 2');
        }
    });


}


function completeHandler(event) {
    $("#status").val("Upload Failed");
}

function errorHandler(event) {
    $("#status").val("Upload Failed");
}

function abortHandler(event) {
    $("#status").val("Upload Aborted");
}


function drag_and_drop() {
    var dropZone = $("#drop_zone");
    var mouseOverClass = "mouseOverClass";
    var ooleft = dropZone.offset().left;
    var ooright = dropZone.outerWidth() + ooleft;
    var ootop = dropZone.offset().top;
    var oobottom = dropZone.outerHeight() + ootop;
    var inputFile = $("#file");
    var flag = true;

    document.getElementById("drop_zone").addEventListener("dragover", function(e) {
        e.preventDefault();
        e.stopPropagation();
        if (flag) {
            dropZone.addClass(mouseOverClass);
            flag = false;
        }
        var x = e.pageX;
        var y = e.pageY;

        if (!(x < ooleft || x > ooright || y < ootop || y > oobottom)) {
            inputFile.offset({ top: y - 15, left: x - 100 });
        } else {
            inputFile.offset({ top: -400, left: -400 });
        }
    }, true);

    document.getElementById("drop_zone").addEventListener("dragleave", function(e) {
        dropZone.removeClass(mouseOverClass);
        flag = true;
    }, true);

    document.getElementById("file").addEventListener("change", function(e) {
        if (inputFile.prop('files').length) {
            dropZone.removeClass(mouseOverClass);
            flag = true;
            file = inputFile.prop('files')[0];
            let file_name = "";
            if (file.name.length > 12) {
                for (let i = 0; i < 5; i++) {
                    file_name += file.name[i];
                }
                file_name += "...";
                let temp = "";
                for (let i = 1; i < 10; i++) {
                    temp += file.name[file.name.length - i];
                }
                file_name += temp.split("").reverse().join("");
            } else {
                file_name = file.name;
            }
            $('.load_file_title').text(file_name + ' is ready!');
            $('#upload').text('change file');
        }
    });
}


function switch_about_block() {
    form_alg = $('.choose_alghoritm_form');
    document.getElementsByClassName("choose_alghoritm_form")[0].addEventListener("change", function(e) {
        if ($('#NNI')[0].checked) {
            $('#alg_titile').text('N-N interpolation');
            $('.about_NNI').prop('style', 'display: block');
            $('.about_BI').prop('style', 'display: none');
            $('.about_BIL').prop('style', 'display: none');

        }
        if ($('#BI')[0].checked) {
            $('#alg_titile').text('Bicubic interpolation');
            $('.about_NNI').prop('style', 'display: none');
            $('.about_BI').prop('style', 'display: block');
            $('.about_BIL').prop('style', 'display: none');
        }
        if ($('#KIM')[0].checked) {
            $('#alg_titile').text('Bilinear interpolation');
            $('.about_NNI').prop('style', 'display: none');
            $('.about_BI').prop('style', 'display: none');
            $('.about_BIL').prop('style', 'display: block');
        }
    });
}


$(document).ready(function() {
    initComparisons();
    switch_about_block();
    drag_and_drop();
    $('#upload').click(function() {
        $('#file').click();
    });

});