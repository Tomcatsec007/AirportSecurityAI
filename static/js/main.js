// ==========================
// Animated Counter
// ==========================

const counters = document.querySelectorAll(".counter");

const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

        if (!entry.isIntersecting) return;

        const counter = entry.target;

        const target = Number(counter.dataset.target);

        let current = 0;

        const increment = target / 120;

        const update = () => {

            current += increment;

            if (current >= target) {

                counter.innerText = target;

            } else {

                if(target % 1 !== 0){

                    counter.innerText = current.toFixed(1);

                }else{

                    counter.innerText = Math.ceil(current);

                }

                requestAnimationFrame(update);

            }

        };

        update();

        observer.unobserve(counter);

    });

});

counters.forEach(counter => observer.observe(counter));