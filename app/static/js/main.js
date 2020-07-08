
// Menu Show
const showMenu = (toggleId, navId) => {
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId);

    if(toggle && nav) {
        toggle.addEventListener('click', ()=> {
            nav.classList.toggle('show')
        })
    }
};
showMenu('nav-toggle', 'nav-menu');

// Active and remove active menu
const navLink = document.querySelectorAll('.nav-link');

function linkAction() {
    // Active link
    navLink.forEach(n => n.classList.remove('active'))
    this.classList.add('active')

    // remove menu mobile
    const navMenu = document.getElementById('nav-menu')
    navMenu.classList.remove('show')
};

navLink.forEach(n => n.addEventListener('click', linkAction))


// Scroll to top button
const btnScrollToTop = document.querySelector('#scroll-to-top');

btnScrollToTop.addEventListener("click", function () {
    // may not work in all browsers
    // window.scrollTo( {
    //     top: 0,
    //     left: 0,
    //     behavior: "smooth"
    // });

    //
    $("html, body").animate({ scrollTop: 0 }, "slow");
});