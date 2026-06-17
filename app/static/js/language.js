(function() {
  const PATH = window.location.pathname;
  if (PATH !== '/') return;

  const persianTxts = new Map([
    ['app-name', 'بازارفلو'],
    ['login', 'ورود یا ثبت‌نام'],
    ['terms', 'قوانین و مقررات'],
    ['user-dashboard', 'خاطر'],
    ['chamber-dashboard', 'تالارها'],

    // home-page spicific

    ['name', 'بازار فلو'],
    ['intro', 'از فروش کالا تا گپ زدنت با رفیقات و برگذاری جلسات مجازیت با ما!'],
    ['explaining', 'بازار فلو به درد کسی میخوره که میخواهند محصولات خود را به فروش برسانند یا هم چند رفیق می‌خواهند با هم مکالمه جمعی به صورت صوتی و یا تصویری داشته باشند.'],
    ['chatting', 'این وبسایت خدماتی به نام "تالار" به شما ارائه میدهد٬ شما میتوانید در این تالارها انواع مدیا(عکس٬ فیلم٬ صوت) را بفرستید٬ همچنین میتوانید ارائه زنده یا "مجلس" را در تالار آغاز کنید.'],
    ['ad', 'فروشندگان میتوانند یک تبلیغ یاAd برای کالاهای خود انتخاب کنند که در صورت تمایل٬ با هزینه ناچیزی در وبسایت پخش کنند٬و یا هم لینک آن را کپی مرده و در سایت های دیگر مانند وبسایت یکتانت آنها را پخش کنند.فروشندگان هر هفته یک آنالیز کلی برای فروش ها٬ سودها و زیان های خود خواهند داشته.و جالبترین بخش ماجرا٬ اگه هم خواستید با یک دکمه بزارید بقیه برای شما تبلیغ کنند!'],
    ['home-login', 'ورود'],
    ['home-register', 'ثبت‌نام']
  ]);

  const englishTxts = new Map([
    ['app-name', 'BazaarFlow'],
    ['login', 'Login/Register'],
    ['terms', 'Terms And Conditions'],
    ['user-dashboard', 'Memory'],
    ['chamber-dashboard', 'Chambers'],
    
    // home-page spicific
    
    ['name', 'Bazaar Flow'],
    ['intro', 'From selling goods to chatting with your friends and holding meetings, you can do it all with us!'],
    ['explaining', 'Bazaar Flow is useful for those who want to sell their products or for a group of friends who want to have a collective conversation via audio or video.'],
    ['chatting', 'This website offers you a service called "Chamber". In these Chambers, you can send all kinds of media (photos, videos, audio). You can also start a live presentation or "Gathering" within the Chamber.'],
    ['ad', 'Sellers can choose an advertisement (Ad) for their products to be broadcast on the website for a small fee if they wish, or copy its link and broadcast it on other sites like Yektanet. Sellers will have a weekly overall analysis of their sales, profits, and losses. And the most interesting part: if you want, with a single button, let others advertise for you!'],
    ['home-login', 'Login'],
    ['home-register', 'Register']
  ]);

  let curlang = localStorage.getItem('lang') || 'persian';

  function applyLanguage(lang) {
    const elMap = {
        'app-name': document.getElementById('app-name'),
        'login': document.getElementById('login'),
        'terms': document.getElementById('terms-and-conditions'),
        'user-dashboard': document.getElementById('user-dashboard'),
        'chamber-dashboard': document.getElementById('chamber-dashboard')
      };

    if (PATH === '/') {
      elMap['name'] = document.getElementById('name');
      elMap['intro'] = document.getElementById('small-intro');
      elMap['explaining'] = document.getElementById('full-explanation');
      elMap['chatting'] = document.getElementById('chatting-features');
      elMap['ad'] = document.getElementById('ad-features');
      elMap['home-login'] = document.getElementById('home-login');
      elMap['home-register'] = document.getElementById('home-register');
    }

    const texts = lang === 'persian' ? persianTxts : englishTxts;

    for (const [key, el] of Object.entries(elMap)) {
      if (el && texts.has(key)) {
        el.textContent = texts.get(key);
      }
    }

    document.getElementById('navbar-star').classList.remove('border-end', 'border-start', 'pe-2', 'me-2');
    document.getElementById('navbar-star').classList.add(
      ...(lang === 'persian' ?
      ['border-end', 'pe-2', 'me-2'] :
      ['border-start', 'ps-2', 'ms-2'])
    );
    document.documentElement.dir = lang === 'persian' ? 'rtl' : 'ltr';
    document.body.classList.remove('persian', 'english');
    document.body.classList.add(lang);
    localStorage.setItem('lang', lang);
    // It is the opposite so they can read if they are from the other language
    document.getElementById('change-language-btn').title = lang === 'persian' ? 'Change Language' : 'تغییر زبان';
  }

  function toggleLanguage() {
    curlang = curlang === 'persian' ? 'english' : 'persian';
    applyLanguage(curlang);
  }

  // Ensure DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => applyLanguage(curlang));
  } else {
    applyLanguage(curlang);
  }

  window.toggleLanguage = toggleLanguage;
})();

changeLangBtn = document.getElementById('change-language-btn')
changeLangBtn.addEventListener('click', () => {
  toggleLanguage();
});
