var swiper = new Swiper(".mySwiper", {
    slidesPerView: 1,
    spaceBetween: 80,
    grabCursor: true,
    loop: false,
    breakpoints: {
        991: {
            slidesPerView: 3,
        }
    },
    on: {
        click: function (event) {
            const clickedSlide = event.clickedSlide;
            if (clickedSlide) {
                if (clickedSlide.classList.contains('activo')) {
                    clickedSlide.classList.remove('activo');
                } else {
                    document.querySelectorAll('.swiper-slide').forEach(slide => {
                        slide.classList.remove('activo');
                    });
                    clickedSlide.classList.add('activo');
                    clickedSlide.focus();
                }
            }
        }
    }
});
