$(function () {
    initSwiper();
    initnav();
});


function initSwiper() {
    var mySwiper = new Swiper ('#topSwiper', {
    // direction: 'vertical',
        loop: true,
        autoplay:true,  //是否自动滚动
        speed:3000,  //速度,即间隔多长时间自动切换

        // 如果需要分页器
        pagination: '.swiper-pagination',
  })
}

function initnav() {
     var swiper = new Swiper('#swiperMenu', {
        // pagination: '.swiper-pagination',
        slidesPerView: 3,
        loop: true,
        // paginationClickable: true,
        spaceBetween: 10
    })
}
