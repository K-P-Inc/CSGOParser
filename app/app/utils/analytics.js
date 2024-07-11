const ga4tag = 'G-G09RN92J4H'
const gtmtag = 'GTM-5QXHSJRM'

// Инициализация Google Analytics 4
export const initGA = (trackingId = ga4tag) => {
    window.dataLayer = window.dataLayer || [];
    function gtag() {
        window.dataLayer.push(arguments);
    }
    window.gtag = gtag;

    gtag('js', new Date());
    gtag('config', trackingId);
};

// Логирование просмотров страницы в Google Analytics 4
export const logPageView = (url) => {
    if (window.gtag) {
        window.gtag('config', ga4tag, {
            page_path: url,
        });
    }
};

// Логирование событий в Google Analytics 4
export const logEvent = (action, category, label) => {
    if (window.gtag) {
        window.gtag('event', action, {
            event_category: category,
            event_label: label,
        });
    }
};

// Инициализация Google Tag Manager
export const initGTM = (gtmId = gtmtag) => {
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtm.js?id=${gtmId}`;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtmPush() {
        window.dataLayer.push(arguments);
    }
    window.gtmPush = gtmPush;
};

// Логирование событий в Google Tag Manager
export const logGTMEvent = (eventName, eventParams) => {
    if (window.gtmPush) {
        window.gtmPush({
            event: eventName,
            ...eventParams,
        });
    }
};
