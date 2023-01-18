const pages = Array.from(document.querySelectorAll("form .page"));
const nextBtn = document.querySelectorAll("form .next-btn");

const prevBtn = document.querySelectorAll("form .prev-btn");
const submitBtn = document.querySelectorAll("form .submit-btn");
const form = document.querySelector("form");


// buttons 
nextBtn.forEach((button) => {
  button.addEventListener("click", () => {
    let index = 0;
    const active = document.querySelector(".active");
    index = pages.indexOf(active)
    changePage("next");
    if (validateForm(index) == false){
      changePage("prev");
    }
  });
});

prevBtn.forEach((button) => {
  button.addEventListener("click", () => {
    changePage("prev");
  });
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

// Form submission 
form.addEventListener("submit", (e) => {
  e.preventDefault();
  
  // const logs = [];
  // form.querySelectorAll("input").forEach((input) => {
  //   const { name, value } = input;
  //   logs.push({ name, value });
  // });

  // form.querySelectorAll("select").forEach((select) => {
  //   const { name, value } = select;
  //   logs.push({ name, value });
  // });
  
  // console.log(logs);
  // form.reset();
  // let index = 0;
  // const active = document.querySelector(".active");
  // index = pages.indexOf(active)
  // changePage("next");
  // if (validateForm(index) == false){
  //   changePage("prev");
  // }
});

// Form Validations
function validateForm(index) {
  if (index == 0) return validatePage1();
  if (index == 1) return validatePage2();
  if (index == 2) return validatePage3();
  if (index == 3) return validatePage4();
  if (index == 4) return validatePage5();
  if (index == 5) return validatePage6();
  if (index == 6) return validatePage7();
  if (index == 7) return validatePage8();
}


function validatePage1(){
  let name = document.forms["form"]["name"].value;
  let email = document.forms["form"]["email"].value;
  if (name == "") {
    alert("Please enter your name");
    return false;
  }
  if (email == "") {
    alert("Pleae enter your email");
    return false;
  }
}

function validatePage2(){
  let age = document.forms["form"]["age"].value;
  let ft = document.forms["form"]["ft"].value;
  let inch = document.forms["form"]["inch"].value;
  
  if (age == "" || age> 100 || age < 0) {
    alert("Please enter a valid age");
    return false;
  }
  if (ft == "" || ft > 10 || ft < 0 || inch == "" ||inch < 0 || inch > 12) {
    alert("Please enter a valid height");
    return false;
  }
}

function validatePage3(){
  let gender = document.forms["form"]["gender"].value;
  let sexualorient = document.forms["form"]["sexualorient"].value;
  let race = document.forms["form"]["race"].value;

  if(gender == ""){
    alert("Please select a gender");
    return false;
  }
  if(sexualorient== ""){
    alert("Please select a sexual orientation");
    return false;
  }
  if(race == ""){
    alert("Please select a race");
    return false;
  }
}

  function validatePage4(){
    let prefAge = document.forms["form"]["preferred-age"].value;
    let prefFt = document.forms["form"]["preferred-ft"].value;
    let prefInch = document.forms["form"]["preferred-inch"].value;
    let prefRace = document.forms["form"]["preferred-race"].value;
  
    if (prefAge == "" || prefAge> 100 || prefAge < 0) {
      alert("Please enter a valid age");
      return false;
    }
    if (prefFt == "" || prefFt > 10 || prefFt < 0 || prefInch == "" ||prefInch < 0 || prefInch > 11) {
      alert("Please enter a valid height");
      return false;
    }

    if(prefRace == ""){
      alert("Please select a race");
      return false;
    }
}


function validatePage5(){
  let religion = document.forms["form"]["religion"].value;
  let mbti = document.forms["form"]["mbti"].value;

  if(religion == ""){
    alert("Please select a religion");
    return false;
  }

  if(mbti == ""){
    alert("Please select a mbti");
    return false;
  }
}

function validatePage6(){
  
  for (var i = 1; i < 11; i++){
    var hobby = document.getElementById("hobby" + i);
    if (hobby.checked) {
      hobby.value = 1;
    }
    else hobby.value = 0;
  }  
  
  return true;
}


function validatePage7(){
    var aesthetic1 = document.getElementById("Feminine Charm");
    var aesthetic2 = document.getElementById("Fresh Lavender");
    var aesthetic3 = document.getElementById("Rustic Feels");
    var aesthetic4 = document.getElementById("The Minimalist");

    if (aesthetic1.checked) checkRadio(aesthetic1.id);
    else if (aesthetic2.checked)  checkRadio(aesthetic2.id);
    else if (aesthetic3.checked)  checkRadio(aesthetic3.id);
    else if (aesthetic4.checked)  checkRadio(aesthetic4.id);
    else {
      alert("Please select a color palette");
      return false;
    }
    return true;
}

function checkRadio(id){
  document.getElementsByName("aesthetic").forEach((a) => {
    a.value = id;
  })
}


function validatePage8(){
  alert("hi");
  for(var i = 1; i < 6; i ++){
    let lovelanguage =  document.getElementById("lovelanguage" + i);
    if(lovelanguage.value == ""){
      alert("Please rank all love languages!");
      return false;
    }
  }
  return true;
}