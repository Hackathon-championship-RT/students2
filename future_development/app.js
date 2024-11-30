const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        } else {
            entry.target.classList.remove('show');
        }
    });
});


const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));

document.addEventListener("DOMContentLoaded", function () {
    const brandLinks = document.querySelectorAll('.brand-link'); // Все ссылки на марки
    brandLinks.forEach(link => {
        const img = link.querySelector('img');
        const text = link.querySelector('.brand-text');
        
        // Обработчик клика на картинку
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Предотвращаем переход по ссылке

            // Переключаем активный класс на картинку
            img.classList.toggle('active');
            text.classList.toggle('active');
        });
    });
});



// Модальное окно и обработчики
const modal = document.getElementById('modal');
const closeBtn = document.getElementsByClassName('close-btn')[0];
const brandDescription = document.getElementById('brand-description');

// Описание брендов
// Описание брендов
const descriptions = {
    aito: "Китайский бренд электромобилей, разработанный в партнерстве с Huawei, ориентирован на инновационные и умные электромобили",
    atom: "Российский проект электрического автомобиля-гаджета с широкими возможностями персонализации и цифровым взаимодействием с городом, разработан для городской среды будущего",
    audi: "Немецкий производитель роскошных автомобилей, известный передовыми технологиями, полным приводом Quattro и элегантным дизайном",
    bmw: "Немецкий автопроизводитель, знаменитый своими высокопроизводительными роскошными автомобилями, включая культовую модель 'Ultimate Driving Machine'",
    bugatti: "Французский бренд роскошных гиперкаров, знаменитый инженерными шедеврами, такими как Veyron и Chiron",
    chevrolet: "Американский автопроизводитель, выпускающий широкий ассортимент автомобилей, от культового спортивного автомобиля Corvette до надежных грузовиков, таких как Silverado",
    chrysler: "Американский бренд, известный своими минивэн-автомобилями, седанами и роскошной серией 300",
    citroen: "Французский автопроизводитель, прославившийся своими инновационными дизайнами и новаторскими подвесками, такими как модель DS",
    delahaye: "Исторический французский бренд роскошных и спортивных автомобилей, популярный в первой половине 20 века",
    fiat: "Итальянский автопроизводитель, известный своими маленькими городскими автомобилями, такими как Fiat 500, и долговечным европейским наследием",
    honda: "Японский автопроизводитель, известный надежными, экономичными автомобилями и мотоциклами, такими как Civic и Accord",
    horch: "Умерший немецкий бренд роскошных автомобилей, один из предшественников Audi",
    infiniti: "Роскошное подразделение Nissan, предлагающее премиальные автомобили и внедорожники с передовыми технологиями",
    jaguar: "Британский производитель роскошных автомобилей, известный спортивными седанами и стильными внедорожниками, такими как F-Type и F-Pace",
    jensen: "Британский автопроизводитель, известный производством роскошных и высокопроизводительных автомобилей, таких как Interceptor",
    lada: "Российский автомобильный бренд, знаменитый своими доступными и надежными автомобилями, особенно в сложных условиях",
    lexus: "Роскошное подразделение Toyota, выпускающее премиальные седаны, внедорожники и гибриды с акцентом на утонченность и качество",
    maserati: "Итальянский производитель роскошных автомобилей, специализирующийся на спортивных и высокопроизводительных моделях, таких как GranTurismo и Levante",
    maybach: "Немецкий бренд ультра-роскошных автомобилей под маркой Mercedes-Benz, выпускающий роскошные седаны и внедорожники",
    mazda: "Японский автопроизводитель, известный своими автомобилями, которые доставляют удовольствие от вождения, и технологиями роторных двигателей, такими как MX-5 Miata",
    mitsubishi: "Японский бренд, предлагающий разнообразие автомобилей, от внедорожников, таких как Outlander, до доступных компактных машин",
    mustang: "Американская икона, олицетворяющая производительность и наследие muscle car",
    nissan: "Японский автопроизводитель, предлагающий разнообразный модельный ряд, включая спортивную модель GT-R и универсальные внедорожники, такие как Rogue",
    oldsmobile: "Умерший американский бренд, известный инновационной инженерией и классическими моделями, такими как Cutlass",
    packard: "Исторический американский бренд роскошных автомобилей, знаменитый своими элегантными автомобилями до Второй мировой войны и слоганом 'Спросите того, кто владеет'",
    peugeot: "Французский автопроизводитель, известный стильными и практичными автомобилями, с сильным присутствием в Европе",
    porsche: "Немецкий производитель спортивных автомобилей, знаменитый точной инженерией и культовыми моделями, такими как 911",
    renault: "Французский автопроизводитель, выпускающий доступные и инновационные автомобили, включая электромобили, такие как Zoe",
    rollsRoyce: "Британский роскошный бренд, производящий одни из самых роскошных автомобилей в мире, включая Phantom и Ghost",
    mercedes: "Немецкий производитель автомобилей класса люкс, известный своими передовыми технологиями, элегантным дизайном и высоким качеством, включая модели S-Class и G-Class",
    saab: "Умерший шведский бренд, известный инновационной инженерией и дизайном, вдохновленным авиацией",
    smart: "Бренд под маркой Mercedes-Benz, специализирующийся на компактных, городских электрических и бензиновых автомобилях",
    tesla: "Американский пионер в области электрических автомобилей, известный инновациями в технологиях электромобилей и моделями, такими как Model S и Model 3",
    charger: "Американский классический бренд, известный своими мощными мускульными автомобилями 1960-1970-х годов, включая культовые модели, такие как Dodge Charger R/T",
    mercedesBenz: "Немецкий бренд, знаменитый своими роскошными и высококачественными автомобилями, выпускающий культовые модели с 1920-х годов, включая классические седаны и спортивные машины, такие как Mercedes-Benz 300SL Gullwing",
    oldsmobile: "Американский бренд, существовавший с 1897 по 2004 год, известный своими инновациями в автомобильной инженерии и выпуском таких культовых моделей, как Oldsmobile 88 и Cutlass, ставшие символами своего времени",
    toyota: "Японский автопроизводитель, известный своими надежными, экономичными автомобилями, такими как Corolla и Camry, а также гибридами, такими как Prius",
    dodgeRT: "Американский бренд, известный своими мощными и агрессивными моделями, особенно в серии RT, включая культовый Dodge Charger RT, который стал символом мощности и стиля в 1960-70-х годах",
    thunderbird: "Американский бренд, выпускающий стильные спортивные автомобили, известные своим элегантным дизайном и мощностью. Thunderbird стал иконой 1950-60-х годов, символизируя роскошь и передовые технологии своего времени",
    hanomag: "Немецкий бренд, известный своими ретро автомобилями и грузовиками, который стал популярным в 1920-х годах благодаря моделям, таким как Hanomag 2/10 PS, и вкладу в производство тракторов и коммерческого транспорта",
    byd: "Китайский автопроизводитель, известный своими электромобилями и инновациями в области возобновляемых источников энергии, выпускающий автомобили с 2003 года, включая популярные модели, такие как BYD Tang и BYD Qin",
    mini: "Британский автопроизводитель, знаменитый своими компактными и стильными автомобилями, включая культовую модель Mini Cooper, которая стала иконой автомобильной культуры с 1960-х годов",
    volkswagen: "Немецкий автопроизводитель, известный своими универсальными и популярными моделями, такими как Golf, Passat и Beetle"
};



const brands = document.querySelectorAll('.brand');
brands.forEach(brand => {
    brand.addEventListener('click', function (e) {
        e.preventDefault(); 

        const brandName = brand.getAttribute('data-brand'); 
        const description = descriptions[brandName] || "Описание бренда не доступно."; 
        
        brandDescription.textContent = description; 
        modal.style.display = 'flex'; 
        modal.classList.add('fade-in'); 
    });
});


closeBtn.addEventListener('click', function () {
    modal.style.display = 'none'; 
    modal.classList.remove('fade-in'); 
});


const backButton = document.querySelector('.back-btn');
if (backButton) {
    backButton.addEventListener('click', function () {
        window.location.href = '#right-section'; 
    });
}


window.addEventListener('click', function (e) {
    if (e.target === modal) {
        modal.style.display = 'none';
        modal.classList.remove('fade-in'); 
    }
});




const showRulesButton = document.getElementById('show-rules');
const rulesPopup = document.getElementById('rules-popup');
const closePopupButton = document.getElementById('close-popup');


showRulesButton.addEventListener('click', function(e) {
    e.preventDefault(); 
    rulesPopup.classList.add('visible'); 
});

closePopupButton.addEventListener('click', function() {
    rulesPopup.classList.remove('visible'); 
});