$(function () {
    //设置富文本
    tinymce.init({
        selector: '.mytextarea',
        height: 400,
        plugins: "quickbars emoticons",
        inline: false,
        toolbar: true,
        menubar: true,
        quickbars_selection_toolbar: 'bold italic | link h2 h3 blockquote',
        quickbars_insert_toolbar: 'guickimage quicktable',
    });
    //验证手机号码
    $('#InputPhone').blur(function () {
        console.log('aaa');
    });
    $('.right1').hide();
    $('.right1').eq(0).show();
    $("#left p").first().css({'background-color': 'rgba(30,150,196,0.94)'});
    //切换右侧div
    $("#left p").each(function (i) {
        $(this).click(function () {
            $("#left p").css({'background-color': 'rgba(30,150,196,0.94)'});
            $(this).css({
                'background-color': 'skyblue',
                'box-shadow': '1px 1px 1px 1px'
            }).siblings().css({'background-color': 'transparency', 'box-shadow': 'none'});
            $('.right1').hide();
            $('.right1').eq(i).show();
            // if (index == 0) {
            //         $(".right1").eq(0).show();
            //         $(".right1").eq(1).hide();
            //     } else {
            //         $(".right1").eq(0).hide();
            //         $(".right1").eq(1).show();
            //     }
        });

    });
    //相册图片的删除
    $('.photo_del').click(function () {
        //判断是否删除
        flag = confirm('确定删除此图片嘛?')
        if(flag){
           //获取属性值tag,tag属性的值就是图片的主键
        //拿住照片的id
        let pid = $(this).attr('tag')
        //1. ajax , 2.location.href
        //外部链接不能使用模板，模板语法只能在模板中使用
        location.href = '/user/photo_del?pid=' + pid;
        }


    });
});