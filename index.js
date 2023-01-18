const pages = Array.from(document.querySelectorAll("form .page"));
const nextBtn = document.querySelectorAll("form .next-btn");
const prevBtn = document.querySelectorAll("form .prev-btn");


const form = document.querySelector("form");

nextBtn.forEach((button) => {
  button.addEventListener("click", () => {
    changePage("next");
  });
});

prevBtn.forEach((button) => {
  button.addEventListener("click", () => {
    changePage("prev");
  });
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const inputs = [];
  form.querySelectorAll("input").forEach((input) => {
    const { name, value } = input;
    inputs.push({ name, value });
  });
  console.log(inputs);
  form.reset();
});

function changePage(btn) {
  let index = 0;
  const active = document.querySelector(".active");
  index = pages.indexOf(active);
  pages[index].classList.remove("active");
  if (btn === "next") {
    index++;
  } 
  else if (btn === "prev") {
    index--;
  } 
  pages[index].classList.add("active");
}
