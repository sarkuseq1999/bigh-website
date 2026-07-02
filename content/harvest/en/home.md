---
{
  "source_url": "https://bighnow.com",
  "locale": "en",
  "slug": "home",
  "title": "BiGH – Official Home Page",
  "description": "",
  "images": [
    "https://bighnow.com/wp-content/uploads/2019/01/Black-Logo-300x168.png"
  ],
  "external_links": []
}
---

![](https://bighnow.com/wp-content/uploads/2019/01/Black-Logo-300x168.png)

Please Select Your LanguageEnglish中文한국어日本Tiếng Việt

{"prefetch":[{"source":"document","where":{"and":[{"href\_matches":"/\*"},{"not":{"href\_matches":["/wp-\*.php","/wp-admin/\*","/wp-content/uploads/\*","/wp-content/\*","/wp-content/plugins/\*","/wp-content/themes/astra/\*","/\*\\?(.+)"]}},{"not":{"selector\_matches":"a[rel~=\"nofollow\"]"}},{"not":{"selector\_matches":".no-prefetch, .no-prefetch a"}}]},"eagerness":"conservative"}]}

Scroll to Top

const lazyloadRunObserver = () => {
const lazyloadBackgrounds = document.querySelectorAll( `.e-con.e-parent:not(.e-lazyloaded)` );
const lazyloadBackgroundObserver = new IntersectionObserver( ( entries ) => {
entries.forEach( ( entry ) => {
if ( entry.isIntersecting ) {
let lazyloadBackground = entry.target;
if( lazyloadBackground ) {
lazyloadBackground.classList.add( 'e-lazyloaded' );
}
lazyloadBackgroundObserver.unobserve( entry.target );
}
});
}, { rootMargin: '200px 0px 200px 0px' } );
lazyloadBackgrounds.forEach( ( lazyloadBackground ) => {
lazyloadBackgroundObserver.observe( lazyloadBackground );
} );
};
const events = [
'DOMContentLoaded',
'elementor/lazyload/observe',
];
events.forEach( ( event ) => {
document.addEventListener( event, lazyloadRunObserver );
} );

/(trident|msie)/i.test(navigator.userAgent)&&document.getElementById&&window.addEventListener&&window.addEventListener("hashchange",function(){var t,e=location.hash.substring(1);/^[A-z0-9\_-]+$/.test(e)&&(t=document.getElementById(e))&&(/^(?:a|select|input|button|textarea)$/i.test(t.tagName)||(t.tabIndex=-1),t.focus())},!1);

var astra = {"break\_point":"921","isRtl":"","is\_scroll\_to\_id":"","is\_scroll\_to\_top":"1","is\_header\_footer\_builder\_active":"","edit\_post\_url":"https://bighnow.com/wp-admin/post.php?post={{id}}&action=edit","ajax\_url":"https://bighnow.com/wp-admin/admin-ajax.php","infinite\_count":"2","infinite\_total":"0","pagination":"number","infinite\_scroll\_event":"scroll","no\_more\_post\_message":"No more posts to show.","grid\_layout":"1","site\_url":"https://bighnow.com","show\_comments":"Show Comments","masonryEnabled":"","blogMasonryBreakPoint":"768"};
//# sourceURL=astra-theme-js-js-extra

var astraAddon = {"sticky\_active":"","svgIconClose":"\u003Cspan class=\"ast-icon icon-close\"\u003E\u003C/span\u003E","header\_main\_stick":"0","header\_above\_stick":"0","header\_below\_stick":"0","stick\_header\_meta":"","header\_main\_stick\_meta":"","header\_above\_stick\_meta":"","header\_below\_stick\_meta":"","sticky\_header\_on\_devices":"desktop","sticky\_header\_style":"none","sticky\_hide\_on\_scroll":"0","break\_point":"921","tablet\_break\_point":"768","mobile\_break\_point":"544","header\_main\_shrink":"1","header\_logo\_width":"","responsive\_header\_logo\_width":{"desktop":"","tablet":"","mobile":""},"stick\_origin\_position":"","site\_layout":"ast-full-width-layout","site\_content\_width":"1240","site\_layout\_padded\_width":"1200","site\_layout\_box\_width":"1200","header\_builder\_active":"","component\_limit":"10","is\_header\_builder\_active":""};
//# sourceURL=astra-addon-js-js-extra

var ElementorProFrontendConfig = {"ajaxurl":"https:\/\/bighnow.com\/wp-admin\/admin-ajax.php","nonce":"3357dc634c","urls":{"assets":"https:\/\/bighnow.com\/wp-content\/plugins\/elementor-pro\/assets\/","rest":"https:\/\/bighnow.com\/wp-json\/"},"i18n":{"toc\_no\_headings\_found":"No headings were found on this page."},"shareButtonsNetworks":{"facebook":{"title":"Facebook","has\_counter":true},"twitter":{"title":"Twitter"},"google":{"title":"Google+","has\_counter":true},"linkedin":{"title":"LinkedIn","has\_counter":true},"pinterest":{"title":"Pinterest","has\_counter":true},"reddit":{"title":"Reddit","has\_counter":true},"vk":{"title":"VK","has\_counter":true},"odnoklassniki":{"title":"OK","has\_counter":true},"tumblr":{"title":"Tumblr"},"digg":{"title":"Digg"},"skype":{"title":"Skype"},"stumbleupon":{"title":"StumbleUpon","has\_counter":true},"mix":{"title":"Mix"},"telegram":{"title":"Telegram"},"pocket":{"title":"Pocket","has\_counter":true},"xing":{"title":"XING","has\_counter":true},"whatsapp":{"title":"WhatsApp"},"email":{"title":"Email"},"print":{"title":"Print"}},"facebook\_sdk":{"lang":"en\_US","app\_id":""},"lottie":{"defaultAnimationUrl":"https:\/\/bighnow.com\/wp-content\/plugins\/elementor-pro\/modules\/lottie\/assets\/animations\/default.json"}};
//# sourceURL=elementor-pro-frontend-js-before

var papro\_addons = {"url":"https://bighnow.com/wp-admin/admin-ajax.php","particles\_url":"https://bighnow.com/wp-content/plugins/premium-addons-pro/assets/frontend/min-js/particles.min.js","kenburns\_url":"https://bighnow.com/wp-content/plugins/premium-addons-pro/assets/frontend/min-js/cycle.min.js","gradient\_url":"https://bighnow.com/wp-content/plugins/premium-addons-pro/assets/frontend/min-js/premium-gradient.min.js","parallax\_url":"https://bighnow.com/wp-content/plugins/premium-addons-pro/assets/frontend/min-js/premium-parallax.min.js","lottie\_url":"https://bighnow.com/wp-content/plugins/premium-addons-for-elementor/assets/frontend/min-js/lottie.min.js","anime\_js":"https://bighnow.com/wp-content/plugins/premium-addons-pro/assets/frontend/min-js/anime.min.js","blob\_url":"https://bighnow.com/wp-content/plugins/premium-addons-pro/assets/frontend/min-js/premium-blob.min.js","path\_url":"https://bighnow.com/wp-content/plugins/premium-addons-pro/assets/editor/js/generate-path.js"};
//# sourceURL=elementor-frontend-js-extra

var elementorFrontendConfig = {"environmentMode":{"edit":false,"wpPreview":false,"isScriptDebug":false},"i18n":{"shareOnFacebook":"Share on Facebook","shareOnTwitter":"Share on Twitter","pinIt":"Pin it","download":"Download","downloadImage":"Download image","fullscreen":"Fullscreen","zoom":"Zoom","share":"Share","playVideo":"Play Video","previous":"Previous","next":"Next","close":"Close","a11yCarouselPrevSlideMessage":"Previous slide","a11yCarouselNextSlideMessage":"Next slide","a11yCarouselFirstSlideMessage":"This is the first slide","a11yCarouselLastSlideMessage":"This is the last slide","a11yCarouselPaginationBulletMessage":"Go to slide"},"is\_rtl":false,"breakpoints":{"xs":0,"sm":480,"md":768,"lg":1025,"xl":1440,"xxl":1600},"responsive":{"breakpoints":{"mobile":{"label":"Mobile Portrait","value":767,"default\_value":767,"direction":"max","is\_enabled":true},"mobile\_extra":{"label":"Mobile Landscape","value":880,"default\_value":880,"direction":"max","is\_enabled":false},"tablet":{"label":"Tablet Portrait","value":1024,"default\_value":1024,"direction":"max","is\_enabled":true},"tablet\_extra":{"label":"Tablet Landscape","value":1200,"default\_value":1200,"direction":"max","is\_enabled":false},"laptop":{"label":"Laptop","value":1366,"default\_value":1366,"direction":"max","is\_enabled":false},"widescreen":{"label":"Widescreen","value":2400,"default\_value":2400,"direction":"min","is\_enabled":false}},"hasCustomBreakpoints":false},"version":"3.27.5","is\_static":false,"experimentalFeatures":{"additional\_custom\_breakpoints":true,"e\_swiper\_latest":true,"e\_onboarding":true,"home\_screen":true,"landing-pages":true,"editor\_v2":true,"link-in-bio":true,"floating-buttons":true,"form-submissions":true},"urls":{"assets":"https:\/\/bighnow.com\/wp-content\/plugins\/elementor\/assets\/","ajaxurl":"https:\/\/bighnow.com\/wp-admin\/admin-ajax.php","uploadUrl":"https:\/\/bighnow.com\/wp-content\/uploads"},"nonces":{"floatingButtonsClickTracking":"3367024f01"},"swiperClass":"swiper","settings":{"page":[],"editorPreferences":[]},"kit":{"active\_breakpoints":["viewport\_mobile","viewport\_tablet"],"global\_image\_lightbox":"yes","lightbox\_enable\_counter":"yes","lightbox\_enable\_fullscreen":"yes","lightbox\_enable\_zoom":"yes","lightbox\_enable\_share":"yes","lightbox\_title\_src":"title","lightbox\_description\_src":"description"},"post":{"id":1071,"title":"BiGH%20%E2%80%93%20Official%20Home%20Page","excerpt":"","featuredImage":false}};
//# sourceURL=elementor-frontend-js-before

var ppLogin = {"empty\_username":"Enter a username or email address.","empty\_password":"Enter password.","empty\_password\_1":"Enter a password.","empty\_password\_2":"Re-enter password.","empty\_recaptcha":"Please check the captcha to verify you are not a robot.","email\_sent":"A password reset email has been sent to the email address for your account, but may take several minutes to show up in your inbox. Please wait at least 10 minutes before attempting another reset.","reset\_success":"Your password has been reset successfully.","ajax\_url":"https://bighnow.com/wp-admin/admin-ajax.php","show\_password":"Show password","hide\_password":"Hide password"};
var ppRegistration = {"invalid\_username":"This username is invalid because it uses illegal characters. Please enter a valid username.","username\_exists":"This username is already registered. Please choose another one.","empty\_email":"Please type your email address.","invalid\_email":"The email address isn\u2019t correct!","email\_exists":"The email is already registered, please choose another one.","password":"Password must not contain the character \"\\\\\"","password\_length":"Your password should be at least 8 characters long.","password\_mismatch":"Password does not match.","invalid\_url":"URL seems to be invalid.","recaptcha\_php\_ver":"reCAPTCHA API requires PHP version 5.3 or above.","recaptcha\_missing\_key":"Your reCAPTCHA Site or Secret Key is missing!","show\_password":"Show password","hide\_password":"Hide password","ajax\_url":"https://bighnow.com/wp-admin/admin-ajax.php"};
var ppCoupons = {"copied\_text":"Copied"};
//# sourceURL=powerpack-frontend-js-extra

{"baseUrl":"https://s.w.org/images/core/emoji/17.0.2/72x72/","ext":".png","svgUrl":"https://s.w.org/images/core/emoji/17.0.2/svg/","svgExt":".svg","source":{"concatemoji":"https://bighnow.com/wp-includes/js/wp-emoji-release.min.js?ver=6.9.4"}}

/\*! This file is auto-generated \*/
const a=JSON.parse(document.getElementById("wp-emoji-settings").textContent),o=(window.\_wpemojiSettings=a,"wpEmojiSettingsSupports"),s=["flag","emoji"];function i(e){try{var t={supportTests:e,timestamp:(new Date).valueOf()};sessionStorage.setItem(o,JSON.stringify(t))}catch(e){}}function c(e,t,n){e.clearRect(0,0,e.canvas.width,e.canvas.height),e.fillText(t,0,0);t=new Uint32Array(e.getImageData(0,0,e.canvas.width,e.canvas.height).data);e.clearRect(0,0,e.canvas.width,e.canvas.height),e.fillText(n,0,0);const a=new Uint32Array(e.getImageData(0,0,e.canvas.width,e.canvas.height).data);return t.every((e,t)=>e===a[t])}function p(e,t){e.clearRect(0,0,e.canvas.width,e.canvas.height),e.fillText(t,0,0);var n=e.getImageData(16,16,1,1);for(let e=0;e<n.data.length;e++)if(0!==n.data[e])return!1;return!0}function u(e,t,n,a){switch(t){case"flag":return n(e,"\ud83c\udff3\ufe0f\u200d\u26a7\ufe0f","\ud83c\udff3\ufe0f\u200b\u26a7\ufe0f")?!1:!n(e,"\ud83c\udde8\ud83c\uddf6","\ud83c\udde8\u200b\ud83c\uddf6")&&!n(e,"\ud83c\udff4\udb40\udc67\udb40\udc62\udb40\udc65\udb40\udc6e\udb40\udc67\udb40\udc7f","\ud83c\udff4\u200b\udb40\udc67\u200b\udb40\udc62\u200b\udb40\udc65\u200b\udb40\udc6e\u200b\udb40\udc67\u200b\udb40\udc7f");case"emoji":return!a(e,"\ud83e\u1fac8")}return!1}function f(e,t,n,a){let r;const o=(r="undefined"!=typeof WorkerGlobalScope&&self instanceof WorkerGlobalScope?new OffscreenCanvas(300,150):document.createElement("canvas")).getContext("2d",{willReadFrequently:!0}),s=(o.textBaseline="top",o.font="600 32px Arial",{});return e.forEach(e=>{s[e]=t(o,e,n,a)}),s}function r(e){var t=document.createElement("script");t.src=e,t.defer=!0,document.head.appendChild(t)}a.supports={everything:!0,everythingExceptFlag:!0},new Promise(t=>{let n=function(){try{var e=JSON.parse(sessionStorage.getItem(o));if("object"==typeof e&&"number"==typeof e.timestamp&&(new Date).valueOf()<e.timestamp+604800&&"object"==typeof e.supportTests)return e.supportTests}catch(e){}return null}();if(!n){if("undefined"!=typeof Worker&&"undefined"!=typeof OffscreenCanvas&&"undefined"!=typeof URL&&URL.createObjectURL&&"undefined"!=typeof Blob)try{var e="postMessage("+f.toString()+"("+[JSON.stringify(s),u.toString(),c.toString(),p.toString()].join(",")+"));",a=new Blob([e],{type:"text/javascript"});const r=new Worker(URL.createObjectURL(a),{name:"wpTestEmojiSupports"});return void(r.onmessage=e=>{i(n=e.data),r.terminate(),t(n)})}catch(e){}i(n=f(s,u,c,p))}t(n)}).then(e=>{for(const n in e)a.supports[n]=e[n],a.supports.everything=a.supports.everything&&a.supports[n],"flag"!==n&&(a.supports.everythingExceptFlag=a.supports.everythingExceptFlag&&a.supports[n]);var t;a.supports.everythingExceptFlag=a.supports.everythingExceptFlag&&!a.supports.flag,a.supports.everything||((t=a.source||{}).concatemoji?r(t.concatemoji):t.wpemoji&&t.twemoji&&(r(t.twemoji),r(t.wpemoji)))});
//# sourceURL=https://bighnow.com/wp-includes/js/wp-emoji-loader.min.js
