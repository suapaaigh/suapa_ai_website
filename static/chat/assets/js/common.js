$(document).ready(function () {
    const $body = $('body');
    const mobileBreakpoint = 991.98;

    // Add overlay dynamically (only once)
    if (!$('.sidebar-overlay').length) {
        $('body').append('<div class="sidebar-overlay"></div>');
    }

    // Sidebar toggle
    $('.btn-toggle-leftsidebar').on('click', function (e) {
        e.stopPropagation();
        if (window.innerWidth <= mobileBreakpoint) {
            $body.toggleClass('open no-scroll'); // Mobile: open + scroll lock
        } else {
            $body.toggleClass('layout-fullwidth'); // Desktop: same as before
        }
    });

    // Click overlay closes sidebar (only mobile)
    $(document).on('click', '.sidebar-overlay', function () {
        if (window.innerWidth <= mobileBreakpoint) {
            $body.removeClass('open no-scroll');
        }
    });

    // Remove scroll lock when resizing back to desktop
    $(window).on('resize', function () {
        if (window.innerWidth > mobileBreakpoint) {
            $body.removeClass('open no-scroll');
        }
    });

    // === Theme Color (Skin) Selector ===
    const THEME_STORAGE_KEY = 'theme-color';
    // === Set Theme to DOM ===
    const applyTheme = (themeName) => {
        $body.attr('data-thunderal', `theme-${themeName}`);
        $('.choose-skin li').removeClass('active');
        $(`.choose-skin li[data-theme="${themeName}"]`).addClass('active');
    };
    // === On Page Load: Apply stored theme or default ===
    const storedTheme = localStorage.getItem(THEME_STORAGE_KEY);
    const defaultTheme = 'default'; // Change if you have a preferred default
    if (storedTheme) {
        applyTheme(storedTheme);
    } else {
        applyTheme(defaultTheme);
        localStorage.setItem(THEME_STORAGE_KEY, defaultTheme);
    }
    // === On Click: Set Theme & Save ===
    $('.choose-skin li').on('click', function () {
        const selectedTheme = $(this).data('theme');
        localStorage.setItem(THEME_STORAGE_KEY, selectedTheme);
        applyTheme(selectedTheme);
    });

    // === Google Font Selection ===
    const savedFont = localStorage.getItem('thunderal-font');
    if (savedFont) {
        $body.addClass(savedFont);
        $(`.font_setting input:radio[value="${savedFont}"]`).prop('checked', true);
    }

    // === Google Font Selection ===
    $('.font_setting input:radio').on('click', function () {
        const group = this.name;

        // Remove existing font classes in the group
        const allFontClasses = $(`[name="${group}"]`).map(function () {
            return this.value;
        }).get().join(' ');

        // Apply new font
        $body.removeClass(allFontClasses).addClass(this.value);

        // Save selected font to localStorage
        localStorage.setItem('thunderal-font', this.value);
    });

    // === Toggle: Breadcrumbs Primary Color ===
    $('.breadcrumbs-toggle input:checkbox').on('change', function () {
        $body.toggleClass('breadcrumbs-primary', this.checked);
    });

    // === Toggle: Border Radius (radius-0) ===
    $(document).ready(function () {
        const $body = $('body');
        const $checkbox = $('.radius-toggle input:checkbox');
    
        // Apply initial state on page load (reverse logic)
        $body.toggleClass('radius-0', !$checkbox.prop('checked'));
    
        // Listen for changes (reverse logic)
        $checkbox.on('change', function () {
            $body.toggleClass('radius-0', !this.checked);
        });
    });
    

    // === Toggle: Card Box Shadow ===
    $('.cb-shadow input:checkbox').on('change', function () {
        $('.card').toggleClass('shadow-active');
    });

    // === Image File Input Preview ===
    $('.image-input .form-control').on('change', function () {
        const imageURL = URL.createObjectURL(this.files[0]);
        $(this).closest('.image-input')
               .find('.avatar-wrapper')
               .css('background', `url(${imageURL}) no-repeat`);
    });

    // === Password Strength Meter ===
    $(".password-meter .form-control").on("input", function () {
        const password = $(this).val();
        let score = 0;

        const rules = [
            /.{8,}/,                    // Minimum 8 characters
            /[A-Z]/,                    // At least one uppercase letter
            /[a-z]/,                    // At least one lowercase letter
            /[0-9]/,                    // At least one number
            /[#?!@$%^&*-]/              // At least one special character
        ];

        // Check each rule
        rules.forEach(rule => {
            if (rule.test(password)) score++;
        });

        // Update progress bar width (max 100%)
        $(".password-meter .progress-bar").css('width', (score * 20) + '%');
    });
});

// Enable offcanvas
const offcanvasElementList = document.querySelectorAll('.offcanvas')
const offcanvasList = [...offcanvasElementList].map(offcanvasEl => new bootstrap.Offcanvas(offcanvasEl))

// Enable popovers
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

// Enable tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// Enable Toasts
const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')

if (toastTrigger) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
    toastTrigger.addEventListener('click', () => {
        toastBootstrap.show()
    })
}

