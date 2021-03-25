const nxtbtn = document.querySelector('#nxtbtn')

const prevbtn = document.querySelector('#prevbtn')

const imageCorousel = document.querySelector('.carousel-items')

const corouselImages = document.querySelectorAll('.carousel-items img')


var counter = 1

var size = corouselImages[0].clientWidth;
var answer = counter * -size
imageCorousel.style.transform = `translateX(${answer}px)`

nxtbtn.addEventListener('click', () => {
    if (counter >= corouselImages.length - 1) return;
    imageCorousel.style.transition = 'transform 0.9s ease-in-out'
    counter++;
    var result = counter * -size
    imageCorousel.style.transform = `translateX(${result}px)`
})

prevbtn.addEventListener('click', () => {
    if (counter <= 0) return;
    imageCorousel.style.transition = 'transform 0.9s ease-in-out'
    counter--;
    var result = counter * -size
    imageCorousel.style.transform = `translateX(${result}px)`
})

imageCorousel.addEventListener('transitionend', () => {
    if (corouselImages[counter].id === 'lastelement') {
        imageCorousel.style.transition = "none"
        counter = corouselImages.length - 2
        var result = counter * -size
        imageCorousel.style.transform = `translateX(${result}px)`
    }

    if (corouselImages[counter].id === 'firstelement') {
        imageCorousel.style.transition = "none"
        counter = corouselImages.length - counter
        var result = counter * -size
        imageCorousel.style.transform = `translateX(${result}px)`
    }
})
//modal for display
const modal = document.querySelector('.modal-section')

//preparing user into the payment session
const sessionbtn = document.querySelectorAll('.btn')

sessionbtn.forEach((item, index)=>{
	item.addEventListener("click", ()=>{
		if(modal.style.visibility === "hidden"){
			modal.style.visibility = "visible";
			modal.style.opacity = 1;
		}
	});
});
