let sidebar = document.getElementById('sidebar')
let navbar = document.getElementById('navbar')
let current = window.pageYOffset
let cards = document.querySelectorAll('.cards-category');

let currentpostion = 0;
let difference = 20
let border = 60

function begin(){
	for (var i = cards.length - 1; i >= 0; i--) {
		cards[i].style.height = cards[0].offsetWidth+'px';
	}
	correctSlider()
	versionControl()
	sortCards()
}


function versionControl() {
	items = document.querySelectorAll('.slider-item')
	platform = window.navigator.platform.split(" ")[0];
	if ('Android' == platform) {
		document.querySelector('.slider').style.width = '400%'
		difference = 25
		border = 75
	}
}

function correctSlider(){
	try	{
		let item = document.querySelector('.slider')
		let height = window.innerHeight - ((window.innerHeight/100)*25);
		item.style.height = height+'px';
	}
	catch(e){
		return
	}
}


function sortCards(){
	let modelCards = document.querySelectorAll('.model-card')
	let modelImage = document.querySelectorAll('.model-image')
	// let tempWidth = modelCards[i].offsetWidth
	for (var i = modelCards.length - 1; i >= 0; i--) {
		modelCards[i].style.height = modelCards[i].offsetWidth+((modelCards[i].offsetWidth/100)*50)+'px'
		modelImage[i].style.height = modelCards[i].offsetWidth+'px'
	}
	return modelCards
}


function slide(direction){
	if (direction == 'right'){
		if (currentpostion >= border) return
		currentpostion+=difference;
		item = document.querySelector('.slider-inner');
		temp = 'translateX(-'+currentpostion+'%)';
		item.style.transform = temp;
	}
	else{
		if (currentpostion == 0) return
		currentpostion-=difference;
		item = document.querySelector('.slider-inner');
		temp = 'translateX(-'+currentpostion+'%)';
		item.style.transform = temp;
	}
}


let displacement = 0
function catslide(direction){
	if (direction == 'right'){
		if (displacement >= 100) return
		displacement+=10;
		item = document.querySelector('.catslider-inner');
		temp = 'translateX(-'+displacement+'%)';
		item.style.transform = temp;
	}
	else{
		if (displacement == 0) return
		displacement-=10;
		item = document.querySelector('.catslider-inner');
		temp = 'translateX(-'+displacement+'%)';
		item.style.transform = temp;
	}
}


function hideMessage(item){
	item.remove()
}