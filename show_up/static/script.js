const sliderEl = document.querySelector("#range2")
const sliderValue = document.querySelector(".value2")

sliderEl.addEventListener("input", (event) => {
  const tempSliderValue = event.target.value; 
  sliderValue.textContent = tempSliderValue;
  
  const progress = (tempSliderValue / sliderEl.max) * 100;
 
  sliderEl.style.background = `linear-gradient(to right, #f50 ${progress}%, #ccc ${progress}%)`;
})

// 2

const sliderEl3 = document.querySelector("#range3")
const sliderValue3 = document.querySelector(".value3")

sliderEl3.addEventListener("input", (event) => {
  const tempSliderValue = Number(event.target.value); 
  
  sliderValue3.textContent = tempSliderValue; 
  
  const progress = (tempSliderValue / sliderEl3.max) * 100;
 
  sliderEl3.style.background = `linear-gradient(to right, #f50 ${progress}%, #ccc ${progress}%)`;
  
  sliderEl3.style.setProperty("--thumb-rotate", `${(tempSliderValue/100) * 2160}deg`)
})
const boxes = document.querySelectorAll(".box");

// Add event listener to each box
boxes.forEach((box) => {
  box.addEventListener("click", () => {
    // Get the content from the data attribute
    const content = box.dataset.content;
    
    // Perform action with the content
    console.log("Box clicked:", content);
  });
});
