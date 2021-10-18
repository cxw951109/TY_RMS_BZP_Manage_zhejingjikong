
//条码扫描仪前端驱动

//条码扫描仪按键处理函数
function barCode_Proc(e) {
    var keyChar = String.fromCharCode(e.which);
    if (keyChar == "\r") {
        var scaner_buffer = $(this).data("barcode-scaner-buffer");
        $(this).data("barcode-scaner-buffer", "");
        e.data.proc(scaner_buffer);
    }
    else {
        var scaner_buffer = $(this).data("barcode-scaner-buffer");
        if (scaner_buffer == undefined) {
            scaner_buffer = "";
        }
        scaner_buffer += keyChar;
        $(this).data("barcode-scaner-buffer", scaner_buffer);
    }
}

//条码扫描仪jQuery拓展方法
jQuery.fn.extend({
    barCodeScanerModeEnter: function (findBarCode_Event) {
        $(this).data("barcode-scaner-buffer", "");
        $(this).off("keypress", barCode_Proc);
        $(this).on("keypress", { proc: findBarCode_Event }, barCode_Proc);
    },
    barCodeScanerModeExit: function () {
        $(this).data("barcode-scaner-buffer", "");
        $(this).off("keypress", barCode_Proc);
    }
});

$(function () {
    var visitType = window.parent.frames.getUrlParam('visitType');
    if(visitType=='2')
    {
        $('.virtualkeyboard',window.top.document).remove();
        $('body').virtualkeyboard();
    }
    var $inputImage = $("#inputImage");
    if (window.FileReader) {
        $inputImage.change(function () {

            var $image = $(".image-crop > img")
            $($image).cropper({
                aspectRatio: 1,
                preview: ".img-preview",
                done: function (data) {
                    // 输出结果
                }
            });

            var fileReader = new FileReader(),
                files = this.files,
                file;

            if (!files.length) {
                return;
            }

            file = files[0];

            if (/^image\/\w+$/.test(file.type)) {
                fileReader.readAsDataURL(file);
                fileReader.onload = function () {
                    $inputImage.val("");
                    $image.cropper("reset", true).cropper("replace", this.result);
                };
            } else {
                showMessage("请选择图片文件");
            }
        });
    } else {
        $inputImage.addClass("hide");
    }

    $("#download").click(function () {
        window.open($image.cropper("getDataURL"));
    });

    $("#zoomIn").click(function () {
        $image.cropper("zoom", 0.1);
    });

    $("#zoomOut").click(function () {
        $image.cropper("zoom", -0.1);
    });

    $("#rotateLeft").click(function () {
        $image.cropper("rotate", 45);
    });

    $("#rotateRight").click(function () {
        $image.cropper("rotate", -45);
    });

    $("#setDrag").click(function () {
        $image.cropper("setDragMode", "crop");
    });
    // $("#sYear").chosen({
    //     no_results_text: "没有找到",
    //     allow_single_deselect: false,
    //     disable_search: true
    // });
    SetMonth($("#sYear").val());
    $("#sYear").change(function () {
        SetMonth($("#sYear").val());
    });
})
var currentYear, currentMonth;
//获取url中的参数
function getUrlParam(key) {
    var search = location.search.slice(1); //得到get方式提交的查询字符串
    var arr = search.split("&");
    for (var i = 0; i < arr.length; i++) {
        var ar = arr[i].split("=");
        if (ar[0] == key) {
            if (unescape(ar[1]) == 'undefined') {
                return "";
            } else {
                return unescape(ar[1]);
            }
        }
    }
    return "";
}

var elem = document.querySelector('.js-switch');
var switchery = new Switchery(elem, {
    color: '#1AB394'
});

var elem_2 = document.querySelector('.js-switch_2');
var switchery_2 = new Switchery(elem_2, {
    color: '#f8ac59'
});

var elem_3 = document.querySelector('.js-switch_3');
var switchery_3 = new Switchery(elem_3, {
    color: '#1AB394'
});

$('.input-group.date').datepicker({
    startView: 1,
    todayBtn: "linked",
    keyboardNavigation: false,
    forceParse: false,
    autoclose: true,
    format: "yyyy-mm-dd"
});

$(".btn-group .btn").click(function () {

    $(this).addClass("active").siblings(".btn").removeClass("")

})
function msg(a, b) {
    layer.msg(a, { shift: 0, time: 1500 }, function () {
        b();
    })
}

function SetMonth(year) {
    $("#sMonth").empty();
    $("#sMonth").append("<option value='0' hassubinfo='true'>所有月份</option>");
    for (var i = 0; i < 12; i++) {
        if (year == currentYear && i >= currentMonth) {
            break;
        }
        $("#sMonth").append("<option value='" + (i + 1) + "' hassubinfo='true'>" + (i + 1) + "月</option>");

    }
    // $("#sMonth").trigger("chosen:updated")
    // $("#sMonth").chosen({
    //     no_results_text: "没有找到",
    //     allow_single_deselect: false,
    //     disable_search: true
    // });

}




function uuid() {
    var s = [];
    var hexDigits = "0123456789abcdef";
    for (var i = 0; i < 36; i++) {
        s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
    }
    s[14] = "4";  // bits 12-15 of the time_hi_and_version field to 0010
    s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);  // bits 6-7 of the clock_seq_hi_and_reserved to 01
    s[8] = s[13] = s[18] = s[23] = "-";
 
    var uuid = s.join("");
    return uuid;
}



