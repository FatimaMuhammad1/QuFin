// Navigation data
const navigationData = [
    { name: 'Home', href: 'index.html', icon: 'fa-home' },
    { 
        name: 'Product', 
        href: 'pages/product.html', 
        icon: 'fa-box',
        dropdown: [
            'AI Score Grid', 'CurrenQâ„˘', 'EnergAIâ„˘', 'MetalAIâ„˘', 'FuturAIâ„˘', 
            'Commoditasâ„˘', 'Equivestiaâ„˘', 'Indicemâ„˘', 'CryptAIâ„˘', 'TradeFit Quotientâ„˘',
            'Corelation Matrixâ„˘', 'Country Matrixâ„˘', 'CrossFire AIâ„˘', 'NeuroLockâ„˘',
            'Strategy DNAâ„˘', 'Signal Sieveâ„˘', 'Capital Guardâ„˘', 'Glass Bookâ„˘'
        ]
    },
    { name: 'Pricing', href: '/pages/pricing.html', icon: 'fa-dollar-sign' },
    { 
        name: 'AI Score Grid', 
        href: '/pages/aiscoregrid.html', 
        icon: 'fa-chart-line',
        dropdown: [
            'Forex Scores', 'Energies Scores', 'Metals Scores', 'Futures Scores',
            'Commodity Scores', 'Stock Scores', 'Indices Scores', 'Crypto Scores',
            'ETF Scores', 'Bonds Scores', 'Country Scores'
        ]
    },
    { 
        name: 'AI Strategies', 
        href: 'pages/aistrategies.html', 
        icon: 'fa-cogs',
        dropdown: [
            { 
                name: 'Equity Strategies',
                items: ['Long/Short Equity', 'Equity Market Neutral', 'Short Bias']
            },
            { 
                name: 'Event-Driven',
                items: ['Distressed Securities', 'Restructuring Arbitrage']
            },
            { 
                name: 'Macro Strategy',
                items: ['Global Macro Strategy', 'Commodity Trading Strategy']
            },
            { 
                name: 'Relative Value Arbitrage',
                items: ['Convertible Arbitrage', 'Fixed Income Arbitrage', 'Volatility Arbitrage', 'Merger Arbitrage']
            },
            { 
                name: 'Quantitative Strategy',
                items: ['Statistical Arbitrage', 'High Frequency Trading', 'Machine Learning Models', 'Factor Investing']
            },
            { 
                name: 'Alternative Data Strategy',
                items: [
                    'Michael Burry', 'Lobbying Spending Growth', 'Congress Sells',
                    'Wikipedia Most-Viewed', 'Sector Weighted DC Insider', 'Josh Gottheimer',
                    'Energy and Commerce Committee (House)', 'Top Gov Contract Recipients'
                ]
            }
        ]
    },
    { 
        name: 'Global Data', 
        href: 'pages/globaldata.html', 
        icon: 'fa-globe',
        dropdown: [
            { 
                name: 'Northern America',
                items: ['Canada', 'United States']
            },
            { 
                name: 'South America',
                items: [
                    'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador',
                    'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Mexico', 'Venezuela'
                ]
            },
            { 
                name: 'Europe',
                items: [
                    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
                    'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
                    'Iceland', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
                    'Malta', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania',
                    'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'United Kingdom'
                ]
            },
            { 
                name: 'Asia',
                items: [
                    'Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh',
                    'Bhutan', 'Brunei Darussalam', 'Cambodia', 'China', 'Georgia',
                    'India', 'Indonesia', 'Iran', 'Iraq'
            ]
            },
            { 
                name: 'Africa',
                items: [
                        'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi',
                        'Cabo Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros',
                        'Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea',
                        'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea',
                        'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia', 'Libya',
                        'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco',
                        'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe',
                        'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa',
                        'South Sudan', 'Sudan', 'Togo', 'Tunisia', 'Uganda', 'Tanzania',
                        'Zambia', 'Zimbabwe'
                ]
            },
            { 
                name: 'Oceania',
                items: [
                        'Australia', 'Fiji', 'Kiribati', 'New Caledonia','New Zealand',
                        'Palau', 'Papua New Guinea','Samoa', 'Solomon Islands','Tonga','Tuvalu','Vanuatu']
            },
            { 
                name: 'Middle East & North Africa',
                items: [
                        'Algeria', 'Bahrain', 'Djibouti', 'Egypt', 'Iran', 'Iraq', 'Israel','Jordan','Kuwait',
                        'Lebanon','Libya','Malta','Morocco','Oman','Qatar','Saudi Arabia','Syria','Tunisia',
                        'United Arab Emirates','Yemen'
                ]
            },
            { 
                name: 'European Union',
                items: [
                    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
                    'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
                    'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
                    'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania',
                    'Slovakia', 'Slovenia', 'Spain', 'Sweden'
                ]
            }

        ]
    },
    { 
        name: 'Resources', 
        href: 'pages/resources.html', 
        icon: 'fa-book',
        dropdown: [
            'Backtesting', 'AI Explainability', 'Global Heatmap', 'Global Sentiment',
            'CoT Crystalizer (AI)', 'AI Trading Academy', 'Traders\' Community',
            'Economic Calendar', 'Reports', 'Black Swan Grounds', 'Black Pools Decoder',
            'Market Meme Stock'
        ]
    }
];

