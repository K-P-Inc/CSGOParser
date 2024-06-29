export const initGA = (trackingId) => {
    window.dataLayer = window.dataLayer || [];
    function gtag() {
        window.dataLayer.push(arguments);
    }
    window.gtag = gtag;

    gtag('js', new Date());
    gtag('config', trackingId);
};

export const logPageView = (url) => {
    if (window.gtag) {
        window.gtag('config', 'G-G09RN92J4H', {
            page_path: url,
        });
    }
};

export const logEvent = (action, category, label) => {
    if (window.gtag) {
        window.gtag('event', action, {
            event_category: category,
            event_label: label,
        });
    }
};
