/**
 * Created by uson on 19-12-3.
 */

$(function () {
    var swiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination',
        prevButton: '.swiper-button-prev',
        nextButton: '.swiper-button-next',
        initialSlide :1,
        paginationClickable: true,
        loop: true,
        autoplay:3000,
        autoplayDisableOnInteraction:false
    });
    function changeimg() {
        //当手机导航消失, 取消菜单
        if(!$('.navbar-toggle').attr('display')){
            $('.mob-menu').addClass('hide');
        }

        if($(window).width() < 970){
            $('.swiper-wrapper img').each(function () {
                var mysrc = $(this).attr('src');

                mysrc = mysrc.replace(/\d+/, function (k) {
                    // console.log(k);
                    if(!k.startsWith('0')){
                        return '0'+k;
                    }else{
                        return k;
                    }

                });
                // console.log(mysrc);
                $(this).attr('src', mysrc);
            })
        }else if($(window).width() > 970){
            $('.swiper-wrapper img').each(function () {
                var mysrc = $(this).attr('src');

                mysrc = mysrc.replace(/\d+/, function (k) {
                    if (k[0] == 0) {
                        return k[1];
                    } else {
                        return k;
                    }
                });
                $(this).attr('src', mysrc);
            });
        }
    }
    changeimg();
    $(window).resize(function () {
        // window.addEventListener('resize',calc);
        changeimg();
    });
});