// Feature cards data
const features = [
    {
        title: 'AI Score Grid',
        description: 'Evaluate investment opportunities across assets with our proprietary scoring system.',
        icon: 'fa-chart-line',
    href: 'pages/aiscoregrid.html'
    },
    {
        title: 'AI Strategies',
        description: 'Access pre-built algorithmic strategies or build your own for optimized trading.',
        icon: 'fa-cogs',
        href: 'pages/aistrategies.html'
    },
    {
        title: 'Global Data',
        description: 'Comprehensive market data and economic indicators from around the world.',
        icon: 'fa-globe',
        href: 'pages/globaldata.html'
    }
];

// Market data
const marketData = [
    { name: 'S&P 500', symbol: 'US Equities', value: '4,567.89', change: '+1.24%', icon: 'fa-dollar-sign', color: 'blue' },
    { name: 'Bitcoin', symbol: 'Cryptocurrency', value: '$63,452.34', change: '+3.72%', icon: 'fa-coins', color: 'green' },
    { name: 'Crude Oil', symbol: 'Commodities', value: '$78.45', change: '-0.87%', icon: 'fa-gas-pump', color: 'yellow' },
    { name: 'EUR/USD', symbol: 'Forex', value: '1.0845', change: '+0.12%', icon: 'fa-euro-sign', color: 'purple' }
];