// Light/Dark topbar
/*!
* Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
* Copyright 2011-2022 The Bootstrap Authors
* Licensed under the Creative Commons Attribution 3.0 Unported License.
*/

(() => {
    'use strict';

    // Retrieve the stored theme from localStorage
    const storedTheme = localStorage.getItem('theme');

    // Get the user's preferred theme (light/dark)
    const getPreferredTheme = () => {
        if (storedTheme) return storedTheme;
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    // Apply the selected theme to the <html> element
    const setTheme = (theme) => {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const finalTheme = (theme === 'auto' && prefersDark) ? 'dark' : theme;
        document.documentElement.setAttribute('data-bs-theme', finalTheme);
    };

    // Highlight the active theme icon and button
    const showActiveTheme = (theme) => {
        const activeIcon = document.querySelector('.theme-icon-active use');
        const activeBtn = document.querySelector(`[data-bs-theme-value="${theme}"]`);
        if (!activeBtn || !activeIcon) return;

        const svgIconHref = activeBtn.querySelector('svg use')?.getAttribute('href') || '';

        // Remove 'active' class from all theme buttons
        document.querySelectorAll('[data-bs-theme-value]').forEach(el => el.classList.remove('active'));

        // Activate the current button and icon
        activeBtn.classList.add('active');
        activeIcon.setAttribute('href', svgIconHref);
    };

    // Update theme on system preference change (if not explicitly set)
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        if (storedTheme !== 'light' && storedTheme !== 'dark') {
            setTheme(getPreferredTheme());
        }
    });

    // On DOM ready: set and display the preferred theme
    window.addEventListener('DOMContentLoaded', () => {
        const preferredTheme = getPreferredTheme();
        setTheme(preferredTheme);
        showActiveTheme(preferredTheme);

        // Add click handlers to all theme toggle buttons
        document.querySelectorAll('[data-bs-theme-value]').forEach(toggle => {
            toggle.addEventListener('click', () => {
                const selectedTheme = toggle.getAttribute('data-bs-theme-value');
                localStorage.setItem('theme', selectedTheme);
                setTheme(selectedTheme);
                showActiveTheme(selectedTheme);
            });
        });
    });
})();

// SVG path animated on hover
// Check if the device is touch-enabled (mobile/tablet)
const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

if (!isTouchDevice) {
    // Run this code only on non-touch devices (desktop)
    document.querySelectorAll('.animated-icon, .module-box').forEach(svg => {
        const paths = svg.querySelectorAll('path');

        paths.forEach(path => {
            const length = path.getTotalLength();

            path.style.strokeDasharray = length;
            path.style.strokeDashoffset = '0';

            svg.addEventListener('mouseenter', () => {
                path.style.transition = 'none'; // reset instantly
                path.style.strokeDashoffset = length;

                // Force reflow to restart animation
                void path.getBoundingClientRect();

                path.style.transition = 'stroke-dashoffset 1s ease';
                path.style.strokeDashoffset = '0';
            });
        });
    });
}

// page search
const searchBtn = document.getElementById("searchToggleBtn");
const searchInput = document.getElementById("PageSearchInput");
// Toggle input on button click
searchBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    searchInput.classList.toggle("active");
    if (searchInput.classList.contains("active")) {
        searchInput.focus();
    }
});
// Close on Esc key
document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
        searchInput.classList.remove("active");
    }
});

// Start of Tawk.to Script 

var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/5c6d4867f324050cfe342c69/default';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();