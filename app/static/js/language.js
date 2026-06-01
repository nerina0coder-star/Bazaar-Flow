const PATH = window.location.pathname;
var curlang = 'persian';

if (PATH === '/') {
    const elements = new Map([
        [ 'name', document.getElementById('name') ],
        [ 'intro', document.getElementById('small-intro') ],
        [ 'explaining', document.getElementById('full-explanation') ],
        [ 'chatting', document.getElementById('chatting-features') ],
        [ 'ad', document.getElementById('ad-features') ]
    ]);
}

const persianTxts = new Map([
    [ 'name', 'بازار فلو' ],
    [ 'intro', 'از فروش کالا تا گپ زدنت با رفیقات و برگذاری جلسات مجازیت با ما!' ],
    [ 'explaining', 'بازار فلو به درد کسی میخوره که میخواهند محصولات خود را به فروش برسانند یا هم چند رفیق می‌خواهند با هم مکالمه جمعی به صورت صوتی و یا تصویری داشته باشند.'],
    [ 'chatting', 'این وبسایت خدماتی به نام "تالار" به شما ارائه میدهد٬ شما میتوانید در این تالارها انواع مدیا(عکس٬ فیلم٬ صوت) را بفرستید٬ همچنین میتوانید ارائه زنده یا "مجلس" را در تالار آغاز کنید.' ],
    [ 'ad', 'فروشندگان میتوانند یک تبلیغ یاAd برای کالاهای خود انتخاب کنند که در صورت تمایل٬ با هزینه ناچیزی در وبسایت پخش کنند٬و یا هم لینک آن را کپی مرده و در سایت های دیگر مانند وبسایت یکتانت آنها را پخش کنند.فروشندگان هر هفته یک آنالیز کلی برای فروش ها٬ سودها و زیان های خود خواهند داشته.و جالبترین بخش ماجرا٬ اگه هم خواستید با یک دکمه بزارید بقیه برای شما تبلیغ کنند!' ]
]);

const englishTxts = new Map([
    [ 'name', 'Bazaar Flow' ],
    [ 'intro', 'From selling goods to chatting with your friends and holding meetings, you can do it all with us!' ],
    [ 'explaining', 'Bazaar Flow is useful for those who want to sell their products or for a group of friends who want to have a collective conversation via audio or video.' ],
    [ 'chatting', 'This website offers you a service called "Chamber". In these Chambers, you can send all kinds of media (photos, videos, audio). You can also start a live presentation or "Gathering" within the Chamber.' ],
    [ 'ad', 'Sellers can choose an advertisement (Ad) for their products to be broadcast on the website for a small fee if they wish, or copy its link and broadcast it on other sites like Yektanet. Sellers will have a weekly overall analysis of their sales, profits, and losses. And the most interesting part: if you want, with a single button, let others advertise for you!' ]
]);

function toggleLanguage() {
    if (curlang == 'persian') {
        for (const [name, element] of elements) {
            element.innerText = englishTxts.get(name);
        }
        curlang = 'english';
    } else {
        for (const [name, element] of elements) {
            element.innerText = persianTxts.get(name);
        }
        curlang = 'persian';
    }
}



(function() {
  const PATH = window.location.pathname;

  // Only run on the home page (or wherever the togglable elements exist)
  if (PATH !== '/') return;

  // Elements – wait for DOM to be ready if needed
  const elements = {
    name: document.getElementById('name'),
    intro: document.getElementById('small-intro'),
    explaining: document.getElementById('full-explanation'),
    chatting: document.getElementById('chatting-features'),
    ad: document.getElementById('ad-features'),
  };

  const persianTxts = new Map([
        [ 'name', 'بازار فلو' ],
        [ 'intro', 'از فروش کالا تا گپ زدنت با رفیقات و برگذاری جلسات مجازیت با ما!' ],
        [ 'explaining', 'بازار فلو به درد کسی میخوره که میخواهند محصولات خود را به فروش برسانند یا هم چند رفیق می‌خواهند با هم مکالمه جمعی به صورت صوتی و یا تصویری داشته باشند.'],
        [ 'chatting', 'این وبسایت خدماتی به نام "تالار" به شما ارائه میدهد٬ شما میتوانید در این تالارها انواع مدیا(عکس٬ فیلم٬ صوت) را بفرستید٬ همچنین میتوانید ارائه زنده یا "مجلس" را در تالار آغاز کنید.' ],
        [ 'ad', 'فروشندگان میتوانند یک تبلیغ یاAd برای کالاهای خود انتخاب کنند که در صورت تمایل٬ با هزینه ناچیزی در وبسایت پخش کنند٬و یا هم لینک آن را کپی مرده و در سایت های دیگر مانند وبسایت یکتانت آنها را پخش کنند.فروشندگان هر هفته یک آنالیز کلی برای فروش ها٬ سودها و زیان های خود خواهند داشته.و جالبترین بخش ماجرا٬ اگه هم خواستید با یک دکمه بزارید بقیه برای شما تبلیغ کنند!' ]
    ]);
  const englishTxts = new Map([
        [ 'name', 'Bazaar Flow' ],
        [ 'intro', 'From selling goods to chatting with your friends and holding meetings, you can do it all with us!' ],
        [ 'explaining', 'Bazaar Flow is useful for those who want to sell their products or for a group of friends who want to have a collective conversation via audio or video.' ],
        [ 'chatting', 'This website offers you a service called "Chamber". In these Chambers, you can send all kinds of media (photos, videos, audio). You can also start a live presentation or "Gathering" within the Chamber.' ],
        [ 'ad', 'Sellers can choose an advertisement (Ad) for their products to be broadcast on the website for a small fee if they wish, or copy its link and broadcast it on other sites like Yektanet. Sellers will have a weekly overall analysis of their sales, profits, and losses. And the most interesting part: if you want, with a single button, let others advertise for you!' ]
    ]);

  let curlang = localStorage.getItem('lang') || 'persian';

  function applyLanguage(lang) {
    const texts = lang === 'persian' ? persian : english;
    for (const [key, el] of Object.entries(elements)) {
      if (el && texts[key]) {
        el.innerText = texts[key];
      }
    }
    // Update direction
    document.documentElement.dir = lang === 'persian' ? 'rtl' : 'ltr';
    localStorage.setItem('lang', lang);
  }

  function toggleLanguage() {
    curlang = curlang === 'persian' ? 'english' : 'persian';
    applyLanguage(curlang);
  }

  // Set initial state
  applyLanguage(curlang);

  // Expose only what's needed
  window.toggleLanguage = toggleLanguage;
})();