// Navigation Item Component
function NavItem({ item }) {
    const [isOpen, setIsOpen] = React.useState(false);
    
    return React.createElement(
        'div', 
        { 
            className: 'relative group nav-item',
            onMouseEnter: () => setIsOpen(true),
            onMouseLeave: () => setIsOpen(false)
        },
        React.createElement(
            'a',
            { 
                href: item.href, 
                className: 'nav-link'
            },
            React.createElement('i', { className: `fa-solid ${item.icon} mr-2` }),
            item.name,
            item.dropdown && React.createElement('i', { className: 'fa-solid fa-chevron-down ml-2 text-xs' })
        ),
        item.dropdown && React.createElement(
            'ul', 
            { 
                className: `dropdown ${isOpen ? 'open' : ''}` 
            },
            Array.isArray(item.dropdown[0]) || typeof item.dropdown[0] === 'string' ? (
                item.dropdown.map((dropdownItem, index) => 
                    React.createElement(
                        'li',
                        { key: index, className: 'dropdown-item' },
                        React.createElement(
                            'a',
                            { href: '#', className: 'dropdown-link' },
                            dropdownItem
                        )
                    )
                )
            ) : (
                item.dropdown.map((dropdownGroup, groupIndex) => 
                    React.createElement(
                        'li',
                        { key: groupIndex, className: 'dropdown-item has-children' },
                        React.createElement(
                            'a',
                            { href: '#', className: 'dropdown-link' },
                            dropdownGroup.name,
                            React.createElement('i', { className: 'fa-solid fa-chevron-right ml-2 text-xs' })
                        ),
                        React.createElement(
                            'ul',
                            { className: 'dropdown second-level' },
                            dropdownGroup.items.map((subItem, subIndex) => 
                                React.createElement(
                                    'li',
                                    { key: subIndex, className: 'dropdown-item' },
                                    React.createElement(
                                        'a',
                                        { href: '#', className: 'dropdown-link' },
                                        subItem
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    );
}

// Feature Card Component
function FeatureCard({ feature }) {
    return React.createElement(
        'div',
        { className: 'feature-card bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm hover:shadow-md' },
        React.createElement(
            'div',
            { className: `w-14 h-14 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-5` },
            React.createElement(
                'i',
                { className: `fa-solid ${feature.icon} text-primary dark:text-blue-400 text-2xl` }
            )
        ),
        React.createElement(
            'h3',
            { className: 'text-xl font-bold mb-3' },
            feature.title
        ),
        React.createElement(
            'p',
            { className: 'text-gray-600 dark:text-slate-400 mb-5' },
            feature.description
        ),
        React.createElement(
            'a',
            { href: feature.href, className: 'text-primary font-medium flex items-center' },
            'Learn More',
            React.createElement('i', { className: 'fa-solid fa-arrow-right ml-2 text-sm' })
        )
    );
}

// Market Item Component
function MarketItem({ item }) {
    return React.createElement(
        'div',
        { className: 'flex justify-between items-center pb-3 border-b border-gray-100 dark:border-slate-700' },
        React.createElement(
            'div',
            { className: 'flex items-center' },
            React.createElement(
                'div',
                { className: `w-10 h-10 rounded-full bg-${item.color}-100 dark:bg-${item.color}-900/30 flex items-center justify-center mr-3` },
                React.createElement('i', { className: `fa-solid ${item.icon} text-${item.color}-500` })
            ),
            React.createElement(
                'div',
                null,
                React.createElement(
                    'p',
                    { className: 'font-medium' },
                    item.name
                ),
                React.createElement(
                    'p',
                    { className: 'text-sm text-gray-500 dark:text-slate-400' },
                    item.symbol
                )
            )
        ),
        React.createElement(
            'div',
            { className: 'text-right' },
            React.createElement(
                'p',
                { className: 'font-medium' },
                item.value
            ),
            React.createElement(
                'p',
                { className: `text-sm ${item.change.startsWith('+') ? 'text-green-500' : 'text-red-500'}` },
                item.change
            )
        )
    );
}

// Theme Toggle Component (Single Icon Version)
function ThemeToggle({ darkMode, toggleDarkMode }) {
    return React.createElement(
        'button',
        {
            onClick: toggleDarkMode,
            className: 'theme-toggle-btn',
            'aria-label': 'Toggle dark mode'
        },
        darkMode ? 
            React.createElement('i', { 
                className: 'fa-solid fa-sun text-yellow-400' 
            }) :
            React.createElement('i', { 
                className: 'fa-solid fa-moon text-blue-400' 
            })
    );
}

// Main App Component
function App() {
    const [darkMode, setDarkMode] = React.useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
    const [authModalOpen, setAuthModalOpen] = React.useState(false);
    const [activeAuthTab, setActiveAuthTab] = React.useState('login');
    const authModalRef = React.useRef(null);
    const authContainerRef = React.useRef(null);

    // Initialize dark mode
    React.useEffect(() => {
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
            setDarkMode(true);
            document.documentElement.classList.add('dark');
        }
    }, []);

    // Handle ESC key to close modal
    React.useEffect(() => {
        const handleEscKey = (e) => {
            if (e.keyCode === 27 && authModalOpen) {
                setAuthModalOpen(false);
            }
        };

        const handleClickOutside = (e) => {
            if (authModalOpen && 
                authContainerRef.current && 
                !authContainerRef.current.contains(e.target)) {
                setAuthModalOpen(false);
            }
        };

        document.addEventListener('keydown', handleEscKey);
        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            document.removeEventListener('keydown', handleEscKey);
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [authModalOpen]);

    // Toggle dark mode
    const toggleDarkMode = () => {
        setDarkMode(!darkMode);
        document.documentElement.classList.toggle('dark');
        localStorage.setItem('theme', darkMode ? 'light' : 'dark');
    };

    // Toggle mobile menu
    const toggleMobileMenu = () => {
        setMobileMenuOpen(!mobileMenuOpen);
    };

    // Toggle auth modal
    const toggleAuthModal = () => {
        setAuthModalOpen(!authModalOpen);
    };

    // Close auth modal
    const closeAuthModal = () => {
        setAuthModalOpen(false);
    };

    // Switch auth tabs
    const switchAuthTab = (tab) => {
        setActiveAuthTab(tab);
    };

    // Handle form submission
    const handleSubmit = (e) => {
        e.preventDefault();
        alert('Form submitted! (This is a demo)');
        setAuthModalOpen(false);
    };

    return React.createElement(
        'div',
        { className: `min-h-screen ${darkMode ? 'dark' : ''}` },
        // Header
        React.createElement(
            'header',
            { className: 'sticky top-0 z-50 bg-white dark:bg-slate-800 shadow-md' },
            React.createElement(
                'div',
                { className: 'container mx-auto px-4 py-3 flex justify-between items-center' },
                React.createElement(
                    'div',
                    { className: 'flex items-center' },
                    React.createElement(
                        'div',
                        { 
                            className: `logo-container p-1 rounded-lg ${darkMode ? 'bg-transparent' : 'bg-gray-800'}` 
                        },
                        React.createElement('img', {
                            src: '/assets/logos/qufin-logo.png',
                            alt: 'QuFin Logo',
                            className: 'logo-img',
                            style: { height: '25px' }
                        })
                    )
                ),
                React.createElement(
                    'nav',
                    { className: 'hidden md:flex space-x-1' },
                    navigationData.map((item, index) => React.createElement(NavItem, { key: index, item: item }))
                ),
                React.createElement(
                    'div',
                    { className: 'flex items-center space-x-4' },
                    // Theme Toggle (Single Icon Version)
                    React.createElement(ThemeToggle, {
                        darkMode: darkMode,
                        toggleDarkMode: toggleDarkMode
                    }),
                    React.createElement(
                        'button',
                        {
                            onClick: toggleAuthModal,
                            className: 'px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 flex items-center'
                        },
                        React.createElement('i', { className: 'fa-solid fa-user mr-2' }),
                        'Login'
                    ),
                    React.createElement(
                        'button',
                        {
                            onClick: toggleMobileMenu,
                            className: 'md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-700'
                        },
                        React.createElement('i', { className: 'fa-solid fa-bars' })
                    )
                )
            ),
            // Mobile Menu
            React.createElement(
                'div',
                { className: `mobile-menu md:hidden ${mobileMenuOpen ? 'open' : ''}` },
                React.createElement(
                    'div',
                    { className: 'flex flex-col space-y-3' },
                    navigationData.map((item, index) => 
                        React.createElement(
                            'a',
                            {
                                key: index,
                                href: item.href,
                                className: 'py-2 px-4 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-700 flex items-center'
                            },
                            React.createElement('i', { className: `fa-solid ${item.icon} mr-3` }),
                            item.name
                        )
                    ),
                    React.createElement(
                        'div',
                        { className: 'pt-4 border-t border-gray-200 dark:border-slate-700' },
                        React.createElement(
                            'button',
                            {
                                onClick: toggleAuthModal,
                                className: 'w-full py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 flex items-center justify-center'
                            },
                            React.createElement('i', { className: 'fa-solid fa-user mr-2' }),
                            'Login'
                        )
                    )
                )
            )
        ),
        // Auth Modal
        React.createElement(
            'div',
            { 
                className: `auth-modal ${authModalOpen ? 'open' : ''}`,
                ref: authModalRef
            },
            React.createElement(
                'div',
                { 
                    className: 'auth-container',
                    ref: authContainerRef
                },
                React.createElement(
                    'button',
                    {
                        onClick: closeAuthModal,
                        className: 'auth-close'
                    },
                    React.createElement('i', { className: 'fa-solid fa-times' })
                ),
                React.createElement(
                    'div',
                    { className: 'auth-tabs' },
                    React.createElement(
                        'div',
                        {
                            className: `auth-tab ${activeAuthTab === 'login' ? 'active' : ''}`,
                            onClick: () => switchAuthTab('login')
                        },
                        'Login'
                    ),
                    React.createElement(
                        'div',
                        {
                            className: `auth-tab ${activeAuthTab === 'signup' ? 'active' : ''}`,
                            onClick: () => switchAuthTab('signup')
                        },
                        'Sign Up'
                    )
                ),
                React.createElement(
                    'div',
                    { className: 'auth-forms' },
                    activeAuthTab === 'login' && React.createElement(
                        'form',
                        { className: 'auth-form active', onSubmit: handleSubmit },
                        React.createElement(
                            'div',
                            { className: 'form-group' },
                            React.createElement('label', { htmlFor: 'login-email' }, 'Email'),
                            React.createElement('input', { type: 'email', id: 'login-email', placeholder: 'Enter your email' })
                        ),
                        React.createElement(
                            'div',
                            { className: 'form-group' },
                            React.createElement('label', { htmlFor: 'login-password' }, 'Password'),
                            React.createElement('input', { type: 'password', id: 'login-password', placeholder: 'Enter your password' })
                        ),
                        React.createElement('button', { type: 'submit', className: 'auth-submit' }, 'Login'),
                        React.createElement(
                            'div',
                            { className: 'mt-4 text-center' },
                            React.createElement(
                                'a',
                                { href: '#', className: 'text-primary-500 hover:underline' },
                                'Forgot password?'
                            )
                        )
                    ),
                    activeAuthTab === 'signup' && React.createElement(
                        'form',
                        { className: 'auth-form active', onSubmit: handleSubmit },
                        React.createElement(
                            'div',
                            { className: 'form-group' },
                            React.createElement('label', { htmlFor: 'signup-name' }, 'Full Name'),
                            React.createElement('input', { type: 'text', id: 'signup-name', placeholder: 'Enter your full name' })
                        ),
                        React.createElement(
                            'div',
                            { className: 'form-group' },
                            React.createElement('label', { htmlFor: 'signup-email' }, 'Email'),
                            React.createElement('input', { type: 'email', id: 'signup-email', placeholder: 'Enter your email' })
                        ),
                        React.createElement(
                            'div',
                            { className: 'form-group' },
                            React.createElement('label', { htmlFor: 'signup-password' }, 'Password'),
                            React.createElement('input', { type: 'password', id: 'signup-password', placeholder: 'Create a password' })
                        ),
                        React.createElement(
                            'div',
                            { className: 'form-group' },
                            React.createElement('label', { htmlFor: 'signup-confirm' }, 'Confirm Password'),
                            React.createElement('input', { type: 'password', id: 'signup-confirm', placeholder: 'Confirm your password' })
                        ),
                        React.createElement('button', { type: 'submit', className: 'auth-submit' }, 'Sign Up')
                    )
                )
            )
        ),
        // Hero Section
        React.createElement(
            'section',
            { className: 'hero-gradient text-white py-16 md:py-24' },
            React.createElement(
                'div',
                { className: 'container mx-auto px-4' },
                React.createElement(
                    'div',
                    { className: 'max-w-3xl mx-auto text-center' },
                    React.createElement(
                        'h1',
                        { className: 'text-4xl md:text-5xl font-bold mb-6' },
                        'Revolutionize Your Trading with AI Intelligence'
                    ),
                    React.createElement(
                        'p',
                        { className: 'text-xl mb-10 opacity-90' },
                        'Discover cutting-edge AI-powered tools for market analysis, strategies, and insights. Unlock opportunities with quantum-inspired algorithms and alternative data signals.'
                    ),
                    React.createElement(
                        'div',
                        { className: 'flex flex-col sm:flex-row justify-center gap-4' },
                        React.createElement(
                            'a',
                            { href: '#', className: 'px-8 py-3 bg-white text-primary-500 font-semibold rounded-lg hover:bg-gray-100 transition' },
                            'Explore Platform'
                        ),
                        React.createElement(
                            'a',
                            { href: '#', className: 'px-8 py-3 bg-transparent border-2 border-white text-white font-semibold rounded-lg hover:bg-white/10 transition' },
                            'View Pricing'
                        )
                    )
                )
            )
        ),
        // Features Section
        React.createElement(
            'section',
            { className: 'py-16 bg-gray-50 dark:bg-slate-900' },
            React.createElement(
                'div',
                { className: 'container mx-auto px-4' },
                React.createElement(
                    'div',
                    { className: 'text-center max-w-2xl mx-auto mb-16' },
                    React.createElement(
                        'h2',
                        { className: 'text-3xl font-bold mb-4' },
                        'Powerful Financial Tools'
                    ),
                    React.createElement(
                        'p',
                        { className: 'text-gray-600 dark:text-slate-400' },
                        'QuFin empowers investors with advanced AI tools. Navigate our platform to access powerful features designed for success in modern markets.'
                    )
                ),
                React.createElement(
                    'div',
                    { className: 'grid grid-cols-1 md:grid-cols-3 gap-8' },
                    features.map((feature, index) => React.createElement(FeatureCard, { key: index, feature: feature }))
                )
            )
        ),
        // Dashboard Preview
        React.createElement(
            'section',
            { className: 'py-16' },
            React.createElement(
                'div',
                { className: 'container mx-auto px-4' },
                React.createElement(
                    'div',
                    { className: 'text-center max-w-2xl mx-auto mb-16' },
                    React.createElement(
                        'h2',
                        { className: 'text-3xl font-bold mb-4' },
                        'Intuitive Dashboard'
                    ),
                    React.createElement(
                        'p',
                        { className: 'text-gray-600 dark:text-slate-400' },
                        'Monitor your investments and market trends with our clean, customizable dashboard.'
                    )
                ),
                React.createElement(
                    'div',
                    { className: 'grid grid-cols-1 lg:grid-cols-3 gap-6' },
                    React.createElement(
                        'div',
                        { className: 'dashboard-card lg:col-span-2' },
                        React.createElement(
                            'div',
                            { className: 'flex justify-between items-center mb-6' },
                            React.createElement(
                                'h3',
                                { className: 'text-xl font-bold' },
                                'Portfolio Performance'
                            ),
                            React.createElement(
                                'div',
                                { className: 'flex space-x-2' },
                                React.createElement(
                                    'button',
                                    { className: 'px-3 py-1 text-sm rounded-lg bg-gray-100 dark:bg-slate-700' },
                                    '1D'
                                ),
                                React.createElement(
                                    'button',
                                    { className: 'px-3 py-1 text-sm rounded-lg bg-gray-100 dark:bg-slate-700' },
                                    '1W'
                                ),
                                React.createElement(
                                    'button',
                                    { className: 'px-3 py-1 text-sm rounded-lg bg-primary-500 text-white' },
                                    '1M'
                                ),
                                React.createElement(
                                    'button',
                                    { className: 'px-3 py-1 text-sm rounded-lg bg-gray-100 dark:bg-slate-700' },
                                    '1Y'
                                )
                            )
                        ),
                        React.createElement(
                            'div',
                            { className: 'chart-container' },
                            React.createElement(
                                'div',
                                { className: 'text-center' },
                                React.createElement('i', { className: 'fa-solid fa-chart-line text-4xl text-gray-400 mb-3' }),
                                React.createElement(
                                    'p',
                                    { className: 'text-gray-500 dark:text-slate-400' },
                                    'Performance chart visualization'
                                )
                            )
                        )
                    ),
                    React.createElement(
                        'div',
                        { className: 'dashboard-card' },
                        React.createElement(
                            'h3',
                            { className: 'text-xl font-bold mb-6' },
                            'Market Overview'
                        ),
                        React.createElement(
                            'div',
                            { className: 'space-y-4' },
                            marketData.map((item, index) => React.createElement(MarketItem, { key: index, item: item }))
                        )
                    )
                )
            )
        ),
        // Footer
        React.createElement(
            'footer',
            { className: 'bg-slate-800 text-slate-300 pt-16 pb-8' },
            React.createElement(
                'div',
                { className: 'container mx-auto px-4' },
                React.createElement(
                    'div',
                    { className: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-12' },
                    React.createElement(
                        'div',
                        { className: 'lg:col-span-2' },
                        React.createElement(
                            'div',
                            { 
                                className: `flex items-center mb-4 p-1 rounded-lg ${darkMode ? 'bg-transparent' : 'bg-gray-800'}` 
                            },
                            React.createElement('img', {
                                src: '/assets/logos/qufin-logo.png',
                                alt: 'QuFin Logo',
                                className: 'logo-img',
                                style: { height: '25px' }
                            })
                        ),
                        React.createElement(
                            'p',
                            { className: 'mb-6 max-w-md' },
                            'AI-powered trading intelligence platform providing cutting-edge analytics and alternative data signals for modern investors.'
                        ),
                        React.createElement(
                            'div',
                            { className: 'flex space-x-4' },
                            React.createElement(
                                'a',
                                { href: 'https://twitter.com/yourusername', className: 'w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center hover:bg-primary-500 transition' },
                                React.createElement('i', { className: 'fab fa-twitter' })
                            ),
                            React.createElement(
                                'a',
                                { href: 'https://linkedin.com/company/yourcompany', className: 'w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center hover:bg-primary-500 transition' },
                                React.createElement('i', { className: 'fab fa-linkedin-in' })
                            ),
                            React.createElement(
                                'a',
                                { href: 'https://facebook.com/yourpage', className: 'w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center hover:bg-primary-500 transition' },
                                React.createElement('i', { className: 'fab fa-facebook-f' })
                            ),
                            React.createElement(
                                'a',
                                { href: 'https://github.com/yourusername', className: 'w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center hover:bg-primary-500 transition' },
                                React.createElement('i', { className: 'fab fa-github' })
                            )
                        )
                    ),
                    React.createElement(
                        'div',
                        null,
                        React.createElement(
                            'h3',
                            { className: 'text-white text-lg font-semibold mb-4' },
                            'Products'
                        ),
                        React.createElement(
                            'ul',
                            { className: 'space-y-3' },
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: 'pages/product.html', className: 'hover:text-white transition' },
                                    'AI Score Grid'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: 'pages/product.html', className: 'hover:text-white transition' },
                                    'Market Data'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: 'pages/aistrategies.html', className: 'hover:text-white transition' },
                                    'Trading Strategies'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: 'pages/product.html', className: 'hover:text-white transition' },
                                    'Backtesting'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: 'pages/product.html', className: 'hover:text-white transition' },
                                    'Risk Management'
                                )
                            )
                        )
                    ),
                    React.createElement(
                        'div',
                        null,
                        React.createElement(
                            'h3',
                            { className: 'text-white text-lg font-semibold mb-4' },
                            'Resources'
                        ),
                        React.createElement(
                            'ul',
                            { className: 'space-y-3' },
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: 'pages/resources.html', className: 'hover:text-white transition' },
                                    'Learning Academy'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: 'pages/reports.html', className: 'hover:text-white transition' },
                                    'Market Reports'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: '#', className: 'hover:text-white transition' },
                                    'Blog'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: '#', className: 'hover:text-white transition' },
                                    'Webinars'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: '#', className: 'hover:text-white transition' },
                                    'API Documentation'
                                )
                            )
                        )
                    ),
                    React.createElement(
                        'div',
                        null,
                        React.createElement(
                            'h3',
                            { className: 'text-white text-lg font-semibold mb-4' },
                            'Company'
                        ),
                        React.createElement(
                            'ul',
                            { className: 'space-y-3' },
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: '#', className: 'hover:text-white transition' },
                                    'About Us'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: '#', className: 'hover:text-white transition' },
                                    'Careers'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: '#', className: 'hover:text-white transition' },
                                    'Contact'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: '#', className: 'hover:text-white transition' },
                                    'Privacy Policy'
                                )
                            ),
                            React.createElement(
                                'li',
                                null,
                                React.createElement(
                                    'a',
                                    { href: '#', className: 'hover:text-white transition' },
                                    'Terms of Service'
                                )
                            )
                        )
                    )
                ),
                React.createElement(
                    'div',
                    { className: 'pt-8 border-t border-slate-700 text-center text-sm' },
                    React.createElement(
                        'p',
                        null,
                        'Â© 2025 QuFin. All rights reserved.'
                    )
                )
            )
        )
    );
}

// Render the app
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(React.createElement(App));