$(function () {
    var visitType = window.parent.frames.getUrlParam('visitType');
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

/************************ Layer扩展 ****************************/

/* 
* Layer弹出Alert提示框 
* @param message 提示信息 
* @param type 类型 1成功 2失败 3疑问 7提示 
* @param fn (可选)点击后回调方法 
* @return 
*/
function LayerAlert(message, type, fn) {
    // layer.alert(message, { icon: type, closeBtn: 0, move: false }, fn);
    layer.alert(message, { icon: type, move: false }, fn);
}


/* 
* Layer弹出Confirm提示框 
* @param message 确认提示信息 
* @param okfn 确认后回调 function (index) { alert("确认操作后回调,一般执行程序,完成后layer.close(index)关闭Layer"); } 
* @param errorfn (可选)取消操作后回调 function () { alert("取消操作后回调"); } 
* @return 
*/
function LayerConfirm(message, okfn, cancelfn) {
    layer.confirm(
        message,
        { btn: ['是的', '点错了'], icon: 3, title: '提示', move: false },
        okfn,
        cancelfn
    );
}

/* 
* Layer弹出主窗口 
* @param url 网址 
* @param title 标题 
* @param width 宽 
* @param height 高 
* @param closefn (可选)关闭后回调 function (index) { alert("关闭"); layer.close(index);} 
* @return 
*/
function LayerOpenMain(url) {

    return layer.open({
        type: 2,
        anim: 6,
        title: false,
        shadeClose: false, //必须点弹窗关闭按钮关闭  
        shade: 0,
        closeBtn: 0,
        move: false,
        offset: '50px',
        area: ['1000px', '550px'],
        content: url, //让iframe出现滚动条content: ['http://www.xxx.com', 'no']  
    });
}

/* 
* Layer弹出新窗口 
* @param url 网址 
* @param title 标题 
* @param width 宽 
* @param height 高 
* @param closefn (可选)关闭后回调 function (index) { alert("关闭"); layer.close(index);} 
* @return 
*/
function LayerOpen(url, title, width, height, topOffset, btnName, btnFun) {

    var yesFun = btnFun;
    if (yesFun == undefined) {
        yesFun = function (index, layero) {
            frames[$(layero).find("iframe").prop("name")].submit();
        }
    }

    return layer.open({
        type: 2,
        title: title,
        shadeClose: false, //必须点弹窗关闭按钮关闭  
        btn: [btnName, '关闭'],
        shade: 0.1,
        closeBtn: 0,
        move: false,
        offset: topOffset,
        area: [width, height],
        content: url, //让iframe出现滚动条content: ['http://www.xxx.com', 'no']  
        yes: yesFun
    });
}
/* 
* Layer成功消息框
* @param msg 消息内容
* @return 
*/
function LayerSuccessMsg(msg, fun) {
    var index = layer.msg(msg, { icon: 1, shade: 0.01, shadeClose: true, time: 1000 }, fun);
    return index;
}

/* 
* Layer等待消息框
* @param msg 消息内容
* @return 
*/
function LayerLoadMsg(msg, fun) {
    var index = layer.msg(msg, {
        icon: 16
        , shade: 0.01
        , time: 60000
        , success: fun
    });
    return index;
}


/* 
* Layer错误消息框
* @param msg 消息内容
* @return 
*/
function LayerErrorMsg(msg, fun) {
    var index = layer.msg(msg, { icon: 2, time: 3000 }, fun);
    return index;
}
/* 
* Layer加载效果(自动关闭) 
* @param type 0-2加载效果 
* @param minute 几秒钟后消失 
* @return 
*/
function LayerLoadAuto(type, second) {
    layer.load(type, { time: second * 1000, shade: 0.1 });
}

/* 
* Layer加载效果 
* @param type 0-2加载效果 
* @return 
*/
function LayerLoad(type) {
    var index = layer.load(type);
    return index;
}