document.addEventListener('DOMContentLoaded', function () {
    const serviceItems = document.querySelectorAll('.service-item');

    serviceItems.forEach(item => {
        item.addEventListener('mousemove', function (e) {
            const { offsetX: x, offsetY: y } = e;

            const { offsetWidth: width, offsetHeight: height } = this;

            const move = 20;

            const xMove = x / width * (move * 2) - move;
            const yMove = y / height * (move * 2) - move;

            this.querySelector('img').style.transform = `translate(${xMove}px, ${yMove}px)`;
        });

        item.addEventListener('mouseleave', function () {
            this.querySelector('img').style.transform = '';
        });
    });
});
