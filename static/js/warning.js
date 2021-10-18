 // 定时无操作退出
var quiteTime = 3600;
    var currentTime = 0;
    $("*").click(function () {
        currentTime = 0;
    });

    $('*').mouseover(function () {
         currentTime = 0;
    });
    setInterval(function () {
        currentTime++;
        var strHref='/account/login'
        var visitType=parent.getUrlParam('visitType');
        if(visitType!="")
        {
            strHref='/account/login?visitType='+visitType;
        }
        if(currentTime>=quiteTime)
        {
            top.location.href = strHref;
            // if(parent.location.href === 'http://127.0.0.1:9000/'){
            //     top.location.href = strHref;
            // }else{
            //     top.location.href = strHref;
            // }
        }
    }, 1000);

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


