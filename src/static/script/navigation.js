const navEl = document.querySelector(".page-navigation");
const hiderEl = document.querySelector(
  ".page-navigation .page-navigation__hider"
);

const toggleOpen = () => {
  navEl.classList.toggle("page-navigation--open");
};

hiderEl.addEventListener("click", toggleOpen);
