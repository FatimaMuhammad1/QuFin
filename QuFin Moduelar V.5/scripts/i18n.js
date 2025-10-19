// Simple i18n for the QuFin static site
(function(){
    const translations = {
        en: {
            'nav.home': 'Home',
            'nav.products': 'Products',
            'nav.pricing': 'Pricing',
            'nav.ai_score_grid': 'AI Score Grid',
            'nav.ai_strategies': 'AI Strategies',
            'nav.global_data': 'Global Data',
            'nav.resources': 'Resources',
            'nav.reports': 'Reports',
            'hero.explore': 'Explore Data',
            'hero.download': 'Download Reports'
        ,
            'hero.title': 'Global Market Data',
            'products.title': 'Our Products',
            'product.ai_score_grid.title': 'AI Score Grid',
            'product.ai_score_grid.desc': 'Our proprietary scoring system evaluates thousands of data points to rate investment opportunities across multiple asset classes.',
            'product.advanced_analytics.title': 'Advanced Analytics',
            'product.advanced_analytics.desc': 'Deep dive into market trends, correlations, and predictive patterns with our advanced visualization tools.',
            'product.ai_strategies.title': 'AI Strategies',
            'product.ai_strategies.desc': 'Access a suite of pre-built algorithmic trading strategies or create your own with our strategy builder.',
            'product.global_data.title': 'Global Data',
            'product.global_data.desc': 'Comprehensive market data covering equities, forex, commodities, cryptocurrencies, and economic indicators.',
            'product.resources.title': 'Resources',
            'product.resources.desc': 'Educational content, market reports, and trading insights to help you make informed decisions.',
            'product.reports.title': 'In-Depth Reports'
        },
        ar: {
            'nav.home': 'الرئيسية',
            'nav.products': 'المنتجات',
            'nav.pricing': 'الأسعار',
            'nav.ai_score_grid': 'شبكة تقييم الذكاء الصناعي',
            'nav.ai_strategies': 'استراتيجيات الذكاء الصناعي',
            'nav.global_data': 'البيانات العالمية',
            'nav.resources': 'الموارد',
            'nav.reports': 'التقارير',
            'hero.explore': 'استكشاف البيانات',
            'hero.download': 'تحميل التقارير'
        ,
            'hero.title': 'البيانات السوقية العالمية',
            'products.title': 'منتجاتنا',
            'product.ai_score_grid.title': 'شبكة تقييم الذكاء الصناعي',
            'product.ai_score_grid.desc': 'يقيّم نظام التقييم الخاص بنا آلاف نقاط البيانات لتصنيف فرص الاستثمار عبر فئات أصول متعددة.',
            'product.advanced_analytics.title': 'التحليلات المتقدمة',
            'product.advanced_analytics.desc': 'تحليل متعمق لاتجاهات السوق والارتباطات والأنماط التنبؤية باستخدام أدوات العرض المتقدمة.',
            'product.ai_strategies.title': 'استراتيجيات الذكاء الصناعي',
            'product.ai_strategies.desc': 'الوصول إلى مجموعة من الاستراتيجيات الخوارزمية الجاهزة أو إنشاء استراتيجياتك الخاصة باستخدام منشئ الاستراتيجيات.',
            'product.global_data.title': 'البيانات العالمية',
            'product.global_data.desc': 'بيانات سوق شاملة تغطي الأسهم والفوركس والسلع والعملات المشفرة والمؤشرات الاقتصادية.',
            'product.resources.title': 'الموارد',
            'product.resources.desc': 'محتوى تعليمي وتقارير السوق ورؤى التداول لمساعدتك في اتخاذ قرارات مستنيرة.',
            'product.reports.title': 'تقارير متعمقة'
        },
        fr: {
            'nav.home': 'Accueil',
            'nav.products': 'Produits',
            'nav.pricing': 'Tarifs',
            'nav.ai_score_grid': 'Grille de score IA',
            'nav.ai_strategies': 'Stratégies IA',
            'nav.global_data': 'Données Globales',
            'nav.resources': 'Ressources',
            'nav.reports': 'Rapports',
            'hero.explore': 'Explorer les données',
            'hero.download': 'Télécharger les rapports'
        ,
            'hero.title': 'Données de marché mondiales',
            'products.title': 'Nos produits',
            'product.ai_score_grid.title': 'Grille de score IA',
            'product.ai_score_grid.desc': 'Notre système de notation propriétaire évalue des milliers de points de données pour classer les opportunités d\'investissement.',
            'product.advanced_analytics.title': 'Analytique avancée',
            'product.advanced_analytics.desc': 'Analyse approfondie des tendances du marché, des corrélations et des modèles prédictifs avec nos outils de visualisation.',
            'product.ai_strategies.title': 'Stratégies IA',
            'product.ai_strategies.desc': 'Accédez à une suite de stratégies de trading algorithmiques préconstruites ou créez la vôtre avec notre générateur.',
            'product.global_data.title': 'Données Globales',
            'product.global_data.desc': 'Données de marché complètes couvrant actions, forex, matières premières, crypto-monnaies et indicateurs économiques.',
            'product.resources.title': 'Ressources',
            'product.resources.desc': 'Contenu éducatif, rapports de marché et analyses pour vous aider à prendre des décisions éclairées.',
            'product.reports.title': 'Rapports approfondis'
        },
        de: {
            'nav.home': 'Startseite',
            'nav.products': 'Produkte',
            'nav.pricing': 'Preise',
            'nav.ai_score_grid': 'KI-Score-Grid',
            'nav.ai_strategies': 'KI-Strategien',
            'nav.global_data': 'Globale Daten',
            'nav.resources': 'Ressourcen',
            'nav.reports': 'Berichte',
            'hero.explore': 'Daten erkunden',
            'hero.download': 'Berichte herunterladen'
        ,
            'hero.title': 'Globale Marktdaten',
            'products.title': 'Unsere Produkte',
            'product.ai_score_grid.title': 'KI-Score-Grid',
            'product.ai_score_grid.desc': 'Unser proprietäres Bewertungssystem wertet Tausende von Datenpunkten aus, um Anlagemöglichkeiten zu bewerten.',
            'product.advanced_analytics.title': 'Fortgeschrittene Analysen',
            'product.advanced_analytics.desc': 'Tiefer Einblick in Markttrends, Korrelationen und prädiktive Muster mit unseren Visualisierungstools.',
            'product.ai_strategies.title': 'KI-Strategien',
            'product.ai_strategies.desc': 'Zugriff auf eine Suite vorgefertigter algorithmischer Handelsstrategien oder erstellen Sie Ihre eigene mit unserem Builder.',
            'product.global_data.title': 'Globale Daten',
            'product.global_data.desc': 'Umfassende Marktdaten zu Aktien, Forex, Rohstoffen, Kryptowährungen und Wirtschaftsdaten.',
            'product.resources.title': 'Ressourcen',
            'product.resources.desc': 'Bildungsinhalte, Marktberichte und Trading-Insights zur Unterstützung fundierter Entscheidungen.',
            'product.reports.title': 'Ausführliche Berichte'
        },
        es: {
            'nav.home': 'Inicio',
            'nav.products': 'Productos',
            'nav.pricing': 'Precios',
            'nav.ai_score_grid': 'Cuadrícula de Puntuación IA',
            'nav.ai_strategies': 'Estrategias IA',
            'nav.global_data': 'Datos Globales',
            'nav.resources': 'Recursos',
            'nav.reports': 'Informes',
            'hero.explore': 'Explorar datos',
            'hero.download': 'Descargar informes'
        ,
            'hero.title': 'Datos del mercado global',
            'products.title': 'Nuestros productos',
            'product.ai_score_grid.title': 'Cuadrícula de Puntuación IA',
            'product.ai_score_grid.desc': 'Nuestro sistema de puntuación propietario evalúa miles de puntos de datos para calificar oportunidades de inversión.',
            'product.advanced_analytics.title': 'Analítica avanzada',
            'product.advanced_analytics.desc': 'Profundice en tendencias del mercado, correlaciones y patrones predictivos con nuestras herramientas de visualización.',
            'product.ai_strategies.title': 'Estrategias IA',
            'product.ai_strategies.desc': 'Acceda a un conjunto de estrategias algorítmicas preconstruidas o cree las suyas con nuestro generador.',
            'product.global_data.title': 'Datos Globales',
            'product.global_data.desc': 'Datos de mercado integrales que cubren acciones, forex, materias primas, criptomonedas e indicadores económicos.',
            'product.resources.title': 'Recursos',
            'product.resources.desc': 'Contenido educativo, informes de mercado e ideas de trading para ayudarle a tomar decisiones informadas.',
            'product.reports.title': 'Informes en profundidad'
        }
    };

    const LANG_KEY = 'qufin_lang';
    const DEFAULT = 'en';

    function getLang(){
        return localStorage.getItem(LANG_KEY) || DEFAULT;
    }

    function setLang(lang){
        localStorage.setItem(LANG_KEY, lang);
        applyLang(lang);
        translatePage(lang);
        document.dispatchEvent(new CustomEvent('qufin:language-changed', { detail: { lang } }));
    }

    function applyLang(lang){
        try{
            document.documentElement.lang = lang;
            if(lang === 'ar'){
                document.documentElement.dir = 'rtl';
                document.documentElement.classList.add('rtl');
            } else {
                document.documentElement.dir = 'ltr';
                document.documentElement.classList.remove('rtl');
            }
        }catch(e){console.warn('i18n applyLang error', e)}
    }

    // Translation by data-i18n attribute
    function translatePage(lang){
        const dict = translations[lang] || translations[DEFAULT];
        // data-i18n attributes
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if(key){
                const text = dict[key] || translations[DEFAULT][key] || el.textContent;
                el.textContent = text;
            }
        });

        // simple nav auto-mapping for static anchors (fallback)
        const navMap = {
            'Home': 'nav.home',
            'Products': 'nav.products',
            'Product': 'nav.products',
            'Pricing': 'nav.pricing',
            'AI Score Grid': 'nav.ai_score_grid',
            'AI Strategies': 'nav.ai_strategies',
            'Global Data': 'nav.global_data',
            'Resources': 'nav.resources',
            'Reports': 'nav.reports'
        };

        document.querySelectorAll('a.nav-link, nav a, header a, .nav-link').forEach(a => {
            const txt = a.textContent && a.textContent.trim();
            if(txt && navMap[txt]){
                a.textContent = dict[navMap[txt]] || translations[DEFAULT][navMap[txt]] || txt;
            }
        });
    }

    // Observe DOM changes (for React rendered content) and re-run translatePage (debounced)
    let translateTimer = null;
    const observer = new MutationObserver(() => {
        if(translateTimer) clearTimeout(translateTimer);
        translateTimer = setTimeout(() => {
            try{ translatePage(getLang()); }catch(e){}
        }, 150);
    });
    observer.observe(document.documentElement || document.body, { childList: true, subtree: true });

    function createLanguageSwitcher(){
        // Avoid duplicates
        if(document.getElementById('qufin-lang-select')) return;

        const select = document.createElement('select');
        select.id = 'qufin-lang-select';
        select.setAttribute('aria-label', 'Language selector');
        select.style.padding = '6px';
        select.style.borderRadius = '6px';
        select.style.border = '1px solid #d1d5db';
        select.style.background = 'white';
        select.style.marginLeft = '8px';

        const opts = [
            { code: 'en', label: 'English' },
            { code: 'ar', label: 'العربية' },
            { code: 'fr', label: 'Français' },
            { code: 'de', label: 'Deutsch' },
            { code: 'es', label: 'Español' }
        ];

        opts.forEach(o => {
            const option = document.createElement('option');
            option.value = o.code;
            option.textContent = o.label;
            select.appendChild(option);
        });

        select.addEventListener('change', e => setLang(e.target.value));

        // Try to append into the header container
        function attach(){
            const headerContainer = document.querySelector('header .container') || document.querySelector('header .container.mx-auto') || document.querySelector('header .container.mx-auto') || document.querySelector('header .container-fluid') || document.querySelector('header .container') || document.querySelector('header');
            if(headerContainer){
                // right-aligned area
                const right = headerContainer.querySelector('.flex.items-center') || headerContainer.querySelector('.flex.items-center.space-x-4') || headerContainer;
                if(right && !document.getElementById('qufin-lang-select')){
                    right.appendChild(select);
                    // set current
                    select.value = getLang();
                }
                return true;
            }
            return false;
        }

        if(!attach()){
            // in case of React-rendered header, observe for header
            const observer = new MutationObserver((mutations, obs) => {
                if(attach()){ obs.disconnect(); }
            });
            observer.observe(document.body, { childList: true, subtree: true });
        }
    }

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', () => {
        const lang = getLang();
        applyLang(lang);
        translatePage(lang);
        createLanguageSwitcher();
    });

    // Expose basic API
    window.qufinI18n = {
        getLang, setLang, translatePage, translations
    };
})();
